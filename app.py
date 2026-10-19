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

# शानदार नेबुला बैकग्राउंड और ग्लास-इफेक्ट स्टाइलिंग
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
# भाषा के अनुसार हर एक लेबल का डिक्शनरी मैपिंग
LANG_DICT = {
    "English": {
        "title": "✨ Alignment Matrix", "nakshatra": "🔮 Active Nakshatra Focus:", "energy": "⚡ Day Energy Scale:", 
        "todo": "🟢 What to Do:", "avoid": "🔴 What to Avoid:", "portal": "📝 Reflection Portal", 
        "vault": "📚 Archival Vault", "config_title": "✨ Configure Birth Profile (Setup Once)",
        "pob_place": "City, Country", "sync_btn": "Synchronize System Matrix?", "btn_save": "📖 Close Latch & Commit to Vault",
        "chat_title": "💬 Celestial Chat Assistant", "chat_place": "Ask anything about today's transits...",
        "vault_open": "📖 Open Book Vault Ledger Pages", "btn_print": "🖨️ Print / Export Entire Ledger History"
    },
    "Hindi (हिंदी)": {
        "title": "✨ संरेखण मैट्रिक्स (Alignment Matrix)", "nakshatra": "🔮 सक्रिय नक्षत्र प्रभाव:", "energy": "⚡ आज की ऊर्जा स्तर:", 
        "todo": "🟢 आज क्या करें:", "avoid": "🔴 किस चीज़ से बचें:", "portal": "📝 आत्म-चिंतन पोर्टल", 
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
        "chat_title": "💬 فلکیاتی چیٹ اسسٹنٹ", "chat_place": "آج کے ٹرانزٹ کے بارے में کچھ بھی پوچھیں...",
        "vault_open": "📖 وولٹ لیجر کے صفحات کھولیں", "btn_print": "🖨️ ہسٹری پرنٹ یا ایکسپورٹ کریں"
    }
}

col_l1, col_l2 = st.columns([2, 1])
with col_l2:
    selected_lang = st.selectbox("🌐 Language/زبان", ["English", "Hindi (हिंदी)", "Urdu (اُردو)"])
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
    # डिफ़ॉल्ट डेटाबेस (बिना कुंडली सिंक के)
    if not has_chart:
        if lang == "Hindi (हिंदी)":
            return {
                "star": "उत्तरा आषाढ़ ➔ श्रवण (अजेयता का संक्रमण काल)",
                "rating": "92/100 (उत्कृष्ट - बहुत उच्च सकारात्मक ऊर्जा प्रवाह)",
                "do": "तकनीकी काम पूरे करें, सक्रिय रूप से दूसरों की सुनें, और अपने कोड्स को सुरक्षित सेव करें।",
                "avoid": "जिद में आकर बहस करने से बचें, जल्दबाजी में डिज़ाइन न बदलें, और बिना वजह सफाई न दें।"
            }
        elif lang == "Urdu (اُردو)":
            return {
                "star": "उत्तरा आषाढ़ ➔ श्रवण",
                "rating": "92/100 (عمدہ توانائی کا بہاؤ)",
                "do": "تکنیکی کام مکمل کریں، گہرائی سے سنیں، اور اپنے کوڈز کو محفوظ کریں۔",
                "avoid": "ضد میں آکر بحث کرنے سے بچیں، جلد بازی میں ڈیزائن نہ بنائیں، اور بلا وجہ وضاحت نہ دیں۔"
            }
        else:
            return {
                "star": "Uttara Ashadha ➔ Shravana",
                "rating": "92/100 (Exalted - Excellent high vibration flow)",
                "do": "Executing technical workflows, deep active listening, and saving codes.",
                "avoid": "Engaging in stubborn arguments, rush-handling designs, or over-explaining."
            }
    
    # कुंडली सिंक होने पर जन्म तारीख के आधार पर गणना
    calc_idx = (b_date.day % 3)
    if calc_idx == 1:
        if lang == "Hindi (हिंदी)":
            return {
                "star": "मूल जन्म नक्षत्र अत्यधिक सक्रिय (शुभ गोचर)",
                "rating": "96/100 (दीप्तिमान ऊर्जा - रणनीतिक विस्तार के लिए शानदार दिन)",
                "do": "महत्वपूर्ण योजनाओं की शुरुआत करें, एडवांस कोडिंग फॉर्मूला सीखें, और अपनी अंतरात्मा की टाइमिंग पर भरोसा करें।",
                "avoid": "मानसिक थकान को नजरअंदाज न करें, जबरदस्ती किसी से उलझने की कोशिश न करें, और दूसरों से तारीफ की उम्मीद न रखें।"
            }
        else:
            return {
                "star": "Native Janma Placement Highly Activated",
                "rating": "96/100 (Radiant Energy - A fantastic day for strategic expansion)",
                "do": "Launching structural plans, studying advanced syntax sheets, and trusting intuitive timing.",
                "avoid": "Ignoring mental exhaustion signals, forcing high-risk communication streams, or seeking external validation."
            }
    elif calc_idx == 2:
        if lang == "Hindi (हिंदी)":
            return {
                "star": "सामंजस्यपूर्ण सहायक तारा तरंग (Harmonious Supporting Star)",
                "rating": "78/100 (स्थिर प्रवाह - संतुलित रचनात्मक मानसिकता)",
                "do": "एप्लिकेशन के लेआउट को ठीक करें, फ़ाइलों की सफ़ाई करें, और टेक्स्ट स्पेस को व्यवस्थित करें।",
                "avoid": "एक साथ कई सारे अलग-अलग कामों के चक्कर में न पड़ें और तनाव के चक्र में फँसने से बचें।"
            }
        elif lang == "Urdu (اُردو)":
            return {
                "star": "سازگار معاون ستارہ لہر",
                "rating": "78/100 (مستحکم بہاؤ - متوازن تخلیقی ذہن)",
                "do": "ایپلی کیشن کے لے آؤٹ کو درست کریں، فائلوں کی صفائی کریں، اور ٹیکسٹ اسپیس کو ترتیب دیں۔",
                "avoid": "ایک ساتھ کئی متضاد کاموں کو ہاتھ میں نہ لیں اور تناؤ کے چکر میں پھنسنے سے بچیں۔"
            }
        else:
            return {
                "star": "Harmonious Supporting Star Wave",
                "rating": "78/100 (Steady Flow - Balanced creative mindset stability)",
                "do": "Refining system layout properties, cleaning data files, and organizing text spaces.",
                "avoid": "Taking on multiple contrasting tasks at once or entering stress loops."
            }
    else:
        if lang == "Hindi (हिंदी)":
            return {
                "star": "आत्मनिरीक्षण चंद्र नक्षत्र गोचर (लो-एनर्जी फेज)",
                "rating": "45/100 (कम ऊर्जा स्तर - मानसिक विश्राम की सलाह)",
                "do": "अपने पुराने डेटा का मूक ऑडिट करें, गहरी सांस लेने का अभ्यास करें, और स्क्रीन से थोड़ी दूरी बनाएं।",
                "avoid": "आज किसी बड़े बदलाव को लाइव करने से बचें, कोई नया एग्रीमेंट साइन न करें, और खुद पर शक न करें।"
            }
        else:
            return {
                "star": "Introspective Lunar Mansion Crossing",
                "rating": "45/100 (Low Energy - Restorative rest period advised)",
                "do": "Conducting silent audits, practicing breathing metrics, and stepping away from screens.",
                "avoid": "Deploying massive framework changes, signing contracts, or letting self-doubt cloud judgments."
            }

