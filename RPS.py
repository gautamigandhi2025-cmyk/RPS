# rps_app.py
import streamlit as st
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Rock Paper Scissors", page_icon="✊✋✌️")

st.title("✊ Rock — Paper — Scissors — ✌️")

# --- Helper data ---
OPTIONS = ["Rock", "Paper", "Scissors"]
EMOJI = {"Rock": "✊", "Paper": "✋", "Scissors": "✌️"}
WIN_RULES = {
    ("Rock", "Scissors"),
    ("Paper", "Rock"),
    ("Scissors", "Paper"),
}

# --- Session state initialization ---
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "losses" not in st.session_state:
    st.session_state.losses = 0
if "ties" not in st.session_state:
    st.session_state.ties = 0
if "rounds_played" not in st.session_state:
    st.session_state.rounds_played = 0
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# --- Controls ---
col1, col2 = st.columns([2, 1])
with col1:
    user_choice = st.radio("Choose your move:", OPTIONS, index=0, horizontal=True, format_func=lambda x: f"{EMOJI[x]} {x}")
with col2:
    best_of = st.selectbox("Best of:", ["No limit", "1", "3", "5", "7"], index=0)

play = st.button("Play")
reset = st.button("Reset Game", help="Clears scores and history")

# --- Reset logic ---
if reset:
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.ties = 0
    st.session_state.rounds_played = 0
    st.session_state.history = []
    st.session_state.game_over = False
    st.success("Game reset. Have fun!")

# --- Play logic ---
if play and not st.session_state.game_over:
    comp_choice = random.choice(OPTIONS)
    st.session_state.rounds_played += 1

    # Determine result
    if user_choice == comp_choice:
        result = "Tie"
        st.session_state.ties += 1
        st.info(f"Both chose {EMOJI[user_choice]} {user_choice}. It's a tie!")
    elif (user_choice, comp_choice) in WIN_RULES:
        result = "Win"
        st.session_state.wins += 1
        st.success(f"You win! {EMOJI[user_choice]} {user_choice} beats {EMOJI[comp_choice]} {comp_choice}.")
    else:
        result = "Loss"
        st.session_state.losses += 1
        st.error(f"You lose… {EMOJI[comp_choice]} {comp_choice} beats {EMOJI[user_choice]} {user_choice}.")

    # Append to history
    st.session_state.history.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "you": f"{EMOJI[user_choice]} {user_choice}",
        "computer": f"{EMOJI[comp_choice]} {comp_choice}",
        "result": result
    })

    # Check Best-of condition
    if best_of != "No limit":
        target = int(best_of)
        needed = (target // 2) + 1
        if st.session_state.wins >= needed or st.session_state.losses >= needed:
            st.session_state.game_over = True
            if st.session_state.wins > st.session_state.losses:
                st.balloons()
                st.success(f"🏆 You won the Best-of-{best_of} match! (Wins: {st.session_state.wins}, Losses: {st.session_state.losses})")
            else:
                st.warning(f"🙁 You lost the Best-of-{best_of} match. (Wins: {st.session_state.wins}, Losses: {st.session_state.losses})")

# If user tries to play after game over
if st.session_state.game_over and play:
    st.info("The Best-of match is over. Press Reset Game to start a new match.")

# --- Scoreboard & History ---
st.sidebar.header("Scoreboard")
st.sidebar.write(f"Rounds played: {st.session_state.rounds_played}")
st.sidebar.write(f"✅ Wins: {st.session_state.wins}")
st.sidebar.write(f"❌ Losses: {st.session_state.losses}")
st.sidebar.write(f"➖ Ties: {st.session_state.ties}")

if st.session_state.history:
    st.subheader("History")
    df = pd.DataFrame(st.session_state.history[::-1])  # latest first
    st.dataframe(df, use_container_width=True)
else:
    st.subheader("History")
    st.write("No rounds played yet. Click Play to start!")

# --- Small tips ---
st.markdown("---")
st.write("Tips: Try the Best-of modes for short matches. Want features like sound, CPU difficulty, or animated icons? Ask and I’ll add them!")
