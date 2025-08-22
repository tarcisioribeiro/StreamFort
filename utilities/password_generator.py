import streamlit as st
import string
from random import choice
from time import sleep


class PasswordGenerator:
    """
    Classe com métodos para a geração de senhas fortes.
    """

    def generate_password(
        self,
        password_length: int,
        password_elements: list
    ) -> str:
        """
        Gera uma senha de acordo com o tamanho da cadeia de caracteres
        e complexidade definidas pelo usuário.

        Parameters
        ----------
        password_length : int
            O comprimento da senha, definido pelo usuário.
        password_elements : list
            Os elementos que irão compor a senha, como números,
            letras maiúsculas e minúsculas e caracteres especiais.

        Returns
        -------
        formatted_password : str
            A senha gerada de acordo com a seleção do usuário.
        """

        formatted_password = ""

        lower_case_alphabet = string.ascii_lowercase
        lower_case_alphabet_list = []
        for i in range(0, len(lower_case_alphabet)):
            lower_case_alphabet_list.append(lower_case_alphabet[i])

        upper_case_alphabet = string.ascii_uppercase
        upper_case_alphabet_list = []
        for i in range(0, len(upper_case_alphabet)):
            upper_case_alphabet_list.append(upper_case_alphabet[i])

        numbers_list = []
        for i in range(0, 10):
            numbers_list.append(str(i))

        special_characters_group = string.punctuation
        special_characters_group_list = []
        for i in range(0, len(special_characters_group)):
            special_characters_group_list.append(special_characters_group[i])

        for i in range(0, password_length):
            random_element = ""
            random_choice = choice(password_elements)
            if random_choice == "lower_cases":
                random_element = choice(lower_case_alphabet_list)
            elif random_choice == "upper_cases":
                random_element = choice(upper_case_alphabet_list)
            elif random_choice == "numbers":
                random_element = choice(numbers_list)
            elif random_choice == "special_characters":
                random_element = choice(special_characters_group_list)
            formatted_password += random_element

        return formatted_password

    def main_menu(self):
        """
        Menu principal.
        """

        password_length_options = []

        for i in range(8, 21):
            password_length_options.append(i)

        password_elements = {
            "Letras maiúsculas": "upper_cases",
            "Letras minúsculas": "lower_cases",
            "Números": "numbers",
            "Caracteres especiais": "special_characters",
        }

        col1, col2 = st.columns(2)

        with col1:
            with st.expander(label="Opções", expanded=True):
                selected_password_length = st.select_slider(
                    label="Comprimento da senha",
                    options=password_length_options,
                    help="Comprimento da senha em caracteres.",
                )
                password_elements_selection = st.multiselect(
                    label="Opções",
                    options=password_elements.keys(),
                    help="""
                    Elementos opcionais para a senha.
                    Caso nenhum seja selecionado,
                    serão incluídas letras minúsculas.
                    """,
                    placeholder="Selecione uma opção",
                )
                confirm_options = st.checkbox(label="Confirmar opções")
            generate_password_button = st.button(label=":key: Gerar senha")

        with col2:
            data_validation_expander = st.expander(
                label="Validação dos dados", expanded=True
            )

            if confirm_options and generate_password_button:
                with st.spinner(text="Aguarde..."):
                    sleep(1.25)

                password_selected_elements = []
                for i in range(0, len(password_elements_selection)):
                    password_selected_elements.append(
                        password_elements[password_elements_selection[i]]
                    )

                generated_password = self.generate_password(
                    password_length=selected_password_length,
                    password_elements=password_selected_elements,
                )

                with data_validation_expander:
                    st.write("Senha gerada:")
                    st.code(generated_password)
