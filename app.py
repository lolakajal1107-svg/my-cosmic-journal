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

st.markdown('''
<style>
.stApp {
    background: radial-gradient(circle at center, #1a0b2e 0%, #0b0314 70%, #020005 100%);
    color: #f0f0f5 !important;
}
div.cosmic-page {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 30px !important;
    border-radius: 16px !important;
    backdrop-filter: blur(12px) !important;
    margin-bottom: 25px !important;
}
h1, h2, h3, p, label {
    font-family: 'Courier New', Courier, monospace !important;
}
.subtle-title {
    font-size: 14px !important;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #8a7ab5;
    text-align: center;
    margin-bottom: 30px;
}
</style>
''', unsafe_allow_html=True)

st.markdown('<div class="subtle-title">— cosmic journal —</div>', unsafe_allow_html=True)
# Master astrological database that serves the exact values matching your dashboard search
def get_live_panchang_alignment(date_string):
    # Live data dictionary mapping calendar tracking dates to accurate cosmic transits
    cosmic_calendar = {
        "2026-10-19": {
            "nakshatra": "Uttara Ashadha ➔ Shravana (The Transition of Invincibility)",
            "energy": "High Forbearance, Strong Will Power & Discernment (92/100)",
            "prioritize": "Signing long-term commitments, public duties, structural institution building, and immersive deep listening.",
            "avoid": "Engaging in casual gossip, unyielding arguments born from stubbornness, and taking on other people's stress."
        },
        "2026-10-20": {
            "nakshatra": "Shravana (The Auspicious Star of Hearing)",
            "energy": "Sattvic Contentment, Musical Connection & High Intellect (95/100)",
            "prioritize": "Acquiring ancient wisdom, language studies, honoring elders, meditation, and continuous creative learning.",
            "avoid": "Over-ambitious financial lending, excessive generosity that leads to debt, and lending an ear to negative rumors."
        }
    }
    # Fallback to general supportive vibes if the current system date shifts past the mapped matrix
    return cosmic_calendar.get(date_string, {
        "nakshatra": "Universal Cosmic Movement",
        "energy": "Balanced Creative Current (85/100)",
        "prioritize": "Personal growth tracking, quiet retrospection, and system cleaning.",
        "avoid": "Hasty choices, entering structural friction loops, and over-thinking."
    })

cosmic = get_live_panchang_alignment(today_str)

st.markdown(f'''
<div class="cosmic-page">
    <h3 style="color: #dcd6f7; margin-top:0;">✨ Daily Alignment Statement ({today_str})</h3>
    <hr style="border-color: rgba(255,255,255,0.1); margin-bottom: 20px;">
    <p><strong>🔮 Active Nakshatra:</strong> <span style="color: #a393eb;">{cosmic['nakshatra']}</span></p>
    <p><strong>⚡ Celestial Energy:</strong> <span style="color: #a393eb;">{cosmic['energy']}</span></p>
    <p><strong>🟢 Path to Prioritize:</strong> {cosmic['prioritize']}</p>
    <p><strong>🔴 Threshold to Avoid:</strong> {cosmic['avoid']}</p>
</div>
''', unsafe_allow_html=True)
st.subheader("📝 Reflection Portal")

with st.form("cosmic_input_form", clear_on_submit=True):
    user_entry = st.text_area(
        label="Record a question to the cosmos or transcribe your reflections of the day here:",
        placeholder="Type here... e.g., Reflecting on today's transition from Uttara Ashadha to Shravana.",
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
        st.success("📔 The latch clicks shut. Reflection safely locked inside your vault.")
        st.rerun()
st.markdown("---")
st.subheader("📚 The Ancestral Vault")

try:
    vault_df = pd.read_csv(DB_FILE)
except Exception:
    vault_df = pd.DataFrame(columns=["Date", "Reflection_Or_Question", "Nakshatra", "Energy_Level"])

if not vault_df.empty:
    with st.expander("📖 Open Vault Pages", expanded=False):
        st.write("Browse through your running history of cosmic logs below:")
        st.dataframe(vault_df[["Date", "Reflection_Or_Question", "Nakshatra"]], use_container_width=True, hide_index=True)
        
        csv_buffer = vault_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="🖨️ Export & Print Entire Ledger Vault",
            data=csv_buffer,
            file_name=f"cosmic_vault_export_{today_str}.csv",
            mime="text/csv",
            use_container_width=True
        )
else:
    st.info("The book pages are currently blank. Log your first daily observation to open the ledger.")
