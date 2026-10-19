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

# 100% वर्किंग मोबाइल फ्रेंडली डीप स्पेस नेबुला इफ़ेक्ट
st.markdown('''
<style>
.stApp {
    background: radial-gradient(circle at 50% 50%, #1a0b2e 0%, #0c0517 50%, #030006 100%) !important;
    background-attachment: fixed !important;
    color: #f0f0f5 !important;
}
div.cosmic-page, div.chat-panel {
    background: rgba(18, 9, 36, 0.75) !important;
    border: 1px solid rgba(163, 147, 235, 0.25) !important;
    padding: 22px !important;
    border-radius: 14px !important;
    backdrop-filter: blur(20px) !important;
    margin-bottom: 15px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6) !important;
}
h1, h2, h3, p, label, textarea, select {
    font-family: 'Courier New', Courier, monospace !important;
}
div.cosmic-page p, div.cosmic-page strong, div.cosmic-page span {
    color: #ffffff !important;
}
.subtle-title {
    font-size: 13px !important;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: #a393eb !important;
    text-align: center;
    margin-top: 5px;
    margin-bottom: 15px;
}
.stTextArea div[data-baseweb="textarea"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(163, 147, 235, 0.20) !important;
}
textarea {
    color: #ffffff !important;
}
.chat-msg {
    padding: 8px 12px;
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 13px;
}
</style>''', unsafe_allow_html=True)

st.markdown('<div class="subtle-title">— cosmic journal —</div>', unsafe_allow_html=True)
LANG_DICT = {
    "English": {
        "title": "✨ Alignment Matrix & Overview", "nakshatra": "🔮 Active Nakshatra Focus:", "energy": "⚡ Day Energy Scale & Output:", 
        "todo": "🟢 Broad Guidance (What to Prioritize):", "avoid": "🔴 Threshold Boundaries (What to Avoid):", "portal": "📝 Reflection Portal", 
        "vault": "📚 Archival Vault", "config_title": "✨ Configure Birth Profile (Setup Once)",
        "pob_place": "City, Country", "sync_btn": "Synchronize System Matrix?", "btn_save": "📖 Close Latch & Commit to Vault",
        "chat_title": "💬 Celestial Chat Assistant", "chat_place": "Ask anything about today's transits...",
        "vault_open": "📖 Open Book Vault Ledger Pages", "btn_print": "🖨️ Print / Export Entire Ledger History"
    },
    "Hindi (हिंदी)": {
        "title": "✨ संरेखण मैट्रिक्स एवं विस्तृत अवलोकन", "nakshatra": "🔮 सक्रिय नक्षत्र गोचर एवं प्रभाव:", "energy": "⚡ दैनिक ऊर्जा स्तर एवं मानसिक स्थिति:", 
        "todo": "🟢 व्यापक मार्गदर्शन (आज किन चीज़ों को प्राथमिकता दें):", "avoid": "🔴 नकारात्मक प्रभाव सीमा (किन चीज़ों से पूरी तरह बचें):", "portal": "📝 आत्म-चिंतन पोर्टल", 
        "vault": "📚 पुरालेख तिजोरी", "config_title": "✨ जन्म प्रोफ़ाइल सेट करें (सिर्फ़ एक बार)",
        "pob_place": "शहर, देश का नाम", "sync_btn": "कुंडली मैट्रिक्स को सिंक्रनाइज़ करें?", "btn_save": "📖 तिजोरी में सुरक्षित लॉग करें",
        "chat_title": "💬 आकाशीय एआई चैट असिस्टेंट", "chat_place": "आज के नक्षत्र या अपनी ऊर्जा के बारे में कुछ भी पूछें...",
        "vault_open": "📖 तिजोरी के पन्ने खोलें", "btn_print": "🖨️ पूरा इतिहास प्रिंट / एक्सपोर्ट करें"
    },
    "Urdu (اُردو)": {
        "title": "✨ الائنمنٹ میٹرکس", "nakshatra": "🔮 فعال نکشتر فوکس:", "energy": "⚡ آج کی توانائی کا پیمانہ:", 
        "todo": "🟢 کیا کرنا ہے:", "avoid": "🔴 کس چیز سے پرہیز کرنا ہے:", "portal": "📝 پورٹل کی عکاسی", 
        "vault": "📚 آرکائیول وولٹ", "config_title": "✨ برتھ پروفائل کنفیگر کریں",
        "pob_place": "شہر، ملک کا نام", "sync_btn": "سسٹم میٹرکس کو سنکرونائز کریں؟", "btn_save": "📖 لیس بند کریں اور وولٹ میں محفوظ کریں",
        "chat_title": "💬 فلکیاتی چیٹ اسسٹنٹ", "chat_place": "آج کے ٹرانزٹ کے بارے में कुछ भी पूछें...",
        "vault_open": "📖 وولٹ لیجر کے صفحات کھولیں", "btn_print": "🖨️ ہسٹری پرنٹ या एक्सपोर्ट करें"
    }
}

