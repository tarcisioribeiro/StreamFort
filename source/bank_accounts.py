from data.session_state import logged_user
from data.user_data import logged_user_name, logged_user_document
from dictionary.sql import check_user_bank_accounts_query, search_bank_accounts_query
from dictionary.vars import financial_institution_list, to_remove_list, bank_account_field_names
from functions.query_executor import QueryExecutor
from time import sleep
import streamlit as st


class BankAccount:

    def __init__(self):

        query_executor = QueryExecutor()

        def get_new_bank_account():
            col1, col2, col3 = st.columns(3)

            with col1:
                with st.expander(label="Dados da Conta", expanded=True):
                    account_name = st.text_input(label="Nome", max_chars=100, placeholder='Conta')
                    financial_institution = st.selectbox(label='Instituição', options=financial_institution_list)
                    financial_institution_code = st.number_input(label="Código da instituição", max_value=99999, step=1)
                    agency = st.number_input(label="Agência", max_value=9999999999, step=1)
                
                confirm_data = st.checkbox(label="Confirmar dados")

            with col2:
                with st.expander(label="Dados da Conta", expanded=True):
                    account_number = st.number_input(label="Número da conta", max_value=999999999999999, step=1)
                    account_digit = st.number_input(label="Dígito", max_value=9, step=1)
                    account_password = st.text_input(label="Senha da conta", max_chars=30, type='password')
                    digital_account_password = st.text_input(label="Senha digital da conta", max_chars=30, type='password')
                    
                register_new_account = st.button(label=":floppy_disk: Cadastrar conta")

                if confirm_data == True and register_new_account:
                    
                    insert_password_query = "INSERT INTO contas_bancarias(nome_conta, instituicao_financeira, codigo_instituicao_financeira, agencia, numero_conta, digito_conta, senha_bancaria_conta, senha_digital_conta, nome_proprietario_conta, documento_proprietario_conta) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    query_values = (account_name, financial_institution, financial_institution_code, agency, account_number, account_digit, account_password, digital_account_password, logged_user_name, logged_user_document)

                    query_executor.insert_query(insert_password_query, query_values, 'Conta cadastrada com sucesso!', 'Erro ao cadastrar conta:')

                    log_query = '''INSERT INTO logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)'''
                    log_query_values = (logged_user, 'Cadastro', 'Cadastrou a conta {}'.format(query_values[0]))
                    query_executor.insert_query(query=log_query, values=log_query_values, success_message='Log gravado.', error_message='Erro ao gravar log:')

        def show_bank_accounts():
            col1, col2, col3 = st.columns(3)

            user_accounts_quantity = query_executor.simple_consult_query(check_user_bank_accounts_query)
            user_accounts_quantity = query_executor.treat_simple_result(user_accounts_quantity, to_remove_list)
            user_accounts_quantity = int(user_accounts_quantity)

            if user_accounts_quantity == 0:
                with col2:
                    st.warning(body="Você ainda não possui senhas cadastradas.")

            elif user_accounts_quantity >= 1:

                with col3:

                    cl1, cl2 = st.columns(2)

                    user_bank_accounts = ["Selecione uma opção"]

                    bank_accounts = query_executor.complex_consult_query(query=search_bank_accounts_query)
                    bank_accounts = query_executor.treat_numerous_simple_result(bank_accounts, to_remove_list)

                    for i in range(0, len(bank_accounts)):
                        user_bank_accounts.append(bank_accounts[i])

                    with col1:

                        cl1, cl2 = st.columns(2)

                        with cl1:

                            selected_option = st.selectbox(label="Selecione a conta", options=user_bank_accounts)

                            consult_button = st.button(label=":floppy_disk: Consultar senha")

                    account_details_query = '''SELECT CONCAT('', contas_bancarias.nome_conta, ' - ', contas_bancarias.instituicao_financeira), contas_bancarias.agencia, CONCAT('', contas_bancarias.numero_conta, '-', contas_bancarias.digito_conta), contas_bancarias.senha_bancaria_conta, contas_bancarias.senha_digital_conta FROM contas_bancarias WHERE contas_bancarias.nome_conta = '{}' AND contas_bancarias.nome_proprietario_conta = '{}' AND contas_bancarias.documento_proprietario_conta = '{}';'''.format(selected_option, logged_user_name, logged_user_document)

                    result_list = query_executor.complex_consult_query(query=account_details_query)
                    result_list = query_executor.treat_complex_result(values_to_treat=result_list, values_to_remove=to_remove_list)

                    if selected_option != "Selecione uma opção" and consult_button:

                        with col2:
                            with st.spinner(text="Aguarde..."):
                                sleep(1.5)

                            with st.expander(label="Dados", expanded=True):

                                aux_string = ''

                                for i in range(0, len(result_list)):
                                    if i == len(result_list) - 1:
                                        st.write(bank_account_field_names[i])
                                        st.code(body="{}".format(result_list[i]))
                                    else:
                                        st.write(bank_account_field_names[i])
                                        aux_string = str(result_list[i])
                                        aux_string = aux_string.replace('"', '')
                                        st.code(body="{}".format(aux_string))

                                log_query = '''INSERT into logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)'''
                                query_values = (logged_user, 'Consulta', 'Consultou a senha {} associada ao email {}'.format(result_list[0], result_list[2]))
                                query_executor.insert_query(query=log_query, values=query_values, success_message='Log gravado.', error_message='Erro ao gravar log:')

        def back_account_main_menu():
            col1, col2, col3 = st.columns(3)

            with col2:
                menu_options = ["Cadastrar conta", "Consultar contas"]
                selected_option = st.selectbox(label="Menu", options=menu_options)

            st.divider()

            if selected_option == menu_options[0]:
                get_new_bank_account()

            if selected_option == menu_options[1]:
                show_bank_accounts()

        self.main_menu = back_account_main_menu