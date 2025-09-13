import pandas as pd
import streamlit as st


#st.write("Hello World")
# Titre principal de l'application (affiché en haut de la page)
st.title("Pick up a film")

# Titre de section important (taille 1)
#st.header("An Important Header")

# Sous-titre (taille 2), utile pour organiser le contenu par sous-sections
#st.subheader("A Secondary Header")

# Affiche une ligne de texte simple (sans mise en forme particulière)
#st.text("My classic hello")

# Affiche du texte avec mise en forme Markdown
#st.markdown(''':rainbow: :rainbow[My markdown]''')  # Ici, un effet arc-en-ciel est appliqué

# Affiche un dataframe (st.write accepte plusieurs arguments et plusieurs types de données)
df_movies = pd.read_csv("projet_2/data/films_final.csv")
st.write(df_movies
    
    )

from streamlit_searchbox import st_searchbox

#search_term = st.text_input("Search for a movie title:")

# Case-insensitive search
#if search_term:
#   results = df_movies[df_movies["title"].str.contains(search_term, case=False, na=False)]
#    if not results.empty:
#        st.write("### Search Results", results)
#    else:
#        st.warning("No matching titles found.")
#''''def search_wikipedia(searchterm: str) -> list:
#    # search wikipedia for the searchterm
#    return movies['title'].search(searchterm) if searchterm else []'''

def search_film(searchterm):

    # search for the searchterm
    #if searchterm:
    results = df_movies[df_movies["title"].str.contains(searchterm, case=False, na=False)]
    return results["title"].tolist()

# pass search function and other options as needed

selected_value = st_searchbox(
    search_film,
    placeholder="Search Film... ",
    #key="my_key",
)
film_id = df_movies[df_movies["title"].str.contains( "Le plaisir" if not isinstance(selected_value, str) else selected_value
    
)]
img4 = film_id['poster_path'].iloc[0]
img4title = film_id['title'].iloc[0]
st.write(f"Selected value: {selected_value}")



from streamlit_carousel import carousel

test_items = [
    dict(
        title="Slide 1",
        text="A tree in the savannah",
        img="https://img.freepik.com/free-photo/wide-angle-shot-single-tree-growing-clouded-sky-during-sunset-surrounded-by-grass_181624-22807.jpg?w=1380&t=st=1688825493~exp=1688826093~hmac=cb486d2646b48acbd5a49a32b02bda8330ad7f8a0d53880ce2da471a45ad08a4",
        link="https://discuss.streamlit.io/t/new-component-react-bootstrap-carousel/46819",
    ),
    dict(
        title="Slide 2",
        text="A wooden bridge in a forest in Autumn",
        img="https://img.freepik.com/free-photo/beautiful-wooden-pathway-going-breathtaking-colorful-trees-forest_181624-5840.jpg?w=1380&t=st=1688825780~exp=1688826380~hmac=dbaa75d8743e501f20f0e820fa77f9e377ec5d558d06635bd3f1f08443bdb2c1",
        link="https://github.com/thomasbs17/streamlit-contributions/tree/master/bootstrap_carousel",
    ),
    dict(
        title="Slide 3",
        text="A distant mountain chain preceded by a sea",
        img="https://img.freepik.com/free-photo/aerial-beautiful-shot-seashore-with-hills-background-sunset_181624-24143.jpg?w=1380&t=st=1688825798~exp=1688826398~hmac=f623f88d5ece83600dac7e6af29a0230d06619f7305745db387481a4bb5874a0",
        link="https://github.com/thomasbs17/streamlit-contributions/tree/master",
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
        img="cat.jpg",
    ),
]

carousel(items=test_items, container_height=800)


#Carousel doc https://pypi.org/project/st-ant-carousel/
import streamlit as st
from st_ant_carousel import st_ant_carousel

# Define the content with images
content = [
    {
        "style": {"textAlign": "center"},
        "content": f'<img src="{img4}" width="100" height="200">'"<b>2. Entry</b>"
    },
    {
        "style": {"textAlign": "center"},
        "content": '<img src="https://via.placeholder.com/300x200.png?text=Slide+2" width="300" height="200">'
    },
    {
        "style": {"textAlign": "center"},
        "content": """
            <div style="padding: 10px;">
                <img src="https://via.placeholder.com/300x200.png?text=Slide+2" width="300" height="200">
                <h2 style="color: #2E86AB;">🎬 Featured Movie</h2>
                <p>Explore the world of imagination through our spotlight feature.</p>
            </div>
        """
    },
    {
        "style": {"textAlign": "center"},
        "content": f'''
            <div>
                <a href="https://www.imdb.com/title/tt1375666/" target="_blank">
                    <img src="{img4}" width="100" height="200">
                </a>
                <h3>Inception</h3>
                <p>Open IMDb page in new tab</p>
            </div>
        '''
    }
]

# Define carousel styling
carousel_style = {
    "width": "110px",        # set desired width
    "height": "210px",       # optional height
    "margin": "0 auto",      # center the carousel
    "background-color": "#f0f2f5",
    "border": "2px solid #ccc",
    "border-radius": "8px",
    "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
    "padding": "5px"
}

# Display the carousel
st_ant_carousel(
    content,
    carousel_style=carousel_style,
    autoplay=True,
    autoplaySpeed=2000,
    dotPosition="bottom",
    dots=True,
    waitForAnimate=True,
    easing="ease-in-out",
    effect="scrollx",
    pauseOnDotsHover=True,
    pauseOnHover=True,
    animationSpeed=500,
    vertical=False,
    adaptiveHeight=True
)



if st.button("nm0000003"):
    st.session_state.selected_intervenant = "nm0000003"
    st.switch_page("pages\intervenant.py")
if st.button("nm0000079"):
    st.session_state.selected_intervenant = "nm0000079"
    st.switch_page("pages\intervenant.py")