col_l1, col_l2 = st.columns(2)
with col_l2:
    selected_lang = st.selectbox("🌐 Language/ज़बान", ["English", "Hindi (हिंदी)", "Urdu (اُردو)"])
L = LANG_DICT[selected_lang]

with st.expander(L["config_title"], expanded=False):
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        dob = st.date_input("Date of Birth:", value=dt_lib.date(1994, 7, 11))
        tob = st.time_input("Time of Birth:", value=dt_lib.time(8, 50))
    with col_b2:
        pob = st.text_input("Place of Birth:", placeholder=L["pob_place"])
        sync_chart = st.checkbox(L["sync_btn"], value=False)
def compute_cosmic_flow(has_chart, b_date, lang):
    if not has_chart:
        if lang == "Hindi (हिंदी)":
            return {
                "star": "उत्तरा आषाढ़ ➔ श्रवण (अजेयता से बौद्धिक श्रवण का संक्रमण काल)",
                "rating": "92/100 (उत्कृष्ट - उच्च मानसिक चेतना एवं वैचारिक स्पष्टता)",
                "do": "आज ब्रह्मांडीय ऊर्जा आपको गहरी समझ और तार्किक शक्ति दे रही है। यदि आप कोई नया अध्ययन (Study Project) या जटिल कोडिंग (App Development) शुरू करना चाहते हैं, तो यह समय सर्वोत्तम है। अपनी योजनाओं को लिखित रूप में संकलित करें, दूसरों के विचारों को ध्यान से सुनें, और अपने महत्वपूर्ण डेटा या कोड्स को सुरक्षित रूप से बैकअप करें।",
                "avoid": "अनावश्यक सामाजिक गपशप या ज़िद में आकर की जाने वाली बहसों में अपनी ऊर्जा नष्ट न करें। आज जल्दबाजी में आकर अपनी किसी पुरानी ऐप या प्रोजेक्ट के मूल डिज़ाइन में कोई बड़ा फेरबदल न करें। बिना माँगे दूसरों को सलाह देने या अपने काम का स्पष्टीकरण देने से पूरी तरह बचें।"
            }
        else:
            return {
                "star": "Uttara Ashadha ➔ Shravana (Transition from Invincibility to Intellectual Listening)",
                "rating": "92/100 (Exalted - High mental clarity and vital thought current)",
                "do": "The cosmic current provides profound analytical skills today. Perfect for commencing complicated study sprints or architecture development. Write down frameworks, listen carefully to insights, and strictly execute technical workflows while saving system files.",
                "avoid": "Do not deplete your valuable energy in stubborn arguments or casual social gossip. Avoid rush-handling structural design systems or rewriting fully functional templates under impulse. Do not over-explain your strategies to skeptics."
            }
    
    calc_idx = (b_date.day % 3)
    if calc_idx == 1:
        if lang == "Hindi (हिंदी)":
            return {
                "star": "मूल जन्म नक्षत्र गोचर से अत्यधिक संरेखित (विशेष रूप से जागृत)",
                "rating": "96/100 (दीप्तिमान आत्म-बल - रणनीतिक योजना और दीर्घकालिक निर्णयों के लिए अद्भुत दिन)",
                "do": "यह आपकी निजी ऊर्जा का चरमोत्कर्ष दिन है। आपके सोचने, याद रखने और किसी विषय को गहराई से सीखने की क्षमता इस समय 100% पर काम कर रही है। किसी भी नए बड़े अध्ययन लक्ष्य (Study Goal) या कोडिंग प्रोजेक्ट की आज नींव रखें। अपने अंतर्ज्ञान (Intuitive Timing) पर पूरा भरोसा करके आगे बढ़ें और जटिल समस्याओं को आज सुलझा लें।",
                "avoid": "काम की धुन में मानसिक थकान और आँखों के तनाव को नजरअंदाज न करें। आज अति-उत्साह में आकर एक साथ बहुत सारे वित्तीय वादों या बिलिंग चक्रों में पैर न फँसाएं। किसी बाहरी व्यक्ति से अपने काम की प्रशंसा या मंजूरी (Validation) की उम्मीद रखकर अपना समय खराब न करें।"
            }
        else:
            return {
                "star": "Native Janma Placement Highly Activated (Personal Cosmic Alignment)",
                "rating": "96/100 (Radiant Self-Will - A spectacular day for strategic expansions and massive blueprints)",
                "do": "Your personal cognitive processing and absorption limits are peaking today. This is the optimal window to launch structural study planners, dive into advanced logic programming syntax, and trust your internal timing implicitly. Tackle the hardest technical barriers now.",
                "avoid": "Do not ignore minor somatic signals of mental exhaustion or fatigue loops. Avoid entering multiple complicated communication streams or micro-managing temporary systems. Refrain from seeking external praise for your silent milestones."
            }
    elif calc_idx == 2:
        if lang == "Hindi (हिंदी)":
            return {
                "star": "सामंजस्यपूर्ण सहायक तारा तरंग (Harmonious Supporting Star Matrix)",
                "rating": "78/100 (स्थिर प्रवाह - संतुलित रचनात्मक मानसिकता)",
                "do": "आज का दिन किसी बड़े धमाके का नहीं, बल्कि व्यवस्था बनाने का है। अपने एप्लिकेशन के मौजूदा कोड के लेआउट को ठीक करें, फ़ाइलों के भीतर की गड़बड़ियों को साफ़ करें, डिजिटल दस्तावेज़ों को व्यवस्थित करें, और अपनी डेस्क या पढ़ाई के स्थान को साफ़-सुथरा बनाएं। यह स्थिरता आपके आगे के बड़े लक्ष्यों के लिए मज़बूत नींव तैयार करेगी।",
                "avoid": "एक साथ कई सारे विपरीत प्रकृति के कार्यों को अपने हाथ में लेने की भूल न करें (Multitasking से बचें)। जब तक एक काम पूरा न हो, दूसरे पर न जाएँ। खुद को व्यर्थ के मानसिक तनाव और चिंता के लूप (Stress Loops) में फँसने से रोकें।"
            }
        else:
            return {
                "star": "Harmonious Supporting Star Wave (System Maintenance Alignment)",
                "rating": "78/100 (Steady Flow - Balanced creative mindset stability and optimization focus)",
                "do": "Today calls for structural refinement rather than high-risk execution. Dedicate your hours to refining application layout properties, auditing operational files, organizing text configurations, and decluttering your logical workspace to build a solid pad.",
                "avoid": "Strictly avoid aggressive multitasking or handling conflicting logging requests simultaneously. Do not allow brief external delays to draw you into anxious overthinking or negative logic loops."
            }
    else:
        if lang == "Hindi (हिंदी)":
            return {
                "star": "आत्मनिरीक्षण चंद्र नक्षत्र गोचर (Restorative Rest & Audit Phase)",
                "rating": "45/100 (धीमा ऊर्जा प्रवाह - मानसिक विश्राम और आंतरिक समीक्षा का दिन)",
                "do": "आज आपकी ऊर्जा का स्तर थोड़ा धीमा महसूस हो सकता है, जो कि पूरी तरह सामान्य है। आज कोई नया भारी काम करने के बजाय अपने पुराने किए गए कार्यों का शांत ऑडिट करें। गहरी सांस लेने का अभ्यास करें, प्रकृति के साथ थोड़ा समय बिताएं, और स्क्रीन टाइम से उचित दूरी बनाकर अपने मस्तिष्क को रिचार्ज होने का मौका दें।",
                "avoid": "आज किसी बड़े प्रोजेक्ट या ऐप को पब्लिक रूप से लाइव (Deploy) करने की जल्दबाजी न करें। किसी नए वित्तीय दस्तावेज़ या बड़े एग्रीमेंट पर हस्ताक्षर करने से बचें। यदि कोई काम उम्मीद के मुताबिक न चले, तो हीन भावना या आत्म-संदेह (Self-Doubt) को अपने ऊपर हावी न होने दें।"
            }
        else:
            return {
                "star": "Introspective Lunar Mansion Crossing (Low Energy Re-calibration)",
                "rating": "45/100 (Reflective Current - Introspective evaluation and vital rest advised)",
                "do": "Your computational energy is running on a conservative mode today. Use this space to conduct silent hidden audits, save local back-ups, practice deep relaxation metrics, and completely step away from heavy screen exposures to replenish your reserves.",
                "avoid": "Do not attempt massive database deployments or live structural rollouts today. Postpone signing permanent contracts or automated billing setups. Do not let temporary slow paces trigger toxic self-doubt loops."
            }

