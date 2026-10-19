import streamlit as st
import pandas as pd
import json
import os
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

# ADVANCED LAYERED DRY-CSS STELLAR ANIMATION ENGINE
st.markdown('''
<style>
@keyframes starDrift {
    from { background-position: 0 0, 0 0, 0 0; }
    to { background-position: 1000px 500px, 400px 800px, 300px 600px; }
}
.stApp {
    background: radial-gradient(circle at center, #0f051d 0%, #05010a 75%, #000000 100%);
    background-image: 
        radial-gradient(rgba(255, 255, 255, 0.25) 1.5px, transparent 40px),
        radial-gradient(rgba(255, 255, 255, 0.15) 1px, transparent 30px),
        radial-gradient(rgba(163, 147, 235, 0.1) 2px, transparent 50px);
    background-size: 400px 400px, 250px 250px, 600px 600px;
    animation: starDrift 160s linear infinite;
    color: #f0f0f5 !important;
}
div.cosmic-page {
    background: rgba(12, 6, 24, 0.75) !important;
    border: 1px solid rgba(138, 122, 181, 0.15) !important;
    padding: 32px !important;
    border-radius: 16px !important;
    backdrop-filter: blur(25px) !important;
    margin-bottom: 30px !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5) !important;
}
h1, h2, h3, p, label, textarea {
    font-family: 'Courier New', Courier, monospace !important;
}
.subtle-title {
    font-size: 13px !important;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: #8a7ab5;
    text-align: center;
    margin-top: 15px;
    margin-bottom: 35px;
    opacity: 0.8;
}
</style>
''', unsafe_allow_html=True)

st.markdown('<div class="subtle-title">— cosmic journal —</div>', unsafe_allow_html=True)
# AUTOMATED CALENDAR MATRIX - Maps daily values instantly without checking user configuration toggles
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
        "prioritize": "Quiet personal reviews, clearing workspace clutter, and steady, consistent daily learning.",
        "avoid": "Hasty choices, letting sudden distractions interrupt your focus, or overthinking your long-term roadmap."
    })

cosmic = get_automated_daily_alignment(today_str)

st.markdown(f'''
<div class="cosmic-page">
    <h3 style="color: #dcd6f7; margin-top:0; font-size:18px;">✨ Daily Cosmic Alignment ({today_str})</h3>
    <hr style="border-color: rgba(138,122,181,0.15); margin-bottom: 22px;">
    <p style="font-size:15px; line-height:1.6;"><strong>🔮 Influenced Nakshatra:</strong> <br><span style="color: #a393eb;">{cosmic['nakshatra']}</span></p>
    <p style="font-size:15px; line-height:1.6;"><strong>⚡ Energy of the Day:</strong> <br><span style="color: #a393eb;">{cosmic['energy']}</span></p>
    <p style="font-size:15px; line-height:1.6; margin-top:18px;"><strong>🟢 What to Do:</strong> <br>{cosmic['prioritize']}</p>
    <p style="font-size:15px; line-height:1.6; margin-top:18px;"><strong>🔴 What to Avoid:</strong> <br>{cosmic['avoid']}</p>
</div>
''', unsafe_allow_html=True)
st.markdown("<p style='font-size:14px; margin-bottom:8px; color:#8a7ab5;'>📝 Reflection Portal</p>", unsafe_allow_html=True)

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
st.markdown("<br><hr style='border-color: rgba(138,122,181,0.1);'>", unsafe_allow_html=True)
st.markdown("<p style='font-size:14px; margin-bottom:8px; color:#8a7ab5;'>📚 The Personal Vault</p>", unsafe_allow_html=True)

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
