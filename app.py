import streamlit as st
import requests

# URL du logo
logo_url = "pngtree-black-and-white-chess-board-chess-pieces-png-image_2901949.jpg"  # Exemple de logo
# Ajouter un style CSS amélioré
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    body {
        font-family: 'Poppins', sans-serif;
        background-color: #00632A; /* Vert italien pour le fond */
        margin: 0;
    }
    .stApp {
        background-color: #2f3136; /* Gris sidéral */
        border-radius: 12px;
        box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.15);
        padding: 30px;
        margin: 30px auto;
        max-width: 800px;
    }
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff; /* Blanc pour contraster avec le gris sidéral */
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #cccccc; /* Gris clair pour le sous-titre */
        text-align: center;
        margin-bottom: 40px;
    }
    .chess-box {
        background-color: #40444b; /* Gris sidéral plus clair pour différencier */
        color: #ffffff; /* Blanc pour le texte */
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #555a60; /* Bordure gris foncé */
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 10px 0;
    }
    textarea {
        background-color: #40444b; /* Gris sidéral pour le champ de texte */
        color: #ffffff; /* Texte blanc pour contraste */
        border: 1px solid #555a60; /* Bordure assortie */
        border-radius: 5px;
        padding: 10px;
        font-size: 1rem;
        font-family: 'Poppins', sans-serif;
    }
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    button {
        background-color: #4caf50; /* Vert chess.com */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 1rem;
        font-family: 'Poppins', sans-serif;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# Ajouter le logo
st.image(logo_url, width=150)

# Titre principal
st.markdown('<div class="title">Chess ELO Predictor</div>', unsafe_allow_html=True)

# Sous-titre
st.markdown('<div class="subtitle">Paste your PGN to discover the skill levels of both players!</div>', unsafe_allow_html=True)

'''
## Add Your Chess Game PGN
'''

# Champ de saisie pour PGN
pgn_input = st.text_area('Paste your PGN of the chess game below:', height=150)

'''
## Retrieve Prediction
'''

st.markdown('''
Once we have the PGN, let's call our API to retrieve predictions for both players.
''')

# URL de l'API
url = 'https://chess-elo-prediction-556540502853.europe-west1.run.app'

# Bouton pour prédire
if st.button('Predict ELO'):
    if pgn_input.strip():  # Vérifie si le champ PGN n'est pas vide
        try:
            with st.spinner('Fetching prediction...'):
                # Appel à l'API
                response = requests.post(url, json={"pgn": pgn_input})

            if response.status_code == 200:
                # Récupère les résultats
                result = response.json()
                elo_white = result.get('elo_white', 'No ELO returned')
                elo_black = result.get('elo_black', 'No ELO returned')

                # Affiche les résultats dans deux colonnes
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown('<div class="chess-box">White ELO<br>{}</div>'.format(elo_white), unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="chess-box">Black ELO<br>{}</div>'.format(elo_black), unsafe_allow_html=True)
            elif response.status_code == 422:
                st.error("The PGN provided is not valid. Please check your input and try again.")
            else:
                st.error(f'Error from API: {response.status_code} - {response.text}')
        except Exception as e:
            st.error(f'An error occurred: {e}')
    else:
        st.warning('Please paste a valid PGN before predicting.')

'''
## Notes
'''
st.markdown('''
- **PGN Format**: Ensure the PGN is valid before submission.
- **Predictions**: The ELOs displayed represent the model’s best estimation based on the game data.
''')
