import streamlit as st

st.set_page_config(
    page_title="StreamFort - Gerenciador de Senhas",
    page_icon=":closed_lock_with_key:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def main():
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    if st.session_state.is_logged_in:
        pass
    else:
        pass


if __name__ == "__main__":
    main()
