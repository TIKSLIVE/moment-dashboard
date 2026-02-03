import streamlit as st
import requests

st.title("🕵️ Testeur de Clé API")

API_KEY = st.sidebar.text_input("Clé API", type="password").strip()

if API_KEY:
    # On teste la route la plus basique possible (infos organisation)
    url = "https://vivenu.com/api/v1/manager/organizations/66acb9607b37c536d8f0d5ed"
    
    headers = {
        "X-Api-Key": API_KEY,
        "Accept": "application/json"
    }
    
    res = requests.get(url, headers=headers)
    
    if res.status_code == 200:
        st.success("✅ TA CLÉ FONCTIONNE !")
        st.json(res.json())
        st.info("Si cette route marche mais pas l'autre, c'est que tu dois demander à Moment d'activer l'accès 'Events' sur ton API.")
    else:
        st.error(f"❌ Erreur {res.status_code}")
        st.write("Le serveur dit :", res.text)
        st.warning("Si tu as 404 ici, ta clé n'est pas reconnue du tout.")
