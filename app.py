import streamlit as st
import pandas as pd
import json
import os
import streamlit.components.v1 as components
from datetime import datetime, timedelta

DB_FILE = "horoscope_vault.csv"

def init_db():
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=["Date", "Reflection_Or_Question", "Nakshatra", "Energy_Level"])
        df.to_csv(DB_FILE, index=False)

def get_ist_date():
    utc_time = datetime.utcnow()
    return (utc_time + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d")

st.set_page_config(page_title="Cosmic Journal", layout="centered")
init_db()
today_str = get_ist_date()

# FORCING COMPACT GLASSMETRIC FRAMES TO KEEP ITEMS WITHIN MOBILE SCREEN HEIGHT
st.markdown('''
<style>
.stApp {
    background-color: #030006 !important;
}
iframe {
    background-color: transparent !important;
}
/* Streamlined card with tighter paddings */
div.cosmic-page {
    background: rgba(22, 13, 44, 0.70) !important;
    border: 1px solid rgba(138, 122, 181, 0.20) !important;
    padding: 20px 24px !important;
    border-radius: 14px !important;
    backdrop-filter: blur(20px) !important;
    margin-bottom: 12px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5) !important;
}
h1, h2, h3, p, label, textarea, div {
    font-family: 'Courier New', Courier, monospace !important;
}
.subtle-title {
    font-size: 13px !important;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: #a393eb;
    text-align: center;
    margin-top: 5px;
    margin-bottom: 15px;
}
/* Make text input sections tighter */
.stTextArea div[data-baseweb="textarea"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(138, 122, 181, 0.20) !important;
}
textarea {
    color: #ffffff !important;
}
</style>
''', unsafe_allow_html=True)

# Smooth micro-particle space canvas running perfectly on the server background layer
cosmic_bg_html = """
<div id="stars-container" style="position:fixed; top:0; left:0; width:100vw; height:100vh; background:radial-gradient(circle at center, #0a0314 0%, #020005 100%); z-index:-1; overflow:hidden;">
  <div class="stars" style="position:absolute; width:200%; height:200%; background-image: radial-gradient(white, rgba(255,255,255,.2) 1.5px, transparent 30px), radial-gradient(rgba(163,147,235,0.3) 1px, transparent 20px); background-size: 250px 250px, 180px 180px; animation: moveStars 160s linear infinite;"></div>
</div>
<style>
@keyframes moveStars {
  from { transform: translate(0, 0); }
  to { transform: translate(-400px, -400px); }
}
</style>
"""
components.html(cosmic_bg_html, height=0)

st.markdown('<div class="subtle-title">— cosmic journal —</div>', unsafe_allow_html=True)
def get_automated_daily_alignment(date_string):
    cosmic_matrix = {
        "2026-10-19": {
            "nakshatra": "Uttara Ashadha ➔ Shravana (The Shifting Current of Mastery)",
            "energy": "High Perseverance, Refined Discernment & Mental Focus (92/100)",
            "prioritize": "Executing technical workflows, deep listening, documenting project steps, and grounding your thoughts.",
            "avoid": "Engaging in stubborn arguments, rush-handling design templates, or over-explaining your plans."
        },
        "2026-10-20": {
            "nakshatra": "Shravana (The Lunar Mansion of Sacred Listening)",
            "energy": "High Receptive Intelligence, Clarity & Creative Flow (95/100)",
            "prioritize": "Absorbing new code structures, reflecting on strategic ideas, organizing digital workspaces, and sleeping well.",
            "avoid": "Over-committing your energy blocks, repeating old communication errors, or forcing quick rollouts."
        }
    }
    return cosmic_matrix.get(date_string, {
        "nakshatra": "Universal Lunar Transition",
        "energy": "Stable Grounding Vibration (85/100)",
        "prioritize": "Quiet personal reviews, clearing workspace clutter, and steady daily learning.",
        "avoid": "Hasty choices, letting sudden distractions interrupt your focus, or overthinking your long-term roadmap."
    })

cosmic = get_automated_daily_alignment(today_str)

# Using tighter text margins to maximize visible area
st.markdown(f'''
<div class="cosmic-page">
    <h3 style="color: #dcd6f7; margin-top:0; margin-bottom:12px; font-size:16px;">✨ Cosmic Alignment ({today_str})</h3>
    <p style="font-size:14px; margin-bottom:8px; line-height:1.4;"><strong>🔮 Nakshatra:</strong> <span style="color: #a393eb;">{cosmic['nakshatra']}</span></p>
    <p style="font-size:14px; margin-bottom:10px; line-height:1.4;"><strong>⚡ Energy:</strong> <span style="color: #a393eb;">{cosmic['energy']}</span></p>
    <p style="font-size:14px; margin-bottom:8px; line-height:1.4;"><strong>🟢 What to Do:</strong> {cosmic['prioritize']}</p>
    <p style="font-size:14px; margin-bottom:0; line-height:1.4;"><strong>🔴 What to Avoid:</strong> {cosmic['avoid']}</p>
</div>
''', unsafe_allow_html=True)
st.markdown("<p style='font-size:13px; margin-bottom:4px; margin-top:4px; color:#a393eb; font-weight:bold;'>📝 Reflection Portal</p>", unsafe_allow_html=True)

with st.form("cosmic_input_form", clear_on_submit=True):
    user_entry = st.text_area(
        label="Portal Input Space",
        placeholder="Record your thoughts or questions to the cosmos here...",
        label_visibility="collapsed",
        height=80  # Compact container height for clean mobile layout wrapping
    )
    submit_log = st.form_submit_button("📖 Close Latch & Commit to Vault", use_container_width=True)
    
    if submit_log and user_entry.strip():
        try:
            df_log = pd.read_csv(DB_FILE)
        except Exception:
            df_log = pd.DataFrame(columns=["Date", "Reflection_Or_Question", "Nakshatra", "Energy_Level"])
            
        new_row = pd.DataFrame([[today_str, user_entry.strip(), cosmic['nakshatra'], cosmic['energy']]], 
                               columns=["Date", "Reflection_Or_Question", "Nakshatra", "Energy_Level"])
        new_row.to_csv(DB_FILE, mode='a', header=False, index=False)
        st.success("📔 Safely committed inside your vault.")
        st.rerun()
st.markdown("<hr style='margin:12px 0; border-color: rgba(138,122,181,0.15);'>", unsafe_allow_html=True)

try:
    vault_df = pd.read_csv(DB_FILE)
except Exception:
    vault_df = pd.DataFrame(columns=["Date", "Reflection_Or_Question", "Nakshatra", "Energy_Level"])

if not vault_df.empty:
    with st.expander("📚 Open Book Vault Ledger Pages", expanded=False):
        st.dataframe(vault_df[["Date", "Reflection_Or_Question", "Nakshatra"]], use_container_width=True, hide_index=True)
        
        csv_buffer = vault_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="🖨️ Print / Export Entire Ledger History",
            data=csv_buffer,
            file_name=f"cosmic_journal_vault_{today_str}.csv",
            mime="text/csv",
            use_container_width=True
        )
else:
    st.markdown("<p style='font-size:12px; color:#8a7ab5; text-align:center;'>Your historical pages are currently blank.</p>", unsafe_allow_html=True)
