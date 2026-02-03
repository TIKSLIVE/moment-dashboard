import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Dashboard Moment Live", layout="wide")
st.title("📊 Moment Live Sales")

# Votre ID d'organisation
ORG_ID = "66acb9607b37c536d8f0d5ed"
st.caption(f"Organisation ID : {ORG_ID}")

# Clé API
api_input = st.sidebar.text_input("Clé API Organisation (key_org_...)", type="password")
API_KEY = api_input.strip() if api_input else None

if API_KEY:
    # Sur une instance dédiée, l'API est souvent sur le même domaine que le dashboard
    # On va tester la route la plus standard pour les événements
    url = "https://dashboard.moment.is/api/v1/manager/events"
    
    # Paramètres d'organisation
    params = {"organization": ORG_ID}
    
    # Header selon les standards de sécurité de votre instance
    headers = {
        "X-Api-Key": API_KEY,
        "Accept": "application/json"
    }
    
    try:
        # Tentative 1 : Route standard
        res = requests.get(url, headers=headers, params=params)
        
        # Tentative 2 : Si 404, on tente sans le préfixe /manager/
        if res.status_code == 404:
            url_alt = "https://dashboard.moment.is/api/v1/events"
            res = requests.get(url_alt, headers=headers, params=params)

        if res.status_code == 200:
            data = res.json()
            # On extrait la liste des événements
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

                # --- DASHBOARD ---
                c1, c2, c3 = st.columns(3)
                c1.metric("Billets Vendus", int(df['Vendus'].sum()))
                c2.metric("CA Total", f"{df['CA (€)'].sum():,.2f} €")
                c3.metric("Événements", len(df))

                st.divider()
                st.subheader("Ventes par événement")
                st.bar_chart(df.set_index("Événement")["Vendus"])
                st.dataframe(df.sort_values(by="Vendus", ascending=False), use_container_width=True)
                
            else:
                st.info("Connecté au serveur Moment ! Mais aucun événement n'est listé pour cette clé.")
        
        elif res.status_code == 401:
            st.error("Erreur 401 : Clé API non reconnue par le serveur Moment.is.")
        else:
            st.error(f"Erreur {res.status_code}")
            st.write("Réponse du serveur :", res.text)
            
    except Exception as e:
        st.error(f"Erreur technique : {e}")
else:
    st.info("👈 Entrez votre clé API (key_org_...) générée sur dashboard.moment.is/apikeys")
