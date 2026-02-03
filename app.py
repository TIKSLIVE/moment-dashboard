import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Dashboard Moment Live", layout="wide")

# Interface
st.title("🎟️ Moment Live Sales")
api_input = st.sidebar.text_input("Clé API Organisation", type="password")
API_KEY = api_input.strip() if api_input else None

if API_KEY:
    # On revient sur l'API centrale qui distribue les données pour Moment
    url = "https://vivenu.com/api/v1/managers/events"
    
    headers = {
        "X-Api-Key": API_KEY,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:
        # On tente de récupérer les données
        res = requests.get(url, headers=headers)
        
        if res.status_code == 200:
            data = res.json()
            events = data.get('data', [])
            
            if events:
                # Extraction des données
                df = pd.DataFrame([{
                    "Nom": e.get('name'),
                    "Vendus": e.get('ticketsSold', 0),
                    "CA (€)": e.get('revenue', 0) / 100,
                    "Capacité": e.get('capacity', 0)
                } for e in events])

                # Affichage des chiffres en gros
                c1, c2 = st.columns(2)
                c1.metric("Billets Vendus", int(df['Vendus'].sum()))
                c2.metric("CA Total", f"{df['CA (€)'].sum():,.2f} €")

                st.divider()
                
                # Graphique et Tableau
                st.subheader("Ventes par événement")
                st.bar_chart(df.set_index("Nom")["Vendus"])
                st.table(df)
            else:
                st.info("Aucun événement actif trouvé.")
        
        elif res.status_code == 404:
            # Si 404, on tente la version SANS le 's' à managers
            alt_url = "https://vivenu.com/api/v1/manager/events"
            res_alt = requests.get(alt_url, headers=headers)
            if res_alt.status_code == 200:
                st.success("Connecté via URL alternative !")
                # (Répéter la logique d'affichage ici ou rafraîchir)
                st.rerun()
            else:
                st.error("Erreur 404 persistante. Votre clé API ne semble pas autorisée à lister les événements via l'API publique.")
                st.info("Vérifiez sur Moment > Settings > API que votre clé a bien les droits 'MANAGER'.")
        
        else:
            st.error(f"Erreur {res.status_code}")
            st.write("Détails :", res.text)

    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
else:
    st.info("Veuillez saisir votre Clé API dans la barre latérale.")
