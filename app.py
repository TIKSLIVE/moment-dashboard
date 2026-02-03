import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Moment Dashboard", layout="wide")
st.title("📊 Moment Live Dashboard")

ORG_ID = "66acb9607b37c536d8f0d5ed"
API_KEY = st.sidebar.text_input("Clé API Organisation", type="password").strip()

if API_KEY:
    # Les 3 seules URLs qui peuvent techniquement fonctionner pour une organisation Vivenu/Moment
    endpoints = [
        "https://vivenu.com/api/v1/manager/events",        # API Standard
        "https://vivenu.com/api/v1/managers/events",       # API Standard (pluriel)
        "https://api.vivenu.com/v1/manager/events"         # API Développeur
    ]
    
    headers = {
        "X-Api-Key": API_KEY,
        "X-Organization-Id": ORG_ID, # On force l'ID ici
        "Accept": "application/json"
    }
    
    params = {"organization": ORG_ID}
    
    found = False
    for url in endpoints:
        try:
            res = requests.get(url, headers=headers, params=params)
            # Si échec, on tente avec le format Bearer sur la même URL
            if res.status_code != 200:
                auth_headers = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}
                res = requests.get(url, headers=auth_headers, params=params)

            if res.status_code == 200:
                data = res.json()
                events = data.get('data', [])
                if events:
                    df = pd.DataFrame([{
                        "Événement": e.get('name'),
                        "Vendus": e.get('ticketsSold', 0),
                        "CA (€)": e.get('revenue', 0) / 100
                    } for e in events])
                    
                    st.success(f"Connecté avec succès via {url.split('/')[2]} !")
                    c1, c2 = st.columns(2)
                    c1.metric("Billets Vendus", int(df['Vendus'].sum()))
                    c2.metric("CA Total", f"{df['CA (€)'].sum():,.2f} €")
                    st.divider()
                    st.bar_chart(df.set_index("Événement")["Vendus"])
                    st.dataframe(df, use_container_width=True)
                    found = True
                    break
        except:
            continue

    if not found:
        st.error("Routes API épuisées (404/401).")
        st.info("""
        ### 💡 Vérification ultime sur ton compte Moment :
        1. Va sur **dashboard.moment.is/apikeys**.
        2. Clique sur ta clé.
        3. Regarde bien la liste des **Permissions**.
        4. Est-ce que **"Managers"** ou **"Events"** est coché ?
        
        Si tu ne peux pas modifier les permissions, c'est que la clé n'a pas le droit "Lecture".
        """)
else:
    st.info("👈 Entre ta clé API pour scanner les serveurs.")
