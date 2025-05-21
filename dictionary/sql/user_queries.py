user_data_query = """
SELECT
    u.id, u.documento
FROM
    usuarios AS u
INNER JOIN
    usuarios_logados AS ul
    ON u.id = ul.id_usuario
WHERE
    ul.sessao_id = %s;
"""

name_query: str = """
SELECT
    nome
FROM
    usuarios
WHERE
    id = %s
AND documento = %s;"""

sex_query: str = """
SELECT
    sexo
FROM
    usuarios
WHERE
    id = %s
AND documento = %s;
"""

name_doc_query = """
SELECT
    id, nome, documento
FROM
    usuarios
WHERE
    login = %s
    AND senha = %s;
"""

insert_new_user_query = """
INSERT INTO
    usuarios (
        login,
        senha,
        nome,
        documento,
        sexo
    )
VALUES (%s, %s, %s, %s, %s);
"""

check_if_user_document_exists_query = """
SELECT
    COUNT(id)
FROM
    usuarios
WHERE
    documento_usuario = %s;
"""

check_user_query = '''SELECT COUNT(id) FROM usuarios;'''

check_user_id_query = """
SELECT
    id
FROM
    usuarios
WHERE
    login = %s
    AND documento = %s;
"""