cosmic = compute_cosmic_flow(sync_chart, dob, selected_lang)

st.markdown(f'''
<div class="cosmic-page">
    <h3 style="color: #dcd6f7 !important; margin-top:0; margin-bottom:12px; font-size:16px;">{L['title']} ({today_str})</h3>
    <hr style="border-color: rgba(163,147,235,0.2); margin-bottom: 20px;">
    <p style="font-size:14px; margin-bottom:12px; line-height:1.5;"><strong>{L['nakshatra']}</strong> <br><span style="color: #a393eb !important; font-weight: bold;">{cosmic['star']}</span></p>
    <p style="font-size:14px; margin-bottom:14px; line-height:1.5;"><strong>{L['energy']}</strong> <br><span style="color: #a393eb !important; font-weight: bold;">{cosmic['rating']}</span></p>
    <p style="font-size:14px; margin-bottom:14px; line-height:1.6; text-align: justify;"><strong>{L['todo']}</strong> <br>{cosmic['do']}</p>
    <p style="font-size:14px; margin-bottom:0; line-height:1.6; text-align: justify;"><strong>{L['avoid']}</strong> <br>{cosmic['avoid']}</p>
</div>''', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:14px; margin-bottom:4px; color:#a393eb; font-weight:bold;'>{L['chat_title']}</p>", unsafe_allow_html=True)

with st.container(border=False):
    st.markdown('<div class="chat-panel">', unsafe_allow_html=True)
    chat_query = st.text_input(L["chat_title"], placeholder=L["chat_place"], label_visibility="collapsed")
    
    if chat_query:
        q_clean = chat_query.lower()
        st.markdown(f'<div class="chat-msg" style="background:rgba(255,255,255,0.05); color:#a393eb;"><strong>🧑 You:</strong> {chat_query}</div>', unsafe_allow_html=True)
        
        if selected_lang == "Hindi (हिंदी)":
            if "paise" in q_clean or "kharch" in q_clean or "money" in q_clean or "पैसे" in q_clean or "खर्च" in q_clean:
                ai_ans = f"आज का ऊर्जा स्तर {cosmic['rating']} है और चंद्रमा श्रवण नक्षत्र में है। यह दिन नए निवेश या बड़े खर्चों के लिए जल्दबाजी करने का नहीं है। अपने बजट ट्रैकर (Spend Tracker) के नियमों का पालन करें और आज केवल आवश्यक खर्चों को ही प्राथमिकता दें!"
            elif "study" in q_clean or "padhai" in q_clean or "पढ़ाई" in q_clean or "परीक्षा" in q_clean:
                ai_ans = f"पढ़ाई के दृष्टिकोण से आज का दिन बहुत अनुकूल है! श्रवण नक्षत्र गहन शिक्षण (deep learning) और नए कोडिंग फॉर्मूले सीखने के लिए सर्वोत्तम है। आलस्य से बचें, आपका ध्यान आज बहुत मजबूत रहेगा।"
            elif "ऊर्जा" in q_clean or "कम" in q_clean or "अच्छा" in q_clean or "energy" in q_clean:
                ai_ans = f"आज का ब्रह्मांडीय पैमाना {cosmic['rating']} का स्तर दिखा रहा है। इस संरेखण के आधार पर, आपके काम करने की क्षमता बहुत मजबूत है। आज 'क्या करें' वाले बिंदुओं पर ध्यान दें और अनावश्यक तनाव से बचें।"
            elif "जन्म" in q_clean or "कुंडली" in q_clean or "तारीख" in q_clean:
                ai_ans = f"आपकी जन्म कुंडली का विवरण सुरक्षित रूप से ब्राउज़र कैश में सेव है। वर्तमान गणना के अनुसार आपका {cosmic['star']} पथ सक्रिय है, जो आज के गोचर के साथ जुड़ा हुआ है।"
            else:
                ai_ans = "ग्रहों की चाल आज सामान्य और सहायक बनी हुई है। अपने कार्यों को आज की प्राथमिकताओं के साथ जोड़ें, आलस से बचें और धीरे-धीरे आगे बढ़ें।"
        else:
            if "money" in q_clean or "spend" in q_clean or "expense" in q_clean:
                ai_ans = f"Today's energy is {cosmic['rating']}. It's a day for calculation rather than impulsive shopping. Stick to your Pocket Spend Tracker goals and avoid signing high-risk financial commitments today!"
            elif "study" in q_clean or "exam" in q_clean or "learn" in q_clean:
                ai_ans = "Shravana Nakshatra is highly active today, making it perfect for absorbing deep technical knowledge, writing application scripts, and focused self-study."
            elif "energy" in q_clean or "low" in q_clean or "good" in q_clean:
                ai_ans = f"Today's active scale indicates a rating of {cosmic['rating']}. Based on this alignment, lean directly into the prioritized guidelines."
            else:
                ai_ans = "The cosmic vectors suggest standard energetic supportive currents. Align your actions to what is prioritized today and advance steadily."
            
        st.markdown(f'<div class="chat-msg" style="background:rgba(163,147,235,0.1); color:#ffffff;"><strong>🔮 Coll AI:</strong> {ai_ans}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<p style='font-size:13px; margin-bottom:4px; color:#a393eb; font-weight:bold;'>{L['portal']}</p>", unsafe_allow_html=True)

with st.form("cosmic_input_form", clear_on_submit=True):
    user_entry = st.text_area(label="Input", placeholder="Write notes about your day here...", label_visibility="collapsed", height=70)
    submit_log = st.form_submit_button(L["btn_save"], use_container_width=True)
    
    if submit_log and user_entry.strip():
        try:
            df_log = pd.read_csv(DB_FILE)
        except Exception:
            df_log = pd.DataFrame(columns=["Date", "Reflection", "Transit", "Energy", "Language"])
            
        new_row = pd.DataFrame([[today_str, user_entry.strip(), cosmic['star'], cosmic['rating'], selected_lang]], columns=["Date", "Reflection", "Transit", "Energy", "Language"])
        new_row.to_csv(DB_FILE, mode='a', header=False, index=False)
        st.success("📔 तिजोरी बंद हो गई है। आपका विचार सुरक्षित लॉग कर लिया गया है।")
        st.rerun()

st.markdown("<hr style='margin:12px 0; border-color: rgba(163,147,235,0.15);'>", unsafe_allow_html=True)

try:
    vault_df = pd.read_csv(DB_FILE)
except Exception:
    vault_df = pd.DataFrame(columns=["Date", "Reflection", "Transit", "Energy", "Language"])

if not vault_df.empty:
    with st.expander(L["vault_open"], expanded=False):
        st.dataframe(vault_df[["Date", "Reflection", "Transit"]], use_container_width=True, hide_index=True)
        csv_buffer = vault_df.to_csv(index=False).encode('utf-8')
        st.download_button(label=L["btn_print"], data=csv_buffer, file_name=f"cosmic_vault_{today_str}.csv", mime="text/csv", use_container_width=True)