cosmic = compute_cosmic_flow(sync_chart, dob, selected_lang)

st.markdown(f'''
<div class="cosmic-page">
    <h3 style="color: #dcd6f7; margin-top:0; font-size:16px;">{L['title']} ({today_str})</h3>
    <hr style="border-color: rgba(163,147,235,0.2); margin-bottom: 20px;">
    <p style="font-size:14px; margin-bottom:8px;"><strong>{L['nakshatra']}</strong> <br><span style="color: #a393eb;">{cosmic['star']}</span></p>
    <p style="font-size:14px; margin-bottom:12px;"><strong>{L['energy']}</strong> <br><span style="color: #a393eb;">{cosmic['rating']}</span></p>
    <p style="font-size:14px; margin-bottom:8px;"><strong>{L['todo']}</strong> <br>{cosmic['do']}</p>
    <p style="font-size:14px; margin-bottom:0;"><strong>{L['avoid']}</strong> <br>{cosmic['avoid']}</p>
</div>''', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:14px; margin-bottom:4px; color:#a393eb; font-weight:bold;'>{L['chat_title']}</p>", unsafe_allow_html=True)

with st.container(border=False):
    st.markdown('<div class="chat-panel">', unsafe_allow_html=True)
    chat_query = st.text_input(L["chat_title"], placeholder=L["chat_place"], label_visibility="collapsed")
    
    if chat_query:
        q_clean = chat_query.lower()
        st.markdown(f'<div class="chat-msg" style="background:rgba(255,255,255,0.05); color:#a393eb;"><strong>🧑 You:</strong> {chat_query}</div>', unsafe_allow_html=True)
        
        # चुनी गई भाषा के हिसाब से एआई का प्रतिक्रिया लॉजिक
        if selected_lang == "Hindi (हिंदी)":
            if "ऊर्जा" in q_clean or "कम" in q_clean or "अच्छा" in q_clean or "energy" in q_clean:
                ai_ans = f"आज का ब्रह्मांडीय पैमाना {cosmic['rating']} का स्तर दिखा रहा है। इस संरेखण के आधार पर, आपके काम करने की क्षमता ऊपर बताए गए सुझावों के अनुसार चलेगी। आज 'क्या करें' वाले बिंदुओं पर ध्यान दें और तनाव से बचें।"
            elif "जन्म" in q_clean or "कुंडली" in q_clean or "तारीख" in q_clean:
                ai_ans = f"आपकी जन्म कुंडली का विवरण सुरक्षित रूप से ब्राउज़र कैश में सेव है। वर्तमान गणना के अनुसार आपका {cosmic['star']} पथ सक्रिय है, जो आज के गोचर के साथ जुड़ा हुआ है।"
            else:
                ai_ans = "ग्रहों की चाल आज सामान्य और सहायक बनी हुई है। अपने कार्यों को आज की प्राथमिकताओं के साथ जोड़ें, आलस से बचें और धीरे-धीरे आगे बढ़ें।"
        else:
            if "energy" in q_clean or "low" in q_clean or "good" in q_clean:
                ai_ans = f"Today's active scale indicates a rating of {cosmic['rating']}. Based on this alignment, lean directly into the prioritized guidelines and avoid structural fatigue loops."
            elif "birth" in q_clean or "chart" in q_clean or "details" in q_clean:
                ai_ans = f"Your planetary grid layout is processed safely. The current configuration tracks a {cosmic['star']} path across today's live transits."
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
