"""3_Advanced_analysis.py"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def advanced_analysis_page():
    """Shows analysis considering multiple variables at once."""

    if 'df' not in st.session_state:
        st.session_state.df = None
        st.session_state.analytics_ready = False   

    if not st.session_state.analytics_ready:
        st.info("Upload a valid dataset to enable the analytics section.", icon='ℹ️')
    else:

        with st.expander("Scatter plot of age vs length of credit card number"):
            # Scatter plot of age vs length of credit card number
            fig = px.scatter(data_frame=st.session_state.df, x='age', y='ccnumber_length', color='state',
                            title='Age vs length of credit card number', labels={'age': 'Age', 'ccnumber_length': 'Length of credit card number'})
            st.plotly_chart(fig)

        with st.expander("Age distribution by state"):
            fig = px.box(data_frame=st.session_state.df, x='state', y='age', title='Age distribution by state')
            st.plotly_chart(fig)

        with st.expander("Clustering algorithm"):
            from sklearn.cluster import KMeans

            # Choose numerical columns.
            numeric_data = st.session_state.df[['age', 'ccnumber_length']]

            # Add slider to select num of clusters
            num_clusters = st.slider("Select number of clusters", 2, 10, 3)

            # Use KMeans to construct clusters according to slider value.
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            st.session_state.df['cluster'] = kmeans.fit_predict(numeric_data)

            # Show scatter plot
            fig = px.scatter(data_frame=st.session_state.df, x='age', y='ccnumber_length', color='cluster',
                            title=f'Clustering of data by age and length of credit card number (k={num_clusters})', 
                            labels={'age': 'Age', 'ccnumber_length': 'Length of credit card number'})
            st.plotly_chart(fig)

        with st.expander("Heatmap correlation"):
                import seaborn as sns
                import matplotlib.pyplot as plt

                numeric_data = st.session_state.df.select_dtypes(include=['number'])
                numeric_data = numeric_data.drop(columns=['cluster'])

                corr_matrix = numeric_data.corr()

                fig, ax = plt.subplots()
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
                st.pyplot(fig)

                        

if __name__ == '__main__':
    advanced_analysis_page()