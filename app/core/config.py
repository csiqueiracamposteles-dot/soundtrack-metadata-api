

import os
from pathlib import Path

from dotenv import load_dotenv


# ===========================================================
# RAIZ DO PROJETO
# ===========================================================

BASE_DIR = Path(__file__).resolve().parents[2]


# ===========================================================
# PROFILE
# ===========================================================

ACTIVE_PROFILE = (
    os.getenv("ACTIVE_PROFILE")
    or os.getenv("ENVIRONMENT")
    or "dev"
).lower().strip()


# aliases comuns
_PROFILE_ALIASES = {
    "development": "dev",
    "homologacao": "dev",
    "hml": "dev",
    "production": "prod",
    "producao": "prod",
}

ACTIVE_PROFILE = _PROFILE_ALIASES.get(
    ACTIVE_PROFILE,
    ACTIVE_PROFILE
)


# ===========================================================
# LOAD .env.<profile>
# ===========================================================

ENV_FILE = BASE_DIR / f".env.{ACTIVE_PROFILE}"

if ENV_FILE.exists():

    load_dotenv(
        ENV_FILE,
        override=False
    )

    print(
        f"[CONFIG] .env carregado: {ENV_FILE}"
    )

else:

    print(
        f"[CONFIG] Arquivo {ENV_FILE} não encontrado, "
        f"usando apenas variáveis do ambiente."
    )


# ===========================================================
# HELPERS
# ===========================================================

def _get(*names, default=None):

    for n in names:

        v = os.getenv(n)

        if v not in (None, ""):
            return v

    return default


# ===========================================================
# ROUTE PREFIX
# ===========================================================

ROUTE_PREFIX = _get(
    "ROUTE_PREFIX",
    default="/api"
) or ""

# remove barra final
if ROUTE_PREFIX.endswith("/"):
    ROUTE_PREFIX = ROUTE_PREFIX.rstrip("/")

# garante barra inicial
if ROUTE_PREFIX and not ROUTE_PREFIX.startswith("/"):
    ROUTE_PREFIX = "/" + ROUTE_PREFIX


# ===========================================================
# SERVIÇOS EXTERNOS
# ===========================================================

TMDB_TOKEN = _get(
    "TMDB_TOKEN"
)

SPOTIFY_CLIENT_ID = _get(
    "SPOTIFY_CLIENT_ID"
)

SPOTIFY_CLIENT_SECRET = _get(
    "SPOTIFY_CLIENT_SECRET"
)

MUSICBRAINZ_USER_AGENT = _get(
    "MUSICBRAINZ_USER_AGENT",
    default="soundtrack-metadata-api/1.0"
)


# ===========================================================
# CACHE
# ===========================================================

CACHE_DB = _get(
    "CACHE_DB_PATH",
    default=str(BASE_DIR / "cache.db"),
)


# ===========================================================
# DEBUG INFO
# ===========================================================

print(
    f"[CONFIG] "
    f"profile={ACTIVE_PROFILE} | "
    f"route_prefix={ROUTE_PREFIX} | "
    f"tmdb={'OK' if TMDB_TOKEN else 'EMPTY'} | "
    f"spotify={'OK' if SPOTIFY_CLIENT_ID else 'EMPTY'} | "
    f"musicbrainz={'OK' if MUSICBRAINZ_USER_AGENT else 'EMPTY'}"
)