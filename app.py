import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Vivenu Live Dashboard", layout="wide")
st.title("📊 Dashboard Live Vivenu")

API_KEY = st.sidebar.text_input("Clé API Vivenu", type="password")

if API_KEY:
    # On définit les deux variantes possibles de l'URL
    urls_to_try = [
        "https://vivenu.com/api/v1/manager/events",
        "https://vivenu.com/api/v1/managers/events"
    ]
    
    headers = {
        "X-Api-Key": API_KEY,
        "Accept": "application/json"
    }
    
    data = None
    success_url = None

    # On teste les URLs une par une
    for url in urls_to_try:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                success_url = url
                break
        except:
            continue

    if data:
        # Si on arrive ici, c'est qu'une des deux URLs a fonctionné !
        events_list = data.get('data', [])
        
        if events_list:
            summary = []
            for e in events_list:
                summary.append({
                    "Nom": e.get('name'),
                    "Vendus": e.get('ticketsSold', 0),
                    "Capacité": e.get('capacity', 0),
                    "CA (€)": e.get('revenue', 0) / 100 
                })
            
            df = pd.DataFrame(summary)

            col1, col2, col3 = st.columns(3)
            col1.metric("Billets vendus", int(df['Vendus'].sum()))
            col2.metric("Chiffre d'Affaires Total", f"{df['CA (€)'].sum():,.2f} €")
            col3.metric("Événements", len(df))

            st.divider()
            st.subheader("Ventes par Événement")
            st.bar_chart(df.set_index("Nom")["Vendus"])
            st.table(df)
        else:
            st.info("Connexion réussie, mais aucun événement trouvé.")
    else:
        st.error("Impossible de trouver vos données. Vérifiez que votre Clé API est une 'Manager API Key' et non une clé limitée à une seule boutique.")
        st.info("💡 Conseil : Allez dans Settings > API sur Vivenu et assurez-vous de copier la 'Secret Key'.")
else:
    st.info("👈 Entrez votre clé API dans la barre latérale.")
