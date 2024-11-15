from data.session_state import logged_user, logged_user_password


name_doc_query = """SELECT nome, documento_usuario FROM usuarios WHERE login = '{}' AND senha = '{}';""".format(logged_user, logged_user_password)

search_accounts_query = """
    SELECT 
        senhas.nome_site
    FROM
        senhas
            INNER JOIN
        usuarios ON senhas.usuario_associado = usuarios.nome
            AND senhas.documento_usuario_associado = usuarios.documento_usuario
    WHERE
        usuarios.login = '{}'
            AND usuarios.senha = '{}'
    ORDER BY senhas.nome_site;
""".format(logged_user, logged_user_password)

search_user_credit_cards_number = """
    SELECT 
        COUNT(cartao_credito.id_cartao)
    FROM
        cartao_credito
            INNER JOIN
        usuarios ON cartao_credito.proprietario_cartao = usuarios.nome
            AND cartao_credito.documento_titular = usuarios.documento_usuario
    WHERE
        usuarios.login = '{}'
            AND usuarios.senha = '{}';
""".format(logged_user, logged_user_password)

search_user_credit_cards_names = """
    SELECT 
        cartao_credito.nome_cartao
    FROM
        cartao_credito
            INNER JOIN
        usuarios ON cartao_credito.proprietario_cartao = usuarios.nome
            AND cartao_credito.documento_titular = usuarios.documento_usuario
    WHERE
        usuarios.login = '{}'
            AND usuarios.senha = '{}';
""".format(logged_user, logged_user_password)

search_user_archives_quantity = """
    SELECT 
        COUNT(arquivo_texto.id_arquivo)
    FROM
        arquivo_texto
            INNER JOIN
        usuarios ON arquivo_texto.usuario_associado = usuarios.nome
            AND arquivo_texto.documento_usuario_associado = usuarios.documento_usuario
    WHERE
        usuarios.login = '{}'
            AND usuarios.senha = '{}';
""".format(logged_user, logged_user_password)

search_user_archives_name = """
    SELECT 
        arquivo_texto.nome_arquivo
    FROM
        arquivo_texto
            INNER JOIN
        usuarios ON arquivo_texto.usuario_associado = usuarios.nome
            AND arquivo_texto.documento_usuario_associado = usuarios.documento_usuario
    WHERE
        usuarios.login = '{}'
            AND usuarios.senha = '{}';
""".format(logged_user, logged_user_password)

check_user_query = '''SELECT COUNT(id_usuario) FROM usuarios;'''

name_query: str = "SELECT nome FROM usuarios WHERE login = '{}' AND senha = '{}'".format(logged_user, logged_user_password)

sex_query: str = "SELECT sexo FROM usuarios WHERE login = '{}' AND senha = '{}'".format(logged_user, logged_user_password)

check_user_passwords_quantity_query = '''
    SELECT 
        COUNT(senhas.id_senha)
    FROM
        senhas
            INNER JOIN
        usuarios ON usuarios.nome = senhas.usuario_associado
            AND usuarios.documento_usuario = senhas.documento_usuario_associado
    WHERE
        usuarios.login = '{}'
            AND usuarios.senha = '{}';
'''.format(logged_user, logged_user_password)

user_passwords_query = '''
    SELECT 
        senhas.senha
    FROM
        senhas
            INNER JOIN
        usuarios ON usuarios.nome = senhas.usuario_associado
            AND usuarios.documento_usuario = senhas.documento_usuario_associado
    WHERE
        usuarios.login = '{}'
            AND usuarios.senha = '{}'
            AND senhas.ativa = 'S';
'''.format(logged_user, logged_user_password)

check_user_bank_accounts_query = '''
    SELECT 
        COUNT(contas_bancarias.id_conta)
    FROM
        contas_bancarias
            INNER JOIN
        usuarios ON contas_bancarias.nome_proprietario_conta = usuarios.nome
            AND contas_bancarias.documento_proprietario_conta = usuarios.documento_usuario
    WHERE
        usuarios.login = '{}'
            AND usuarios.senha = '{}';
'''.format(logged_user, logged_user_password)

search_bank_accounts_query = """
    SELECT 
        contas_bancarias.nome_conta
    FROM
        contas_bancarias
            INNER JOIN
        usuarios ON contas_bancarias.nome_proprietario_conta = usuarios.nome
            AND contas_bancarias.documento_proprietario_conta = usuarios.documento_usuario
    WHERE
        usuarios.login = '{}'
            AND usuarios.senha = '{}'
    ORDER BY contas_bancarias.nome_conta;
""".format(logged_user, logged_user_password)