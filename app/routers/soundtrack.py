import logging

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from pydantic import BaseModel, Field

from app.services.soundtrack_service import buscar_soundtrack

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["Soundtrack"],
)


# ======================================================
# REQUEST MODEL
# ======================================================

class SoundtrackRequest(BaseModel):
    titulo: str = Field(
        ...,
        min_length=1,
        description="Título do filme ou série."
    )


# ======================================================
# GET
# ======================================================

@router.get(
    "/soundtrack",
    summary="Pesquisar trilha sonora",
    description="Retorna os metadados da trilha sonora de um filme ou série.",
    response_description="Metadados encontrados.",
    status_code=200,
)
async def soundtrack(
    titulo: str = Query(
        ...,
        min_length=1,
        description="Título do filme ou série."
    )
) -> dict:

    try:

        resultado = buscar_soundtrack(titulo)

        if resultado.get("erro"):
            raise HTTPException(
                status_code=404,
                detail=resultado["erro"]
            )

        return resultado

    except HTTPException:
        raise

    except Exception:

        logger.exception("Erro ao consultar trilha sonora.")

        raise HTTPException(
            status_code=500,
            detail="Erro interno da aplicação."
        )


# ======================================================
# POST
# ======================================================

@router.post(
    "/soundtrack",
    summary="Pesquisar trilha sonora",
    description="Consulta uma trilha sonora utilizando um JSON no corpo da requisição.",
    response_description="Metadados encontrados.",
    status_code=200,
)
async def soundtrack_post(
    body: SoundtrackRequest
) -> dict:

    try:

        resultado = buscar_soundtrack(body.titulo)

        if resultado.get("erro"):
            raise HTTPException(
                status_code=404,
                detail=resultado["erro"]
            )

        return resultado

    except HTTPException:
        raise

    except Exception:

        logger.exception("Erro ao consultar trilha sonora.")

        raise HTTPException(
            status_code=500,
            detail="Erro interno da aplicação."
        )