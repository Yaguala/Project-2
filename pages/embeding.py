import numpy as np
import pandas as pd
import streamlit as st
from stqdm import stqdm


#FastEmbed is a lightweight, fast, Python library built for embedding generation.
# https://github.com/qdrant/fastembed
# from fastembed import TextEmbedding

# Cosine_similarity -- Compute cosine similarity between samples in X and Y.
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer


# ------------------- set page config ----------
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
# ---------------Remove side bar navigation------
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)
#---------------------------------------------------------------

# --------------------------- Bar naviagation ----------------------------------
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




# ----------------------------------------------------

# --------------------------- Main page sugestion -----------------------------
right, mid, left = st.columns([2,4.3,2])

with mid:
    if st.button("Revenir aux différentes suggestions", use_container_width=True):
        st.switch_page("pages/Sugestion.py")

#-------------------------- Load csv films -----------------------------
df_films = pd.read_csv('data/films_final.csv')




#-------------------------- Page title ----------------------------
st.header("Décrivez le film que vous souhaitez.", divider="green")
st.write('Vous avez une idée précise en tête ? ')
st.write('Décrivez le type de film que vous avez envie de voir par exemple : "un thriller psychologique dans un univers futuriste avec une héroïne forte", et notre modèle intelligent analysera votre description pour trouver les films les plus proches de vos envies.')

# Add sujestions.
# Add a row to the data frame.
def addsugestion(sugestion_title, sugenstion_genres, sugestion_words, sugestion_overview):
    sugestion_user = {'backdrop_path': 'Nothing', 'budget': 'Nothing', 'id' : 'Nothing', 'origin_country' : 'Nothing', 'overview' : sugestion_overview,
        'popularity': 'Nothing', 'poster_path' : 'Nothing', 'revenue' : 'Nothing', 'mots_cles': sugestion_words, 'title' : sugestion_title, 'tconst' :  'Nothing',
        'startYear' : 'Nothing', 'runtimeMinutes' : 'Nothing', 'genres' : sugenstion_genres, 'averageRating' : 'Nothing', 'numVotes' : 'Nothing',
        'bande_annonce' : 'Nothing'}
    df_films_sgestion = pd.concat([df_films, pd.DataFrame([sugestion_user])], ignore_index=True)
    return df_films_sgestion


# ---------------Aplication of sugestion and user input--------------------------

sugestion_title = "user_sugestion"
# sugenstion_genres = st.text_input(f"Sugenstion_genres : ")
sugenstion_genres = " "
# sugestion_words = st.text_input(f'sugestion_words :')
sugestion_words = " "
sugestion_overview = st.text_input(f"Description:")


# --------------------- Start search ----------------------------
# ---- intervenants ------
def get_intervenants(tconst):
    matched_names = df_intervenant.loc[
        df_intervenant["knownForTitles"].str.contains(tconst, na=False), "primaryName"
    ]
    return ", ".join(matched_names.tolist())
#--------

right, mid, left = st.columns(3)
if mid.button("Analyser ma description"):
    df_films = addsugestion(sugestion_title, sugenstion_genres, sugestion_words, sugestion_overview)
    st.session_state.df_films = df_films
    # st.write(df_films.title.tail(5))
    df_intervenant = pd.read_csv("data/intervenantes_final.csv")

    df_films["intervenants"] = df_films["tconst"].apply(get_intervenants)
    #Treating data
    df_films['all_text'] = (
        "Genres : " + df_films['genres'] + ".\n"
        "Genres : " + df_films['genres'] + ".\n"
        "Mots_cles : " + df_films['mots_cles'] + ".\n"
        "Title : " + df_films['title'] + ".\n"
        "Overview : " + df_films['overview'] 
        
        )

    #Make a list of treated data
    st.session_state.documents = df_films['all_text'].to_list()

    df_films.tail(1)


