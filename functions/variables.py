import streamlit as st


class Variables:
    """
    Classe com métodos para análise de variáveis.
    """

    def create_variable(self, name, value):
        """
        Cria uma nova variável.

        Parameters
        ----------
        name
            O nome da variável a ser criada.
        value
            O valor da variável que está sendo criada.
        """
        globals()[name] = value

    def debug_variable(self, variable):
        """
        Realiza a análise de uma variável.

        Parameters
        ----------
        variable
            A variável a ser analisada.
        """
        variable_type = type(variable).__name__

        st.info(body="Tipo: {}.".format(variable_type))
        st.info(body="Conteúdo: {}.".format(variable))

        if (
            variable_type != "int"
            and variable_type != "float"
            and variable_type != "complex"
            and variable_type != "UploadedFile"
        ):
            st.info(body="Tamanho: {}.".format(len(variable)))
