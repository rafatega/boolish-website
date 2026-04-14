from __future__ import annotations

import logging
from io import BytesIO

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, StreamingResponse

from app.dependencies import coord_to_geohash_use_case, run_store
from app.modules.coord_to_geohash.api.schemas import CoordToGeohashRunRequest, CoordToGeohashRunResponse
from app.modules.coord_to_geohash.domain.errors import CoordToGeohashValidationError
from app.modules.coord_to_geohash.domain.models import CoordToGeohashInput

logger = logging.getLogger("boolish-website.coord-to-geohash")

router = APIRouter(prefix="/api/coord-to-geohash", tags=["coord-to-geohash"])


def _run_coord_to_geohash(raw_coords: str, target_precision: int, max_outside: float) -> CoordToGeohashRunResponse:
    logger.info(
        "Executando coord_to_geohash | precision=%s | max_outside=%s",
        target_precision,
        max_outside,
    )

    try:
        output = coord_to_geohash_use_case.execute(
            CoordToGeohashInput(
                raw_coords=raw_coords,
                target_precision=target_precision,
                max_outside=max_outside,
            )
        )
    except CoordToGeohashValidationError as exc:
        logger.warning("Erro de validacao no coord_to_geohash: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Erro inesperado no processamento coord_to_geohash.")
        raise HTTPException(status_code=500, detail="Erro interno ao processar coordenadas.") from exc

    run_id = run_store.save(map_html=output.map_html, excel_bytes=output.excel_bytes)
    logger.info("Processamento concluido | run_id=%s | geohashes=%s", run_id, output.geohash_count)

    return CoordToGeohashRunResponse(
        run_id=run_id,
        geohash_count=output.geohash_count,
        geohashes=output.geohashes,
        stats_by_length=output.stats_by_length,
        rings_count=output.rings_count,
    )


@router.post("/run", response_model=CoordToGeohashRunResponse)
def run(payload: CoordToGeohashRunRequest) -> CoordToGeohashRunResponse:
    return _run_coord_to_geohash(
        raw_coords=payload.raw_coords,
        target_precision=payload.target_precision,
        max_outside=payload.max_outside,
    )


@router.post("/run-raw", response_model=CoordToGeohashRunResponse)
async def run_raw(
    request: Request,
    target_precision: int = Query(5, ge=4, le=12),
    max_outside: float = Query(1.0, ge=0.0, le=1.0),
) -> CoordToGeohashRunResponse:
    body_text = (await request.body()).decode("utf-8").strip()
    if not body_text:
        raise HTTPException(
            status_code=400,
            detail="Body vazio. Envie as coordenadas no formato 'lon, lat' em linhas separadas.",
        )

    return _run_coord_to_geohash(
        raw_coords=body_text,
        target_precision=target_precision,
        max_outside=max_outside,
    )


@router.get("/{run_id}/map", response_class=HTMLResponse)
def map_html(run_id: str) -> str:
    stored = run_store.get(run_id)
    if stored is None:
        raise HTTPException(status_code=404, detail="Resultado nao encontrado ou expirado.")
    return stored.map_html


@router.get("/{run_id}/xlsx")
def xlsx(run_id: str) -> StreamingResponse:
    stored = run_store.get(run_id)
    if stored is None:
        raise HTTPException(status_code=404, detail="Resultado nao encontrado ou expirado.")

    return StreamingResponse(
        BytesIO(stored.excel_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=geohashes.xlsx"},
    )