# Funtion for model
# For sorme reason tqdm mmust be near the funtion to work...


    st.info(" À la recherche des meilleurs films faits pour vous!...")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    documents = st.session_state.documents
    total = len(documents)

    # Create progress bar
    progress_bar = st.progress(0)
    embeddings = []

    for i, doc in enumerate(documents):
        # Encode one document at a time
        embedding = model.encode([doc])[0]
        embeddings.append(embedding)

        # Update progress bar
        progress = int((i + 1) / total * 100)
        progress_bar.progress(progress)

    # Save to session state
    st.session_state.embeddings = np.array(embeddings)

    progress_bar.empty()
    st.success("Voilà une suggestion rien que pour vous !")


    if "embeddings" in st.session_state:
        distances = cosine_similarity(st.session_state.embeddings)
        df_distances = pd.DataFrame(distances)
        st.session_state.distances = df_distances
        # st.success("Distances computed.")
    else:
        st.warning("Ups something went wrong pls refresh the page.")


#Find the recomendations
# Funtion to find the films returnning a url of the poster
def get_info_reco(title_input, max_reco = 8) :
    data = st.session_state.df_films
    distance_reco = st.session_state.distances
    
    # avoir la ligne contenant ma recette
    info_input = data[data.title== title_input]
    # récupérer l'index de l'input
    indice_input_index = info_input.index[0]
    #  recupérer la ligne de recommandation dans la matrice de distance
    scores = distance_reco.iloc[ indice_input_index ]

    #  trier de la valeur la plus haute à la plus basse
    scores  = scores.sort_values(ascending = False)


    # récuperer les indices de reco
    best_scores_index = scores.index.to_list()[1:max_reco+ 1]


    # récupérer les images des plats recmmandé

    #st.write(f" pour le place {title_input}")
    #st.write(info_input.poster_path.values[0])
    #indices_reco = np.argsort(scores)[::-1][1:]

    # st.write(f' les recommandations : ')
    reco = data.iloc[best_scores_index]
    # st.write(reco.poster_path.values)
    return reco


# Test 
title = "user_sugestion"
if "distances" in st.session_state:
    st.session_state.df_sugest = get_info_reco(title)

# ---------------------------- Show results --------------------------
if "df_sugest" in st.session_state:
    df_sugest = st.session_state.df_sugest
    # Acess the links of poster films
    backdrop = df_sugest.backdrop_path.tolist()
    img1, img2, img3, img4, img5, im6, img7, img8 = backdrop[:9]
    titles = df_sugest['title'].str.upper().tolist()
    title1, title2, title3, title4, title5, title6, title7, title8 = titles[:9]


    # img4title = film_id['title'].iloc[0]

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
            "content": f'<b2>{title1}</b2><img src="{img1}" width="700" height="500">'
        },
        {
            "style": {"textAlign": "center", "color": "white", "fontSize": "50px"},
            "content": f'<b2>{title2}</b2><img src="{img2}" width="700" height="500">'
        },
        {
            "style": {"textAlign": "center", "color": "white", "fontSize": "50px"},
            "content": f'<b2>{title3}</b2><img src="{img3}" width="700" height="500" style="cursor: pointer;">'
        },
        {
            "style": {"textAlign": "center", "color": "white", "fontSize": "50px"},
            "content": f'<b2>{title4}</b2><img src="{img4}" width="700" height="500" style="cursor: pointer;">'
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

    import textwrap
    st.header("Sugestion de Films", divider="green")
    colist = ["col1", "col2", "col3", 'col4']
    colist = st.columns(4)
    for col, i in enumerate(df_sugest.index[:8]):
        with colist[col % 4]:
        #st.write(df_sugest.primaryName[i])
            st.image(df_sugest.poster_path[i], width=260)
            if st.button(textwrap.shorten(df_sugest.title[i], width=19,  placeholder="…"), use_container_width=True,  key=f"btn_{i}"):
                st.session_state.selected_film = df_sugest.tconst[i]
                st.session_state.page_embeding = True
                st.switch_page("pages/film.py")




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
