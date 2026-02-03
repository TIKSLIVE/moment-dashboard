import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Moment Live Dashboard", layout="wide")
st.title("🚀 Moment Live Sales (Miroir Session)")

# Ton Seller ID extrait de ton URL
SELLER_ID = "6969240f664198ab3ee3f4df"

# Barre latérale pour le JWT
jwt_input = st.sidebar.text_area("Collez votre Jeton (JWT) ici", height=150)

if jwt_input:
    # On construit l'URL exacte qui a fonctionné dans ton navigateur
    url = "https://vivenu.com/api/events"
    
    # Dates dynamique (aujourd'hui à +3 jours comme dans ton URL)
    start_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    params = {
        "sellerId": SELLER_ID,
        "start": start_date,
        "end": end_date,
        "type[0]": "SINGLE",
        "type[1]": "RECURRENCE",
        "top": 50, # On en prend plus que 6
        "sortDir": 1
    }
    
    headers = {
        "Authorization": f"Bearer {jwt_input.strip()}",
        "Accept": "application/json"
    }
    
    try:
        res = requests.get(url, headers=headers, params=params)
        
        if res.status_code == 200:
            data = res.json()
            # Dans cette route, les événements sont souvent directement dans la liste ou dans 'data'
            events = data if isinstance(data, list) else data.get('data', [])
            
            if events:
                rows = []
                for e in events:
                    rows.append({
                        "Événement": e.get('name'),
                        "Date": e.get('start'),
                        "Vendus": e.get('ticketsSold', 0),
                        "CA (€)": e.get('revenue', 0) / 100,
                        "Capacité": e.get('capacity', 0)
                    })
                
                df = pd.DataFrame(rows)

                # --- DASHBOARD ---
                c1, c2, c3 = st.columns(3)
                c1.metric("Billets Vendus", int(df['Vendus'].sum()))
                c2.metric("CA Total", f"{df['CA (€)'].sum():,.2f} €")
                c3.metric("Événements", len(df))

                st.divider()
                st.subheader("Ventes par événement")
                st.bar_chart(df.set_index("Événement")["Vendus"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Connexion réussie ! Mais aucun événement trouvé sur cette période.")
        else:
            st.error(f"Erreur {res.status_code}")
            st.write("Détails :", res.text)
            
    except Exception as e:
        st.error(f"Erreur technique : {e}")
else:
    st.info("👈 Collez le JWT pour synchroniser les données en temps réel.")
