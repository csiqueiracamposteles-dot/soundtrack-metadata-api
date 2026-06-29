"""Spotify service - busca soundtrack validada."""

import logging

from requests.auth import HTTPBasicAuth

from app.core import config
from app.core.http import request_json
from app.core.cache import get_cache, set_cache
from app.utils.normalize import limpar

log = logging.getLogger("spotify")


# ==========================================================
# TOKEN
# ==========================================================

def get_spotify_token():

    if not (
        config.SPOTIFY_CLIENT_ID
        and config.SPOTIFY_CLIENT_SECRET
    ):

        raise RuntimeError(
            "SPOTIFY_CLIENT_ID/SECRET não configurados"
        )

    cache = get_cache("spotify_token")

    if cache:

        log.info("[SPOTIFY CACHE TOKEN]")

        return cache

    auth_response = request_json(

        "POST",

        "https://accounts.spotify.com/api/token",

        auth=HTTPBasicAuth(
            config.SPOTIFY_CLIENT_ID,
            config.SPOTIFY_CLIENT_SECRET
        ),

        data={
            "grant_type": "client_credentials"
        },
    )

    token = auth_response.get("access_token")

    if not token:

        raise RuntimeError(
            "Spotify token não retornado"
        )

    set_cache(
        "spotify_token",
        token,
        ttl=3000
    )

    return token


# ==========================================================
# BUSCAR ÁLBUM VALIDADO
# ==========================================================

def buscar_album_validado(titulo, ano):

    cache_key = f"spotify_album:{titulo}:{ano}"

    cache = get_cache(cache_key)

    if cache:
        log.info("[SPOTIFY ALBUM CACHE HIT] %s", titulo)
        return cache

    token = get_spotify_token()

    headers = {"Authorization": f"Bearer {token}"}

    queries = [
        f"{titulo} original motion picture soundtrack",
        f"{titulo} original series soundtrack",
        f"{titulo} soundtrack",
        f"{titulo} soundtrack {ano}",
        f"{titulo} score",
        f"{titulo} music from the motion picture",
        f"{titulo} music from the series",
    ]

    melhor = None
    melhor_score = -999
    titulo_limpo = limpar(titulo)

    for q in queries:

        try:
            r = request_json(
                "GET",
                "https://api.spotify.com/v1/search",
                headers=headers,
                params={"q": q, "type": "album", "limit": 15},
            )
        except Exception as e:
            log.warning("[SPOTIFY SEARCH ERROR] %s", e)
            continue

        albums = r.get("albums", {}).get("items", [])

        for alb in albums:

            nome_album = alb.get("name", "")
            nome_limpo = limpar(nome_album)

            score = 0

            if titulo_limpo in nome_limpo:
                score += 70
            if "soundtrack" in nome_limpo:
                score += 40
            if "score" in nome_limpo:
                score += 25
            if "original" in nome_limpo:
                score += 20
            if titulo_limpo not in nome_limpo:
                score -= 120

            if any(
                x in nome_limpo
                for x in (
                    "deluxe", "expanded", "karaoke",
                    "tribute", "korean", "japanese", "instrumental",
                )
            ):
                score -= 100

            if any(x in nome_limpo for x in ("2", "ii", "iii", "part")):
                score -= 80

            score += alb.get("popularity", 0)

            if score > melhor_score:
                melhor_score = score
                melhor = alb

    if melhor:
        log.info("[SPOTIFY MELHOR ÁLBUM] %s", melhor.get("name"))

    set_cache(cache_key, melhor)
    return melhor


# ==========================================================
# EXTRAIR FAIXAS
# ==========================================================

def extrair_faixas(album_id):

    cache_key = f"spotify_tracks:{album_id}"

    cache = get_cache(cache_key)

    if cache:
        log.info("[SPOTIFY TRACKS CACHE HIT]")
        return cache

    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}

    try:
        itens = request_json(
            "GET",
            f"https://api.spotify.com/v1/albums/{album_id}/tracks",
            headers=headers,
        ).get("items", [])
    except Exception as e:
        log.warning("[SPOTIFY TRACKS ERROR] %s", e)
        return []

    ids = [x["id"] for x in itens if x.get("id")]
    if not ids:
        return []

    try:
        detalhes = request_json(
            "GET",
            "https://api.spotify.com/v1/tracks",
            headers=headers,
            params={"ids": ",".join(ids)},
        ).get("tracks", [])
    except Exception as e:
        log.warning("[SPOTIFY DETAILS ERROR] %s", e)
        return []

    mapa = {t["id"]: t for t in detalhes if t}

    faixas = []
    for faixa in itens:
        info = mapa.get(faixa["id"], {})

        spotify_link = ""
        if info.get("external_urls"):
            spotify_link = info["external_urls"].get("spotify", "")

        faixas.append(
            {
                "musica": faixa.get("name", ""),
                "interprete": ", ".join(
                    a.get("name", "") for a in faixa.get("artists", [])
                ),
                "isrc": info.get("external_ids", {}).get("isrc", ""),
                "spotify_link": spotify_link,
            }
        )

    set_cache(cache_key, faixas)
    return faixas
