import streamlit as st
import requests
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Live Vivenu Dashboard", layout="wide")
st.title("📊 Suivi des Ventes Vivenu en Temps Réel")

# --- CONFIGURATION ---
# Remplacez par votre clé API ou utilisez les "Secrets" de Streamlit
API_KEY = st.sidebar.text_input("Entrez votre Clé API Vivenu", type="password")

if API_KEY:
    headers = {"X-Api-Key": API_KEY}
    
    # Appel à l'API Vivenu pour récupérer les événements
    url = "https://vivenu.com/api/v1/managers/events"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        st.write(data) # Cette ligne affichera le message brut de Vivenu sur votre écran
        
        # Transformation des données pour le dashboard
        events = data.get('data', [])
        
        if events:
            # Création d'une liste propre
            summary = []
            for e in events:
                summary.append({
                    "Événement": e.get('name'),
                    "Vendus": e.get('ticketsSold'),
                    "Capacité": e.get('capacity'),
                    "Revenus (€)": e.get('revenue') / 100 # Vivenu compte souvent en centimes
                })
            
            df = pd.DataFrame(summary)

            # --- AFFICHAGE ---
            # 1. Chiffres clés en haut
            total_vendus = df['Vendus'].sum()
            total_rev = df['Revenus (€)'].sum()
            
            col1, col2 = st.columns(2)
            col1.metric("Total Billets Vendus", total_vendus)
            col2.metric("Chiffre d'Affaires Total", f"{total_rev} €")

            # 2. Graphique simple
            st.subheader("Ventes par Événement")
            st.bar_chart(df.set_index("Événement")["Vendus"])

            # 3. Tableau détaillé
            st.subheader("Détails des Événements")
            st.dataframe(df, use_container_width=True)
            
        else:
            st.warning("Aucun événement trouvé sur ce compte.")
            
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
else:
    st.info("Veuillez entrer votre clé API dans la barre latérale pour voir les données.")
