
import streamlit as st
import os
from PIL import Image
from okey_logic import find_combinations, recommend_discard

st.set_page_config(page_title="Okey Karten-Analyse", layout="wide")
st.title("🃏 Okey Kartenhilfe mit Deck-Verlauf (Metin2)")

# Kartenpfad
CARD_FOLDER = "okey_cards"
all_colors = ["r", "y", "b"]
all_values = list(range(1, 9))
all_cards = [f"{v}{c}" for c in all_colors for v in all_values]

# Session-Init
if "hand" not in st.session_state:
    st.session_state.hand = []
if "deck_state" not in st.session_state:
    st.session_state.deck_state = set(all_cards)
if "history" not in st.session_state:
    st.session_state.history = []

# Kartenanzeige
st.subheader("🎴 Kartenauswahl (Verfügbare Karten)")
available_cards = sorted(st.session_state.deck_state)
cols = st.columns(8)
for i, val in enumerate(all_values):
    for color in all_colors:
        key = f"{val}{color}"
        if key not in available_cards:
            continue
        idx = all_values.index(val)
        col = cols[idx]
        with col:
            path = os.path.join(CARD_FOLDER, f"{key}.png")
            if os.path.exists(path):
                if st.button("", key=f"btn_{key}"):
                    if len(st.session_state.hand) < 5 and key not in st.session_state.hand:
                        st.session_state.hand.append(key)
                st.image(path, width=70, caption=key)

# Aktuelle Hand
st.subheader("🖐️ Deine Handkarten")
hand_cols = st.columns(5)
for i in range(5):
    with hand_cols[i]:
        if i < len(st.session_state.hand):
            card = st.session_state.hand[i]
            path = os.path.join(CARD_FOLDER, f"{card}.png")
            st.image(path, width=100)
            if st.button(f"❌ Entfernen {card}", key=f"remove_{i}"):
                st.session_state.hand.pop(i)
                st.experimental_rerun()
        else:
            st.write("🕳️")

# Analyse
if len(st.session_state.hand) == 5:
    st.subheader("🔍 Analyse deiner Hand")
    combos = find_combinations(st.session_state.hand)
    if combos:
        st.success("✅ Du hast eine gültige 3er-Straße!")
        for combo in combos:
            st.write(" + ".join(f"{v}{c}" for v, c in combo))
        if st.button("✔️ Kombination entfernen"):
            for combo in combos:
                for val, col in combo:
                    st.session_state.deck_state.discard(f"{val}{col}")
                    if f"{val}{col}" in st.session_state.hand:
                        st.session_state.hand.remove(f"{val}{col}")
                st.session_state.history.append(f"Kombination entfernt: {' + '.join(f'{v}{c}' for v,c in combo)}")
            st.experimental_rerun()
    else:
        suggestion = recommend_discard(st.session_state.hand, st.session_state.deck_state)
        if suggestion:
            st.warning(f"💡 Vorschlag: Wirf **{suggestion}** ab – kaum Chance auf Straße.")
            if st.button(f"🗑️ {suggestion} abwerfen"):
                st.session_state.deck_state.discard(suggestion)
                st.session_state.hand.remove(suggestion)
                st.session_state.history.append(f"Abgeworfen: {suggestion}")
                st.experimental_rerun()
        else:
            st.info("Keine klare Empfehlung möglich.")
else:
    st.info("Wähle genau 5 Karten, um eine Analyse durchzuführen.")

# Verlauf
st.markdown("---")
st.subheader("📜 Spielverlauf")
for event in st.session_state.history[::-1]:
    st.write(event)

st.markdown("---")
if st.button("🔄 Spiel vollständig zurücksetzen"):
    st.session_state.hand = []
    st.session_state.deck_state = set(all_cards)
    st.session_state.history = []
    st.experimental_rerun()
