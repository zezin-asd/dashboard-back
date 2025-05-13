import banco
from datetime import datetime

def logar_admin(username,senha):
    usuario = banco.recuperar_admin(username)
    if usuario is not None:
        if usuario[0] == senha:
            return {"sucesso": True, "id_cco": usuario[1],"nome_cco": usuario[2]}
        else: return{"error": "Senha incorreta!"}
    else: return{"error": "Username incorreto!"}

def buscar_reportes(id_linha):
    reportes = banco.buscar_reportes(id_linha)
    if reportes is not None:
        for item in reportes:
            data_str = item.get("data_criacao")
            if data_str:
                 item["data_criacao"] = data_str.strftime("%d/%m/%Y %H:%M")
        return {"sucesso": True, "dados_reportes": reportes}
    return {"erro": "Linha incorreta"}

def buscar_reporte(id_reporte):
    reporte = banco.buscar_reporte(id_reporte)
    if reporte is not None:
        data_str = reporte.get("data_criacao")
        if data_str:
            reporte["data_criacao"] = data_str.strftime("%d/%m/%Y %H:%M")
        data_str = reporte.get("data_ocorrencia")
        if data_str:
            reporte["data_ocorrencia"] = data_str.strftime("%d/%m/%Y")
        return {"sucesso": True, "dado_reporte": reporte}
    return {"erro": "Reporte incorreto"}

def marcar_analisado(id_reporte,analisado):
    msg = banco.marcar_analisado(id_reporte,analisado)
    return {"sucesso": True, "msg": msg}

def buscar_historico(id_linha):
    reportes = banco.buscar_historico(id_linha)
    if reportes is not None:
        for item in reportes:
            data_str = item.get("data_criacao")
            if data_str:
                 item["data_criacao"] = data_str.strftime("%d/%m/%Y %H:%M")
        return {"sucesso": True, "dados_reportes": reportes}

def buscar_overview(id_linha):
    with banco.get_conexao() as con:
        reportes_recentes = banco.reportes_recentes(id_linha,con)
        reportes_solucionados = banco.reportes_solucionados(id_linha,con)
        mais_reportados = banco.mais_reportados(id_linha,con)
        estacao = banco.estacao_reportes(id_linha,con)
    return {"sucesso": True, "overview": {"recentes": reportes_recentes,"solucionados":reportes_solucionados,"mais_reportado":mais_reportados,"estacao":estacao}}