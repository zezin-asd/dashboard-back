import oracledb
from datetime import datetime

def get_conexao():
    con = oracledb.connect(user="rm561187", password="240805",
                          dsn="oracle.fiap.com.br/orcl")
    return con

def recuperar_admin(username):
    sel = '''
    SELECT 
    A.senha, 
    A.id_cco, 
    C.nome_cco
    FROM 
    ADMIN_VM A
    JOIN 
    CCO_VM C ON A.id_cco = C.id_cco
    WHERE 
    A.username = :username
    '''
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sel, {"username": username})
            dados = cur.fetchone()
    if dados is not None:
        return dados
    else:
        return None
    
def buscar_reportes(id_linha):
    sel = '''
    SELECT
    c.ID_REPORTE, 
    c.ID_LINHA, 
    c.ID_ESTACAO, 
    c.DATA_CRIACAO,
    c.TIPO_REPORTE,
    UPPER(d.NOME_LINHA) AS NOME_LINHA
    FROM REPORTE_VM c
    JOIN LINHA_VM d ON d.ID_LINHA = c.ID_LINHA
    WHERE c.ID_LINHA = :linha AND c.ANALISADO = 'N'
    ORDER BY c.DATA_CRIACAO DESC
    '''
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sel, {"linha": id_linha})
            colunas = [desc[0].lower() for desc in cur.description]
            dados = cur.fetchall()
    lista_dicionarios = [dict(zip(colunas, linha)) for linha in dados]
    if lista_dicionarios:
        return lista_dicionarios
    else:
        return None
    
def buscar_reporte(id_reporte):
    sel = '''
    SELECT ID_REPORTE,DATA_OCORRENCIA,ID_LINHA,ID_ESTACAO,HORA_OCORRENCIA,TIPO_REPORTE,DESCRICAO,DATA_CRIACAO
    FROM
    REPORTE_VM
    WHERE ID_REPORTE = :reporte
    '''
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sel, {"reporte": id_reporte})
            colunas = [desc[0].lower() for desc in cur.description]
            linha = cur.fetchone()
    if linha:
        return dict(zip(colunas, linha))
    else:
        return None
    
def marcar_analisado(id_reporte,analisado):
    upt = "UPDATE REPORTE_VM SET ANALISADO = :analisado WHERE ID_REPORTE = :id_reporte"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(upt, {"id_reporte":id_reporte, "analisado": analisado})
        con.commit()
    return True

def buscar_historico(id_linha):
    sel = '''
    SELECT
    c.ID_REPORTE, 
    c.ID_LINHA, 
    c.ID_ESTACAO, 
    c.DATA_CRIACAO,
    c.TIPO_REPORTE,
    UPPER(d.NOME_LINHA) AS NOME_LINHA
    FROM REPORTE_VM c
    JOIN LINHA_VM d ON d.ID_LINHA = c.ID_LINHA
    WHERE c.ID_LINHA = :linha AND c.ANALISADO = 'S'
    ORDER BY c.DATA_CRIACAO DESC
    '''
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sel, {"linha": id_linha})
            colunas = [desc[0].lower() for desc in cur.description]
            dados = cur.fetchall()
    lista_dicionarios = [dict(zip(colunas, linha)) for linha in dados]
    if lista_dicionarios:
        return lista_dicionarios
    else:
        return None
    
def reportes_recentes(id_linha,con):
    sel = '''
    SELECT 
    COUNT(ID_REPORTE) AS reportes_recentes
    FROM REPORTE_VM
    WHERE DATA_CRIACAO >= SYSDATE - 1 AND ID_LINHA=:id_linha
    '''
    with con.cursor() as cur:
        cur.execute(sel, {"id_linha": id_linha})
        dados = cur.fetchone()
    if dados:
        return dados[0]
    else:
        return None

def reportes_solucionados(id_linha,con):
    sel = '''
    SELECT 
    COUNT(ID_REPORTE) AS reportes_recentes
    FROM REPORTE_VM
    WHERE DATA_CRIACAO >= SYSDATE - 1 AND ID_LINHA=:id_linha AND ANALISADO='S'
    '''
    with con.cursor() as cur:
        cur.execute(sel, {"id_linha": id_linha})
        dados = cur.fetchone()
    if dados:
        return dados[0]
    else:
        return None

def mais_reportados(id_linha,con):
    sel = '''
    SELECT TIPO_REPORTE, COUNT(*) AS quantidade
    FROM REPORTE_VM
    WHERE DATA_CRIACAO >= SYSDATE - 1
    AND ID_LINHA = :id_linha
    GROUP BY TIPO_REPORTE
    ORDER BY quantidade DESC
    FETCH FIRST 1 ROWS ONLY
    '''
    with con.cursor() as cur:
        cur.execute(sel, {"id_linha": id_linha})
        dados = cur.fetchone()
    if dados:
        return dados[0]
    else:
        return None

def estacao_reportes(id_linha,con):
    sel = '''
    SELECT ID_ESTACAO, COUNT(*) AS QTD_REPORTES
    FROM REPORTE_VM
    WHERE DATA_CRIACAO >= SYSDATE - 1
    AND ID_LINHA = :id_linha
    GROUP BY ID_ESTACAO
    ORDER BY QTD_REPORTES DESC
    FETCH FIRST 1 ROWS ONLY
    '''
    with con.cursor() as cur:
        cur.execute(sel, {"id_linha": id_linha})
        dados = cur.fetchone()
    if dados:
        return dados[0]
    else:
        return None