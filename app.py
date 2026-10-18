import streamlit as st
import time

st.set_page_config(page_title="АгроСервис", page_icon="🌾", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #121812; background-image: linear-gradient(180deg, #182019 0%, #0c100d 100%); }
    html, body, [class*="css"], .stMarkdown, p, span, label, div { color: #dfe6d8 !important; }
    h1, h2, h3 { color: #f0f4ea !important; }
    
    .selection-panel { background-color: #1c241c; border: 1px solid #3e4d3a; border-radius: 12px; padding: 24px; margin-bottom: 24px; }
    .panel-title { color: #b5c9a5; font-weight: 700; font-size: 1.1rem; margin-bottom: 12px; display: block; }
    
    div[data-testid="stSelectbox"] label { color: #b5c9a5 !important; font-weight: 600 !important; }
    div[data-baseweb="select"] > div { background-color: #2a3429 !important; color: #f0f4ea !important; border: 1px solid #4d6144 !important; }
    div[data-baseweb="select"] span { color: #f0f4ea !important; }
    
    div[data-baseweb="popover"] ul, ul[role="listbox"] { background-color: #1c241c !important; border: 1px solid #4d6144 !important; }
    div[data-baseweb="popover"] li, ul[role="listbox"] li { color: #dfe6d8 !important; background-color: #1c241c !important; }
    div[data-baseweb="popover"] li:hover, ul[role="listbox"] li:hover { background-color: #2a3429 !important; }
    
    div[data-testid="stNumberInput"] label { color: #b5c9a5 !important; }
    div[data-testid="stNumberInput"] input { background-color: #e8ebe4 !important; color: #121812 !important; font-weight: 600 !important; border: 1px solid #6a7f5e !important; }
    
    div[data-testid="stRadio"] label { color: #b5c9a5 !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] label { background-color: #2a3429 !important; border: 1px solid #4d6144 !important; border-radius: 8px !important; padding: 8px 16px !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover { background-color: #384832 !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] label p { color: #dfe6d8 !important; }
    
    .result-card { padding: 24px; border-radius: 10px; margin-top: 16px; border-left: 6px solid #444; background-color: #1c241c; }
    .result-card p { color: #dfe6d8 !important; }
    .status-ok { border-left-color: #81c784; background-color: #1c2a1d; }
    .status-warn { border-left-color: #e0b651; background-color: #2a2618; }
    .status-crit { border-left-color: #e57373; background-color: #2a1c1c; }
    .status-ok h2 { color: #81c784 !important; }
    .status-warn h2 { color: #e0b651 !important; }
    .status-crit h2 { color: #e57373 !important; }
    
    .spec-box { background-color: #1c241c; padding: 12px 16px; border-radius: 8px; border: 1px solid #3e4d3a; margin-bottom: 8px; }
    .fixed-param { background-color: #242e22; padding: 12px 16px; border-radius: 8px; border: 1px solid #4d6144; margin-bottom: 8px; }
    .fixed-param strong { color: #b5c9a5 !important; }
    
    .guide-link { display: inline-block; margin-top: 12px; padding: 12px 20px; background-color: #384832; color: #f0f4ea !important; border-radius: 8px; text-decoration: none; border: 1px solid #5c7052; font-weight: 600; }
    .guide-link:hover { background-color: #4d6144; }
    
    .stButton > button { background-color: #4d6144 !important; color: #ffffff !important; font-weight: 700 !important; border: 1px solid #6a7f5e !important; padding: 12px 24px !important; border-radius: 8px !important; }
    .stButton > button:hover { background-color: #5c7052 !important; }
    
    .gauge-container { margin-bottom: 20px; }
    .gauge-header { display: flex; justify-content: space-between; margin-bottom: 6px; font-weight: 600; color: #dfe6d8; }
    .gauge-bar-bg { width: 100%; height: 22px; background: linear-gradient(90deg, #e57373 0%, #81c784 20%, #81c784 60%, #e0b651 80%, #e57373 100%); border-radius: 11px; overflow: hidden; border: 1px solid #3e4d3a; position: relative; }
    .gauge-bar-fill { height: 100%; background: rgba(255, 255, 255, 0.2); transition: width 0.6s ease; border-radius: 11px; }
    .gauge-pointer { position: absolute; top: -2px; width: 4px; height: 26px; background-color: #ffffff; border-radius: 2px; transition: left 0.6s ease; transform: translateX(-50%); z-index: 10; }
    .gauge-labels { display: flex; justify-content: space-between; font-size: 0.8rem; color: #8a9e7a; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

st.title("АгроСервис: Диагностика техники")

DEFAULT_MACHINES = {
    "МТЗ-80/82": {
        "temp": {k: {"min": 80, "max": 95, "crit_high": 105, "label": "Температура (°C)", "note": "80-95°C"} for k in ["idle","drive","load"]},
        "pressure": {k: {"min": 2.0, "max": 3.5, "crit_low": 1.0, "label": "Давление (бар)", "note": "2.0-3.5 бар"} for k in ["idle","drive","load"]},
        "vibration": {k: {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)", "note": "до 4.5 мм/с"} for k in ["idle","drive","load"]}
    },
    "John Deere": {
        "temp": {k: {"min": 82, "max": 94, "crit_high": 104, "label": "Температура (°C)", "note": "82-94°C"} for k in ["idle","drive","load"]},
        "pressure": {k: {"min": 2.9, "max": 4.5, "crit_low": 1.4, "label": "Давление (бар)", "note": "2.9-4.5 бар"} for k in ["idle","drive","load"]},
        "vibration": {k: {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)", "note": "до 4.5 мм/с"} for k in ["idle","drive","load"]}
    }
}

if "custom" not in st.session_state: st.session_state.custom = {}
all_mach = {**DEFAULT_MACHINES, **st.session_state.custom}

st.markdown('<div class="selection-panel"><span class="panel-title">Параметры</span>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1: selected = st.selectbox("Техника", list(all_mach.keys()) + ["Добавить"])
with c2:
    if selected != "Добавить":
        MODE = {"idle": "Холостые", "drive": "Езда", "load": "Нагрузка"}
        mode_key = st.radio("Режим", list(MODE.keys()), format_func=lambda x: MODE[x], horizontal=True)
    else:
        mode_key = "drive"; MODE = {"idle":"Х","drive":"Е","load":"Н"}
st.markdown('</div>', unsafe_allow_html=True)

if selected == "Добавить":
    with st.form("add"):
        name = st.text_input("Название")
        tmpl = st.selectbox("Шаблон", list(DEFAULT_MACHINES.keys()))
        if st.form_submit_button("Сохранить"):
            if name.strip():
                st.session_state.custom[name] = DEFAULT_MACHINES[tmpl]
                st.rerun()
    st.stop()

spec = all_mach[selected]
cur_t, cur_p, cur_v = spec["temp"][mode_key], spec["pressure"][mode_key], spec["vibration"][mode_key]

st.markdown(f"### {selected} — {MODE[mode_key]}")
st.markdown(f'<div class="spec-box">T: {cur_t["note"]}</div><div class="spec-box">P: {cur_p["note"]}</div><div class="spec-box">V: {cur_v["note"]}</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])
with col1:
    st.subheader("Датчики")
    t_val = st.number_input(cur_t["label"], value=float((cur_t["min"]+cur_t["max"])/2), key=f"t{selected}{mode_key}")
    p_val = st.number_input(cur_p["label"], value=float((cur_p["min"]+cur_p["max"])/2), key=f"p{selected}{mode_key}")
    v_val = st.number_input(cur_v["label"], value=float((cur_v["min"]+cur_v["max"])/2), key=f"v{selected}{mode_key}")

    def gauge(lbl, val, spc, unit, is_p=False):
        mx = spc["max"]*1.5 if is_p else spc["crit_high"]*1.2
        pct = min(100, max(0, (val/mx)*100))
        if is_p:
            clr = "#e57373" if val<spc["crit_low"] else "#e0b651" if val<spc["min"] else "#81c784"
        else:
            clr = "#e57373" if val>spc["crit_high"] else "#e0b651" if val>spc["max"] else "#81c784"
        st.markdown(f'<div class="gauge-container"><div class="gauge-header"><span>{lbl}</span><span style="color:{clr}">{val} {unit}</span></div><div class="gauge-bar-bg"><div class="gauge-bar-fill" style="width:{pct}%"></div><div class="gauge-pointer" style="left:{pct}%"></div></div><div class="gauge-labels"><span>0</span><span>Норма: {spc["min"]}-{spc["max"]}</span><span>{mx:.1f}</span></div></div>', unsafe_allow_html=True)

    gauge("Температура", t_val, cur_t, "°C")
    gauge("Давление", p_val, cur_p, "бар", True)
    gauge("Вибрация", v_val, cur_v, "мм/с")

with col2:
    st.subheader("Результат")
    if st.button("Анализ", type="primary", use_container_width=True):
        score = 0
        if t_val > cur_t["crit_high"]: score += 2
        elif t_val > cur_t["max"] or t_val < cur_t["min"]: score += 1
        if p_val < cur_p["crit_low"]: score += 2
        elif p_val < cur_p["min"] or p_val > cur_p["max"]: score += 1
        if v_val > cur_v["crit_high"]: score += 2
        elif v_val > cur_v["max"]: score += 1
        
        if score == 0:
            st.markdown('<div class="result-card status-ok"><h2>НОРМА</h2><p>Все системы в порядке.</p></div>', unsafe_allow_html=True)
        elif score <= 2:
            st.markdown('<div class="result-card status-warn"><h2>ВНИМАНИЕ</h2><p>Есть отклонения. Требуется проверка.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-card status-crit"><h2>РЕМОНТ</h2><p>Критические показатели!</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-card"><p>Нажмите "Анализ"</p></div>', unsafe_allow_html=True)
