search_user_credit_cards_number = """
SELECT
    COUNT(cc.id)
FROM
    cartao_credito AS cc
INNER JOIN
    usuarios AS u
    ON cc.id_prop_cartao = u.id
    AND cc.doc_titular_cartao = u.documento
WHERE
    cc.id_prop_cartao = %s
    AND cc.doc_titular_cartao = %s;
"""

search_user_credit_cards_names = """
SELECT
    cc.nome_cartao
FROM
    cartao_credito AS cc
INNER JOIN
    usuarios AS u
    ON cc.id_prop_cartao = u.id
    AND cc.doc_titular_cartao = u.documento
WHERE
    cc.id_prop_cartao = %s
    AND cc.doc_titular_cartao = %s;
"""

cards_with_name_query = """
SELECT
    COUNT(id)
FROM
    cartao_credito
WHERE
    nome_cartao = %s
    AND id_prop_cartao = %s
    AND doc_titular_cartao = %s;
"""

card_insert_query = """
INSERT INTO
    seguranca.cartao_credito (
        nome_cartao,
        numero_cartao,
        nome_titular,
        id_prop_cartao,
        doc_titular_cartao,
        data_validade,
        codigo_seguranca
    )
VALUES (%s, %s, %s, %s, %s, %s, %s);
"""

credit_card_data_query = '''
SELECT
    CONCAT(
        cc.numero_cartao,
        ' - ',
        cc.nome_cartao
    ),
    cc.nome_titular,
    DATE_FORMAT(
        cc.data_validade,
        '%d/%m/%Y'
    ),
    cc.codigo_seguranca
FROM
    cartao_credito AS cc
INNER JOIN usuarios AS users
ON
    cc.id_prop_cartao = users.id
AND
cc.doc_titular_cartao = users.documento
WHERE
    cc.id_prop_cartao = %s
AND cc.doc_titular_cartao = %s
AND cc.nome_cartao = %s;
'''

update_card_query = '''
UPDATE
    cartao_credito
SET
    numero_cartao = %s,
    data_validade = %s,
    codigo_seguranca = %s
WHERE
    nome_cartao = %s;
'''

delete_card_query = '''
DELETE
    cartao_credito
FROM
    cartao_credito
WHERE
    nome_cartao = %s
    AND
    id_prop_cartao = %s
    AND doc_titular_cartao = %s;
'''
