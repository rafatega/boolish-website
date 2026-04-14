# Boolish Helper

Site de utilidades ad hoc com FastAPI, organizado de forma modular para crescer com novas funcoes pessoais e de trabalho.

## Arquitetura

Estrutura principal:

- `main.py`: entrypoint WSGI/ASGI para deploy.
- `app/server.py`: factory da aplicacao FastAPI e registro de routers.
- `app/core/`: configuracoes centrais (logging, settings).
- `app/shared/storage/`: infraestrutura compartilhada (store em memoria com expiração).
- `app/modules/home/`: modulo da home e navegação.
- `app/modules/coord_to_geohash/`: modulo completo da feature.

No modulo `coord_to_geohash`:

- `domain/`: modelos de entrada/saida e erros de dominio.
- `services/`: parser, detector de aneis, builder de geometria, cobertura geohash, renderizadores, use case.
- `api/`: schemas e router HTTP.

Essa base permite adicionar novas funcionalidades como novos modulos em `app/modules/<nome_da_funcao>/...` sem acoplamento com as existentes.

## Rodando localmente

```bash
uv sync
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Acesse:

- Site: `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8000/docs`

## Endpoints atuais

- `GET /health`
- `POST /api/coord-to-geohash/run` (JSON)
- `POST /api/coord-to-geohash/run-raw?target_precision=5&max_outside=1` (`text/plain` multiline)
- `GET /api/coord-to-geohash/{run_id}/map`
- `GET /api/coord-to-geohash/{run_id}/xlsx`

## Exemplo run-raw (texto cru)

```powershell
$raw = @"
-46.678568307423085, -23.5004914126868
-46.68145195349477, -23.500621300332426
-46.684307845404255, -23.50100971314417
...
"@

Invoke-WebRequest `
  -Uri "http://127.0.0.1:8000/api/coord-to-geohash/run-raw?target_precision=5&max_outside=1" `
  -Method Post `
  -ContentType "text/plain" `
  -Body $raw
```

## Deploy Railway

`Procfile`:

```text
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Comportamento de armazenamento

- Sem login e sem banco.
- Resultado (mapa/xlsx) fica em memoria por 1 hora.
- Reiniciar a aplicacao limpa os resultados.
