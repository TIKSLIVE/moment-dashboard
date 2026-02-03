import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Vivenu Live Dashboard", layout="wide")
st.title("📊 Dashboard Live Vivenu")

# Nettoyage de la clé pour éviter les erreurs d'espaces
api_input = st.sidebar.text_input("Clé API Vivenu", type="password")
API_KEY = api_input.strip() if api_input else None

if API_KEY:
    # Cette URL est celle utilisée par les dashboards de gestion récents
    url = "https://vivenu.com/api/v1/managers/events"
    
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        # On tente l'appel
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # On cherche les événements dans 'data' ou directement à la racine
            events_list = data.get('data', data if isinstance(data, list) else [])
            
            if events_list:
                summary = []
                for e in events_list:
                    # Extraction sécurisée des données
                    name = e.get('name', 'Sans nom')
                    sold = e.get('ticketsSold', 0)
                    cap = e.get('capacity', 0)
                    rev = e.get('revenue', 0) / 100
                    
                    summary.append({
                        "Événement": name,
                        "Vendus": sold,
                        "Capacité": cap,
                        "CA (€)": rev
                    })
                
                df = pd.DataFrame(summary)

                # Affichage des compteurs
                c1, c2 = st.columns(2)
                c1.metric("Billets vendus", int(df['Vendus'].sum()))
                c2.metric("Total CA", f"{df['CA (€)'].sum():,.2f} €")

                st.divider()
                st.bar_chart(df.set_index("Événement")["Vendus"])
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Connexion réussie mais la liste des événements est vide.")
                st.write("Réponse brute de l'API :", data) # Pour comprendre la structure
                
        else:
            st.error(f"Erreur {response.status_code}")
            st.info("Tentative avec une URL alternative...")
            
            # TENTATIVE B : URL simplifiée
            alt_url = "https://api.vivenu.com/v1/events" # Parfois utilisé sur certaines versions
            alt_res = requests.get(alt_url, headers=headers)
            st.write(f"Test URL Alternative : {alt_res.status_code}")

    except Exception as e:
        st.error(f"Erreur technique : {e}")
else:
    st.info("👈 Entrez votre clé API (Level Organisation de préférence) dans la barre latérale.")
