'''# ------ pour le remplissage du formulaire de contact principale----------------
#---------------affichage du formulaire--------------------
st.markdown("### 📝 Laissez-nous un message")

with st.form("formulaire_contact"):
    nom = st.session_state.nom = st.text_input("Nom", value=st.session_state.nom)
    email = st.session_state.email = st.text_input("Email", value=st.session_state.email)
    message = st.session_state.message = st.text_area("Message", value=st.session_state.message)

    bouton_envoyer = st.form_submit_button("Envoyer")

    if bouton_envoyer:
        if nom and email and message:
            st.success("✅ Merci pour votre message! Nous vous répondrons rapidement.")
           # (nous allons enrégistrer dans un CSV ici)
        else:
            st.warning("⚠️ Merci de remplir tous les champs avant d'envoyer.")

# ----------------------------------------

# --------------pour stocker chaque message envoyer dans un csv----------
if bouton_envoyer:
        if nom and email and message: # si l'utilisateur a cliqué sur le bouton envoyé après avoir tout bien rempli les espaces demandées
            # Préparer les données
            date_envoi = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # la date du jour
            nouvelle_ligne = {
                "date": date_envoi,
                "nom": nom,
                "email": email,
                "message": message
            }

            # Créons le fichier s'il n'existe pas
              
            fichier_csv = os.path.join("Contacts.csv")
            if not os.path.exists(fichier_csv):
                
                df_init = pd.DataFrame(columns=["date", "nom", "email", "message"])
                df_init.to_csv(fichier_csv, index=False)

            # Ajoutons la ligne au fichier
            df = pd.read_csv(fichier_csv)
            df = pd.concat([df, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
            df.to_csv(fichier_csv, index=False)

#-------------------------------
#--------- Réinitialisation des champs
            st.session_state["nom"] = ""
            st.session_state["email"] = ""
            st.session_state["message"] = ""
#-------------------------------------------------------

# ----------------------Infos de contact avec icônes
st.markdown("""
### 📧 Email  
contact@sapemconseil.com

### 📞 Téléphone  
+33 1 00 00 00 00

### 📍 Adresse  
15 rue 3 Fontaines 70240 La Creuse   
""")

#---------------------------------------------

#-------------------fermer le formulaire -------------
            
st.session_state["popup_active"] = False # Masquer le formulaire après avoir envoyé
    
# Fermer le formulaire et revenir à la page principale
st.rerun()


# ---------------------stockons les informations dans un csv
                #dossier_csv = "data\Contacts.csv"
                fichier_csv = os.path.join("projet_2\data\Contacts.csv")
                if not os.path.exists(fichier_csv):
                    #os.makedirs(dossier_csv)
                    pd.DataFrame(columns=["date", "nom", "email", "message"]).to_csv(fichier_csv, index=False)
'''