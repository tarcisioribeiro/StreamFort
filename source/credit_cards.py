from data.session_state import logged_user, logged_user_password
from dictionary.sql import name_doc_query, search_user_credit_cards_number, search_user_credit_cards_names
from dictionary.vars import to_remove_list
from functions.get_actual_time import GetActualTime
from functions.query_executor import QueryExecutor
from functions.validate_document import Documents
from time import sleep
import streamlit as st


class CreditCards:

    def __init__(self):

        call_actual_time = GetActualTime()
        query_executor = QueryExecutor()
        validate_document = Documents()

        def show_credit_cards():
            
            user_credit_cards_number = query_executor.simple_consult_query(search_user_credit_cards_number)
            user_credit_cards_number = query_executor.treat_simple_result(user_credit_cards_number, to_remove_list)
            user_credit_cards_number = int(user_credit_cards_number)

            st.divider()

            if user_credit_cards_number > 0:

                col1, col2, col3 = st.columns(3)

                credit_cards_options = ["Selecione uma opção"]

                user_credit_cards_names = query_executor.complex_consult_query(search_user_credit_cards_names)
                user_credit_cards_names = query_executor.treat_numerous_simple_result(user_credit_cards_names, to_remove_list)

                for i in range(0, len(user_credit_cards_names)):
                    credit_cards_options.append(user_credit_cards_names[i])

                with col3:

                    cl1, cl2 = st.columns(2)

                    with cl2:

                        selected_user_card = st.selectbox(label="Selecione o cartão", options=credit_cards_options)

                        if selected_user_card != "Selecione uma opção":

                            card_field_names = ["Nome do cartão", "Número do cartão", "Nome do titular no cartão", "Data da validade", "Código de segurança"]
                        
                            credit_card_data_query = '''
                            SELECT 
                                cartao_credito.nome_cartao,
                                cartao_credito.numero_cartao,
                                cartao_credito.nome_titular,
                                DATE_FORMAT(cartao_credito.data_validade, '%d/%m/%Y'),
                                cartao_credito.codigo_seguranca
                            FROM
                                cartao_credito
                                    INNER JOIN
                                usuarios ON cartao_credito.proprietario_cartao = usuarios.nome
                                    AND cartao_credito.documento_titular = usuarios.documento_usuario
                            WHERE
                                usuarios.login = '{}'
                                    AND usuarios.senha = '{}'
                                    AND cartao_credito.nome_cartao = '{}';'''.format(logged_user, logged_user_password, selected_user_card)
                            
                            credit_card_data = query_executor.complex_compund_query(credit_card_data_query, 5, 'credit_card_')
                            credit_card_data = query_executor.treat_numerous_simple_result(credit_card_data, to_remove_list)

                            with col2:

                                with st.spinner(text="Aguarde..."):
                                    sleep(2.5)

                                with st.expander(label="Dados do cartão", expanded=True):
                                    for i in range(0, len(credit_card_data)):
                                        st.write(card_field_names[i])
                                        st.code(credit_card_data[i])

                                    last_card_numbers = str(credit_card_data[1])[-4:]
                                    log_query = '''INSERT INTO logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES(%s, %s, %s)'''
                                    log_values = (logged_user, "Consulta", "Consultou os dados do cartão {} com o final {}.".format(credit_card_data[0], last_card_numbers))

                                    query_executor.insert_query(log_query, log_values, "Log gravado.", "Erro ao gravar log:")

            else:

                st.divider()

                col1, col2, col3 = st.columns(3)

                with col2:
                    st.warning(body="Você ainda não possui cartões cadastrados.")

        def get_new_credit_card():

            st.divider()

            def validate_card_values(card_name: str, owner_on_card_name: str, expiration_date: str, actual_date: str, security_code: str):

                if card_name == '':
                    st.error("Informe o nome do cartão.")
                if owner_on_card_name == '':
                    st.error("Informe o nome do titular no cartão.")
                if expiration_date <= actual_date:
                    st.error(body="A data de validade do cartão deve ser maior que a data atual.")
                if security_code == '':
                    st.error(body="Informe o código de segurança do cartão.")

            col1, col2 = st.columns(2)

            with col1:

                with st.expander(label="Dados do Cartão", expanded=True):

                    card_name = st.text_input(label="Nome do cartão", max_chars=100)
                    card_number = st.text_input(label="Número do cartão", max_chars=16)
                    last_card_numbers = card_number[-4:]
                    owner_on_card_name = st.text_input(
                        label="Nome do titular no cartão", max_chars=100
                    )
                    expiration_date = st.date_input(label="Data de validade")
                    expiration_date = str(expiration_date)
                    security_code = st.text_input(
                        label="Código de segurança", max_chars=3
                    )
                    confirm_data = st.checkbox(label="Confirmar dados", value=False)

                    actual_date = call_actual_time.get_actual_data()

                register_button = st.button(label=":floppy_disk: Cadastrar cartão")

                if register_button and confirm_data == True:

                    with st.spinner(text="Aguarde..."):
                        sleep(1)

                    with col2:
                        valid_card = validate_document.validate_credit_card(card_number)

                        if valid_card == False:
                            st.error(body="O número do cartão é inválido.")
                            validate_card_values(card_name, owner_on_card_name, expiration_date, actual_date, security_code)

                        elif valid_card == True:
                            st.success(body="Número de cartão válido.")

                            if expiration_date > actual_date and owner_on_card_name != '' and card_name != '' and security_code != '':

                                user_data = query_executor.simple_consult_query(name_doc_query)
                                user_data = query_executor.treat_numerous_simple_result(user_data, to_remove_list)

                                card_owner_name, card_owner_document = user_data

                                card_insert_query = """INSERT INTO seguranca.cartao_credito (nome_cartao, numero_cartao, nome_titular, proprietario_cartao, documento_titular, data_validade, codigo_seguranca, ativo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
                                card_insert_values = (
                                    card_name,
                                    card_number,
                                    owner_on_card_name,
                                    card_owner_name,
                                    card_owner_document,
                                    expiration_date,
                                    security_code,
                                    "S",
                                )
                                query_executor.insert_query(
                                    query=card_insert_query,
                                    values=card_insert_values,
                                    success_message="Cartão cadastrado com sucesso!",
                                    error_message="Erro ao cadastrar cartão:",
                                )

                                log_query = '''INSERT INTO seguranca.logs_atividades (usuario_log, tipo_log, conteudo_log) VALUES (%s, %s, %s);'''
                                log_values = (logged_user, 'Cadastro', 'Cadastrou o cartão {} com o final {}.'.format(card_name, last_card_numbers))

                                query_executor.insert_query(log_query, log_values, "Log gravado.", "Erro ao gravar log:")


                            else:
                                validate_card_values(card_name, owner_on_card_name, expiration_date, actual_date, security_code)
                elif register_button and confirm_data == False:

                    with st.spinner(text="Aguarde..."):
                        sleep(1)

                    with col2:
                        st.warning(body="Confirme os dados do cartão para prosseguir.")

        def credit_card_main_menu():

            col1, col2, col3 = st.columns(3)

            with col2:
                menu_options = ["Cadastrar cartão", "Consultar cartões"]
                selected_option = st.selectbox(label="Menu", options=menu_options)

            if selected_option == menu_options[0]:
                get_new_credit_card()

            if selected_option == menu_options[1]:
                show_credit_cards()

        self.main_menu = credit_card_main_menu