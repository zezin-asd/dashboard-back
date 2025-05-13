from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import regra_negocio

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere conforme necessário
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/admin")
async def login_admin(request: Request):
    body = await request.json()
    username = body.get("username")
    senha = body.get("password")
    try:
        return regra_negocio.logar_admin(username,senha)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no servidor: {str(e)}")
    
@app.get("/api/admin/reportes/line/{linha}")
async def buscar_reportes(linha: str):
    try:
        return regra_negocio.buscar_reportes(linha)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no servidor: {str(e)}")
    
@app.get("/api/admin/reportes/{reporte}")
async def busca_reporte(reporte: int):
    try:
        return regra_negocio.buscar_reporte(reporte)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no servidor: {str(e)}")
    
@app.put("/api/admin/reportes/analisar")
async def marcar_analisado(request: Request):
    body = await request.json()
    id_reporte = body.get("id_reporte")
    analisado = body.get("analisado")
    try:
        return regra_negocio.marcar_analisado(id_reporte,analisado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no servidor: {str(e)}")

@app.get("/api/admin/historico/line/{linha}")
async def buscar_historico(linha: str):
    try:
        return regra_negocio.buscar_historico(linha)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no servidor: {str(e)}")

@app.get("/api/admin/overview/line/{linha}")
async def buscar_overview(linha: str):
    try:
        return regra_negocio.buscar_overview(linha)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no servidor: {str(e)}")