#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import traceback

import certifi
import urllib3
from colorama import init
from termcolor import colored
# WORKAROUND below in case certificate is not install on workstation
# urllib3.disable_warnings()

# use Colorama to make Termcolor work on Windows too
init()

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where(),
)


# USAGE : python -m get_jira.test.check_certificates

print(colored('TEST: https://google.com', 'yellow'))

try:

    r = http.request('GET', 'https://google.com')
    print(r.status)

except urllib3.exceptions.SSLError as e:
    print(e)
#    sys.stderr.write("Failed to check certificate.  Message: \"%s\".\n" % (e.text));
    sys.exit(2)
except Exception as e:  # noqa: ignore=E722
    traceback.print_exc()
    print(
        colored(
            'Oops!  HTTPS is failing. Switch to manual... {}'.format(
                http,
            ), 'red',
        ),
    )
    sys.exit(2)

print(colored('TEST: https://expired.badssl.com', 'yellow'))

try:

    r = http.request('GET', 'https://expired.badssl.com')
    print(r.status)
    # http = urllib3.PoolManager(
    #    cert_file='/etc/ssl/certs/UK1VSWCERT01-CA-5.crt',
    #    cert_reqs='CERT_REQUIRED',
    #    ca_certs='/etc/ssl/certs/ca-certificates.crt')
    sys.exit(2)

except urllib3.exceptions.MaxRetryError as e:
    #    traceback.print_exc()
    print(
        colored(
            'OK!  HTTPS is failing. As expected... {}'.format(
                e,
            ), 'green',
        ),
    )
except urllib3.exceptions.SSLError as e:
    print(e)
except Exception as e:  # noqa: ignore=E722
    traceback.print_exc()
    print(
        colored(
            'Oops!  HTTPS is failing. Switch to manual... {}'.format(
                http,
            ), 'red',
        ),
    )

print(colored('TEST: http://fr1cslfrbm0060.misys.global.ad/', 'yellow'))

# http = urllib3.PoolManager(
#    cert_file='/etc/ssl/certs/UK1VSWCERT01-CA-5.crt',
#    cert_reqs='CERT_REQUIRED',
#    ca_certs='/etc/ssl/certs/ca-certificates.crt')

try:

    r = http.request('GET', 'http://fr1cslfrbm0060.misys.global.ad/')
    print(r.status)

    # sys.exit(2)

except urllib3.exceptions.MaxRetryError as e:
    #    traceback.print_exc()
    print(
        colored(
            'OK!  HTTPS is failing. As expected... {}'.format(
                e,
            ), 'green',
        ),
    )
except urllib3.exceptions.SSLError as e:
    print(e)
except Exception as e:  # noqa: ignore=E722
    traceback.print_exc()
    print(
        colored(
            'Oops!  HTTPS is failing. Switch to manual... {}'.format(
                http,
            ), 'red',
        ),
    )

print(colored('TEST: https://almtools.misys.global.ad/jira', 'yellow'))

try:

    r = http.request('GET', 'https://almtools.misys.global.ad/jira')
    print(r.status)

    sys.exit(2)

except urllib3.exceptions.MaxRetryError as e:
    #    traceback.print_exc()
    print(
        colored(
            'OK!  HTTPS is failing. As expected... {}'.format(
                e,
            ), 'green',
        ),
    )
except urllib3.exceptions.SSLError as e:
    print(e)
except Exception as e:  # noqa: ignore=E722
    traceback.print_exc()
    print(
        colored(
            'Oops!  HTTPS is failing. Switch to manual... {}'.format(
                http,
            ), 'red',
        ),
    )
