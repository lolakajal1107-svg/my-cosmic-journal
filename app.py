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

# FORCING THE IMMERSIVE DARK THEME AND SLOW-DRIFTING STARDUST FIELD
st.markdown('''
<style>
.stApp {
    background-color: #05010a !important;
}
iframe {
    background-color: transparent !important;
}
div.cosmic-page {
    background: rgba(22, 13, 44, 0.75) !important;
    border: 1px solid rgba(138, 122, 181, 0.25) !important;
    padding: 30px !important;
    border-radius: 16px !important;
    backdrop-filter: blur(20px) !important;
    margin-bottom: 25px !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6) !important;
}
h1, h2, h3, p, label, textarea {
    font-family: 'Courier New', Courier, monospace !important;
    color: #f0f0f5 !important;
}
.subtle-title {
    font-size: 14px !important;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: #a393eb;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 30px;
    font-family: 'Courier New', Courier, monospace !important;
}
</style>
''', unsafe_allow_html=True)

# Embedded canvas frame to force stars to flicker over a true pitch-black galaxy background
cosmic_bg_html = """
<div id="stars-container" style="position:fixed; top:0; left:0; width:100vw; height:100vh; background:radial-gradient(circle at center, #0e051a 0%, #030006 100%); z-index:-1; overflow:hidden;">
  <div class="stars" style="position:absolute; width:200%; height:200%; background-image: radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px), radial-gradient(rgba(163,147,235,0.4) 1.5px, transparent 30px); background-size: 300px 300px, 200px 200px; animation: moveStars 140s linear infinite;"></div>
</div>
<style>
@keyframes moveStars {
  from { transform: translate(0, 0); }
  to { transform: translate(-500px, -500px); }
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

st.markdown(f'''
<div class="cosmic-page">
    <h3 style="color: #dcd6f7; margin-top:0; font-size:18px;">✨ Daily Cosmic Alignment ({today_str})</h3>
    <hr style="border-color: rgba(138,122,181,0.2); margin-bottom: 22px;">
    <p style="font-size:15px; line-height:1.6;"><strong>🔮 Influenced Nakshatra:</strong> <br><span style="color: #a393eb;">{cosmic['nakshatra']}</span></p>
    <p style="font-size:15px; line-height:1.6; margin-top:14px;"><strong>⚡ Energy of the Day:</strong> <br><span style="color: #a393eb;">{cosmic['energy']}</span></p>
    <p style="font-size:15px; line-height:1.6; margin-top:18px;"><strong>🟢 What to Do:</strong> <br>{cosmic['prioritize']}</p>
    <p style="font-size:15px; line-height:1.6; margin-top:18px;"><strong>🔴 What to Avoid:</strong> <br>{cosmic['avoid']}</p>
</div>
''', unsafe_allow_html=True)
st.markdown("<p style='font-size:14px; margin-bottom:8px; color:#a393eb; font-family:monospace;'>📝 Reflection Portal</p>", unsafe_allow_html=True)

with st.form("cosmic_input_form", clear_on_submit=True):
    user_entry = st.text_area(
        label="Portal Input Space",
        placeholder="Say or write about your day, or ask a question to the cosmos here...",
        label_visibility="collapsed"
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
st.markdown("<br><hr style='border-color: rgba(138,122,181,0.15);'>", unsafe_allow_html=True)
st.markdown("<p style='font-size:14px; margin-bottom:8px; color:#a393eb; font-family:monospace;'>📚 The Personal Vault</p>", unsafe_allow_html=True)

try:
    vault_df = pd.read_csv(DB_FILE)
except Exception:
    vault_df = pd.DataFrame(columns=["Date", "Reflection_Or_Question", "Nakshatra", "Energy_Level"])

if not vault_df.empty:
    with st.expander("📖 Open Book Ledger Pages", expanded=False):
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
    st.info("Your historical pages are currently blank.")
