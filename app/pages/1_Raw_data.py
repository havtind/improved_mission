"""1_Raw_data.py"""
import streamlit as st
import pandas as pd



def data_page():
    """ Used for loading the data set. """

    # Cache the data, so that it loads faster if rerun 
    @st.cache_data
    def load_data(file):
        """ Load a CSV file into a DataFrame. """
        return pd.read_csv(file)
 
    # Initialize session state variables
    if 'df' not in st.session_state:
        st.session_state.df = None
        st.session_state.analytics_ready = False  # Analytics not ready initially
 
    # File uploader 
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    column_names = ['latitude', 'longitude']
    if uploaded_file is not None:
        try:
            data = load_data(uploaded_file)
            st.session_state.df = data
            print(data.columns)
            # Check if all required columns are present
            missing_columns = [col for col in column_names if col not in data.columns]
            
            if missing_columns:
                st.warning(f"Missing columns: {', '.join(missing_columns)}. Data cannot be used for analytics.", icon='⚠️')
                st.session_state.analytics_ready = False  # Invalidate analytics readiness
            else:
                st.session_state.analytics_ready = True  # Mark analytics ready for uploaded data
                st.session_state.df['ccnumber_length'] = st.session_state.df['ccnumber'].astype(str).str.len()

        except Exception as e:
            st.error(f"Failed to load uploaded dataset: {e}")
            st.session_state.analytics_ready = False  # Invalidate analytics readiness on error


 
    st.title("Dataset visualization")

    if st.session_state.analytics_ready:
        st.subheader("Raw data")
        columns_to_exclude = ['ccnumber_length']  
        st.dataframe(st.session_state.df.drop(columns=columns_to_exclude, axis=1))

        st.subheader("Basic statistics") # Simple statistics on the numerical columns.
        st.write(st.session_state.df.drop(columns=['seq','ccnumber'], axis=1).describe())

        
        missing_values = st.session_state.df.isnull().sum() # Check for missing values.
        st.write("### Missing values per column")
        st.dataframe(missing_values.to_frame(name="Missing count"))
    else:
        st.info("Upload a valid dataset to enable the analytics section.", icon='ℹ️')


if __name__ == '__main__':
    data_page()