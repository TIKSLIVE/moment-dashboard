import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Dashboard Moment Live", layout="wide")
st.title("🎟️ Moment Live Sales")

api_input = st.sidebar.text_input("Clé API Organisation (key_org_...)", type="password")
API_KEY = api_input.strip() if api_input else None

if API_KEY:
    # On teste les 3 URLs les plus probables pour un domaine dédié
    urls_to_test = [
        "https://api.vivenu.com/v1/manager/events",
        "https://dashboard.moment.is/api/v1/manager/events",
        "https://vivenu.com/api/v1/manager/events"
    ]
    
    headers = {
        "X-Api-Key": API_KEY,
        "Accept": "application/json"
    }
    
    found = False
    for url in urls_to_test:
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                data = res.json()
                events = data.get('data', [])
                
                if events:
                    df = pd.DataFrame([{
                        "Nom": e.get('name'),
                        "Vendus": e.get('ticketsSold', 0),
                        "CA (€)": e.get('revenue', 0) / 100
                    } for e in events])

                    c1, c2 = st.columns(2)
                    c1.metric("Billets Vendus", int(df['Vendus'].sum()))
                    c2.metric("CA Total", f"{df['CA (€)'].sum():,.2f} €")
                    st.divider()
                    st.bar_chart(df.set_index("Nom")["Vendus"])
                    st.table(df)
                    found = True
                    break
        except:
            continue

    if not found:
        st.error("Impossible de trouver vos données via les routes standards.")
        st.info("💡 Action à faire : Regardez dans votre interface Moment, sous votre clé API. Y a-t-il un champ nommé 'Organization ID' ou un lien spécifique pour l'API ?")
        st.write("Dernier test effectué sur :", urls_to_test[0])
else:
    st.info("Saisissez votre clé API Organisation à gauche.")
