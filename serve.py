import logging
import os

import uvicorn
from nabla.main import app

EXPOSE_HOST = os.environ.get("EXPOSE_HOST", "0.0.0.0")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8080)


class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

if __name__ == "__main__":
    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = (
        "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    )
    config = uvicorn.Config(
        app,
        host=EXPOSE_HOST,
        port=EXPOSE_PORT,
        log_config=log_config,
        log_level="info",
    )
    server = uvicorn.Server(config)
    server.run()
