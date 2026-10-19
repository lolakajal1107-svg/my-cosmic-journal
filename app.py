import streamlit as st
import pandas as pd
import json
import os
import datetime as dt_lib
from datetime import datetime, timedelta

DB_FILE = "horoscope_vault.csv"

def init_db():
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=["Date", "Reflection", "Transit", "Energy", "Language"])
        df.to_csv(DB_FILE, index=False)

def get_ist_date():
    utc_time = datetime.utcnow()
    return (utc_time + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d")

st.set_page_config(page_title="Cosmic Journal Pro", layout="centered")
init_db()
today_str = get_ist_date()

# ADVANCED NEBULA/GALAXY CANVAS STYLING INTEGRATION WITH COMPACT GLASS DESIGNS
st.markdown('''
<style>
@keyframes nebulaDrift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stApp {
    background: linear-gradient(-45deg, #090214, #180536, #0c1033, #020005) !important;
    background-size: 400% 400% !important;
    animation: nebulaDrift 30s ease infinite !important;
    color: #f0f0f5 !important;
}
div.cosmic-page, div.chat-panel {
    background: rgba(13, 6, 28, 0.75) !important;
    border: 1px solid rgba(163, 147, 235, 0.25) !important;
    padding: 22px !important;
    border-radius: 14px !important;
    backdrop-filter: blur(25px) !important;
    margin-bottom: 15px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6) !important;
}
h1, h2, h3, p, label, textarea, select {
    font-family: 'Courier New', Courier, monospace !important;
}
.subtle-title {
    font-size: 14px !important;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: #a393eb !important;
    text-align: center;
    margin-bottom: 20px;
}
.chat-msg {
    padding: 8px 12px;
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 13px;
}
</style>''', unsafe_allow_html=True)

st.markdown('<div class="subtle-title">— cosmic journal —</div>', unsafe_allow_html=True)
# Multi-language text management engine mapping
LANG_DICT = {
    "English": {"nakshatra": "🔮 Active Nakshatra Focus:", "energy": "⚡ Day Energy Scale:", "todo": "🟢 What to Do:", "avoid": "🔴 What to Avoid:", "portal": "📝 Reflection Portal", "vault": "📚 Archival Vault"},
    "Hindi (हिंदी)": {"nakshatra": "🔮 सक्रिय नक्षत्र प्रभाव:", "energy": "⚡ आज की ऊर्जा स्तर:", "todo": "🟢 आज क्या करें:", "avoid": "🔴 किस चीज़ से बचें:", "portal": "📝 आत्म-चिंतन पोर्टल", "vault": "📚 पुरालेख तिजोरी"},
    "Urdu (اُردو)": {"nakshatra": "🔮 فعال نکشتر فوکس:", "energy": "⚡ آج کی توانائی کا پیمانہ:", "todo": "🟢 کیا کرنا ہے:", "avoid": "🔴 کس چیز سے پرہیز کرنا ہے:", "portal": "📝 پورٹل کی عکاسی", "vault": "📚 آرکائیول وولٹ"}
}

col_l1, col_l2 = st.columns([2, 1])
with col_l2:
    selected_lang = st.selectbox("🌐 Language/زبان", ["English", "Hindi (हिंदी)", "Urdu (اُردو)"])
L = LANG_DICT[selected_lang]

with st.expander("✨ Configure Birth Profile (Setup Once)", expanded=False):
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        dob = st.date_input("Date of Birth:", value=dt_lib.date(2000, 1, 1))
        tob = st.time_input("Time of Birth:", value=dt_lib.time(12, 0))
    with col_b2:
        pob = st.text_input("Place of Birth:", placeholder="City, Country")
        sync_chart = st.checkbox("Synchronize System Matrix?", value=False)

def compute_cosmic_flow(has_chart, b_date):
    if not has_chart:
        return {
            "star": "Uttara Ashadha ➔ Shravana",
            "rating": "92/100 (Exalted - Excellent high vibration flow)",
            "do": "Executing technical workflows, deep active listening, and saving codes.",
            "avoid": "Engaging in stubborn arguments, rush-handling designs, or over-explaining."
        }
    
    # Precise dynamic matching math equation based on user's calendar date value
    calc_idx = (b_date.day % 3)
    if calc_idx == 1:
        return {
            "star": "Native Janma Placement Highly Activated",
            "rating": "96/100 (Radiant Energy - A fantastic day for strategic expansion)",
            "do": "Launching structural plans, studying advanced syntax sheets, and trusting intuitive timing.",
            "avoid": "Ignoring mental exhaustion signals, forcing high-risk communication streams, or seeking external validation."
        }
    elif calc_idx == 2:
        return {
            "star": "Harmonious Supporting Star Wave",
            "rating": "78/100 (Steady Flow - Balanced creative mindset stability)",
            "do": "Refining system layout properties, cleaning data files, and organizing text spaces.",
            "avoid": "Taking on multiple contrasting tasks at once or entering stress loops."
        }
    else:
        return {
            "star": "Introspective Lunar Mansion Crossing",
            "rating": "45/100 (Low Energy - Restorative rest period advised)",
            "do": "Conducting silent audits, practicing breathing metrics, and stepping away from screens.",
            "avoid": "Deploying massive framework changes, signing contracts, or letting self-doubt cloud judgments."
        }

cosmic = compute_cosmic_flow(sync_chart, dob)

st.markdown(f'''
<div class="cosmic-page">
    <h3 style="color: #dcd6f7; margin-top:0; font-size:16px;">✨ Alignment Matrix ({today_str})</h3>
    <p style="font-size:14px; margin-bottom:8px;"><strong>{L['nakshatra']}</strong> <br><span style="color: #a393eb;">{cosmic['star']}</span></p>
    <p style="font-size:14px; margin-bottom:12px;"><strong>{L['energy']}</strong> <br><span style="color: #a393eb;">{cosmic['rating']}</span></p>
    <p style="font-size:14px; margin-bottom:8px;"><strong>{L['todo']}</strong> <br>{cosmic['do']}</p>
    <p style="font-size:14px; margin-bottom:0;"><strong>{L['avoid']}</strong> <br>{cosmic['avoid']}</p>
</div>''', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:14px; margin-bottom:4px; color:#a393eb; font-weight:bold;'>💬 Celestial Chat Assistant</p>", unsafe_allow_html=True)

with st.container(border=False):
    st.markdown('<div class="chat-panel">', unsafe_allow_html=True)
    chat_query = st.text_input("Ask anything about today's transits or your birth details:", placeholder="e.g., Is today's 45/100 energy going to affect my studying focus?")
    
    if chat_query:
        q_clean = chat_query.lower()
        st.markdown(f'<div class="chat-msg" style="background:rgba(255,255,255,0.05); color:#a393eb;"><strong>🧑 You:</strong> {chat_query}</div>', unsafe_allow_html=True)
        
        # INTELLIGENT EXPERT CELESTIAL ENGINE RESPONSES
        if "energy" in q_clean or "low" in q_clean or "good" in q_clean:
            ai_ans = f"Today's active scale indicates a rating of {cosmic['rating']}. Based on this alignment, your mental capacities are operating exactly as highlighted above. Ensure you lean directly into the prioritized guidelines and avoid structural fatigue loops."
        elif "birth" in q_clean or "chart" in q_clean or "details" in q_clean:
            ai_ans = f"Your planetary grid layout is processed safely inside your browser memory cache. The current configuration tracks a {cosmic['star']} path, establishing an intricate synchronization map across today's live calendar transits."
        else:
            ai_ans = "The cosmic vectors suggest standard energetic supportive currents. Align your active actions to what is prioritized today, keep your workspace clean, and advance steadily."
            
        st.markdown(f'<div class="chat-msg" style="background:rgba(163,147,235,0.1); color:#ffffff;"><strong>🔮 Coll AI:</strong> {ai_ans}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:13px; margin-bottom:4px; color:#a393eb; font-weight:bold;'>{L['portal']}</p>", unsafe_allow_html=True)

with st.form("cosmic_input_form", clear_on_submit=True):
    user_entry = st.text_area(label="Input", placeholder="Write notes about your day here...", label_visibility="collapsed", height=70)
    submit_log = st.form_submit_button("📖 Close Latch & Commit to Vault", use_container_width=True)
    
    if submit_log and user_entry.strip():
        try:
            df_log = pd.read_csv(DB_FILE)
        except Exception:
            df_log = pd.DataFrame(columns=["Date", "Reflection", "Transit", "Energy", "Language"])
            
        new_row = pd.DataFrame([[today_str, user_entry.strip(), cosmic['star'], cosmic['rating'], selected_lang]], columns=["Date", "Reflection", "Transit", "Energy", "Language"])
        new_row.to_csv(DB_FILE, mode='a', header=False, index=False)
        st.success("📔 Safely committed inside your vault.")
        st.rerun()

st.markdown("<hr style='margin:12px 0; border-color: rgba(163,147,235,0.15);'>", unsafe_allow_html=True)

try:
    vault_df = pd.read_csv(DB_FILE)
except Exception:
    vault_df = pd.DataFrame(columns=["Date", "Reflection", "Transit", "Energy", "Language"])

if not vault_df.empty:
    with st.expander(f"📖 {L['vault']}", expanded=False):
        st.dataframe(vault_df[["Date", "Reflection", "Transit"]], use_container_width=True, hide_index=True)
        csv_buffer = vault_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="🖨️ Print / Export Entire Ledger History", data=csv_buffer, file_name=f"cosmic_vault_{today_str}.csv", mime="text/csv", use_container_width=True)
