# the libraries you have to use
import pandas as pd
import matplotlib.pyplot as plt

# Some extra libraries for date conversions and build the webapp
import streamlit as st


# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write(
        "Interactive Project to load a dataset with information about the daily "
        "temperatures of 10 cities around the world, extract some insights using "
        "Pandas and displaying them with Matplotlib."
    )
    st.write(
        "Data extracted from: https://www.kaggle.com/datasets/sudalairajkumar/"
        "daily-temperature-of-major-cities (with some cleaning and modifications)."
    )


# ----- Title of the page -----
st.title("🌦️ Temperatures Dashboard")
st.divider()


# ----- Loading the dataset -----
@st.cache_data
def load_data():
    data_path = "data/cities_temperatures.csv"
    temps_df = pd.read_csv(data_path)
    temps_df["Date"] = pd.to_datetime(temps_df["Date"])
    return temps_df


temps_df = load_data()

# Displaying the dataset in an expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(temps_df)


# ----- Data transformation -----
# Ex 3.2: Create AvgTemperatureCelsius
temps_df["AvgTemperatureCelsius"] = (
    temps_df["AvgTemperatureFahrenheit"] - 32
) * 5 / 9


# ----- Extracting some basic information -----

# Ex 3.3: Unique cities
unique_cities_list = temps_df["City"].unique().tolist()

# Ex 3.4: Min and max dates
min_date = temps_df["Date"].min()
max_date = temps_df["Date"].max()

# Ex 3.5: Global min/max temperatures
min_temp = temps_df["AvgTemperatureCelsius"].min()
min_idx = temps_df["AvgTemperatureCelsius"].idxmin()
min_temp_city = temps_df.loc[min_idx, "City"]
min_temp_date = temps_df.loc[min_idx, "Date"]

max_temp = temps_df["AvgTemperatureCelsius"].max()
max_idx = temps_df["AvgTemperatureCelsius"].idxmax()
max_temp_city = temps_df.loc[max_idx, "City"]
max_temp_date = temps_df.loc[max_idx, "Date"]


# ----- Displaying the extracted information metrics -----
st.write("##")
st.header("Basic Information")

cols1 = st.columns([4, 1, 6])

# Cities list
cols1[0].dataframe(
    pd.Series(unique_cities_list, name="Cities"),
    width="content"
)

# Min / Max temperature info
cols1[2].write("#")

cols1[2].markdown(
    f"""
    ### ☃️ Min Temperature: {min_temp:.1f}°C  
    *{min_temp_city} on {min_temp_date.date()}*
    """
)

cols1[2].write("#")

cols1[2].markdown(
    f"""
    ### 🏜️ Max Temperature: {max_temp:.1f}°C  
    *{max_temp_city} on {max_temp_date.date()}*
    """
)


# ----- Plotting the temperatures over time for the selected cities -----
st.write("##")
st.header("Comparing the Temperatures of the Cities")

selected_cities = st.multiselect(
    "Select the cities to compare:",
    unique_cities_list,
    default=["Buenos Aires", "Dakar"],
    max_selections=4,
)

cols2 = st.columns([6, 1, 6])

start_date = cols2[0].date_input(
    "Select the start date:",
    pd.to_datetime("2009-01-01").date()
)

end_date = cols2[2].date_input(
    "Select the end date:",
    pd.to_datetime("2018-12-31").date()
)


if len(selected_cities) > 0:
    c = st.container(border=True)

    fig, ax = plt.subplots(figsize=(15, 5))

    for city in selected_cities:
        city_df = temps_df[temps_df["City"] == city]
        city_df_period = city_df[
            (city_df["Date"].dt.date >= start_date)
            & (city_df["Date"].dt.date <= end_date)
        ]

        ax.plot(
            city_df_period["Date"],
            city_df_period["AvgTemperatureCelsius"],
            label=city
        )

    ax.set_title(
        f"Temperature for selected cities ({start_date} to {end_date})"
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Average Temperature in Celsius")
    ax.legend()

    c.pyplot(fig)