import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Moment Dashboard", layout="wide")
st.title("📊 Moment Live Dashboard")

# Ton ID d'organisation
ORG_ID = "66acb9607b37c536d8f0d5ed"

# Authentification
API_KEY = st.sidebar.text_input("Clé API Organisation (key_org_...)", type="password").strip()

if API_KEY:
    # Changement d'URL : On utilise le domaine Vivenu pur, car c'est là que vivent les données
    # même pour les comptes "Moment".
    url = "https://vivenu.com/api/v1/manager/events"
    
    # Très important : Vivenu exige parfois l'ID d'organisation dans les headers ET les params
    headers = {
        "X-Api-Key": API_KEY,
        "Accept": "application/json",
        "X-Organization-Id": ORG_ID  # Header spécifique à Vivenu
    }
    
    params = {"organization": ORG_ID}
    
    try:
        res = requests.get(url, headers=headers, params=params)
        
        # Si 404 sur vivenu.com, on tente une dernière fois sur l'API "v2" de Moment
        if res.status_code == 404:
            url_moment = "https://dashboard.moment.is/api/v1/managers/events"
            res = requests.get(url_moment, headers=headers)

        if res.status_code == 200:
            data = res.json()
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
                st.info("Connexion réussie ! Aucun événement n'a pu être récupéré.")
        else:
            st.error(f"Erreur {res.status_code}")
            st.warning("Le serveur refuse l'accès ou la route est incorrecte.")
            st.write("Astuce : Vérifie que ta clé API a bien été créée au niveau 'Organisation' sur dashboard.moment.is/apikeys")
            
    except Exception as e:
        st.error(f"Erreur technique : {e}")
else:
    st.info("👈 Entre ta clé API Organisation (Secret Key) pour commencer.")
