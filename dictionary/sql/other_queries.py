log_query = '''
INSERT INTO
    logs_atividades (
        id_usuario,
        tipo_log,
        conteudo_log
    )
VALUES (%s, %s, %s);'''

delete_session_query = """
DELETE
    usuarios_logados
FROM
    usuarios_logados
WHERE
    id_usuario = %s
    AND
    documento = %s;
"""

register_session_query = """
INSERT INTO
    usuarios_logados (
        id_usuario,
        nome_completo,
        documento,
        sessao_id
    )
VALUES (%s, %s, %s, %s)
ON DUPLICATE KEY
UPDATE
    data_login = CURRENT_TIMESTAMP,
    sessao_id = VALUES(sessao_id);
"""
