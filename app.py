import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Diagnostic Vivenu", layout="wide")
st.title("🔍 Diagnostic de Connexion Vivenu")

API_KEY = st.sidebar.text_input("Clé API Vivenu", type="password")

if API_KEY:
    # On teste l'URL la plus probable
    url = "https://vivenu.com/api/v1/manager/events"
    headers = {
        "X-Api-Key": API_KEY,
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # ZONE DE DIAGNOSTIC
        st.subheader("Résultat du test :")
        if response.status_code == 200:
            st.success("✅ Connexion réussie !")
            st.json(response.json()) # Affiche les données brutes
        elif response.status_code == 401:
            st.error("❌ Erreur 401 : Clé API non valide ou expirée.")
        elif response.status_code == 403:
            st.error("❌ Erreur 403 : Votre clé n'a pas les droits suffisants (Permissions).")
        elif response.status_code == 404:
            st.error("❌ Erreur 404 : L'adresse de l'API n'est pas la bonne pour votre compte.")
        else:
            st.error(f"❌ Erreur {response.status_code}")
            st.write("Message de Vivenu :", response.text)

    except Exception as e:
        st.error(f"Erreur technique : {e}")
else:
    st.info("Entrez votre clé API à gauche.")
