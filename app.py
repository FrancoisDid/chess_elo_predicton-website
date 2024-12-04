import streamlit as st
import chess
import chess.pgn
import chess.svg
import io
from PIL import Image
import cairosvg

# # Enhanced CSS Styling
# st.markdown(
#     """
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

#     body {
#         font-family: 'Inter', sans-serif;
#         background-color: #161512;
#     }

#     .stApp {
#         background-color: #161512;
#         max-width: 1400px;
#         margin: auto;
#         padding: 40px;
#     }

#     /* Chessboard background with chess.com style squares */
#     .chess-background {
#         position: fixed;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         background-color: #161512;
#         background-image:
#             linear-gradient(45deg, #769656 25%, transparent 25%),
#             linear-gradient(-45deg, #769656 25%, transparent 25%),
#             linear-gradient(45deg, transparent 75%, #769656 75%),
#             linear-gradient(-45deg, transparent 75%, #769656 75%);
#         background-size: 80px 80px;
#         background-position: 0 0, 0 0, 40px 40px, 40px 40px;
#         z-index: -1;
#         opacity: 0.1;
#     }

#     .title {
#         font-size: 4rem;
#         font-weight: 700;
#         color: #f0f0f0;
#         text-align: center;
#         margin-bottom: 30px;
#         text-shadow: 0 4px 6px rgba(0,0,0,0.3);
#     }

#     .subtitle {
#         font-size: 1.5rem;
#         color: #aaaaaa;
#         text-align: center;
#         margin-bottom: 40px;
#     }

#     .elo-wrapper {
#         display: flex;
#         justify-content: center;
#         align-items: center;
#         gap: 30px;
#         margin: 30px 0;
#     }

#     .elo-container {
#         display: flex;
#         background-color: #302e2b;
#         border-radius: 15px;
#         overflow: hidden;
#         box-shadow: 0 10px 20px rgba(0,0,0,0.3);
#         width: 800px;
#         max-width: 90%;
#     }

#     .elo-side {
#         flex: 1;
#         padding: 25px;
#         text-align: center;
#         position: relative;
#         transition: all 0.3s ease;
#     }

#     .elo-side.white {
#         background-color: #f0d9b5;
#         color: #202020;
#     }

#     .elo-side.black {
#         background-color: #b58863;
#         color: #ffffff;
#     }

#     .elo-label {
#         font-size: 1.2rem;
#         margin-bottom: 10px;
#         text-transform: uppercase;
#         letter-spacing: 2px;
#         opacity: 0.7;
#     }

#     .elo-value {
#         font-size: 3rem;
#         font-weight: 700;
#     }

#     .elo-side:hover {
#         transform: scale(1.05);
#         z-index: 10;
#     }

#     .stButton>button {
#         background-color: #769656;
#         color: white;
#         border: none;
#         border-radius: 10px;
#         padding: 15px 30px;
#         font-size: 1.2rem;
#         transition: all 0.3s ease;
#         width: 100%;
#         margin-top: 20px;
#     }

#     .stButton>button:hover {
#         background-color: #5f7e4e;
#         transform: translateY(-3px);
#         box-shadow: 0 6px 12px rgba(0,0,0,0.3);
#     }

#     .stTextArea>div>div>textarea {
#         background-color: #302e2b;
#         color: #ffffff;
#         border: 2px solid #4a4a4a;
#         font-size: 1rem;
#         height: 200px !important;
#     }

#     .chessboard-container {
#         display: flex;
#         justify-content: center;
#         align-items: center;
#         margin-top: 40px;
#     }

#     .chessboard-container img {
#         max-width: 800px;
#         width: 100%;
#         height: auto;
#         border-radius: 15px;
#         box-shadow: 0 15px 30px rgba(0,0,0,0.5);
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Add chessboard background
# st.markdown('<div class="chess-background"></div>', unsafe_allow_html=True)

# # Title and Subtitle
# st.markdown('<div class="title">Chess ELO Predictor</div>', unsafe_allow_html=True)
# st.markdown('<div class="subtitle">Analyze your chess game and predict ELO ratings</div>', unsafe_allow_html=True)

# # Initialize session state
# if 'current_move_index' not in st.session_state:
#     st.session_state.current_move_index = 0
# if 'moves' not in st.session_state:
#     st.session_state.moves = []
# if 'board' not in st.session_state:
#     st.session_state.board = chess.Board()
# if 'elo_white' not in st.session_state:
#     st.session_state.elo_white = 1200  # Default ELO
# if 'elo_black' not in st.session_state:
#     st.session_state.elo_black = 1300  # Default ELO
# if 'game_loaded' not in st.session_state:
#     st.session_state.game_loaded = False
# if 'board_image' not in st.session_state:
#     st.session_state.board_image = None

