import logging

from datetime import datetime

from rapidfuzz import fuzz

from app.core.http import request_json
from app.core.cache import get_cache, set_cache
from app.core import config

log = logging.getLogger("tmdb")

ANO_ATUAL = datetime.now().year


# ==========================================================
# SCORE
# ==========================================================

def calcular_score(
    titulo_busca,
    nome,
    ano,
    popularity
):

    score = 0

    titulo_busca = (
        titulo_busca
        .lower()
        .strip()
    )

    nome = (
        nome
        .lower()
        .strip()
    )

    # MATCH EXATO
    if titulo_busca == nome:
        score += 1000

    # FUZZY
    score += (
        fuzz.ratio(
            titulo_busca,
            nome
        ) * 3
    )

    # PENALIZAÇÕES
    palavras_ruins = [

        "2",
        "3",
        "ii",
        "iii",
        "iv",
        "live action",
        "fans",
        "sing along",
    ]

    if any(
        p in nome
        for p in palavras_ruins
    ):
        score -= 300

    # REMAKE FUTURO
    try:

        ano_int = int(ano)

        if ano_int > ANO_ATUAL:
            score -= 500

        if 1980 <= ano_int <= ANO_ATUAL:
            score += 100

    except:
        pass

    # popularidade com peso baixo
    score += popularity * 0.2

    return score


# ==========================================================
# BUSCA TMDB
# ==========================================================

def buscar_tmdb(titulo):

    cache_key = f"tmdb:{titulo}"

    cache = get_cache(cache_key)

    if cache:

        log.info(
            "[TMDB CACHE HIT] %s",
            titulo
        )

        return cache

    headers = {
        "Authorization": f"Bearer {config.TMDB_TOKEN}"
    }

    candidatos = []

    endpoints = [

        ("movie", "movie"),

        ("tv", "tv")
    ]

    for endpoint, tipo in endpoints:

        try:

            r = request_json(

                "GET",

                f"https://api.themoviedb.org/3/search/{endpoint}",

                headers=headers,

                params={
                    "query": titulo,
                    "language": "pt-BR"
                }
            )

        except Exception as e:

            log.warning(
                "[TMDB ERROR] %s",
                e
            )

            continue

        resultados = r.get(
            "results",
            []
        )

        for item in resultados:

            nome = (

                item.get("original_title")

                or item.get("original_name")

                or item.get("title")

                or item.get("name")
            )

            ano = (

                item.get("release_date", "")

                or item.get("first_air_date", "")
            )[:4]

            popularity = item.get(
                "popularity",
                0
            )

            score = calcular_score(
                titulo,
                nome,
                ano,
                popularity
            )

            candidato = {

                "titulo": nome,

                "ano": ano,

                "tipo": tipo,

                "score": score
            }

            print(
                "[TMDB CANDIDATO]",
                candidato
            )

            candidatos.append(candidato)

    if not candidatos:

        return None

    candidatos_ordenados = sorted(

        candidatos,

        key=lambda x: x["score"],

        reverse=True
    )

    melhor = candidatos_ordenados[0]

    print("\n[TMDB MELHOR MATCH]")
    print(melhor)

    log.info("[TMDB MELHOR MATCH] %s", melhor)

    set_cache(cache_key, melhor)

    return melhor
