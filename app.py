import streamlit as st
import chess
import chess.pgn
import chess.svg
import io
from PIL import Image
import cairosvg
import requests
from io import StringIO

st.set_page_config(layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;
    }

    .title-container {
        text-align: center;
        padding: 2rem;
        margin-bottom: 2rem;
    }

    .title {
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        color: #b4b4b4;
        font-size: 1.2rem;
    }

    .stButton > button {
        background-color: #7fa650 !important;
        color: white !important;
        font-size: 24px !important;
        padding: 20px 40px !important;
        width: 100% !important;
    }
</style>

<div class="title-container">
    <div class="title">Chess ELO Predictor</div>
    <div class="subtitle">Analyze your game and predict player ratings</div>
</div>
""", unsafe_allow_html=True)

# URL de l'API
url = 'https://chess-elo-556540502853.europe-west1.run.app/predict'



# URL de l'API
url = 'https://chess-elo-556540502853.europe-west1.run.app/predict'

if 'pgn_headers' not in st.session_state: # ---> for username
    st.session_state.pgn_headers = {}

if 'board' not in st.session_state:
    st.session_state.board = chess.Board()
if 'moves' not in st.session_state:
    st.session_state.moves = []
if 'current_move_index' not in st.session_state:
    st.session_state.current_move_index = 0
if 'game_loaded' not in st.session_state:
    st.session_state.game_loaded = False

_, center_col, _ = st.columns([1, 2, 1])
with center_col:
    pgn_input = st.text_area("""""", height=100, placeholder="Paste your PGN here...")
    params= dict(X=pgn_input)
    r = requests.get(url, params=params)

    if st.button("Analyze Game", use_container_width=True):
        if pgn_input.strip():
            try:
                pgn = io.StringIO(pgn_input)
                game = chess.pgn.read_game(pgn)
                if game:
                    st.session_state.pgn_headers = dict(game.headers)  # Add this line ---> for username
                    st.session_state.moves = list(game.mainline_moves())
                    st.session_state.board = game.board()
                    st.session_state.current_move_index = 0
                    st.session_state.game_loaded = True

                    svg_board = chess.svg.board(st.session_state.board, size=600, coordinates=True, colors={'square light': '#f0d9b5', 'square dark': '#b58863'})
                    png_data = cairosvg.svg2png(bytestring=svg_board)
                    st.session_state.board_image = Image.open(io.BytesIO(png_data))


                    st.session_state.white_elo =r.json()["white"]
                    st.session_state.black_elo =r.json()["black"]
            except Exception as e:
                st.error(f"Error: {str(e)}")


if st.session_state.game_loaded:
    col1, col2 = st.columns([2, 1])  # Tighter ratio

    with col1:
        if hasattr(st.session_state, 'board_image'):
            st.image(st.session_state.board_image, width=900)

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("← Previous"):
                    if st.session_state.current_move_index > 0:
                        st.session_state.current_move_index -= 1
                        st.session_state.board.pop()
                        svg_board = chess.svg.board(st.session_state.board, size=1000, coordinates=True, colors={'square light': '#f0d9b5', 'square dark': '#b58863'})
                        png_data = cairosvg.svg2png(bytestring=svg_board)
                        st.session_state.board_image = Image.open(io.BytesIO(png_data))
                        st.rerun()

            with btn_col2:
                if st.button("Next →"):
                    if st.session_state.current_move_index < len(st.session_state.moves):
                        move = st.session_state.moves[st.session_state.current_move_index]
                        st.session_state.board.push(move)
                        st.session_state.current_move_index += 1
                        svg_board = chess.svg.board(st.session_state.board, size=600, coordinates=True, colors={'square light': '#f0d9b5', 'square dark': '#b58863'})
                        png_data = cairosvg.svg2png(bytestring=svg_board)
                        st.session_state.board_image = Image.open(io.BytesIO(png_data))
                        st.rerun()


    with col2:
        st.markdown(f"""
        <div style="margin-left: -180px; background-color: #262421; padding: 20px; border-radius: 8px; border: 1px solid #404040; margin-bottom: 20px;">
            <h3>♔ White Player</h3>
            <div style="font-size: 32px; font-weight: bold; color: #ffd700;">{st.session_state.white_elo}</div>
            <div style="font-size: 24px; color: #888888; margin-top: 10px;">{st.session_state.pgn_headers.get('White', 'Unknown')}</div>
        </div>
        <div style="margin-left: -180px; background-color: #262421; padding: 20px; border-radius: 8px; border: 1px solid #404040;">
            <h3>♚ Black Player</h3>
            <div style="font-size: 32px; font-weight: bold; color: #ffd700;">{st.session_state.black_elo}</div>
            <div style="font-size: 24px; color: #888888; margin-top: 10px;">{st.session_state.pgn_headers.get('Black', 'Unknown')}</div>
        </div>
        """, unsafe_allow_html=True)

        moves_text = ""
        temp_board = chess.Board()
        for i, move in enumerate(st.session_state.moves):
            move_number = (i // 2) + 1
            if i % 2 == 0:
                current_move = f"{move_number}. {temp_board.san(move)}"
            else:
                current_move = f" {temp_board.san(move)} "
            temp_board.push(move)

            if i == st.session_state.current_move_index - 1:
                moves_text += f'<span style="background-color: #ffd700;">{current_move}</span>'
            else:
                moves_text += current_move

        st.markdown(f"""
        <div style="margin-left: -180px; background-color: #262421; padding: 20px; border-radius: 16px; margin-top: 115px; font-family: monospace; font-size: 20px; color: white; width: 130%;">
            <h3 style="color: #ffd700; margin-bottom: 15px;">Game Moves</h3>
            {moves_text}
        </div>
        """, unsafe_allow_html=True)
