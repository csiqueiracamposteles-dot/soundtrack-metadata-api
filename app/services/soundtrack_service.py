import logging

from app.services.tmdb_service import buscar_tmdb
from app.services.spotify_service import (
    buscar_album_validado,
    extrair_faixas,
)
from app.services.musicbrainz_service import (
    buscar_autor_musicbrainz_isrc,
)

logger = logging.getLogger(__name__)


def buscar_soundtrack(titulo: str) -> dict:
    """
    Busca os metadados de uma trilha sonora utilizando
    múltiplos serviços externos.

    Fluxo:

    1. TMDb
    2. Spotify
    3. MusicBrainz
    """

    logger.info("Iniciando consulta: %s", titulo)

    # ======================================================
    # TMDb
    # ======================================================

    obra = buscar_tmdb(titulo)

    logger.info("Resultado TMDb: %s", obra)

    if not obra:
        return {
            "erro": "Audiovisual não encontrado"
        }

    # ======================================================
    # Spotify
    # ======================================================

    album = buscar_album_validado(
        obra["titulo"],
        obra["ano"]
    )

    logger.info("Álbum encontrado: %s", album)

    if not album:
        return {
            "titulo": obra["titulo"],
            "ano": obra["ano"],
            "tipo": obra["tipo"],
            "faixas": []
        }

    # ======================================================
    # Tracks
    # ======================================================

    faixas = extrair_faixas(album["id"])

    logger.info("Faixas encontradas: %s", len(faixas))

    if not faixas:
        return {
            "titulo": obra["titulo"],
            "ano": obra["ano"],
            "tipo": obra["tipo"],
            "faixas": []
        }

    # ======================================================
    # MusicBrainz
    # ======================================================

    for faixa in faixas:

        autor = ""

        isrc = (
            str(faixa.get("isrc", ""))
            .strip()
            .upper()
        )

        logger.info(
            "Consultando compositor para ISRC %s",
            isrc
        )

        if isrc:

            try:

                autor = buscar_autor_musicbrainz_isrc(
                    isrc
                )

            except Exception:

                logger.exception(
                    "Erro ao consultar MusicBrainz (%s)",
                    isrc
                )

                autor = ""

        faixa["autor"] = autor or ""

    # ======================================================
    # Resultado
    # ======================================================

    resultado = {
        "titulo": obra["titulo"],
        "ano": obra["ano"],
        "tipo": obra["tipo"],
        "album": album["name"],
        "faixas": faixas,
    }

    logger.info("Consulta concluída com sucesso.")

    return resultado