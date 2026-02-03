import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Moment Live Dashboard", layout="wide")
st.title("📊 Moment Live Sales")

# Votre ID d'organisation trouvé précédemment
ORG_ID = "66acb9607b37c536d8f0d5ed"

# Barre latérale
st.sidebar.header("Authentification")
api_input = st.sidebar.text_input("Clé API Organisation (key_org_...)", type="password").strip()

if api_input:
    # L'API Vivenu Doc stipule d'utiliser 'Bearer' pour les clés privées
    # On prépare les headers conformes à la documentation
    headers = {
        "Authorization": f"Bearer {api_input}",
        "Accept": "application/json"
    }
    
    # URL de la doc pour lister les événements d'une organisation
    url = "https://api.vivenu.com/v1/manager/events"
    
    # Paramètres de filtrage pour votre organisation
    params = {"organization": ORG_ID}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
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

                # Dashboard metrics
                c1, c2, c3 = st.columns(3)
                c1.metric("Billets Vendus", int(df['Vendus'].sum()))
                c2.metric("CA Total", f"{df['CA (€)'].sum():,.2f} €")
                c3.metric("Taux d'occupation", f"{(df['Vendus'].sum() / df['Capacité'].sum() * 100) if df['Capacité'].sum() > 0 else 0:.1f}%")

                st.divider()
                st.subheader("Ventes par événement")
                st.bar_chart(df.set_index("Événement")["Vendus"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Connexion réussie ! Aucun événement trouvé pour cet ID d'organisation.")
        
        elif response.status_code == 401:
            st.error("Erreur 401 : La clé est rejetée. Essayez d'utiliser la clé SANS le préfixe 'Bearer' si vous l'aviez ajouté manuellement, ou vérifiez la clé sur Moment.")
        elif response.status_code == 404:
            # Ultime recours si api.vivenu.com échoue
            st.warning("Route 1 (api.vivenu.com) indisponible, tentative sur Route 2...")
            alt_url = f"https://vivenu.com/api/v1/manager/events"
            res_alt = requests.get(alt_url, headers=headers, params=params)
            st.write(f"Résultat Route 2 : {res_alt.status_code}")
        else:
            st.error(f"Erreur {response.status_code}")
            st.write(response.json())

    except Exception as e:
        st.error(f"Erreur technique : {e}")
else:
    st.info("👈 Entrez votre clé API (key_org_...) dans la barre latérale.")
