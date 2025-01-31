import streamlit as st
from functions.check_password_health import PasswordValidator
from functions.variables import Variables
from time import sleep


class PasswordGenerator:
    """
    Classe com métodos para a geração de senhas fortes.
    """

    def generate_password(self, password_length: int, password_elements: list):
        """
        Gera uma senha de acordo com o tamanho da cadeia de caracteres e complexidade definidas pelo usuário.
        """
        ...

    def main_menu(self):
        """
        Menu principal.
        """

        password_length_options = []

        for i in range(8, 21):
            password_length_options.append(i)

        password_elements_options = ["Letras maiúsculas", "Letras minúsculas", "Números", "Caracteres especiais"]

        col1, col2 = st.columns(2)

        with col1:
            with st.expander(label="Opções", expanded=True):
                password_length = st.select_slider(label="Comprimento da senha", options=password_length_options, help="Comprimento da senha em caracteres.")
                password_elements = st.multiselect(label="Opções", options=password_elements_options, help="Elementos opcionais para a senha. Caso nenhum seja selecionado, serão incluídas letras minúsculas.", placeholder="Selecione uma opção")
                confirm_options = st.checkbox(label="Confirmar opções")
            generate_password_button = st.button(label=":key: Gerar senha")

        with col2:
            data_validation_expander = st.expander(label="Validação dos dados", expanded=True)

            if confirm_options and generate_password_button:
                with st.spinner(text="Aguarde..."):
                    sleep(2.5)
                with data_validation_expander:
                    Variables().debug_variable(password_elements)
                    st.info(password_length)
