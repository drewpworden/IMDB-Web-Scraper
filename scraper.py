#IMPORTS
import requests
import pandas as pd
from bs4 import BeautifulSoup

#EMPTY DATAFRAME
queried_media = pd.DataFrame(columns = ["Title", "Year of Release", "IMDB Rating", "Number of Ratings", "Parental Rating", "Runtime", "Genre(s)", "Full Release Date", "Country('s) of Release", "Director(s)", "MetaCritic Score", "Budget"])

#STRIP AND CLEANING FUNCTION
def strip():
    URL = input("IMDB LINK: ")
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    #TITLE
    title = soup.find("h1", "").get_text()
    title = title.split("\xa0")
    title = str(title[0])
    print(title)

    #YEAR OF RELEASE
    year_release = soup.find("h1", "").get_text()
    year_release = year_release.split("\xa0")
    year_release = year_release[1]
    year_release = str(year_release.replace("(", "").replace(")", ""))
    print(year_release)

    #IMDB RATING
    imdb_rating = float(soup.find(itemprop = "ratingValue").get_text())
    print(imdb_rating)
    #NUMBER OF RATINGS
    num_ratings = soup.find(itemprop = "ratingCount").get_text()
    num_ratings = int(num_ratings.replace(",", ""))
    print(num_ratings)

    #PARENTAL RATING
    dirty_parent_rating = soup.find("div", "subtext").get_text()
    dirty_parent_rating = dirty_parent_rating.split(" ")
    parent_rating_list = []

    for element in dirty_parent_rating:
        if element == "" or element == "\n":
            del element
        else:
            parent_rating_list.append(element)

    parent_rating = str(parent_rating_list[0].replace("\n", ""))
    print(parent_rating)

    #RUNTIME
    runtime = soup.find("time").get_text()
    runtime = runtime.split(" ")
    runtime_list = []
    for element in runtime:
        element = element.replace("\n", "")
        if element == "" or element == "\n":
            del element
        else:
            runtime_list.append(element)

    if len(runtime_list) == 2:
        runtime = str(runtime_list[0] + " " + runtime_list[1])
    else:
        runtime = str(runtime_list[0])
    print(runtime)

    #GENRE
    genre = soup.find("div", "subtext").get_text()
    genre = genre.split(" ")

    clean_genre = []
    for element in genre:
        element = element.replace("\n", "").replace("|", ""). replace(",", "")
        if element == '' or element == '' or element == '\n' or element == "|":
            del element
        else:
            clean_genre.append(element)
    genre = clean_genre

    list = []
    imdb_genres = ["Drama", "Adventure", "Comedy", "Romance", "Mystery", "Family", "Musical", "Animation", "Horror", "Action", "Thriller", "Crime", "Biography", "Sci-Fi", "History", "War", "Fantasy", "Western", "Documentary"]
    for element in genre:
        for item in imdb_genres:
            if item in element:
                list.append(item)

    genre = list
    print(genre)

    #FULL RELEASE DATE
    full_release_date = soup.find(title = "See more release dates").get_text()
    full_release_date = full_release_date.split()
    del full_release_date[-1]
    release = ""
    for element in full_release_date:
        if full_release_date.index(element) == len(full_release_date) - 1:
            release += element
        else:
            release += (element + " ")

    full_release_date = release
    print(full_release_date)

    #COUNTRY OF RELEASE
    div_title = soup.find("div", {"id": "titleDetails"})
    div_title_children_list = []
    for child in div_title.children:
        div_title_children_list.append(child)

    for tag in div_title_children_list:
        tag = str(tag)
        if "Country" in tag:
            dirty_country = tag

    dirty_country = dirty_country.split("\n")
    dirty_country_list = []
    for item in dirty_country:
        if "<a" in item:
            dirty_country_list.append(item)

    country = []
    for tag in dirty_country_list:
        tag = tag.split(">")
        del tag[0]
        del tag[-1]
        tag = tag[0].split("<")
        tag = tag[0]
        country.append(tag)

    print(country)




strip()
