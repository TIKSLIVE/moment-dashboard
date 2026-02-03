import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Moment Dash", layout="wide")
st.title("📊 Moment Sales Tracker")

ORG_ID = "66acb9607b37c536d8f0d5ed"
API_KEY = st.sidebar.text_input("Clé API (key_org_...)", type="password").strip()

if API_KEY:
    # Cette route est souvent plus accessible que /manager/events
    url = f"https://vivenu.com/api/v1/organizations/{ORG_ID}/events"
    
    headers = {
        "X-Api-Key": API_KEY,
        "Accept": "application/json"
    }
    
    try:
        res = requests.get(url, headers=headers)
        
        # Si ça ne marche pas, on tente la route des statistiques (plus légère)
        if res.status_code != 200:
            url = f"https://vivenu.com/api/v1/manager/statistics/events"
            res = requests.get(url, headers=headers, params={"organization": ORG_ID})

        if res.status_code == 200:
            data = res.json()
            events = data.get('data', [])
            
            if events:
                df = pd.DataFrame([{
                    "Événement": e.get('name'),
                    "Vendus": e.get('ticketsSold', 0),
                    "CA (€)": e.get('revenue', 0) / 100
                } for e in events])

                st.success("Données récupérées !")
                c1, c2 = st.columns(2)
                c1.metric("Billets Vendus", int(df['Vendus'].sum()))
                c2.metric("CA Total", f"{df['CA (€)'].sum():,.2f} €")
                st.divider()
                st.table(df)
            else:
                st.info("Connexion réussie, mais aucun événement actif trouvé.")
        
        else:
            st.error(f"Erreur {res.status_code}")
            st.write("Détails :", res.text)
            st.warning("⚠️ Ta clé API semble être bridée par Vivenu. Contacte leur support pour demander l'activation des droits 'READ' sur ton API Key.")

    except Exception as e:
        st.error(f"Erreur technique : {e}")
else:
    st.info("Saisis ta clé API à gauche.")
