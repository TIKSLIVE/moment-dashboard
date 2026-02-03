import streamlit as st
import requests

st.title("🕵️ Testeur d'Instance Moment")

# On teste l'URL que les développeurs de Moment utilisent en interne
API_KEY = "key_org_383337d0be787635ed84b3fa3c14af0ca1d1bc6a5856bc1938f6bff633aa7d82632249c372e87c2afcdd5a8f940e0991"
ORG_ID = "66acb9607b37c536d8f0d5ed"

# Liste de tests sur ton instance spécifique
tests = [
    f"https://dashboard.moment.is/api/v1/organizations/{ORG_ID}",
    f"https://dashboard.moment.is/api/v1/manager/events?organization={ORG_ID}",
    f"https://vivenu.com/api/v1/manager/events?organization={ORG_ID}"
]

headers = {
    "X-Api-Key": API_KEY,
    "Accept": "application/json"
}

for url in tests:
    st.write(f"Tentative sur : `{url}`")
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            st.success(f"✅ SUCCÈS sur {url}")
            st.json(res.json())
            st.stop()
        else:
            st.warning(f"Code {res.status_code} sur cette route.")
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")

st.error("🚨 Toutes les tentatives ont échoué.")
st.info("""
### Pourquoi ça ne marche pas ?
Ton instance **Moment** est verrouillée. Dans ton message précédent, on voyait `OWN_URL: http://localhost:3300`. Cela signifie que leur code tourne dans un environnement très spécifique.

**La solution :**
Tu dois envoyer un mail à ton contact chez **Moment** avec ce texte :
"Bonjour, je souhaite connecter un dashboard externe via l'API. Ma clé ORG renvoie systématiquement un 404 sur les endpoints standards. Pouvez-vous me confirmer l'URL de l'API (Endpoint) à utiliser pour mon instance et m'assurer que ma clé a les droits 'Manager' ?"
""")