# # PGN Input
# st.markdown("### Add Your Chess Game PGN")
# pgn_input = st.text_area("Paste your PGN of the chess game below:", height=200)

# # Load PGN Button
# if st.button("Load PGN and Predict ELO"):
#     if pgn_input.strip():
#         try:
#             # Process PGN
#             pgn = io.StringIO(pgn_input)
#             game = chess.pgn.read_game(pgn)

#             if game:
#                 st.session_state.moves = list(game.mainline_moves())
#                 st.session_state.current_move_index = 0
#                 st.session_state.board = game.board()
#                 st.session_state.elo_white = 1200  # Placeholder value
#                 st.session_state.elo_black = 1300  # Placeholder value
#                 st.session_state.game_loaded = True

#                 # Generate initial board image
#                 svg_board = chess.svg.board(st.session_state.board)
#                 png_data = cairosvg.svg2png(bytestring=svg_board)
#                 st.session_state.board_image = Image.open(io.BytesIO(png_data))

#                 st.success("PGN loaded successfully!")
#             else:
#                 st.error("Invalid PGN. Please check your input.")
#         except Exception as e:
#             st.error(f"An error occurred while processing the PGN: {e}")
#     else:
#         st.warning("Please paste a valid PGN.")

# # Display ELO predictions in a chess.com-inspired layout
# if st.session_state.game_loaded:
#     st.markdown('<div class="elo-wrapper">', unsafe_allow_html=True)
#     st.markdown(f'''
#     <div class="elo-container">
#         <div class="elo-side white">
#             <div class="elo-label">White Player</div>
#             <div class="elo-value">{st.session_state.elo_white}</div>
#         </div>
#         <div class="elo-side black">
#             <div class="elo-label">Black Player</div>
#             <div class="elo-value">{st.session_state.elo_black}</div>
#         </div>
#     </div>
#     ''', unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

# # Chessboard Navigation and Display
# if st.session_state.game_loaded:
#     st.markdown("## Game Visualization")
#     cols = st.columns([1, 1, 1])
#     with cols[0]:
#         if st.button("⬅️ Previous Move"):
#             if st.session_state.current_move_index > 0:
#                 st.session_state.current_move_index -= 1
#                 st.session_state.board.pop()

#                 # Update board image
#                 svg_board = chess.svg.board(st.session_state.board)
#                 png_data = cairosvg.svg2png(bytestring=svg_board)
#                 st.session_state.board_image = Image.open(io.BytesIO(png_data))
#             else:
#                 st.warning("You are already at the start of the game.")
#     with cols[2]:
#         if st.button("➡️ Next Move"):
#             if st.session_state.current_move_index < len(st.session_state.moves):
#                 move = st.session_state.moves[st.session_state.current_move_index]
#                 st.session_state.board.push(move)
#                 st.session_state.current_move_index += 1

#                 # Update board image
#                 svg_board = chess.svg.board(st.session_state.board)
#                 png_data = cairosvg.svg2png(bytestring=svg_board)
#                 st.session_state.board_image = Image.open(io.BytesIO(png_data))
#             else:
#                 st.warning("You have reached the end of the game.")

#     # Render the chessboard in the center
#     if st.session_state.board_image:
#         st.markdown('<div class="chessboard-container">', unsafe_allow_html=True)
#         st.image(st.session_state.board_image, use_column_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import chess
import chess.pgn
import chess.svg
import io
from PIL import Image
import cairosvg

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
    pgn_input = st.text_area("", height=100, placeholder="Paste your PGN here...")
    if st.button("Analyze Game", use_container_width=True):
        if pgn_input.strip():
            try:
                pgn = io.StringIO(pgn_input)
                game = chess.pgn.read_game(pgn)
                if game:
                    st.session_state.moves = list(game.mainline_moves())
                    st.session_state.board = game.board()
                    st.session_state.current_move_index = 0
                    st.session_state.game_loaded = True

                    svg_board = chess.svg.board(st.session_state.board, size=600, coordinates=True, colors={'square light': '#f0d9b5', 'square dark': '#b58863'})
                    png_data = cairosvg.svg2png(bytestring=svg_board)
                    st.session_state.board_image = Image.open(io.BytesIO(png_data))

                    import random
                    st.session_state.white_elo = random.randint(800, 2200)
                    st.session_state.black_elo = random.randint(800, 2200)
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
            </div>
            <div style="margin-left: -180px; background-color: #262421; padding: 20px; border-radius: 8px; border: 1px solid #404040;">
                <h3>♚ Black Player</h3>
                <div style="font-size: 32px; font-weight: bold; color: #ffd700;">{st.session_state.black_elo}</div>
            </div>
        """, unsafe_allow_html=True)
