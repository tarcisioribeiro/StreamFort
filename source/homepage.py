from dictionary.sql import user_passwords_query, check_user_passwords_quantity_query
from dictionary.vars import to_remove_list
from functions.check_password_health import PasswordValidator
from functions.query_executor import QueryExecutor
import streamlit as st


class Home:

    def __init__(self):

        query_executor = QueryExecutor()
        check_password = PasswordValidator()

        def general_information():
            user_passwords_quantity = query_executor.simple_consult_query(check_user_passwords_quantity_query)
            user_passwords_quantity = query_executor.treat_simple_result(user_passwords_quantity, to_remove_list)

            return user_passwords_quantity

        def password_analysis():
                
            user_passwords = query_executor.complex_consult_query(user_passwords_query)
            user_passwords = query_executor.treat_numerous_simple_result(user_passwords, to_remove_list)

            empty_password = ''
            password_strength = ''

            very_low = 0
            low = 0
            medium = 0
            strong = 0
            very_strong = 0


            for i in range(0, len(user_passwords)):

                empty_password = user_passwords[i]
                password_strength = check_password.check_password_strength(empty_password)

                if password_strength == "Muito Fraca":
                    very_low += 1
                elif password_strength == "Fraca":
                    low += 1
                elif password_strength == "Média":
                    medium += 1
                elif password_strength == "Forte":
                    strong += 1
                elif password_strength == "Muito Forte":
                    very_strong += 1
                
            return very_low, low, medium, strong, very_strong

        def show_home_page():

            col1, col2, col3 = st.columns(3)

            with col1:
                st.header(body=":closed_lock_with_key: Streamfort")

            st.divider()

            col4, col5, col6 = st.columns(3)

            with col5:

                user_passwords_quantity = general_information()
                get_very_low, get_low, get_medium, get_strong, get_very_strong = password_analysis()

                with st.expander(label="Análise de Senhas", expanded=True):
                    st.info(body="Senhas cadastradas: {}".format(user_passwords_quantity))
                    st.divider()
                    st.error(body="Senhas muito fracas: {}.".format(get_very_low))
                    st.warning(body="Senhas fracas: {}.".format(get_low))
                    st.info(body="Senhas médias: {}.".format(get_medium))
                    st.info(body="Senhas fortes: {}.".format(get_strong))
                    st.success(body="Senhas muito fortes: {}.".format(get_very_strong))

        self.main_menu = show_home_page
