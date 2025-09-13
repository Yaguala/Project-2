# Nos packages
import streamlit as st
import pandas as pd
import datetime
# from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler  # , MinMaxScaler
from sklearn.neighbors import NearestNeighbors
# Search box need to pip install streamlit_searchbox
# Makes a search box for title de filme
from streamlit_searchbox import st_searchbox
from streamlit_carousel import carousel

# Le temps
# https://docs.streamlit.io/develop/api-reference/widgets/st.date_input
today = datetime.datetime.now()
st.write("Aujoud'hui nous sommes le :", today)

# New page
# Titre principal de l'application (affiché en haut de la page)
st.title("ADULTES")

# Load data frame and show if needed:
df_movies = pd.read_csv("data/films_final.csv")
# st.write(df_movies)
dummies = df_movies.genres.str.get_dummies(sep=',').drop(columns="Comedy")
genres = dummies.columns.to_list()
df_movies = pd.concat([df_movies, dummies], axis=1)

cols = ['budget', 'revenue', 'popularity', 'startYear', 'runtimeMinutes',
        'averageRating', 'numVotes'] + genres


# Function sugestion de filme:
def recherche(tconst, cols):

    # colonne ml

    # Defenir les X_class en colluns
    X_class = df_movies[cols]

    # Indiquer le filme au model
    X_test_c = df_movies.loc[df_movies["tconst"] == tconst, cols]

    # Standardiser toutes ces features
    scaler_knn = StandardScaler()
    X_knn_scaled = scaler_knn.fit_transform(X_class)

    # Nombre de voisins à trouver k et indiquer le numero de recumendations
    k = 5
    nn_model = NearestNeighbors(n_neighbors=k).fit(X_knn_scaled)

    # Standardiser toutes ces features
    X_test_c_scaled_knn = scaler_knn.transform(X_test_c)

    # Sélectionner les 3 premiers points de X_test_c (qui sont non
    # standardisés)
    sample_points_scaled = X_test_c_scaled_knn[:3, :]

    # .kneighbors() prend les points standardisés et retourne distances et
    # indices
    distances, indices = nn_model.kneighbors(sample_points_scaled)

    # Find the index
    indicies = indices[0].tolist()

    return df_movies.iloc[indicies]


# Funtion to search the title of filme in the dataframe:
def search_film(searchterm):
    # Search for the searchterm
    results = df_movies[df_movies["title"].str.contains(searchterm, case=False,
                                                        na=False)]
    return results["title"].tolist()


# Search function from streamlit_searchbox and disgn of the box search
selected_value = st_searchbox(
    search_film,
    placeholder="Search Film... ",
    # Text in the search box if nothing inside
    # key="my_key", #No parametre info
)

# If nothing in search box "selected_value' the return of carrousel is
# controled here:
film_id = df_movies[df_movies["title"].str.contains(
    "Le plaisir" if not isinstance(selected_value, str) else selected_value)]

# Acess the links of poster films
df_sugest = recherche(film_id["tconst"].iloc[0], cols)
for i, k in enumerate(df_sugest['poster_path']):
    if i == 0:
        img1 = k
    elif i == 1:
        img2 = k
    elif i == 2:
        img3 = k
    elif i == 3:
        img4 = k
    elif i == 4:
        img5 = k

img4title = film_id['title'].iloc[0]

# Show the value input on the searchbox
st.write(f"Selected value: {selected_value}")

# Carrousel image need to pip install streamlit-carousel:
# More info :
# https://github.com/thomasbs17/streamlit-contributions/tree/master/bootstrap_carousel


test_items = [
    dict(
        title="Slide 1",
        text="A tree in the savannah",
        img=img1,
        link="https://discuss.streamlit.io/t/"
        "new-component-react-bootstrap-carousel/46819",
    ),
    dict(
        title="Slide 2",
        text="A wooden bridge in a forest in Autumn",
        img=img2,
        link="https://github.com/thomasbs17/streamlit-contributions/"
        "tree/master/bootstrap_carousel",
    ),
    dict(
        title="Slide 3",
        text="A distant mountain chain preceded by a sea",
        img=img3,
        link="https://github.com/thomasbs17/streamlit-contributions/"
        "tree/master",
    ),
    dict(
        text="Slide 4",
        title=img4title,
        img=img4,
        link=img4
    ),
    dict(
        title="Slide 5",
        text="CAT",
        img=img5,
    ),
]
# Carrousel parameters:
carousel(items=test_items, container_height=810)
