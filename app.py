import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Moment Dashboard Live", layout="wide")

# Design & Titre
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Moment Live Sales")
st.caption(f"Organisation ID : 66acb9607b37c536d8f0d5ed")

# Configuration latérale
API_KEY = st.sidebar.text_input("Clé API Organisation (key_org_...)", type="password").strip()

if API_KEY:
    # URL Spécifique pour l'API Moment/Vivenu avec ID Organisation
    # On teste la route la plus robuste
    url = "https://vivenu.com/api/v1/manager/events"
    
    # On ajoute l'ID d'organisation dans les paramètres de la requête
    params = {"organization": "66acb9607b37c536d8f0d5ed"}
    headers = {
        "X-Api-Key": API_KEY,
        "Accept": "application/json"
    }
    
    try:
        res = requests.get(url, headers=headers, params=params)
        
        if res.status_code == 200:
            data = res.json()
            events = data.get('data', [])
            
            if events:
                # On transforme les données pour le dashboard
                rows = []
                for e in events:
                    # On ignore les événements archivés ou sans nom
                    if e.get('name'):
                        rows.append({
                            "Événement": e.get('name'),
                            "Vendus": e.get('ticketsSold', 0),
                            "CA (€)": e.get('revenue', 0) / 100,
                            "Capacité": e.get('capacity', 0)
                        })
                
                df = pd.DataFrame(rows)

                # --- PARTIE AFFICHAGE ---
                col1, col2, col3 = st.columns(3)
                col1.metric("Billets Vendus", int(df['Vendus'].sum()))
                col2.metric("CA Total", f"{df['CA (€)'].sum():,.2f} €")
                col3.metric("Taux d'occupation", f"{(df['Vendus'].sum() / df['Capacité'].sum() * 100) if df['Capacité'].sum() > 0 else 0:.1f}%")

                st.divider()

                # Graphique des ventes
                st.subheader("Nombre de billets vendus par événement")
                st.bar_chart(df.set_index("Événement")["Vendus"])

                # Tableau détaillé
                st.subheader("Détail des ventes")
                st.dataframe(df.sort_values(by="Vendus", ascending=False), use_container_width=True)
                
            else:
                st.info("Connexion réussie ! Mais aucun événement actif n'a été trouvé.")
        
        elif res.status_code == 401:
            st.error("Clé API invalide. Vérifiez que vous utilisez bien la 'Secret Key' de niveau Organisation.")
        else:
            st.error(f"Erreur {res.status_code}")
            st.write("Détails techniques :", res.text)

    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
else:
    st.info("👈 Entrez votre clé API dans la barre latérale pour activer le dashboard.")
