from data.session_state import logged_user, logged_user_password


search_accounts_query = """
    SELECT 
        senhas.nome_site
    FROM
        senhas
            INNER JOIN
        usuarios ON senhas.usuario_associado = usuarios.nome
            AND senhas.documento_usuario_associado = usuarios.documento_usuario
    WHERE
        usuarios.login = %s
            AND usuarios.senha = %s
    ORDER BY senhas.nome_site;
"""

search_user_credit_cards_number = """
    SELECT 
        COUNT(cartao_credito.id_cartao)
    FROM
        cartao_credito
            INNER JOIN
        usuarios ON cartao_credito.proprietario_cartao = usuarios.nome
            AND cartao_credito.documento_titular = usuarios.documento_usuario
    WHERE
        cartao_credito.proprietario_cartao = %s
        AND
        cartao_credito.documento_titular = %s;
"""

search_user_credit_cards_names = """
    SELECT 
        cartao_credito.nome_cartao
    FROM
        cartao_credito
            INNER JOIN
        usuarios ON cartao_credito.proprietario_cartao = usuarios.nome
            AND cartao_credito.documento_titular = usuarios.documento_usuario
    WHERE
        cartao_credito.proprietario_cartao = %s
            AND cartao_credito.documento_titular = %s;
"""

search_user_archives_quantity = """
    SELECT 
        COUNT(arquivo_texto.id_arquivo)
    FROM
        arquivo_texto
            INNER JOIN
        usuarios ON arquivo_texto.usuario_associado = usuarios.nome
            AND arquivo_texto.documento_usuario_associado = usuarios.documento_usuario
    WHERE
        arquivo_texto.usuario_associado = %s
            AND arquivo_texto.documento_usuario_associado = %s;
"""

search_user_archives_name = """
    SELECT 
        arquivo_texto.nome_arquivo
    FROM
        arquivo_texto
            INNER JOIN
        usuarios ON arquivo_texto.usuario_associado = usuarios.nome
            AND arquivo_texto.documento_usuario_associado = usuarios.documento_usuario
    WHERE
        arquivo_texto.usuario_associado = %s
            AND arquivo_texto.documento_usuario_associado = %s;
"""

check_user_query = '''SELECT COUNT(id_usuario) FROM usuarios;'''

check_user_passwords_quantity_query = '''
    SELECT 
        COUNT(senhas.id_senha)
    FROM
        senhas
            INNER JOIN
        usuarios ON usuarios.nome = senhas.usuario_associado
            AND usuarios.documento_usuario = senhas.documento_usuario_associado
    WHERE
        usuarios.login = %s
            AND usuarios.senha = %s;
'''

user_passwords_query = '''
    SELECT 
        senhas.senha
    FROM
        senhas
            INNER JOIN
        usuarios ON usuarios.nome = senhas.usuario_associado
            AND usuarios.documento_usuario = senhas.documento_usuario_associado
    WHERE
        usuarios.login = %s
            AND usuarios.senha = %s;
'''

check_user_bank_accounts_query = '''
    SELECT 
        COUNT(contas_bancarias.id_conta)
    FROM
        contas_bancarias
            INNER JOIN
        usuarios ON contas_bancarias.nome_proprietario_conta = usuarios.nome
            AND contas_bancarias.documento_proprietario_conta = usuarios.documento_usuario
    WHERE
        contas_bancarias.nome_proprietario_conta = %s
            AND contas_bancarias.documento_proprietario_conta = %s;
'''

search_bank_accounts_query = """
    SELECT 
        contas_bancarias.nome_conta
    FROM
        contas_bancarias
            INNER JOIN
        usuarios ON contas_bancarias.nome_proprietario_conta = usuarios.nome
            AND contas_bancarias.documento_proprietario_conta = usuarios.documento_usuario
    WHERE
        contas_bancarias.nome_proprietario_conta = %s
            AND contas_bancarias.documento_proprietario_conta = %s
    ORDER BY contas_bancarias.nome_conta;
"""