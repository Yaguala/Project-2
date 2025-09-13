import pandas as pd
import streamlit as st
# from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler  # , MinMaxScaler
from sklearn.neighbors import NearestNeighbors
# Search box need to pip install streamlit_searchbox
# Makes a search box for title de filme
from streamlit_searchbox import st_searchbox
from streamlit_carousel import carousel

# ------ set page config ----------
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
# Remove side bar navigation------
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# Bar naviagation ----------------------------------
from streamlit_option_menu import option_menu

with st.container():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Suggestion", "Enfants", "Contacts"],
        icons=[],  # No icons
        default_index=1,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#05335F",
                "class": "navbar-fixed",  # Add fixed class
            },
            "nav-link": {
                "color": "white",
                "font-size": "16px",
                "margin": "0px",
                "padding": "10px",
            },
            "nav-link-selected": {
                "background-color": "#1B4F72"
            },
        }
    )
if selected == "Home":
    st.switch_page("index.py")
if selected == "Suggestion":
    selected = 'Suggestion'
if selected == "Contacts":
    st.switch_page("pages/Contacts.py")
if selected == "Enfants":
    st.switch_page("pages/Enfants.py")

# --------------------------- Main page sugestion -----------------------------
right, mid, left = st.columns([2,4.3,2])

with mid:
    if st.button("Revenir sur le diferent Suggestion", use_container_width=True):
        st.switch_page("pages/Sugestion.py")


#-----------------------------------------------------------------------------


# Titre de la page
st.header("Film Préféré", divider="green")
st.write('Choisissez votre film préféré dans le genre comédie française.')
st.write('Notre système analysera votre sélection pour vous recommander automatiquement des films similaires.')

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
    placeholder="Recherchez votre film préféré... ",
    # Text in the search box if nothing inside
    # key="my_key", #No parametre info
)

# If nothing in search box "selected_value' the return of carrousel is
# controled here:
if isinstance(selected_value, str) and selected_value.strip() != "":
    film_id = df_movies[df_movies["title"].str.contains(selected_value, case=False, na=False)]


    if not film_id.empty:
        # Acess the links of poster films
        df_sugest = recherche(film_id["tconst"].iloc[0], cols)
        backdrop = df_sugest.backdrop_path.tolist()
        img1, img2, img3, img4, img5 = backdrop[:6]
        titles = df_sugest['title'].str.upper().tolist()
        title1, title2, title3, title4, title5 = titles[:6]


        img4title = film_id['title'].iloc[0]

        # Show the value input on the searchbox



        #Funtion link
        #def chosenlink(linkid):
        #    st.session_state.selected_intervenant = linkid


        #Carousel doc https://pypi.org/project/st-ant-carousel/
        import streamlit as st
        from st_ant_carousel import st_ant_carousel

        # Define the content with images
        content = [
            {
                "style": {"textAlign": "center", "color": "white", "fontSize": "50px"},
                "content": f'<b2>{title2}</b2><img src="{img2}" width="700" height="500">'
            },
            {
                "style": {"textAlign": "center", "color": "white", "fontSize": "50px"},
                "content": f'<b2>{title3}</b2><img src="{img3}" width="700" height="500">'
            },
            {
                "style": {"textAlign": "center", "color": "white", "fontSize": "50px"},
                "content": f'<b2>{title4}</b2><img src="{img4}" width="700" height="500" style="cursor: pointer;">'
            },
            {
                "style": {"textAlign": "center", "color": "white", "fontSize": "50px"},
                "content": f'<b2>{title5}</b2><img src="{img5}" width="700" height="500" style="cursor: pointer;">'
            }
        ]

        # Define carousel styling
        carousel_style = {
            "width": "100%",
            "height": "500px",
            "background-color": "#12980300",
        }

        # Display the carousel
        selected_index = st_ant_carousel(
            content,
            carousel_style=carousel_style,
            autoplay=True,
            autoplaySpeed=3000,
            dotPosition="bottom",
            dots=True,
            waitForAnimate=True,
            easing="ease-in-out",
            effect="scrollx",
            pauseOnDotsHover=True,
            pauseOnHover=True,
            animationSpeed=5000,
            vertical=False,
            adaptiveHeight=True, 
            height=500,
            key=df_sugest['tconst'].iloc[0]
        )

        # ------------ botton with acces to thew films info -----------

        import textwrap
        st.header("Sugestion de Films", divider="green")
        colist = ["col1", "col2", "col3", 'col4']
        colist = st.columns(4)
        for col, i in enumerate(df_sugest.index[1:]):
            with colist[col % 4]:
            #st.write(df_sugest.primaryName[i])
                st.image(df_sugest.poster_path[i], width=260)
                if st.button(textwrap.shorten(df_sugest.title[i], width=19,  placeholder="…"), use_container_width=True,  key=f"btn_{i}"):
                    st.session_state.selected_film = df_sugest.tconst[i]
                    st.switch_page("pages/film.py")

        # --------------------------------------------------------------

        #--------------------------- Film choissi ------------------------------

        left, mid = st.columns([0.5,0.7])
        mid.header("Vous avez choisi :", divider='green')
        mid.title(df_sugest.title.iloc[0])
        mid.subheader(f"Rating: {df_sugest.averageRating.iloc[0]} :star:")
        mid.subheader(f"Sortie: {df_sugest.startYear.iloc[0]}")
        left.image(df_sugest.poster_path.iloc[0], width=300)
        mid.header(" ", divider="green")
        if mid.button(textwrap.shorten(df_sugest.title.iloc[0], width=19,  placeholder="…"), use_container_width=True):
            st.session_state.selected_film = df_sugest.tconst.iloc[0]
            st.switch_page("pages/film.py")

        # ----------------------------------------------------------------------

# --------------------------- bas de page -----------------
st.markdown('<div class="footer">© 2025 SAPEM CONSEIL. All rights reserved.</div>', unsafe_allow_html=True)
st.markdown("""
    <style>
    .footer {
        margin-top: 50px;
        text-align: center;
        font-size: 14px;
        color: #A0A0A0;
    }
    </style>
""", unsafe_allow_html=True)
# -----------------------------------------------------------------