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

# ------ set page config ----------
st.set_page_config(layout="centered")
#----------------------------------

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Le temps
# https://docs.streamlit.io/develop/api-reference/widgets/st.date_input
today = datetime.datetime.now()
st.write("Aujoud'hui nous sommes le :", today.date())

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Le placement
# https://docs.streamlit.io/develop/api-reference/layout/st.columns
left, middle = st.columns(2, vertical_alignment="bottom")

left.text_input("Entrez votre recherche :")
middle.button("valider", use_container_width=True)
# right.checkbox("Check me")
st.write('___')
# Titre principal de l'application (affiché en haut de la page)
st.title("🏠 ACTUELLEMENT EN SALLE 🌎")

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Code pour telecharger le fichier csv
df = pd.read_csv("data/data_movies_details.csv")

# On recupere les elements unique de la colonne pour les proposer en selection
sentiment_mapping = ["film pour enfant", "film pour adulte", "le casting"]

choix = st.selectbox("Veuillez faire votre sélection : ", sentiment_mapping)

# Suivant le choix de la personne, on afficher le type de film
if choix == 'film pour enfant':
    st.markdown(f"Vous avez choisi **{choix}** 🎈")
    for i in range(3):
        left, middle, right = st.columns(3, border=True)
        variable_test = "Origine : " + df.origin_country.unique()[i+7] + ". "
        "Overview : " + df.overview.unique()[i+7]
        left.image(df.poster_path.unique()[i+7], caption="poster_path")
        middle.image(df.backdrop_path.unique()[i+7], caption="backdrop_path")
        right.write(variable_test)
elif choix == 'film pour adulte':
    st.markdown(f"Vous avez choisi **{choix}** ⭐")
    for i in range(3):
        left, middle, right = st.columns(3, border=True)
        variable_test = "Origine : " + df.origin_country.unique()[i] + ". "
        "Overview : " + df.overview.unique()[i]
        left.image(df.poster_path.unique()[i], caption="poster_path")
        middle.image(df.backdrop_path.unique()[i], caption="backdrop_path")
        right.write(variable_test)
elif choix == 'le casting':
    st.markdown(f"Vous avez choisi **{choix}** 🌎")
    df = pd.read_csv("data_movies_details.csv")
    for i in range(3):
        left, middle, right = st.columns(3, border=True)
#       variable_1 = "https://image.tmdb.org/t/p/original"+(df.profile_path[i])
# Voir comment associer le debut de l'url et le profil-path
        variable_1 = "https://image.tmdb.org/t/p/original/" \
                     "ytMrG3T4SbZfZnfXFohjQBOixTQ.jpg"
        variable_2 = "Nom : " + df.name.unique()[i]
        # + "Statut : "+df.known_for_department.unique()[i]
        variable_3 = "Infos : " + df.known_for.unique()[i]
        left.image(variable_1, caption="p_path")
        middle.write(variable_2)
        right.write(variable_3)
else:
    st.write("Oui, ton choix est :", choix)

st.write('___')

st.write('Affichage du dataframe')
st.write(df)

st.write('___')


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Les feedback
# https://docs.streamlit.io/develop/api-reference/widgets/st.feedback
sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")

sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
selected = st.feedback("thumbs")
if selected is not None:
    st.markdown(f"You selected: {sentiment_mapping[selected]}")


st.write(' 🦁 ')

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


st.write('© SAPEM Conseil')
