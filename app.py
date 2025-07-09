
import streamlit as st
import os
from PIL import Image
from okey_logic import find_combinations, recommend_discard

st.set_page_config(page_title="Okey Karten-Analyse", layout="wide")
st.title("🃏 Visuelle Okey-Kartenhilfe (Metin2)")

# Kartenpfad
CARD_FOLDER = "okey_cards"
all_colors = ["r", "y", "b"]
all_values = list(range(1, 9))
deck = [f"{v}{c}" for c in all_colors for v in all_values]

# Session-Init
if "hand" not in st.session_state:
    st.session_state.hand = []

# Kartenanzeige
st.subheader("🎴 Kartenauswahl")
cols = st.columns(8)
for i, val in enumerate(all_values):
    for color in all_colors:
        key = f"{val}{color}"
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

# Zurücksetzen
if st.button("🔄 Hand zurücksetzen"):
    st.session_state.hand = []
    st.experimental_rerun()

# Analyse
if len(st.session_state.hand) == 5:
    st.subheader("🔍 Analyse deiner Hand")
    combos = find_combinations(st.session_state.hand)
    if combos:
        st.success("✅ Du hast eine gültige 3er-Straße!")
        for combo in combos:
            st.write(" + ".join(f"{v}{c}" for v, c in combo))
    else:
        suggestion = recommend_discard(st.session_state.hand)
        if suggestion:
            st.warning(f"💡 Vorschlag: Wirf **{suggestion}** ab, da es am wenigsten zu Kombinationen führt.")
        else:
            st.info("Keine klare Empfehlung möglich.")
else:
    st.info("Wähle genau 5 Karten, um eine Analyse durchzuführen.")
