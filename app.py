import streamlit as st
import chess
import chess.pgn
import chess.svg
import io
from PIL import Image
import cairosvg
import requests
from io import StringIO

# Initialize all session states
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'pgn_headers' not in st.session_state:
    st.session_state.pgn_headers = {}
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()
if 'moves' not in st.session_state:
    st.session_state.moves = []
if 'current_move_index' not in st.session_state:
    st.session_state.current_move_index = 0
if 'game_loaded' not in st.session_state:
    st.session_state.game_loaded = False

st.set_page_config(layout="wide")

# Common CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;
    }
    .title-container {
        text-align: center;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .title {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.25rem;
    }
    .subtitle {
        color: #b4b4b4;
        font-size: 1rem;
    }
    .stButton > button {
        background-color: #7fa650 !important;
        color: white !important;
        font-size: 1.2rem !important;
        padding: 0.75rem 1.5rem !important;
        width: 100% !important;
    }
    .main .block-container {
        max-width: 1400px;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    .navigation-button > button {
        background-color: #1a1a1a !important;
        color: white !important;
        font-size: 1rem !important;
        padding: 0.5rem !important;
        border: 1px solid #404040 !important;
        border-radius: 4px !important;
        margin: 0 !important;
    }
    .player-card {
        background-color: #262421;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #404040;
        margin-bottom: 1rem;
    }
    .moves-container {
        background-color: #262421;
        padding: 1rem;
        border-radius: 8px;
        font-family: monospace;
        font-size: 0.9rem;
        color: white;
        overflow-wrap: break-word;
        word-wrap: break-word;
        word-break: break-word;
    }
</style>
""", unsafe_allow_html=True)

def main_page():
    st.markdown("""
    <div class="title-container">
        <div class="title">Chess ELO Predictor</div>
        <div class="subtitle">Analyze your game and predict player ratings</div>
    </div>
    """, unsafe_allow_html=True)

    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        pgn_input = st.text_area("""""", height=100, placeholder="Paste your PGN here...")

        if st.button("Analyze Game", use_container_width=True):
            if pgn_input.strip():
                try:
                    # Store PGN in session state
                    st.session_state.pgn_input = pgn_input
                    st.session_state.game_loaded = False  # Reset game loaded state
                    # Switch to analysis page
                    st.session_state.page = 'analysis'
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

def analysis_page():
    st.markdown("""
    <div class="title-container">
        <div class="title">Game Analysis</div>
    </div>
    """, unsafe_allow_html=True)

    # Add New Analysis button at the top
    if st.button("New Analysis", key="new_analysis"):
        st.session_state.game_loaded = False
        st.session_state.page = 'main'
        st.rerun()

    # Only load the game once when entering the analysis page
    if not st.session_state.game_loaded:
        url = 'https://chess-elo-556540502853.europe-west1.run.app/predict'
        params = dict(X=st.session_state.pgn_input)
        r = requests.get(url, params=params)

        try:
            pgn = io.StringIO(st.session_state.pgn_input)
            game = chess.pgn.read_game(pgn)
            if game:
                st.session_state.pgn_headers = dict(game.headers)
                st.session_state.moves = list(game.mainline_moves())
                st.session_state.board = game.board()
                st.session_state.current_move_index = 0

                svg_board = chess.svg.board(st.session_state.board, size=400, coordinates=True,
                                          colors={'square light': '#f0d9b5', 'square dark': '#b58863'})
                png_data = cairosvg.svg2png(bytestring=svg_board)
                st.session_state.board_image = Image.open(io.BytesIO(png_data))

                st.session_state.white_elo = r.json()["white"]
                st.session_state.black_elo = r.json()["black"]

                st.session_state.game_loaded = True

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.session_state.page = 'main'
            st.rerun()

    # Display the analysis if game is loaded
    if st.session_state.game_loaded:
        col1, col2 = st.columns([3, 2])

        with col1:
            if hasattr(st.session_state, 'board_image'):
                st.image(st.session_state.board_image,width=700)

                # Custom CSS for the smaller buttons
                st.markdown("""
                <style>
                .main .block-container {
                    padding-top: 0 !important;
                    padding-bottom: 0 !important;
                    margin-top: 0 !important;
                }

                /* Remove extra padding from header */
                header {
                    padding: 0 !important;
                    margin: 0 !important;
                }

                /* Minimize button container spacing */
                .stButton {
                    margin: 0 !important;
                    padding: 0 !important;
                }

                /* Custom button styles with minimal spacing */
                .small-button > button {
                    background-color: #1a1a1a !important;
                    color: white !important;
                    font-size: 24px !important;
                    padding: 20px 20px !important;
                    width: 100% !important;
                    border: 1px solid #404040 !important;
                    border-radius: 8px !important;
                    margin: 0 !important;
                }

                .big-button > button {
                    background-color: #7fa650 !important;
                    color: white !important;
                    font-size: 24px !important;
                    padding: 20px 40px !important;
                    width: 150% !important;
                    margin: 0 !important;
                }

                /* Remove any gap at the top of the app */
                .stApp {
                    margin-top: 0 !important;
                }

                /* Minimize padding in the main content area */
                .element-container {
                    margin: 0 !important;
                    padding: 0 !important;
                }
                </style>
                """, unsafe_allow_html=True)
                # Create 4 columns for all buttons
                btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1, 2, 2, 1])


                with btn_col1:
                    if st.button("⟲ start", key="start", help="Go to start of game", use_container_width=True):
                        st.session_state.current_move_index = 0
                        st.session_state.board = chess.Board()
                        svg_board = chess.svg.board(st.session_state.board, size=300, coordinates=True,
                                                colors={'square light': '#f0d9b5', 'square dark': '#b58863'})
                        png_data = cairosvg.svg2png(bytestring=svg_board)
                        st.session_state.board_image = Image.open(io.BytesIO(png_data))
                        st.rerun()

                with btn_col2:
                    if st.button("← Previous", use_container_width=True):
                        if st.session_state.current_move_index > 0:
                            st.session_state.current_move_index -= 1
                            st.session_state.board.pop()
                            svg_board = chess.svg.board(st.session_state.board, size=300, coordinates=True,
                                                    colors={'square light': '#f0d9b5', 'square dark': '#b58863'})
                            png_data = cairosvg.svg2png(bytestring=svg_board)
                            st.session_state.board_image = Image.open(io.BytesIO(png_data))
                            st.rerun()

                with btn_col3:
                    if st.button("Next →", use_container_width=True):
                        if st.session_state.current_move_index < len(st.session_state.moves):
                            move = st.session_state.moves[st.session_state.current_move_index]
                            st.session_state.board.push(move)
                            st.session_state.current_move_index += 1
                            svg_board = chess.svg.board(st.session_state.board, size=300, coordinates=True,
                                                    colors={'square light': '#f0d9b5', 'square dark': '#b58863'})
                            png_data = cairosvg.svg2png(bytestring=svg_board)
                            st.session_state.board_image = Image.open(io.BytesIO(png_data))
                            st.rerun()

                with btn_col4:
                    if st.button("End ⟳", key="end", help="Go to end of game", use_container_width=True):
                        while st.session_state.current_move_index < len(st.session_state.moves):
                            move = st.session_state.moves[st.session_state.current_move_index]
                            st.session_state.board.push(move)
                            st.session_state.current_move_index += 1
                        svg_board = chess.svg.board(st.session_state.board, size=300, coordinates=True,
                                                colors={'square light': '#f0d9b5', 'square dark': '#b58863'})
                        png_data = cairosvg.svg2png(bytestring=svg_board)
                        st.session_state.board_image = Image.open(io.BytesIO(png_data))
                        st.rerun()

        with col2:
            # Player cards with improved layout
            st.markdown(f"""
            <div class="player-card">
                <h3 style="color: white; margin-bottom: 0.5rem;">♚ Black Player</h3>
                <div style="font-size: 1.5rem; font-weight: bold; color: #ffd700;">{st.session_state.black_elo}</div>
                <div style="font-size: 1rem; color: #888888; margin-top: 0.5rem;">{st.session_state.pgn_headers.get('Black', 'Unknown')}</div>
            </div>
            <div class="player-card">
                <h3 style="color: white; margin-bottom: 0.5rem;">♔ White Player</h3>
                <div style="font-size: 1.5rem; font-weight: bold; color: #ffd700;">{st.session_state.white_elo}</div>
                <div style="font-size: 1rem; color: #888888; margin-top: 0.5rem;">{st.session_state.pgn_headers.get('White', 'Unknown')}</div>
            </div>
            """, unsafe_allow_html=True)

            # Moves display with improved formatting
            moves_text = ""
            temp_board = chess.Board()
            for i, move in enumerate(st.session_state.moves):
                move_number = (i // 2) + 1
                if i % 2 == 0:
                    current_move = f"{move_number}. {temp_board.san(move)}"
                else:
                    current_move = f" {temp_board.san(move)} "
                temp_board.push(move)

                if i == st.session_state.current_move_index - 2:
                    moves_text += f'<span style="background-color: #ffd700;">{current_move}</span>'
                else:
                    moves_text += current_move

            st.markdown(f"""
            <div class="moves-container">
                <h3 style="color: #ffd700; margin-bottom: 0.75rem;">Game Moves</h3>
                <div style="line-height: 1.5;">{moves_text}</div>
            </div>
            <div class="moves-container" style="margin-top: 0.75rem; text-align: center;">
                {st.session_state.pgn_headers.get('Termination', '')}
            </div>
            """, unsafe_allow_html=True)

# Page routing
if st.session_state.page == 'main':
    main_page()
elif st.session_state.page == 'analysis':
    analysis_page()
