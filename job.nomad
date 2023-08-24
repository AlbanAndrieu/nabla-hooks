# nomad job run -var env=uat -var team=uat job.nomad

variable "env" {
  type    = string
  default = "dev"

  validation {
    condition     = var.env == "dev" || var.env == "uat" || var.env == "prod"
    error_message = "The env value must be valid env uat or prod."
  }
}

variable "team" {
  type    = string
  default = "uat"

  validation {
    condition     = var.team == "ateam" || var.team == "bteam" || var.team == "uat" || var.team == "prod" || var.team == "dev"
    error_message = "The env value must be valid team ateam or bteam."
  }
}

variable "datacenters" {
  type        = list(string)
  description = "List of datacenters to deploy to."
  default     = ["gra"]
}

job "nabla-hook" {
  datacenters = var.datacenters
  namespace   = "datascience"
  type        = "service"

  group "nabla-hook" {
    count = 1

    # Canary disable, because service is too big 10 G minimum and cluster is not sized for it, so auto_promote set to false
    update {
      max_parallel      = 1
      canary            = 0
      min_healthy_time  = "10m"
      healthy_deadline  = "30m"
      progress_deadline = 0
      auto_revert       = true
      auto_promote      = false
    }

    network {
      port "server" {
        to     = 8080
      }

      port "worker" {
        to     = 9000
      }
    }

    restart {
      interval = "5m"
      attempts = 3
      delay    = "15s"
      mode     = "fail"
    }

    // volume "nabla" {
    //   type            = "csi"
    //   source          = "juicefs-gra-nabla-${var.env}"
    //   attachment_mode = "file-system"
    //   access_mode     = "multi-node-multi-writer"
    // }

    task "nabla-hook" {
      driver = "docker"
      config {
        image = "[[ .CONTAINER_IMAGE ]]"
        ports = ["server"]

        # force_pull = true
        shm_size = 536870912 # 512MB
        image_pull_timeout = "25m"
      }

      vault {
        policies  = ["cicd"]
      }

      template {
        data        = <<EOF
# {{ with secret "datascience/nabla-hook/${var.env}" }}
# {{.Data.data.ENV}}
# {{ end }}
TEMPORALIO_HOST="temporal-app.service.gra.dev.consul"
UVICORN_LOG_LEVEL=debug
EOF
        destination = "${NOMAD_SECRETS_DIR}/.env.local"

        env         = true
      }

      service {
        name = "nabla-hook"
        port = "server"

        tags = [
          "traefik.enable=true",
          "traefik.http.routers.nabla-hook-${var.env}.entrypoints=http",
          "traefik.http.routers.nabla-hook-${var.env}.rule=Host(`nabla-hook.service.gra.${var.env}.consul`)",
        ]

        # Meta keys are also interpretable.
        meta {
          version  = "v0.0.1"
          region   = "${node.region}"
          dc       = "${node.datacenter}"
          service  = "nabla-hook-${var.env}"
          team     = "${var.team}"
        }

        check {
          name     = "server-alive"
          port     = "server"
          type     = "http"
          path     = "heatlh" # v1/ping /docs /metrics
          # 2m because can be heavy to lead, better to put it at this interval
          interval = "2m"
          timeout  = "20m"
        }

      } # service nabla-hook

      resources {
        cpu    = 200 # MHz
        memory = 100 # MB
      }
    } # task nabla-hook

    task "nabla-hook-worker" {
      driver = "docker"
      config {
        image = "[[ .CONTAINER_IMAGE ]]"
        image_pull_timeout = "25m"
        ports = ["worker"]
        # force_pull = true

        command = "python"
        args = [
            "-m",
            "serve_worker",
        ]
        shm_size = 536870912 # 512MB
      }

      // volume_mount {
      //   volume      = "nabla"
      //   destination = "/usr/share/data/"
      //   read_only   = false
      // }

      vault {
        policies  = ["cicd"]
      }

      template {
        data        = <<EOF
#{{ with secret "datascience/nabla-hook/${var.env}" }}
#{{.Data.data.ENV}}
#{{ end }}
TEMPORALIO_HOST="temporal-app.service.gra.dev.consul"
UVICORN_LOG_LEVEL=debug
EOF
        destination = "${NOMAD_SECRETS_DIR}/.env.local"

        env         = true
      }

      service {
        name = "nabla-hook-worker"
        port = "worker"

        tags = [
          "traefik.enable=true",
          "traefik.http.routers.nabla-hook-worker-${var.env}.entrypoints=http",
          "traefik.http.routers.nabla-hook-worker-${var.env}.rule=Host(`nabla-hook-worker.service.gra.${var.env}.consul`) || Host(`nabla-hook-worker.${var.env}.service.gra.${var.env}.consul`)",
        ]

        check {
          name     = "server-prometheus"
          port     = "worker"
          type     = "http"
          path     = "/metrics"
          interval = "5m"
          timeout  = "20m"
        }

      } # service worker

      resources {
        cpu    = var.env == "dev" ? "1000" : "2000" # MHz
        memory = var.env == "dev" ? "4000" : "5000" # MB 5Gb minimum
      }
    } # task nabla-hook-worker

    task "nabla-hook-kong-registration" {

      driver = "docker"

      lifecycle {
        hook = "poststart"
      }

      config {
        image = "docker.io/kong/deck:v1.19.1"

        volumes = [
          "local/kong.yml:/kong.yml"
        ]

        image_pull_timeout = "10m"

        args = [
          "--kong-addr",
          "http://kong-admin.service.gra.${var.env}.consul",
          "sync",
          "--state",
          "/kong.yml",
          "--select-tag",
          "nabla-hook"
        ]
      }

      template {
        destination = "local/kong.yml"

        data = <<EOF
_format_version: "3.0"
_info:
  select_tags:
  - nabla-hook
services:
- connect_timeout: 60000
  host: nabla-hook.service.gra.${var.env}.consul
  name: nabla-hook
  path: /
  port: 80
  protocol: http
  read_timeout: 60000
  retries: 5
  routes:
  - hosts:
    %{ if var.env == "uat" }
    - nabla-hook.staging.int.jusmundi.com
    %{ endif }
    - nabla-hook.${var.env}.int.jusmundi.com
    https_redirect_status_code: 426
    methods:
    - GET
    - PUT
    - POST
    - DELETE
    name: nabla-hook
    path_handling: v0
    preserve_host: false
    protocols:
    - http
    - https
    regex_priority: 0
    request_buffering: true
    response_buffering: true
    strip_path: true
  tags:
  - nabla-hook
  write_timeout: 60000
EOF
      }

      resources {
        cpu    = 300 # Mhz
        memory = 300 # MB
      }

    } # task kong-registration

     task "nabla-hook-kong-disable" {

       driver = "docker"

       lifecycle {
         hook = "poststop"
       }

       config {
         image = "docker.io/kong/deck:v1.19.1"

         volumes = [
           "local/kong.yml:/kong.yml"
         ]

         image_pull_timeout = "10m"

         args = [
           "--kong-addr",
           "http://kong-admin.service.gra.${var.env}.consul",
           "sync",
           "--state",
           "/kong.yml",
           "--select-tag",
           "nabla-hook"
         ]
       }

       template {
         destination = "local/kong.yml"

         data = <<EOF
_format_version: "3.0"
_info:
  select_tags:
  - nabla-hook
services:
- name: nabla-hook
  enabled: false
  host: nabla-hook.service.gra.${var.env}.consul
EOF
       }

       resources {
         cpu    = 300 # Mhz
         memory = 300 # MB
       }

     } # task kong-disable

  } # group nabla-hook

}
