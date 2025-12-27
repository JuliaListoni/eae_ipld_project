# The libraries you have to use
import pandas as pd
import matplotlib.pyplot as plt

# Some extra libraries to build the webapp
import streamlit as st


# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write("Interactive Project to load a dataset with information about Netflix Movies and Series, extract some insights usign Pandas and displaying them with Matplotlib.")
    st.write("Data extracted from: https://www.kaggle.com/datasets/shivamb/netflix-shows (with some cleaning and modifications)")


# ----- Title of the page -----
st.title("🎬 Netflix Data Analysis")
st.divider()


# ----- Loading the dataset -----

@st.cache_data
def load_data():
    data_path = "data/netflix_titles.csv"

    movies_df = pd.read_csv(data_path, index_col="show_id")
    return movies_df   # a Pandas DataFrame


movies_df = load_data()

# Displaying the dataset in a expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(movies_df)


# ----- Extracting some basic information from the dataset -----

# TODO: Ex 2.2: What is the min and max release years?
min_year = movies_df["release_year"].min()
max_year = movies_df["release_year"].max()

print(f"Min year: {min_year}, Max year: {max_year}")

# TODO: Ex 2.3: How many director names are missing values (NaN)?
num_missing_directors = movies_df["director"].isna().sum()

print(f"Number of missing directors: {num_missing_directors}")

# TODO: Ex 2.4: How many different countries are there in the data?
movies_countries = movies_df["country"].fillna("Unknown")

countries_str = ", ".join(movies_countries)

countries_list = countries_str.split(",")

clean_countries_list = [country.strip() for country in countries_list]

unique_countries = set(clean_countries_list)

n_countries = len(unique_countries)

print("Number of unique countries: ", n_countries)

# TODO: Ex 2.5: How many characters long are on average the title names?
movies_df["title_length"] = movies_df["title"].apply(lambda x: len(x))

avg_title_length = movies_df["title_length"].mean()

print(f"The average title length is {avg_title_length} characters")


# ----- Displaying the extracted information metrics -----

st.write("##")
st.header("Basic Information")

cols1 = st.columns(5)
cols1[0].metric("Min Release Year", min_year)
cols1[1].metric("Max Release Year", max_year)
cols1[2].metric("Missing Dir. Names", num_missing_directors)
cols1[3].metric("Countries", n_countries)
cols1[4].metric("Avg Title Length", str(round(avg_title_length, 2)) if avg_title_length is not None else None)


# ----- Pie Chart: Top year producer countries -----

st.write("##")
st.header("Top Year Producer Countries")

cols2 = st.columns(2)
year = cols2[0].number_input("Select a year:", min_year, max_year, 2005)

# TODO: Ex 2.6: For a given year, get the Pandas Series of how many movies and series 
# combined were made by every country, limit it to the top 10 countries.
top_10_countries = None

# print(top_10_countries)
if top_10_countries is not None:
    fig = plt.figure(figsize=(8, 8))
    plt.pie(top_10_countries, labels=top_10_countries.index, autopct="%.2f%%")
    plt.title(f"Top 10 Countries in {year}")

    st.pyplot(fig)

else:
    st.subheader("⚠️ You still need to develop the Ex 2.6.")


# ----- Line Chart: Avg duration of movies by year -----

st.write("##")
st.header("Avg Duration of Movies by Year")

# TODO: Ex 2.7: Make a line chart of the average duration of movies (not TV shows) in minutes for every year across all the years. 
movie_filter = movies_df.loc[movies_df["type"] == "Movie"]

movie_filter["duration_minutes"] = movie_filter["duration"].apply(
    lambda x: int(x.replace(" min", ""))
)

movies_avg_duration_per_year = (movie_filter.groupby("release_year")["duration_minutes"].mean())

# TODO: generate the line plot using plt.plot() and the information from movies_avg_duration_per_year (the vertical axis with the minutes value) and its index (the horizontal axis with the years)

plt.plot(
    movies_avg_duration_per_year.index,
    movies_avg_duration_per_year.values
)

plt.xlabel("Year")
plt.ylabel("Average Duration in Minutes")
plt.title("Average Duration of Movies Across Years")

plt.show()