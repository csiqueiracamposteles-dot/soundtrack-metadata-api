"""HTTP client com retry, pooling e logging."""

import logging
import time

import requests

log = logging.getLogger("http")

_session = requests.Session()
_adapter = requests.adapters.HTTPAdapter(
    pool_connections=20,
    pool_maxsize=20,
    max_retries=0,
)
_session.mount("http://", _adapter)
_session.mount("https://", _adapter)


def request_json(method, url, *, timeout=30, max_retries=5, **kwargs):
    """
    Faz request e retorna dict do JSON.
    Em caso de erro retorna {} (não lança) — política do projeto.
    """
    for tentativa in range(max_retries):
        try:
            log.info("[HTTP] %s %s (tent=%d)", method, url, tentativa + 1)

            r = _session.request(method, url, timeout=timeout, **kwargs)

            log.info("[HTTP STATUS] %s", r.status_code)

            if r.status_code == 404:
                return {}

            if r.status_code == 429:
                retry_after = r.headers.get("Retry-After")
                try:
                    wait_time = int(retry_after)
                except (TypeError, ValueError):
                    wait_time = 2
                log.info("[HTTP RATE LIMIT] retry-after=%ds", wait_time)
                time.sleep(wait_time)
                continue

            if r.status_code >= 400:
                log.warning("[HTTP ERROR BODY] %s", r.text[:1000])

            r.raise_for_status()

            try:
                return r.json()
            except ValueError as e:
                log.warning("[HTTP JSON ERROR] %s", e)
                return {}

        except requests.exceptions.Timeout:
            log.warning("[HTTP TIMEOUT] %s", url)
        except requests.exceptions.ConnectionError as e:
            log.warning("[HTTP CONNECTION ERROR] %s", e)
        except requests.exceptions.HTTPError as e:
            log.warning("[HTTP REQUEST ERROR] %s", e)
        except Exception as e:
            log.exception("[HTTP UNKNOWN ERROR] %s", e)

        time.sleep(1)

    log.error("[HTTP FAILED AFTER RETRIES] %s", url)
    return {}
