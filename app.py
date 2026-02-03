import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Moment Dashboard", layout="wide")
st.title("📊 Dashboard Live Moment (Vivenu)")

# Nettoyage de la clé
api_input = st.sidebar.text_input("Clé API (Level Organisation)", type="password")
API_KEY = api_input.strip() if api_input else None

if API_KEY:
    # Changement crucial : on utilise votre domaine dédié
    url = "https://dashboard.moment.is/api/v1/managers/events"
    
    headers = {
        "X-Api-Key": API_KEY,
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # Sur certains domaines custom, la structure peut être dans 'data' ou à la racine
            events_list = data.get('data', []) if isinstance(data, dict) else data
            
            if events_list:
                summary = []
                for e in events_list:
                    summary.append({
                        "Événement": e.get('name', 'N/A'),
                        "Vendus": e.get('ticketsSold', 0),
                        "Capacité": e.get('capacity', 0),
                        "CA (€)": e.get('revenue', 0) / 100 
                    })
                
                df = pd.DataFrame(summary)

                # Chiffres clés
                c1, c2, c3 = st.columns(3)
                c1.metric("Billets vendus", int(df['Vendus'].sum()))
                c2.metric("Total CA", f"{df['CA (€)'].sum():,.2f} €")
                c3.metric("Taux d'occupation", f"{(df['Vendus'].sum() / df['Capacité'].sum() * 100) if df['Capacité'].sum() > 0 else 0:.1f}%")

                st.divider()
                st.subheader("Ventes par Événement")
                st.bar_chart(df.set_index("Événement")["Vendus"])
                
                st.subheader("Détails")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Connexion réussie ! Mais aucun événement n'est remonté. Vérifiez que vos événements sont bien publiés.")
        else:
            st.error(f"Erreur {response.status_code}")
            st.write("Détails de l'erreur :", response.text)
            st.info("Essayez avec l'URL alternative si l'erreur est 404...")
            
    except Exception as e:
        st.error(f"Erreur technique : {e}")
else:
    st.info("👈 Entrez votre clé API Moment dans la barre latérale.")
