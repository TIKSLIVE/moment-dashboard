import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Vivenu Live Dashboard", layout="wide")
st.title("📊 Dashboard Live Vivenu")

# Barre latérale pour la clé API
API_KEY = st.sidebar.text_input("Clé API Vivenu", type="password")

if API_KEY:
    # L'URL "manager" sans le 's' à la fin de 'v1' et avec le bon chemin
    url = "https://vivenu.com/api/v1/manager/events"
    headers = {
        "X-Api-Key": API_KEY,
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # Vivenu renvoie souvent les données dans une liste 'data'
            events_list = data.get('data', [])
            
            if events_list:
                # Préparation des données
                summary = []
                for e in events_list:
                    summary.append({
                        "Nom": e.get('name'),
                        "Vendus": e.get('ticketsSold', 0),
                        "Capacité": e.get('capacity', 0),
                        # Le revenu est souvent en centimes, on divise par 100
                        "CA (€)": e.get('revenue', 0) / 100 
                    })
                
                df = pd.DataFrame(summary)

                # --- AFFICHAGE ---
                col1, col2, col3 = st.columns(3)
                col1.metric("Billets vendus", int(df['Vendus'].sum()))
                col2.metric("Chiffre d'Affaires Total", f"{df['CA (€)'].sum():,.2f} €")
                col3.metric("Nombre d'Événements", len(df))

                st.divider()

                st.subheader("Ventes par Événement")
                st.bar_chart(df.set_index("Nom")["Vendus"])

                st.subheader("Détail complet")
                st.table(df)
            else:
                st.info("Connexion réussie, mais aucun événement n'est listé sur ce compte.")
        else:
            st.error(f"Erreur {response.status_code} : {response.text}")
            
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
else:
    st.info("👈 Veuillez entrer votre clé API dans la barre latérale pour commencer.")
