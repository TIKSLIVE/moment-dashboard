import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Moment Live Dashboard", layout="wide")
st.title("🚀 Moment Live Sales (Session Mode)")

# Ton jeton de session (le JWT)
SESSION_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoidXNlciIsImxvZ2luVHlwZSI6InBhc3N3b3JkIiwiaWQiOiI2NmU5MmViMTM2NGE4NzgwNTFiOGE2MjMiLCJpc0FkbWluIjpmYWxzZSwic2VsbGVySWQiOiI2OTY5MjQwZjY2NDE5OGFiM2VlM2Y0ZGYiLCJvcmdJZCI6IjY2YWNiOTYwN2IzN2M1MzZkOGYwZDVlZCIsImlhdCI6MTc3MDAzODQyMSwiZXhwIjoxNzcwMjU0NDIxfQ.tD3q8txkGcLqvijPrjch9omYwTvOsmd_LNs4jpPq_R0"

# L'URL interne que le dashboard utilise
url = "https://vivenu.com/api/v1/manager/events"

headers = {
    "Authorization": f"Bearer {SESSION_TOKEN}",
    "Accept": "application/json"
}

params = {
    "organization": "66acb9607b37c536d8f0d5ed",
    "page": 0,
    "pageSize": 50
}

try:
    res = requests.get(url, headers=headers, params=params)
    
    if res.status_code == 200:
        data = res.json()
        events = data.get('data', [])
        
        if events:
            rows = []
            for e in events:
                rows.append({
                    "Événement": e.get('name'),
                    "Vendus": e.get('ticketsSold', 0),
                    "CA (€)": e.get('revenue', 0) / 100,
                    "Capacité": e.get('capacity', 0)
                })
            
            df = pd.DataFrame(rows)
            
            # Affichage des métriques
            c1, c2, c3 = st.columns(3)
            c1.metric("Billets Vendus", int(df['Vendus'].sum()))
            c2.metric("CA Total", f"{df['CA (€)'].sum():,.2f} €")
            c3.metric("Événements", len(df))
            
            st.divider()
            st.subheader("Détail par événement")
            st.bar_chart(df.set_index("Événement")["Vendus"])
            st.table(df)
        else:
            st.warning("Connecté, mais aucun événement trouvé.")
            
    else:
        st.error(f"Erreur {res.status_code}")
        st.write("Le jeton a peut-être expiré. Reprends-en un nouveau sur ton dashboard.")
        
except Exception as e:
    st.error(f"Erreur technique : {e}")
