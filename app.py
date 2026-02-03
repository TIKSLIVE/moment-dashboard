import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Moment Live Dashboard", layout="wide")
st.title("🚀 Moment Live Sales")
ORG_ID = "66acb9607b37c536d8f0d5ed"
st.caption(f"Organisation ID : {ORG_ID}")

API_KEY = st.sidebar.text_input("Clé API Organisation", type="password").strip()

if API_KEY:
    # On définit les 3 routes possibles pour les comptes avec ID
    routes = [
        f"https://vivenu.com/api/v1/manager/organizations/{ORG_ID}/events",
        f"https://dashboard.moment.is/api/v1/manager/organizations/{ORG_ID}/events",
        f"https://vivenu.com/api/v1/manager/events?organization={ORG_ID}"
    ]
    
    headers = {"X-Api-Key": API_KEY, "Accept": "application/json"}
    
    data = None
    active_url = ""

    # On boucle jusqu'à ce qu'on trouve la bonne route
    for url in routes:
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                data = res.json()
                active_url = url
                break
        except:
            continue

    if data:
        # Extraction des événements (gère les listes ou les objets avec clé 'data')
        events = data.get('data', []) if isinstance(data, dict) else data
        
        if events:
            rows = []
            for e in events:
                rows.append({
                    "Événement": e.get('name', 'N/A'),
                    "Vendus": e.get('ticketsSold', 0),
                    "CA (€)": e.get('revenue', 0) / 100,
                    "Capacité": e.get('capacity', 0)
                })
            
            df = pd.DataFrame(rows)

            # Métriques
            c1, c2, c3 = st.columns(3)
            c1.metric("Billets Vendus", int(df['Vendus'].sum()))
            c2.metric("CA Total", f"{df['CA (€)'].sum():,.2f} €")
            c3.metric("Événements", len(df))

            st.divider()
            st.bar_chart(df.set_index("Événement")["Vendus"])
            st.dataframe(df, use_container_width=True)
            st.success(f"Connecté via : {active_url}")
        else:
            st.info("Connexion réussie, mais aucun événement trouvé.")
    else:
        st.error("Échec de la connexion (Erreur 404 sur toutes les routes).")
        st.info("C'est très rare à ce stade. Pourriez-vous vérifier que votre Clé API possède bien la permission 'Managers' ou 'Events' dans votre interface Moment ?")
else:
    st.info("👈 Entrez votre clé API à gauche.")
