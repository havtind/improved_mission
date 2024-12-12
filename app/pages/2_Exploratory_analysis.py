"""2_Exploratory_analysis.py"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def analysis_page():
    """This page shows exploratory analytics and provides the filter feature."""

    if 'df' not in st.session_state:
        st.session_state.df = None
        st.session_state.analytics_ready = False  # Analytics not ready initially
 
    st.sidebar.header("Filter data")

    if st.session_state.analytics_ready:
        seq_min = st.sidebar.number_input("Minimum index", min_value=int(st.session_state.df['seq'].min()), 
                                        max_value=int(st.session_state.df['seq'].max()), 
                                        value=int(st.session_state.df['seq'].min()), step=1)

        seq_max = st.sidebar.number_input("Maximum index", min_value=int(st.session_state.df['seq'].min()), 
                                        max_value=int(st.session_state.df['seq'].max()), 
                                        value=int(st.session_state.df['seq'].max()), step=1)

        # Ensure seq_min is less than or equal to seq_max
        if seq_min > seq_max:
            st.sidebar.error("Minimum index cannot be greater than maximum index!")


        # Filter by age range
        age_min, age_max = st.sidebar.slider("Select age range", 
                                            int(st.session_state.df['age'].min()), 
                                            int(st.session_state.df['age'].max()), 
                                            (int(st.session_state.df['age'].min()), int(st.session_state.df['age'].max())))

        # Filter by latitude range
        latitude_min, latitude_max = st.sidebar.slider("Select latitude range", 
                                                    float(st.session_state.df['latitude'].min()), 
                                                    float(st.session_state.df['latitude'].max()), 
                                                    (float(st.session_state.df['latitude'].min()), float(st.session_state.df['latitude'].max())))

        # Filter by longitude range
        longitude_min, longitude_max = st.sidebar.slider("Select longitude range", 
                                                    float(st.session_state.df['longitude'].min()), 
                                                    float(st.session_state.df['longitude'].max()), 
                                                    (float(st.session_state.df['longitude'].min()), float(st.session_state.df['longitude'].max())))


        # Filter by substring in the "city" column
        city_filter = st.sidebar.text_input("Enter text to search in city names:", "")

        firstname_filter = st.sidebar.text_input("Enter text to search in first names:", "")

        lastname_filter = st.sidebar.text_input("Enter text to search in last names:", "")

        street_filter = st.sidebar.text_input("Enter text to search in street names:", "")

        cclength_min, cclength_max = st.sidebar.slider("Select length of credit card number", 
                                            int(st.session_state.df['ccnumber_length'].min()), 
                                            int(st.session_state.df['ccnumber_length'].max()), 
                                            (int(st.session_state.df['ccnumber_length'].min()), int(st.session_state.df['ccnumber_length'].max())))

        # Filter by state  
        unique_states = st.session_state.df['state'].unique()
        selected_states = st.sidebar.multiselect("Select states", unique_states, default=unique_states)

        # Apply filters to the data
        filtered_data = st.session_state.df[
            (st.session_state.df['seq'] >= seq_min) & 
            (st.session_state.df['seq'] <= seq_max) & 
            (st.session_state.df['age'] >= age_min) & 
            (st.session_state.df['age'] <= age_max) & 
            (st.session_state.df['state'].isin(selected_states)) & 
            (st.session_state.df['latitude'] >= latitude_min) & 
            (st.session_state.df['latitude'] <= latitude_max) &
            (st.session_state.df['longitude'] >= longitude_min) & 
            (st.session_state.df['longitude'] <= longitude_max) &
            (st.session_state.df['city'].str.contains(city_filter, case=False, na=False)) &
            (st.session_state.df['name/first'].str.contains(firstname_filter, case=False, na=False)) &
            (st.session_state.df['name/last'].str.contains(lastname_filter, case=False, na=False)) &
            (st.session_state.df['street'].str.contains(street_filter, case=False, na=False)) &
            (st.session_state.df['ccnumber_length'] >= cclength_min) & 
            (st.session_state.df['ccnumber_length'] <= cclength_max) 
        ] 

 
    # _-------------------------------

    
    st.subheader("Filtered data")

    if st.session_state.analytics_ready:

        st.write(f"Showing {len(filtered_data):,} rows out of {len(st.session_state.df):,}")
        columns_to_exclude = ['ccnumber_length']  # List of columns to hide
        st.dataframe(filtered_data.drop(columns=columns_to_exclude, axis=1))

        st.subheader("Visualizations for filtered data")

        with st.expander("Numerical data"):

            st.subheader("Age distribution")

            age_counts = filtered_data['age'].value_counts().sort_index()

            # Create the plot
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            sns.barplot(x=age_counts.index, y=age_counts.values, ax=ax2)

            # Reduce the number of x-tick labels to avoid overcrowding
            ticks_to_show = range(0, len(age_counts), 2)   
            ax2.set_xticks(ticks_to_show)
            ax2.set_xticklabels(age_counts.index[ticks_to_show], rotation=45)

            # Set labels and title
            ax2.set_xlabel("Age")
            ax2.set_ylabel("Count")
            ax2.set_title("Age distribution")

            # Display the plot
            st.pyplot(fig2)


        with st.expander("Categorical data"):
    
            # antall unike stater
            unique_states = filtered_data['state'].nunique()
            st.write(f"Number of unique states: {unique_states}")

            # stolpediagram med statene
            state_counts = filtered_data['state'].value_counts()
            st.subheader("State distribution")
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=state_counts.index, y=state_counts.values, ax=ax)
            ax.set_xlabel("State")
            ax.set_ylabel("Count")
            ax.set_title("State distribution")
            plt.xticks(rotation=90)  
            st.pyplot(fig)


            st.subheader("Credit card number length distribution")

            #  (Antar at ccnumber er kredittkort. )
            cc_length_counts = filtered_data['ccnumber_length'].value_counts()
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(
                cc_length_counts,
                labels=cc_length_counts.index,
                autopct='%1.1f%%',
                startangle=90,
                colors=sns.color_palette('pastel')[:len(cc_length_counts)]
            )

            ax.set_title("Distribution of lengths of credit card numbers")

            st.pyplot(fig)


        with st.expander("Textual data"):
    
            st.write(f"**Unique first names**: {filtered_data['name/first'].nunique():,}")
            st.write(f"**Unique last names**: {filtered_data['name/last'].nunique():,}")
            st.write(f"**Unique cities**: {filtered_data['city'].nunique():,}")
            st.write(f"**Unique streets**: {filtered_data['street'].nunique():,}")


            # Sett sammen hele navnet
            full_names = filtered_data['name/first'] + " " + filtered_data['name/last']
            # Rregn ut antall unike navn
            unique_persons_count = full_names.nunique()
            st.write(f"**Number of unique persons**: {unique_persons_count:,}")
            name_combination_counts = full_names.value_counts()

            repeated_combinations = name_combination_counts[name_combination_counts > 1]


            if not repeated_combinations.empty:
                st.write("### Repeated name combinations:")
                st.dataframe(repeated_combinations)
            else:
                st.write("No repeated first and last name combinations found.")


        # -------------------------------------
        # FOLIUM 

        import folium
        from folium.plugins import (
            FastMarkerCluster,
            TagFilterButton,
            MarkerCluster,
            MiniMap
        )
        import streamlit.components.v1 as components

        def create_map_advanced(df):
            """Creates a detailed map, which can be slow with more than 10k markers."""

            m = folium.Map(tiles=None)	
            folium.TileLayer('cartodbpositron', name='Greymap').add_to(m)
            folium.TileLayer('openstreetmap', name='Colormap').add_to(m)

            marker_cluster = MarkerCluster(
                name='1000 clustered icons',
                overlay=True,
                control=False,
                icon_create_function=None
            )

            for i, row in df.iterrows():
                tooltext = (
                    f"Seq: {row['seq']}<br>"
                    f"Name: {row['name/first']+' '+row['name/last']}<br>"
                    f"Age: {row['age']}"
                )
                location=(row['latitude'], row['longitude'])
                marker = folium.Marker(
                    location=location,
                    icon=folium.Icon(
                        icon="user",   
                        prefix="fa",  
                        color="blue"  
                    ),
                    tooltip=tooltext   
                ) 
                marker_cluster.add_child(marker)  

            marker_cluster.add_to(m)

            folium.LayerControl(collapsed=False).add_to(m)
            TagFilterButton(['Filter by values'], filter_on_every_click=True, clear_text='').add_to(m)
            MiniMap(toggle_display=True, zoom_level_offset=-8).add_to(m)

            return m._repr_html_()
             
        def create_map(df):
            """Creates a simple and fast map."""
            # Initialize the map
            m = folium.Map()	

            # Add markers to map
            marker_data = df[['latitude', 'longitude']].values.tolist()
            m.add_child(FastMarkerCluster(marker_data))
         
            MiniMap(toggle_display=True, zoom_level_offset=-8).add_to(m)
            return m._repr_html_()
        
        with st.expander("Geospatial data"):

            st.subheader("Latitude and longitude distribution")
            # Latitude histogram
            st.write("### Latitude distribution")
            fig_lat, ax_lat = plt.subplots()
            sns.histplot(filtered_data['latitude'], bins=20, kde=False, ax=ax_lat, color="skyblue")
            ax_lat.set_title("Latitude histogram")
            ax_lat.set_xlabel("Latitude")
            ax_lat.set_ylabel("Frequency")
            st.pyplot(fig_lat)

            # Longitude histogram
            st.write("### Longitude distribution")
            fig_lon, ax_lon = plt.subplots()
            sns.histplot(filtered_data['longitude'], bins=20, kde=False, ax=ax_lon, color="orange")
            ax_lon.set_title("Longitude histogram")
            ax_lon.set_xlabel("Longitude")
            ax_lon.set_ylabel("Frequency")
            st.pyplot(fig_lon)


            st.subheader("Scatter plot: latitude vs longitude")
            fig, ax = plt.subplots()
            ax.scatter(
                filtered_data['longitude'], 
                filtered_data['latitude'], 
                color='blue',   
                alpha=0.7,      
                s=0.1          
            )

            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            ax.set_title("Geospatial distribution")

            st.pyplot(fig)

        # Open interactive folium map
        if st.button("Show interactive map", type="primary"):
            st.markdown(
                """
                This feature requires internet connection.  
                Details about each entry are only shown if the filtered data contains less than 10,000 entries.  
                Generation time is typically within 10 seconds and should not exceed 1 minute.
                """
            )
            
            if len(filtered_data) < 10000:
                folium_map_html = create_map_advanced(filtered_data)
            else:
                folium_map_html = create_map(filtered_data)
            components.html(folium_map_html, height=500)
        
        # END FOLIUM
        # -------------------------------------
        
    else:
        st.info("Upload a valid dataset to enable the analytics section.", icon='ℹ️')

        
 


if __name__ == '__main__':
    analysis_page()