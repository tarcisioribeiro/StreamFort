delete_archive_query = '''
DELETE
    txt
FROM
    arquivo_texto AS txt
INNER JOIN
    usuarios AS users
    ON txt.id_usuario = users.id
    AND txt.doc_usuario = users.documento
WHERE
    txt.nome_arquivo = %s
    AND txt.id_usuario = %s
    AND txt.doc_usuario = %s;
'''

archive_content_query = """
SELECT
    txt.nome_arquivo,
    txt.conteudo
FROM
    arquivo_texto AS txt
INNER JOIN
    usuarios AS users
    ON txt.id_usuario = users.id
AND
    txt.doc_usuario = users.documento
WHERE
    txt.nome_arquivo = %s
AND
    txt.id_usuario = %s
    AND txt.doc_usuario = %s;
"""

insert_archive_query = """
INSERT INTO
    arquivo_texto (
        nome_arquivo,
        conteudo,
        id_usuario,
        doc_usuario
        )
VALUES (%s, %s, %s, %s)
"""

archives_with_name_query = """
SELECT
    COUNT(id)
FROM
    arquivo_texto
WHERE
    nome_arquivo = %s
    AND
        id_usuario = %s
    AND
        doc_usuario = %s;
"""

search_user_archives_quantity = """
SELECT
    COUNT(at.id)
FROM
    arquivo_texto AS at
INNER JOIN
    usuarios AS u
    ON at.id_usuario = u.id
    AND at.doc_usuario = u.documento
WHERE
    at.id_usuario = %s
    AND at.doc_usuario = %s;
"""

search_user_archives_name = """
SELECT
    at.nome_arquivo
FROM
    arquivo_texto AS at
INNER JOIN
    usuarios AS u
    ON at.id_usuario = u.id
    AND at.doc_usuario = u.documento
WHERE
    at.id_usuario = %s
    AND at.doc_usuario = %s;
"""
