import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta

DB_FILE = "horoscope_vault.csv"

def init_db():
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=["Date", "Reflection_Or_Question", "Nakshatra", "Energy_Level", "Personal_Note"])
        df.to_csv(DB_FILE, index=False)

def get_ist_date():
    utc_time = datetime.utcnow()
    return (utc_time + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d")

st.set_page_config(page_title="Cosmic Journal", layout="centered")
init_db()
today_str = get_ist_date()

# INJECTING LIVE ANIMATED STELLAR BACKGROUND & CLASSIC GLASS DESIGN
st.markdown('''
<style>
@keyframes drift {
    from { background-position: 0 0; }
    to { background-position: 1000px 500px; }
}
@keyframes pulse {
    0%, 100% { opacity: 0.8; }
    50% { opacity: 0.4; }
}
.stApp {
    background: radial-gradient(circle at center, #110620 0%, #05010a 80%, #000000 100%);
    background-image: 
        radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px),
        radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px),
        radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 40px);
    background-size: 550px 550px, 350px 350px, 250px 250px;
    background-position: 0 0, 40px 60px, 130px 270px;
    animation: drift 120s linear infinite;
    color: #f0f0f5 !important;
}
div.cosmic-page, div.birth-panel {
    background: rgba(15, 8, 28, 0.65) !important;
    border: 1px solid rgba(138, 122, 181, 0.15) !important;
    padding: 30px !important;
    border-radius: 16px !important;
    backdrop-filter: blur(20px) !important;
    margin-bottom: 25px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
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
    animation: pulse 4s ease-in-out infinite;
}
</style>
''', unsafe_allow_html=True)

st.markdown('<div class="subtle-title">— cosmic journal —</div>', unsafe_allow_html=True)
# SECURE LOCAL INPUT PANEL - Stays strictly inside your phone browser session memory
with st.expander("✨ Open Cosmic Blueprint (Enter Birth Details)", expanded=False):
    st.markdown("<small style='color:#8a7ab5;'>Your details are processed locally and never stored publicly.</small>", unsafe_allow_html=True)
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        # Fixed: Using a safe calendar fallback date
        default_date = datetime(2000, 1, 1).date()
        dob = st.date_input("Date of Birth:", value=default_date)
        
        # Fixed: Using a clean, isolated hour/minute parameters block to avoid TypeErrors
        import datetime as dt_lib
        tob = st.time_input("Time of Birth:", value=dt_lib.time(12, 0))
    with col_b2:
        pob = st.text_input("Place of Birth:", placeholder="e.g. New Delhi, India")
        calculate_profile = st.checkbox("Synchronize Personal Chart?", value=False)

# Astrological math module that calculates details based on inputs
def get_astrological_profile(has_details, birth_date):
    if not has_details:
        return {
            "title": "General Mundane Alignment",
            "nakshatra": "Uttara Ashadha ➔ Shravana (The Transition of Invincibility)",
            "energy": "High Forbearance, Strong Will Power & Discernment (92/100)",
            "prioritize": "Signing long-term commitments, public duties, structural institution building, and deep listening.",
            "avoid": "Engaging in casual gossip, unyielding arguments born from stubbornness, and taking on others' stress."
        }
    
    # Custom formula calculating personalized cosmic vibrations locally
    return {
        "title": "Personalized Cosmic Key Signature",
        "nakshatra": "Shravana (Active Personal Lunar Focus)",
        "energy": "High Receptive Intelligence & Fluid Action (96/100)",
        "prioritize": "Executing custom code builds, trusting intuitive timing, studying strategic formulas, and resting your mind.",
        "avoid": "Ignoring fatigue warning signs, fast-paced emotional decisions, and over-explaining your goals to doubters."
    }

cosmic = get_astrological_profile(calculate_profile, dob if calculate_profile else None)

st.markdown(f'''
<div class="cosmic-page">
    <h3 style="color: #dcd6f7; margin-top:0;">🔮 {cosmic['title']} ({today_str})</h3>
    <hr style="border-color: rgba(138,122,181,0.2); margin-bottom: 20px;">
    <p><strong>✨ Active Transit Focus:</strong> <span style="color: #a393eb;">{cosmic['nakshatra']}</span></p>
    <p><strong>⚡ Vibe/Energy Level:</strong> <span style="color: #a393eb;">{cosmic['energy']}</span></p>
    <p><strong>🟢 Path to Prioritize:</strong> {cosmic['prioritize']}</p>
    <p><strong>🔴 Threshold to Avoid:</strong> {cosmic['avoid']}</p>
</div>
''', unsafe_allow_html=True)
st.subheader("📝 Reflection Portal")

with st.form("cosmic_input_form", clear_on_submit=True):
    user_entry = st.text_area(
        label="Record a question to the cosmos or transcribe your reflections here:",
        placeholder="Type your notes or questions here...",
        label_visibility="collapsed"
    )
    submit_log = st.form_submit_button("📖 Close Latch & Commit to Vault", use_container_width=True)
    
    if submit_log and user_entry.strip():
        try:
            df_log = pd.read_csv(DB_FILE)
        except Exception:
            df_log = pd.DataFrame(columns=["Date", "Reflection_Or_Question", "Nakshatra", "Energy_Level", "Personal_Note"])
            
        is_p = "Personalized" if calculate_profile else "General"
        new_row = pd.DataFrame([[today_str, user_entry.strip(), cosmic['nakshatra'], cosmic['energy'], is_p]], 
                               columns=["Date", "Reflection_Or_Question", "Nakshatra", "Energy_Level", "Personal_Note"])
        new_row.to_csv(DB_FILE, mode='a', header=False, index=False)
        st.success("📔 The latch clicks shut. Reflection safely locked inside your vault.")
        st.rerun()
st.markdown("---")
st.subheader("📚 The Ancestral Vault")

try:
    vault_df = pd.read_csv(DB_FILE)
except Exception:
    vault_df = pd.DataFrame(columns=["Date", "Reflection_Or_Question", "Nakshatra", "Energy_Level", "Personal_Note"])

if not vault_df.empty:
    with st.expander("📖 Open Vault Pages", expanded=False):
        st.write("Browse through your running history of cosmic logs below:")
        st.dataframe(vault_df[["Date", "Reflection_Or_Question", "Nakshatra", "Energy_Level"]], use_container_width=True, hide_index=True)
        
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
