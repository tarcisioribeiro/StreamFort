bank_accounts_with_name_query = """
SELECT
    COUNT(id)
FROM
    contas_bancarias
WHERE
    nome_conta = %s
    AND
        id_prop_conta = %s
    AND
        doc_prop_conta = %s;
"""

insert_password_query = """
INSERT INTO
    contas_bancarias (
        nome_conta,
        instituicao,
        cod_instituicao,
        agencia,
        numero_conta,
        digito_conta,
        senha_bancaria,
        senha_digital,
        id_prop_conta,
        doc_prop_conta
        )
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

account_details_query = '''
SELECT
    CONCAT('Conta: ',
            cb.nome_conta,
            ' - Instituição: ',
            cb.instituicao),
    cb.agencia,
    CONCAT('',
            cb.numero_conta,
            '-',
            cb.digito_conta),
    cb.senha_bancaria,
    cb.senha_digital
FROM
    contas_bancarias AS cb
WHERE
    cb.nome_conta = %s
    AND cb.id_prop_conta = %s
    AND cb.doc_prop_conta = %s;
'''

update_account_query = '''
UPDATE
    contas_bancarias
SET
    senha_bancaria = %s,
    senha_digital = %s
WHERE
    nome_conta = %s
    AND
        id_prop_conta = %s
    AND
        doc_prop_conta = %s;
'''

delete_account_query = '''
DELETE
    contas_bancarias
FROM
    contas_bancarias
WHERE
    nome_conta = %s
    AND
        id_prop_conta = %s
    AND
        doc_prop_conta = %s;
'''

check_user_bank_accounts_query = '''
SELECT
    COUNT(cb.id)
FROM
    contas_bancarias AS cb
INNER JOIN
    usuarios AS u
    ON cb.id_prop_conta = u.id
    AND cb.doc_prop_conta = u.documento
WHERE
    cb.id_prop_conta = %s
    AND cb.doc_prop_conta = %s;
'''

search_bank_accounts_query = """
SELECT
    cb.nome_conta
FROM
    contas_bancarias AS cb
INNER JOIN usuarios AS u
    ON cb.id_prop_conta = u.id
    AND cb.doc_prop_conta = u.documento
WHERE
    cb.id_prop_conta = %s
    AND cb.doc_prop_conta = %s
ORDER BY
    cb.nome_conta;
"""
