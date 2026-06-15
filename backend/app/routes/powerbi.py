from fastapi import APIRouter

from ..services.powerbi.embed_service import (
    generate_embed_config
)

router = APIRouter()

@router.get("/reports")
def get_powerbi_reports():

    return generate_embed_config()