import logging
import time

from app.core.http import request_json
from app.core.cache import get_cache, set_cache

log = logging.getLogger("musicbrainz")


def buscar_autor_musicbrainz_isrc(isrc):

    if not isrc:
        return ""

    isrc = str(isrc).strip().upper()

    cache_key = f"mb:{isrc}"

    cache = get_cache(cache_key)

    if cache:

        log.info("[MUSICBRAINZ CACHE HIT] %s", isrc)

        autor = cache.get("autor", "")

        if autor == "__NOT_FOUND__":
            return ""

        return autor

    headers = {
        "User-Agent": "soundtrack-metadata-api/1.0"
    }

    autores = set()

    try:

        time.sleep(1)

        log.info("[MUSICBRAINZ] Buscando ISRC: %s", isrc)

        dados_isrc = request_json(

            "GET",

            f"https://musicbrainz.org/ws/2/isrc/{isrc}",

            headers=headers,

            params={
                "fmt": "json"
            }
        )

    except Exception as e:

        log.warning("[MUSICBRAINZ ERROR ISRC] %s", e)

        return ""

    recordings = dados_isrc.get(
        "recordings",
        []
    )

    print(f"[MUSICBRAINZ RECORDINGS] {len(recordings)}")

    if not recordings:

        set_cache(cache_key, {
            "autor": "__NOT_FOUND__"
        })

        return ""

    for rec in recordings:

        recording_id = rec.get("id")

        if not recording_id:
            continue

        try:

            time.sleep(1)

            detalhe = request_json(

                "GET",

                f"https://musicbrainz.org/ws/2/recording/{recording_id}",

                headers=headers,

                params={
                    "fmt": "json",
                    "inc": "work-rels+work-level-rels"
                }
            )

        except Exception as e:

            log.warning("[MUSICBRAINZ ERROR RECORDING] %s", e)

            continue

        relations = detalhe.get(
            "relations",
            []
        )

        for rel in relations:

            print(f"[RELATION TYPE] {rel.get('type')}")

            if rel.get("type") != "performance":
                continue

            work = rel.get("work", {})

            work_id = work.get("id")

            if not work_id:
                continue

            try:

                time.sleep(1)

                work_data = request_json(

                    "GET",

                    f"https://musicbrainz.org/ws/2/work/{work_id}",

                    headers=headers,

                    params={
                        "fmt": "json",
                        "inc": "artist-rels"
                    }
                )

            except Exception as e:

                log.warning("[MUSICBRAINZ ERROR WORK] %s", e)

                continue

            for wrel in work_data.get("relations", []):

                tipo = (wrel.get("type") or "").lower()

                if tipo in ("composer", "writer", "lyricist"):

                    artist = wrel.get("artist", {})

                    nome = artist.get("name")

                    if nome:
                        autores.add(nome)

    autor_final = ", ".join(sorted(autores)) or "__NOT_FOUND__"

    set_cache(cache_key, {"autor": autor_final})

    if autor_final == "__NOT_FOUND__":
        log.info("[MUSICBRAINZ] Autor não encontrado: %s", isrc)
        return ""

    log.info("[MUSICBRAINZ OK] %s -> %s", isrc, autor_final)
    return autor_final
