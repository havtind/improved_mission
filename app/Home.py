"""Home.py"""
import streamlit as st



def run_streamlit_app():
    """Entry point for the app"""
      
    if 'theme_dark' not in st.session_state:
        st.session_state.theme_dark = True   

    if st.sidebar.toggle("Dark mode", value=st.session_state.theme_dark, key=st.session_state.theme_dark):
        st._config.set_option('theme.base', "dark")
        st.session_state.theme_dark = True
    else:
        st._config.set_option('theme.base', "light")
        st.session_state.theme_dark = False

    st.title('Home')

    st.write("This is a data visualization tool intented for the 'special project' ")

    st.write("The features include:")
    st.markdown("""
    - Uploading a data set.
    - Displaying the data set.
    - Filter, search and sort the content of the data.
    - Interactive map with the data values.
    - Analytics/statistics on the data.
    """)


if __name__ == "__main__":
    run_streamlit_app()




