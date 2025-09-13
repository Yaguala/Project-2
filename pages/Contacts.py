# Nos packages
import streamlit as st
from datetime import datetime
import pandas as pd
from streamlit_option_menu import option_menu

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

with st.container():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Suggestion", "Enfants", "Contacts"],
        icons=[],  # No icons
        default_index=3,
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
    st.switch_page("pages/Sugestion.py")
if selected == "Contacts":
    selected = "Contacts"
if selected == "Enfants":
    st.switch_page("pages/Enfants.py")




#----------------------------------------------------

# la page de contact de notre application streamlit
#--------------------mettre le logo
left_co, cent_co, last_co = st.columns([0.2,0.4,0.7])
with cent_co:
    # le chemin de l'image de notre logo 
    logo = "assets/sapem_logo_final.png"
    st.image(logo, width=150) # paramètre du logo
#-------En-tête avec bouton à droite et Titre principal de l'application (affiché en haut de la page)
# --------------------2eme  column avec descriptive de group-------------------
with last_co:
    st.write("""

    ### 👥 Notre Équipe Projet

      
    - 📊 **Pedro** — *Product Owner*
    - 🧭 **Lylle Audrey** — *Scrum Master*
    - 👨‍💻 **Samuel** — *Développeur*          
    - 👨‍💼 **Samir** — *Data Analyst*
    - 👩‍💻 **Marie Claude** — *Data Analyst*
            
    """)
# --------------------------------------

st.markdown('<div class="subtitle">SAPEM CONSEIL - Experts en stratégie et données</div>', unsafe_allow_html=True)
st.header(" ", divider="green")

#-------------------------------------------------------------------------------------------
# --- Initialisation de l'état ---
if "popup_active" not in st.session_state:
    st.session_state["popup_active"] = False

# Initialiser les champs lors que l'utilisateur vient écrire le message
if "nom" not in st.session_state:
    st.session_state.nom = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "message" not in st.session_state:
    st.session_state.message = ""
# -----------En-tête-----------------------------
centrleft, center ,centerright= st.columns([0.2, 0.6, 0.2])
center.title("Contactez-nous") # le titre de notre formulaire
# ----------------------------------------------
center.write("""
Vous avez une question, une suggestion ou un bug à signaler ?  
N'hésitez pas à nous contacter !""")


# nous avons créer les colonnes pour mettre le bouton à droite car nous n'utilisaons pas html dans streamlit
#----------------- Pop up menssage ------------------
@st.dialog("Contactez-nous")
def show_contact_form():
    # -----------------------------style CSS du popup
    st.markdown(
        """
        <style>
        .popup-style {
            background-color: #f0f2f6;
            border-radius: 1rem;
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
            margin-top: 0px;
        }
        </style>
        """,
        unsafe_allow_html=True  
    )
    #--------------------------------------------
 
 
    # --- Affichage du formulaire popup si bouton cliqué ---
    # centrons avec les colonnes 
    st.markdown('<div class="popup-style">', unsafe_allow_html=True)
    with st.form(key="formulaire_popup"):
        st.markdown("###  Envoyer un message")
        st.session_state.nom = st.text_input("Nom", value=st.session_state.nom)
        st.session_state.email = st.text_input("Email", value=st.session_state.email)
        st.session_state.message = st.text_area("Message", value=st.session_state.message)

        submit = st.form_submit_button("Envoyer")

        if submit:
            # si envoyer, enrégistrer les informations dans le CSV
            if st.session_state.nom and st.session_state.email and st.session_state.message:
                nouvelle_ligne = {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "nom": st.session_state.nom,
                    "email": st.session_state.email,
                    "message": st.session_state.message
                }
# ---------------------stockons les informations dans un csv
# dossier_csv = "data\Contacts.csv"
                fichier_csv = 'data/Contacts.csv'
                df = pd.read_csv(fichier_csv)
                df = pd.concat([df, pd.DataFrame([nouvelle_ligne])],
                                ignore_index=True)
                df.to_csv(fichier_csv, index=False)
                # ajouter la nouvelle ligne
                #df = pd.concat([df, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
                #df.to_csv(fichier_csv, index=False)
            # valider si le message a été bien envoyer   
                st.success("✅ Merci pour votre message !")
            # réinitialise le formulaire
                st.session_state.nom = ""
                st.session_state.email = ""
                st.session_state.message = ""
                    # Masquer le formulaire après avoir envoyé                            
                st.session_state["popup_active"] = False 
            
            # sinon affiche un message d'erreur
            else:
                st.warning("⚠️ Merci de remplir tous les champs.")
    # Masquer le formulaire après avoir envoyé                            
                st.session_state["popup_active"] = False 
    # ------------------------------------Réinitialiser les champs

            # sinon affiche un message d'erreur
        else:
            st.warning("⚠️ Merci de remplir tous les champs.")
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------
st.divider()

# -----------colonne titre + bouton ----------------

col1, col2, col3 = st.columns([2, 3, 1])
# nous ajustons les largeurs, plus large à gauche pour le titre
# --------------Création du bouton pour afficher le formulaire
with col2:
    if st.button("📬 Écrire un message"):
        show_contact_form()
        
# ---------------------------------------------------
with col3:
    st.markdown("")
# --------------Titre du formulaire ---------------------------
with col1:
    st.markdown("###")  # espace pour le titre

# -----------------------  
# ------------------------------
st.markdown("---")
# -------------------------------------------------------

# --- bas de page ---
st.markdown('<div class="footer">© 2025 SAPEM CONSEIL. All rights reserved.</div>', unsafe_allow_html=True)

# --- Styles personnalisés de notre page de contact ---
st.markdown("""
    <style>
    .main {
        background-color: #EFF5F3;
    }
    .title { 
        color: #0B2C4A;
        font-size: 36px;
        text-align: center;
        font-family: 'Georgia';
        margin-bottom: 10px;
    }
    .subtitle {
        color: #00C5A2;
        font-size: 20px;
        text-align: center;
        font-family: 'Verdana';
    }
    .footer {
        margin-top: 50px;
        text-align: center;
        font-size: 14px;
        color: #A0A0A0;
    }
    </style>
""", unsafe_allow_html=True)
# -------

# --------------style du bouton du formulaire
st.markdown("""
<style>
    .stButton>button {
        background-color: #05335F;
        color: white;
        border-radius: 12px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)
# ----------------------------------------------
