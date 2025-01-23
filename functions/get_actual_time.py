import datetime
import streamlit as st


class GetActualTime:
    """
    Classe com métodos para obtenção e exibição da data e hora atual.
    """

    def get_actual_time(self):
        """
        Obtém a hora atual.

        Returns
        -------
        hour (str): A hora atual.
        """
        now = datetime.datetime.now()
        hour = now.strftime("%H:%M:%S")
        return hour

    def show_current_time(self):
        """
        Exibe a hora atual.
        """
        actual_hour = self.get_actual_time()
        st.info(body="Hora atual: {}".format(actual_hour))

    def get_actual_data(self):
        """
        Obtém a data atual.

        Returns
        -------
        data (str): A data atual.
        """
        now = datetime.datetime.now()
        data = now.strftime("%Y-%m-%d")
        return data
