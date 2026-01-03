# the libraries you have to use
import pandas as pd
import matplotlib.pyplot as plt

# Some extra libraries for date conversions and build the webapp
import streamlit as st


# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write("Interactive Project to load a dataset with information about the daily temperatures of 10 cities around the world, extract some insights usign Pandas and displaying them with Matplotlib.")
    st.write("Data extracted from: https://www.kaggle.com/datasets/sudalairajkumar/daily-temperature-of-major-cities (with some cleaning and modifications).")


# ----- Title of the page -----
st.title("🌦️ Temperatures Dashboard")
st.divider()


# ----- Loading the dataset -----

@st.cache_data
def load_data():
    data_path = "data/cities_temperatures.csv"

    temps_df = pd.read_csv(data_path)  # TODO: Ex 3.1: Load the dataset using Pandas, use the data_path variable and set the index column to "show_id"

    if temps_df is not None:
        temps_df["Date"] = pd.to_datetime(temps_df["Date"]).dt.date

    return temps_df  # a Pandas DataFrame


temps_df = load_data()

# Displaying the dataset in a expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(temps_df)


# ----- Data transformation -----

# TODO: Ex 3.2: Create a new column called `AvgTemperatureCelsius` that contains the temperature in Celsius degrees.
temps_df["AvgTemperatureCelsius"] = ((temps_df["AvgTemperatureFahrenheit"] - 32) * 5 / 9).round(1)     # uncomment this line to complete it


# ----- Extracting some basic information from the dataset -----

# TODO: Ex 3.3: How many different cities are there? Provide a list of them.
unique_countries_list = unique_countries_list = temps_df["City"].unique().tolist()

# TODO: Ex 3.4: Which are the minimum and maximum dates?
min_date = temps_df["Date"].min()
max_date = temps_df["Date"].max()

# TODO:  Ex 3.5: What are the global minimum and maximum temperatures? Find the city and the date of each of them.
temps_df["Date"] = pd.to_datetime(temps_df["Date"])

idx_min = temps_df["AvgTemperatureFahrenheit"].idxmin()
idx_max = temps_df["AvgTemperatureFahrenheit"].idxmax()

min_temp = min_temp = temps_df.loc[idx_min, "AvgTemperatureCelsius"]
max_temp = max_temp = temps_df.loc[idx_max, "AvgTemperatureCelsius"]

min_temp_city = min_temp_city = temps_df.loc[idx_min, "City"]
min_temp_date = min_temp_date = temps_df.loc[idx_min, "Date"]

max_temp_city = max_temp_city = temps_df.loc[idx_max, "City"]
max_temp_date = temps_df.loc[idx_max, "Date"]


# ----- Displaying the extracted information metrics -----

st.write("##")
st.header("Basic Information")

cols1 = st.columns([4, 1, 6])
if unique_countries_list is not None:
    cols1[0].dataframe(pd.Series(unique_countries_list, name="Cities"), width="content")
else:
    cols1[0].write("⚠️ You still need to develop the Ex 3.3.")

if min_date is not None and max_date is not None:

    cols1[2].write("#")

    min_temp_text = f"""
    ### ☃️ Min Temperature: {min_temp:.1f}°C
    *{min_temp_city} on {min_temp_date}*
    """
    cols1[2].write(min_temp_text)

    cols1[2].write("#")

    max_temp_text = f"""
    ### 🏜️ Max Temperature: {max_temp:.1f}°C
    *{max_temp_city} on {max_temp_date}*
    """
    cols1[2].write(max_temp_text)

else:
    cols1[2].write("⚠️ You still need to develop the Ex 3.5.")


# ----- Plotting the temperatures over time for the selected cities -----

st.write("##")
st.header("Comparing the Temperatures of the Cities")

if unique_countries_list is not None:
    # Getting the list of cities to compare from the user
    selected_cities = st.multiselect("Select the cities to compare:", unique_countries_list, default=["Buenos Aires", "Dakar"], max_selections=4)

    cols2 = st.columns([6, 1, 6])

    start_date = cols2[0].date_input("Select the start date:", pd.to_datetime("2009-01-01").date())     # Getting the start date from the user
    end_date = cols2[2].date_input("Select the end date:", pd.to_datetime("2018-12-31").date())         # Getting the end date from the user

else:
    st.subheader("⚠️ You still need to develop the Ex 3.3.")


if unique_countries_list is not None and len(selected_cities) > 0:

    c = st.container(border=True)

    # TODO: Ex 3.7: Plot the temperatures over time for the selected cities for the selected time period,
    # every city has to be its own line with a different color.

    fig = plt.figure(figsize=(10, 5))

    for city in selected_cities:
        # TODO: get a dataframe with the rows of the selected city
        city_df = temps_df[temps_df["City"] == city] #I added copy to avoid having pandas warnings in my output
    
        # TODO: get a dataframe with the rows of the selected city and the selected period of time using the Date column and any of the <, >, <=, >= operators to compare with start_date and end_date
        city_df["Date"] = pd.to_datetime(city_df["Date"])
        city_df_period = city_df[(city_df["Date"].dt.date >= start_date) & (city_df["Date"].dt.date <= end_date)]

        # TODO: Uncomment and complete the following lines to plot the line plot using the city_df_period AvgTemperatureCelsius column as the y axis and the Date column as the x axis
        city_df_period = city_df_period.sort_values("Date")

        # TODO plot each city line and use the label parameter to set the legend name for each city
        plt.plot(city_df_period["Date"], city_df_period["AvgTemperatureCelsius"], label=city)
           
    plt.title(f"Temperature comparison overtime from {start_date} to {end_date})")
    plt.xlabel("Time")
    plt.ylabel("Temperature (Celsius)")

    plt.legend()
    
    c.pyplot(fig)



# TODO: Make a histogram of the temperature reads of a list of selected cities, for the selected time period, 
# every city has to be its own distribution with a different color.

    fig = plt.figure(figsize=(10, 5))

    for city in selected_cities:
        # TODO: get a dataframe with the rows of the selected city
        city_df = temps_df[temps_df["City"] == city]
    
        # TODO: get a dataframe with the rows of the selected city and the selected period of time using the Date column and any of the <, >, <=, >= operators to compare with start_date and end_date
        city_df_period = city_df[(city_df["Date"].dt.date >= start_date) & (city_df["Date"] .dt.date <= end_date)]
    
        # TODO: plot each city histogram in the same plot and use the label parameter to set the legend name for each city 
        plt.hist(city_df_period["AvgTemperatureCelsius"],alpha=0.5, bins=20, label=city, edgecolor='black')                  

    plt.title(f"Temperature Comparison overtime from {start_date} to {end_date}")
    plt.xlabel("Temperature (Celsius)")
    plt.ylabel("Days")


    plt.legend()

    c.pyplot(fig)









