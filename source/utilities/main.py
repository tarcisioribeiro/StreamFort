import streamlit as st
from source.utilities.database_backup import Backup
from source.utilities.password_generator import PasswordGenerator


class Utilities:
    """
    Classe com métodos de utilitários utéis para a aplicação, como gerador de senhas e backup de dados.
    """

    def main_menu(self):
        """
        Menu principal.
        """
        menu_options = {
            "Backup de Dados": Backup(),
            "Gerador de Senhas": PasswordGenerator()
        }
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header(body=":desktop_computer: Utilitários")
        with col2:
            selected_option = st.selectbox(label="Menu", options=menu_options.keys())
        st.divider()
        if selected_option:
            option = menu_options[selected_option]
            option.main_menu()
