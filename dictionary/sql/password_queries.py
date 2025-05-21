search_accounts_query = """
SELECT
    s.nome
FROM
    senhas AS s
INNER JOIN
    usuarios AS u
    ON s.id_usuario = u.id
    AND s.doc_usuario = u.documento
WHERE
    u.id = %s
    AND u.documento = %s
ORDER BY s.nome;
"""

check_user_passwords_quantity_query = '''
SELECT
    COUNT(s.id)
FROM
    senhas AS s
INNER JOIN usuarios AS u
    ON u.id = s.id_usuario
    AND u.documento = s.doc_usuario
WHERE
    u.id = %s
    AND u.documento = %s;
'''

user_passwords_query = '''
SELECT
    s.senha
FROM
    senhas AS s
INNER JOIN
    usuarios AS u
    ON u.id = s.id_usuario
    AND u.documento = s.doc_usuario
WHERE
    u.id = %s
    AND u.documento = %s;
'''

delete_password_query = '''
DELETE
    senhas
FROM
    senhas
WHERE
    nome = %s
    AND
        id_usuario = %s
    AND
        doc_usuario = %s;
    '''

accounts_with_parameter_name_query = """
SELECT
    COUNT(id)
FROM
    senhas
WHERE
    nome = %s
    AND id_usuario = %s
    AND doc_usuario = %s;
"""

insert_password_query = """
INSERT INTO
senhas(
    nome,
    url,
    login,
    senha,
    id_usuario,
    doc_usuario
)
VALUES(%s, %s, %s, %s, %s, %s);
"""

account_details_query = '''
SELECT
    s.nome,
    s.url,
    s.login,
    s.senha
FROM
    senhas AS s
WHERE
    s.nome = %s
    AND s.id_usuario = %s
    AND s.doc_usuario = %s;
'''

update_site_query = '''
UPDATE senhas
SET
    url = %s,
    login = %s,
    senha = %s
WHERE
    nome = %s
    AND
        id_usuario = %s
    AND
        doc_usuario = %s;
'''
