import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Fixed file locations
file_location_1 = 'C:\\Users\\Administrator\\Desktop\\ML\\location of connectivity.csv'
file_location_2 = 'C:\\Users\\Administrator\\Desktop\\ML\\location of request.csv'
file_location_3 = 'C:\\Users\\Administrator\\Desktop\\ML\\location of transaction.csv'

def load_data(file_path, file_name):
    data = pd.read_csv(file_path)
    data['File'] = file_name  # Add 'File' column
    return data

def auto_select_lat_lon_columns(data):
    lat_column = next((col for col in data.columns if 'lat' in col.lower()), None)
    lon_column = next((col for col in data.columns if 'lon' in col.lower()), None)
    return lat_column, lon_column

def display_map(data, lat_column, lon_column, title):
    map_center = [data[lat_column].mean(), data[lon_column].mean()]
    my_map = folium.Map(location=map_center, zoom_start=10, tiles="OpenStreetMap")

    for index, row in data.iterrows():
        color = 'green' if 'most recent connectivity' in row['File'].lower() else ('red' if 'request for sim swap' in row['File'].lower() else 'blue')
        folium.Marker([row[lat_column], row[lon_column]],
                      popup=f"Name: {row['Name']}, File: {row['File']}",
                      icon=folium.Icon(color=color)).add_to(my_map)

    st.write(f"### {title}")
    folium_static(my_map)

def authenticate(username, password):
    # Hardcoded credentials for demonstration purposes
    valid_username = "demo_user"
    valid_password = "demo_pass"

    return username == valid_username and password == valid_password

def home_page():
    st.markdown("<h1 style='color:green;'>Detection System - SIM Swap</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:orange;'>Welcome to the Home Page.</h1>", unsafe_allow_html=True)
    st.write("Navigate to different sections using the sidebar.")

def maps_page(data_1, data_2, data_3, lat_column_1, lon_column_1, lat_column_2, lon_column_2, lat_column_3, lon_column_3):
    st.markdown("<h1 style='color:orange;'>Maps Section.</h1>", unsafe_allow_html=True)

    subpage_selection = st.radio("Select Subpage", ["The Location of most recent connectivity",
                                                    "The Location of Request for SIM Swap",
                                                    "Location of Latest Transaction"])

    if subpage_selection == "The Location of most recent connectivity":
        display_map(data_1, lat_column_1, lon_column_1, "Map - The Location of most recent connectivity")
    elif subpage_selection == "The Location of Request for SIM Swap":
        display_map(data_2, lat_column_2, lon_column_2, "Map - The Location of Request for SIM Swap")
    elif subpage_selection == "Location of Latest Transaction":
        display_map(data_3, lat_column_3, lon_column_3, "Map - Location of Latest Transaction")

def search_page(data_1, data_2, data_3, lat_column_1, lon_column_1, lat_column_2, lon_column_2, lat_column_3, lon_column_3):
    st.title("Search Section")

    # Search Section
    st.header("Search Section")
    search_name = st.text_input("Enter Name for Search:", max_chars=50)

    search_button_key = "search_button_key"  # Unique key for the search button

    if st.button("Search", key=search_button_key):
        if not isinstance(search_name, str) or not search_name.strip():
            st.error("Please enter a valid string for the search.")
        elif '|' in search_name:
            st.error("The vertical bar '|' is not allowed in the search input.")
        else:
            # Search data based on the provided name
            search_result_1 = data_1[data_1['Name'].str.contains(search_name, case=False)]
            search_result_2 = data_2[data_2['Name'].str.contains(search_name, case=False)]
            search_result_3 = data_3[data_3['Name'].str.contains(search_name, case=False)]

            # Combine search results into a single DataFrame
            combined_search_data = pd.concat([search_result_1, search_result_2, search_result_3])

            # Check if search results are empty
            if combined_search_data.empty:
                st.warning(f"No matching records found for '{search_name}'.")

            else:
                # Display search results on the same map
                st.write("### Search Results Map")

                # Convert latitude and longitude columns to numeric for search results
                combined_search_data['Latitude'] = pd.to_numeric(combined_search_data['Latitude'], errors='coerce')
                combined_search_data['Longitude'] = pd.to_numeric(combined_search_data['Longitude'], errors='coerce')

                # Drop rows with missing values in latitude or longitude for search results
                combined_search_data = combined_search_data.dropna(subset=['Latitude', 'Longitude'])

                # Create a folium map for search results
                display_map(combined_search_data, 'Latitude', 'Longitude', "Map - Search Results")


def main():
    st.set_page_config(page_title="SIM Swap Detection.", page_icon=":earth_americas:")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("<h1 style='color:green;'>Detection System - SIM Swap.</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='color:orange;'>Sign In.</h1>", unsafe_allow_html=True)

        # Sidebar for authentication
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")

        sign_in_button_key = "sign_in_button_key"  # Unique key for the sign-in button

        if st.button("Sign In", key=sign_in_button_key):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.success("Authentication successful! You can now access the system.")

            else:
                st.error("Authentication failed. Please check your username and password.")
    else:
        # Load data from the first CSV file
        data_1 = load_data(file_location_1, "The Location of most recent connectivity")

        # Load data from the second CSV file
        data_2 = load_data(file_location_2, "The Location of Request for SIM Swap")

        # Load data from the third CSV file
        data_3 = load_data(file_location_3, "Location of Latest Transaction")

        # Automatically select latitude and longitude columns
        lat_column_1, lon_column_1 = auto_select_lat_lon_columns(data_1)
        lat_column_2, lon_column_2 = auto_select_lat_lon_columns(data_2)
        lat_column_3, lon_column_3 = auto_select_lat_lon_columns(data_3)

        # Show the main content of the app after successful authentication
        st.sidebar.title("Navigation")
        home_button_key = "home_button_key"  # Unique key for the home button
        maps_button_key = "maps_button_key"  # Unique key for the maps button
        search_button_key = "search_button_key"  # Unique key for the search button

        selected_page = st.sidebar.radio("Select Page", ["Home", "Maps", "Search"])

        if selected_page == "Home":
            home_page()
        elif selected_page == "Maps":
            maps_page(data_1, data_2, data_3, lat_column_1, lon_column_1, lat_column_2, lon_column_2, lat_column_3, lon_column_3)
        elif selected_page == "Search":
            search_page(data_1, data_2, data_3, lat_column_1, lon_column_1, lat_column_2, lon_column_2, lat_column_3, lon_column_3)

if __name__ == "__main__":
    main()
