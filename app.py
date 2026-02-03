import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Moment Live Dashboard", layout="wide")
st.title("🚀 Moment Live Sales (Session Mode)")

# Ton ID d'organisation
ORG_ID = "66acb9607b37c536d8f0d5ed"

# Champ pour coller le jeton dans la barre latérale
jwt_input = st.sidebar.text_area("Collez votre Jeton (JWT) ici", height=150)

if jwt_input:
    # URL de ton instance privée
    url = "https://dashboard.moment.is/api/v1/manager/events"
    
    headers = {
        "Authorization": f"Bearer {jwt_input.strip()}",
        "Accept": "application/json"
    }
    
    params = {
        "organization": ORG_ID,
        "page": 0,
        "pageSize": 100
    }
    
    try:
        res = requests.get(url, headers=headers, params=params)
        
        if res.status_code == 200:
            data = res.json()
            events = data.get('data', [])
            
            if events:
                df = pd.DataFrame([{
                    "Événement": e.get('name'),
                    "Vendus": e.get('ticketsSold', 0),
                    "CA (€)": e.get('revenue', 0) / 100,
                    "Capacité": e.get('capacity', 0)
                } for e in events])

                c1, c2, c3 = st.columns(3)
                c1.metric("Billets Vendus", int(df['Vendus'].sum()))
                c2.metric("CA Total", f"{df['CA (€)'].sum():,.2f} €")
                c3.metric("Événements", len(df))

                st.divider()
                st.bar_chart(df.set_index("Événement")["Vendus"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Aucun événement trouvé.")
                
        elif res.status_code == 404:
            st.error("Erreur 404 : L'instance Moment rejette la route API.")
            st.info("💡 Test final : Essayez de changer l'URL dans le code pour 'https://vivenu.com/api/v1/manager/events'")
        else:
            st.error(f"Erreur {res.status_code}")
            st.write(res.text)
            
    except Exception as e:
        st.error(f"Erreur technique : {e}")
else:
    st.info("👈 Veuillez coller votre jeton JWT dans la barre latérale.")
