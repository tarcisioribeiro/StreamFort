from data.session_state import logged_user
from data.user_data import logged_user_name, logged_user_document
from dictionary.sql import check_user_bank_accounts_query, search_bank_accounts_query
from dictionary.vars import financial_institution_list, to_remove_list, bank_account_field_names
from functions.query_executor import QueryExecutor
from functions.login import User
from time import sleep
import streamlit as st


class BankAccount:

    def __init__(self):

        query_executor = QueryExecutor()
        user = User()

        def create_new_bank_account():
            col1, col2 = st.columns(2)

            with col1:
                with st.expander(label="Dados da Conta", expanded=True):
                    account_name = st.text_input(label="Nome", max_chars=100, placeholder='Conta', help="Necessário para identificação. A sugestão é informar algo direto e descritivo, como por exemplo 'Conta Corrente BB'.")
                    financial_institution = st.selectbox(label='Instituição', options=financial_institution_list, help='Insituição financeira a qual pertence a conta.')
                    financial_institution_code = st.text_input(label="Código da instituição", max_chars=5, help="Código da insituição financiera no SPB (Sistemas de Pagamentos Brasileiro).")
                    agency = st.text_input(label="Agência", max_chars=10, help="Número da agência.")
                
                confirm_data = st.checkbox(label="Confirmar dados")

            with col2:
                with st.expander(label="Dados da Conta", expanded=True):
                    account_number = st.text_input(label="Número da conta", max_chars=15, help="Número de identificação da conta.")
                    account_digit = st.text_input(label="Dígito", max_chars=1, placeholder='0', help='Dígito identificador da conta. Caso não haja, preencha como 0.')
                    account_password = st.text_input(label="Senha da conta", max_chars=30, type='password', help='Senha utilizada para saques e demais operações em terminais físicos.')
                    digital_account_password = st.text_input(label="Senha digital da conta", max_chars=30, type='password', help='Senha digital da conta, utilizada para operações virtuais como Pix.')
                    
                register_new_account = st.button(label=":floppy_disk: Cadastrar conta")

                if confirm_data == True and register_new_account:
                    
                    with col2:
                        with st.spinner(text='Aguarde...'):
                            sleep(2.5)
                    
                    insert_password_query = "INSERT INTO contas_bancarias(nome_conta, instituicao_financeira, codigo_instituicao_financeira, agencia, numero_conta, digito_conta, senha_bancaria_conta, senha_digital_conta, nome_proprietario_conta, documento_proprietario_conta) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    query_values = (account_name, financial_institution, financial_institution_code, agency, account_number, account_digit, account_password, digital_account_password, logged_user_name, logged_user_document)

                    query_executor.insert_query(insert_password_query, query_values, 'Conta cadastrada com sucesso!', 'Erro ao cadastrar conta:')

                    log_query = '''INSERT INTO logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)'''
                    log_query_values = (logged_user, 'Cadastro', 'Cadastrou a conta {}'.format(query_values[0]))
                    query_executor.insert_query(query=log_query, values=log_query_values, success_message='Log gravado.', error_message='Erro ao gravar log:')

                elif register_new_account and confirm_data == False:
                    with col2:
                        with st.spinner(text="Aguarde..."):
                            sleep(0.5)
                        st.warning(body="Você deve confirmar os dados antes de prosseguir.")

        def read_bank_accounts():

            user_accounts_quantity = query_executor.simple_consult_query(check_user_bank_accounts_query, params=(logged_user_name, logged_user_document))
            user_accounts_quantity = query_executor.treat_simple_result(user_accounts_quantity, to_remove_list)
            user_accounts_quantity = int(user_accounts_quantity)

            if user_accounts_quantity == 0:

                col1, col2, col3 = st.columns(3)

                with col2:
                    st.warning(body="Você ainda não possui contas cadastradas.")

            elif user_accounts_quantity >= 1:

                col1, col2 = st.columns(2)

                user_bank_accounts = []

                bank_accounts = query_executor.complex_consult_query(query=search_bank_accounts_query, params=(logged_user_name, logged_user_document))
                bank_accounts = query_executor.treat_numerous_simple_result(bank_accounts, to_remove_list)

                for i in range(0, len(bank_accounts)):
                    user_bank_accounts.append(bank_accounts[i])

                with col1:
                    with st.expander(label="Dados", expanded=True):
                        selected_option = st.selectbox(label="Selecione a conta", options=user_bank_accounts)
                        safe_password = st.text_input(label="Informe sua senha", type="password")
                        confirm_safe_password = st.text_input(label="Confirme sua senha", type="password")
                        confirm_password_selection = st.checkbox(label="Confirmar seleção")

                    consult_button = st.button(label=":file_folder: Consultar conta")

                account_details_query = '''
                SELECT 
                    CONCAT('Conta: ',
                            contas_bancarias.nome_conta,
                            ' - Instituição: ',
                            contas_bancarias.instituicao_financeira),
                    contas_bancarias.agencia,
                    CONCAT('',
                            contas_bancarias.numero_conta,
                            '-',
                            contas_bancarias.digito_conta),
                    contas_bancarias.senha_bancaria_conta,
                    contas_bancarias.senha_digital_conta
                FROM
                    contas_bancarias
                WHERE
                    contas_bancarias.nome_conta = %s
                        AND contas_bancarias.nome_proprietario_conta = %s
                        AND contas_bancarias.documento_proprietario_conta = %s;'''

                result_list = query_executor.complex_consult_query(query=account_details_query, params=(selected_option, logged_user_name, logged_user_document))
                result_list = query_executor.treat_complex_result(values_to_treat=result_list, values_to_remove=to_remove_list)

                if confirm_password_selection and consult_button:

                    is_password_valid, hashed_password = user.check_login(logged_user, safe_password)

                    if safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == True:

                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(2.5)

                            with st.expander(label="Dados", expanded=True):

                                aux_string = ''

                                for i in range(0, len(result_list)):
                                    
                                    st.write(bank_account_field_names[i])
                                    aux_string = str(result_list[i])
                                    aux_string = aux_string.replace('"', '')
                                    if aux_string[0] == 'b':
                                        aux_string = aux_string.replace('b', '')
                                    st.code(body="{}".format(aux_string))

                                log_query = '''INSERT into logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)'''
                                query_values = (logged_user, 'Consulta', 'Consultou a conta bancária {}'.format(selected_option))
                                query_executor.insert_query(query=log_query, values=query_values, success_message='Log gravado.', error_message='Erro ao gravar log:')
                    
                    elif safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == False:
                        
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            st.error(body="A senha informada é inválida.")

                    elif safe_password != "" and confirm_safe_password != "" and safe_password != confirm_safe_password:
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            st.error(body="As senhas informadas não coincidem.")

                elif confirm_password_selection == False and consult_button:
                    with col2:
                        st.warning(body="Confirme a seleção da conta.")

        def update_bank_account():

            user_accounts_quantity = query_executor.simple_consult_query(check_user_bank_accounts_query, params=(logged_user_name, logged_user_document))
            user_accounts_quantity = query_executor.treat_simple_result(user_accounts_quantity, to_remove_list)
            user_accounts_quantity = int(user_accounts_quantity)

            if user_accounts_quantity == 0:

                col1, col2, col3 = st.columns(3)

                with col2:
                    st.warning(body="Você ainda não possui contas cadastradas.")

            elif user_accounts_quantity >= 1:
                    
                col1, col2 = st.columns(2)

                user_bank_accounts = []

                bank_accounts = query_executor.complex_consult_query(query=search_bank_accounts_query, params=(logged_user_name, logged_user_document))
                bank_accounts = query_executor.treat_numerous_simple_result(bank_accounts, to_remove_list)

                for i in range(0, len(bank_accounts)):
                    user_bank_accounts.append(bank_accounts[i])

                with col1:
                    with st.expander(label="Dados", expanded=True):
                        selected_option = st.selectbox(label="Selecione a conta", options=user_bank_accounts)
                        safe_password = st.text_input(label="Informe sua senha", type="password")
                        confirm_safe_password = st.text_input(label="Confirme sua senha", type="password")
                        confirm_selection = st.checkbox(label="Confirmar seleção")

                account_details_query = '''
                SELECT 
                    CONCAT('Conta: ',
                            contas_bancarias.nome_conta,
                            ' - Instituição: ',
                            contas_bancarias.instituicao_financeira),
                    contas_bancarias.agencia,
                    CONCAT('',
                            contas_bancarias.numero_conta,
                            '-',
                            contas_bancarias.digito_conta),
                    contas_bancarias.senha_bancaria_conta,
                    contas_bancarias.senha_digital_conta
                FROM
                    contas_bancarias
                WHERE
                    contas_bancarias.nome_conta = %s
                        AND contas_bancarias.nome_proprietario_conta = %s
                        AND contas_bancarias.documento_proprietario_conta = %s;'''

                result_list = query_executor.complex_consult_query(query=account_details_query, params=(selected_option, logged_user_name, logged_user_document))
                result_list = query_executor.treat_complex_result(values_to_treat=result_list, values_to_remove=to_remove_list)

                if confirm_selection:

                    is_password_valid, hashed_password = user.check_login(logged_user, safe_password)

                    if safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == True:

                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)

                            with st.expander(label="Novos Dados", expanded=True):

                                aux_string = ''

                                for i in range(0, 3):
                                    
                                    st.write(bank_account_field_names[i])
                                    aux_string = str(result_list[i])
                                    aux_string = aux_string.replace('"', '')
                                    if aux_string[0] == 'b':
                                        aux_string = aux_string.replace('b', '')
                                    st.code(body="{}".format(aux_string))

                                account_password = st.text_input(label="Senha da conta", max_chars=30, type='password', help='Senha utilizada para saques e demais operações em terminais físicos.')
                                digital_account_password = st.text_input(label="Senha digital da conta", max_chars=30, type='password', help='Senha digital da conta, utilizada para operações virtuais como Pix.')

                                confirm_new_bank_account_data = st.checkbox(label="Confirmar novos dados")

                            update_bank_account_button = st.button(label=":arrows_counterclockwise: Atualizar dados da conta")

                        if confirm_new_bank_account_data and update_bank_account_button and account_password != "" and digital_account_password != "":
                            with col3:
                                with st.spinner(text="Aguarde..."):
                                    sleep(2.5)
                            
                            update_account_query = '''UPDATE contas_bancarias SET senha_bancaria_conta = %s, senha_digital_conta = %s WHERE nome_conta = %s AND nome_proprietario_conta = %s AND documento_proprietario_conta = %s;'''
                            update_account_values = (account_password, digital_account_password, selected_option, logged_user_name, logged_user_document)

                            query_executor.insert_query(query=update_account_query, values=update_account_values, success_message="Conta atualizada com sucesso!", error_message="Erro ao atualizar conta:")

                            log_query = '''INSERT into logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)'''
                            query_values = (logged_user, 'Atualização', 'Atualizou a conta bancária {}'.format(selected_option))
                            query_executor.insert_query(query=log_query, values=query_values, success_message='Log gravado.', error_message='Erro ao gravar log:')

                        elif confirm_new_bank_account_data == False and update_bank_account_button and account_password != "" and digital_account_password != "":
                            with col3:
                                st.warning(body="Confirme os novos dados da conta.")

                    elif safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == False:
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            st.error(body="A senha informada é inválida.")

                    elif safe_password != confirm_safe_password:
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            st.error(body="As senhas informadas não coincidem.")

        def delete_bank_account():
            user_accounts_quantity = query_executor.simple_consult_query(check_user_bank_accounts_query, params=(logged_user_name, logged_user_document))
            user_accounts_quantity = query_executor.treat_simple_result(user_accounts_quantity, to_remove_list)
            user_accounts_quantity = int(user_accounts_quantity)

            if user_accounts_quantity == 0:

                col1, col2, col3 = st.columns(3)

                with col2:
                    st.warning(body="Você ainda não possui contas cadastradas.")

            elif user_accounts_quantity >= 1:

                col1, col2 = st.columns(2)

                user_bank_accounts = []

                bank_accounts = query_executor.complex_consult_query(query=search_bank_accounts_query, params=(logged_user_name, logged_user_document))
                bank_accounts = query_executor.treat_numerous_simple_result(bank_accounts, to_remove_list)

                for i in range(0, len(bank_accounts)):
                    user_bank_accounts.append(bank_accounts[i])

                with col1:
                    with st.expander(label="Dados", expanded=True):
                        selected_option = st.selectbox(label="Selecione a conta", options=user_bank_accounts)
                        safe_password = st.text_input(label="Informe sua senha", type="password")
                        confirm_safe_password = st.text_input(label="Confirme sua senha", type="password")
                        confirm_password_selection = st.checkbox(label="Confirmar seleção")

                account_details_query = '''
                SELECT 
                    CONCAT('Conta: ',
                            contas_bancarias.nome_conta,
                            ' - Instituição: ',
                            contas_bancarias.instituicao_financeira),
                    contas_bancarias.agencia,
                    CONCAT('',
                            contas_bancarias.numero_conta,
                            '-',
                            contas_bancarias.digito_conta),
                    contas_bancarias.senha_bancaria_conta,
                    contas_bancarias.senha_digital_conta
                FROM
                    contas_bancarias
                WHERE
                    contas_bancarias.nome_conta = %s
                        AND contas_bancarias.nome_proprietario_conta = %s
                        AND contas_bancarias.documento_proprietario_conta = %s;'''

                result_list = query_executor.complex_consult_query(query=account_details_query, params=(selected_option, logged_user_name, logged_user_document))
                result_list = query_executor.treat_complex_result(values_to_treat=result_list, values_to_remove=to_remove_list)

                if confirm_password_selection:

                    is_password_valid, hashed_password = user.check_login(logged_user, safe_password)

                    if safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == True:

                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)

                            with st.expander(label="Dados", expanded=True):

                                aux_string = ''

                                for i in range(0, len(result_list)):
                                    
                                    st.write(bank_account_field_names[i])
                                    aux_string = str(result_list[i])
                                    aux_string = aux_string.replace('"', '')
                                    if aux_string[0] == 'b':
                                        aux_string = aux_string.replace('b', '')
                                    st.code(body="{}".format(aux_string))
                                
                                confirm_account_deletion = st.checkbox(label="Confirmar exclusão da conta")

                            delete_account_button = st.button(label=":wastebasket: Deletar conta")

                            if delete_account_button and confirm_account_deletion:

                                with col2:
                                    with st.spinner(text="Aguarde..."):
                                        sleep(2.5)
                                
                                    delete_account_query = '''DELETE contas_bancarias FROM contas_bancarias WHERE nome_conta = %s AND nome_proprietario_conta = %s AND documento_proprietario_conta = %s;'''
                                    delete_account_values = (selected_option, logged_user_name, logged_user_document)

                                    query_executor.insert_query(query=delete_account_query, values=delete_account_values, success_message="Conta excluída com sucesso!", error_message="Erro ao excluir conta:")

                                    log_query = '''INSERT into logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)'''
                                    query_values = (logged_user, 'Exclusão', 'Excluiu a conta bancária {}'.format(selected_option))
                                    query_executor.insert_query(query=log_query, values=query_values, success_message='Log gravado.', error_message='Erro ao gravar log:')

                            elif delete_account_button and confirm_account_deletion == False:
                                with col2:
                                    st.warning(body="Confirme a exclusão da conta.")
                    
                    elif safe_password != "" and confirm_safe_password != "" and safe_password == confirm_safe_password and is_password_valid == False:
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            st.error(body="A senha informada é inválida.")

                    elif safe_password != confirm_safe_password:
                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(0.5)
                            st.error(body="As senhas informadas não coincidem.")

        def back_account_main_menu():
            col1, col2, col3 = st.columns(3)

            with col1:
                st.header(body=":bank: Contas Bancárias")

            with col2:
                menu_options = ["Cadastrar conta", "Consultar conta", "Atualizar conta", "Deletar conta"]
                selected_option = st.selectbox(label="Menu", options=menu_options)

            st.divider()

            if selected_option == menu_options[0]:
                create_new_bank_account()

            if selected_option == menu_options[1]:
                read_bank_accounts()

            if selected_option == menu_options[2]:
                update_bank_account()

            if selected_option == menu_options[3]:
                delete_bank_account()

        self.main_menu = back_account_main_menu