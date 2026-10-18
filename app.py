import streamlit as st
import time

st.set_page_config(page_title="АгроСервис Диагностика", page_icon="⚙️", layout="wide")

# === СТРОГИЙ ИНЖЕНЕРНЫЙ СТИЛЬ (БЕЗ ШУМА) ===
st.markdown("""
<style>
    /* Фон: тёмно-серый, без ярких градиентов */
    .stApp { background-color: #121417; }
    
    /* Текст: мягкий светлый, контрастный но не режущий */
    html, body, [class*="css"], .stMarkdown, p, span, label, div {
        color: #d1d5db !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1, h2, h3 { color: #f3f4f6 !important; font-weight: 600; }
    
    /* Блоки (карточки) */
    .block-container { padding-top: 2rem; }
    div[data-testid="stVerticalBlock"] > div {
        background-color: #1e2126;
        border: 1px solid #333842;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    /* Выпадающий список */
    div[data-testid="stSelectbox"] label { color: #9ca3af !important; font-size: 0.9rem; }
    div[data-baseweb="select"] > div {
        background-color: #2d333b !important;
        color: #d1d5db !important;
        border: 1px solid #444c56 !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] span { color: #d1d5db !important; }
    ul[role="listbox"] { background-color: #2d333b !important; }
    ul[role="listbox"] li { color: #d1d5db !important; }
    ul[role="listbox"] li:hover { background-color: #373e47 !important; }
    
    /* Радиокнопки */
    div[data-testid="stRadio"] label { color: #9ca3af !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background-color: #2d333b !important;
        border: 1px solid #444c56 !important;
        border-radius: 6px !important;
        padding: 6px 12px !important;
        margin-right: 8px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label p { color: #d1d5db !important; }
    
    /* Поля ввода */
    div[data-testid="stNumberInput"] label { color: #9ca3af !important; font-size: 0.9rem; }
    div[data-testid="stNumberInput"] input {
        background-color: #0d1117 !important;
        color: #f3f4f6 !important;
        border: 1px solid #444c56 !important;
        font-weight: 600;
    }
    
    /* Кнопка */
    .stButton > button {
        background-color: #2d333b !important;
        color: #d1d5db !important;
        border: 1px solid #444c56 !important;
        font-weight: 600 !important;
        width: 100%;
    }
    .stButton > button:hover { background-color: #373e47 !important; border-color: #6b7280 !important; }
    
    /* Результаты */
    .res-box { padding: 16px; border-radius: 6px; margin-bottom: 12px; border-left: 4px solid #444; background-color: #1a1d21; }
    .res-ok { border-left-color: #4ade80; background-color: #142115; }
    .res-warn { border-left-color: #fbbf24; background-color: #241f14; }
    .res-crit { border-left-color: #f87171; background-color: #241414; }
    .res-title { font-size: 1.2rem; font-weight: 700; margin-bottom: 8px; }
    .res-text { font-size: 0.95rem; line-height: 1.5; color: #d1d5db; }
    
    /* Ссылки */
    .guide-link { display: inline-block; margin-top: 12px; color: #60a5fa !important; text-decoration: none; font-weight: 600; font-size: 0.9rem; }
    .guide-link:hover { text-decoration: underline; }
    
    /* Полоски */
    .gauge-container { margin-bottom: 16px; }
    .gauge-header { display: flex; justify-content: space-between; font-size: 0.9rem; font-weight: 600; margin-bottom: 4px; }
    .gauge-bar-bg { width: 100%; height: 16px; background: #0d1117; border-radius: 8px; overflow: hidden; border: 1px solid #333842; position: relative; }
    /* Градиент от плохого (красный) к хорошему (зеленый) и обратно */
    .gauge-bar-fill { height: 100%; transition: width 0.4s ease; border-radius: 8px; }
    .gauge-ok { background: #4ade80; }
    .gauge-warn { background: #fbbf24; }
    .gauge-crit { background: #f87171; }
    .gauge-labels { display: flex; justify-content: space-between; font-size: 0.75rem; color: #6b7280; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

st.title("АгроСервис: Диагностика техники")
st.markdown("---")

# === 1. БАЗА ТЕХНИКИ ===
MACHINES = {
    "МТЗ-80/82": {
        "idle": {"t": (70, 85, 95), "p": (0.8, 2.0, 0.5), "v": (0, 3.0, 5.0)},
        "drive": {"t": (80, 95, 105), "p": (2.0, 3.5, 1.0), "v": (0, 4.5, 7.1)},
        "load": {"t": (85, 100, 108), "p": (2.5, 4.5, 1.5), "v": (0, 5.5, 8.0)}
    },
    "John Deere": {
        "idle": {"t": (70, 85, 95), "p": (1.4, 2.9, 0.8), "v": (0, 3.0, 5.0)},
        "drive": {"t": (82, 94, 104), "p": (2.9, 4.5, 1.4), "v": (0, 4.5, 7.1)},
        "load": {"t": (85, 100, 108), "p": (3.5, 5.5, 2.0), "v": (0, 5.5, 8.0)}
    },
    "Кировец": {
        "idle": {"t": (70, 85, 95), "p": (2.0, 4.0, 1.5), "v": (0, 3.0, 5.0)},
        "drive": {"t": (80, 95, 105), "p": (4.0, 7.0, 2.0), "v": (0, 4.5, 7.1)},
        "load": {"t": (85, 100, 108), "p": (5.0, 8.0, 3.0), "v": (0, 5.5, 8.0)}
    }
}

# === 1. ВЫБОР ТЕХНИКИ ===
st.subheader("1. Выбор техники")
machine = st.selectbox("Техника", list(MACHINES.keys()))

# === 2. РЕЖИМ ===
st.subheader("2. Режим использования")
mode_map = {"idle": "Холостой ход", "drive": "Езда", "load": "Рабочая нагрузка"}
mode = st.radio("Режим", list(mode_map.keys()), format_func=lambda x: mode_map[x], horizontal=True)

spec = MACHINES[machine][mode]

# === 3. СТАТИЧНЫЕ НОРМАТИВЫ ===
st.subheader("3. Нормативы (справочно)")
st.markdown(f"""
<div class="block-container">
    <p><b>Температура:</b> {spec['t'][0]} — {spec['t'][1]} °C (критично > {spec['t'][2]})</p>
    <p><b>Давление масла:</b> {spec['p'][0]} — {spec['p'][1]} бар (критично < {spec['p'][2]})</p>
    <p><b>Вибрация:</b> до {spec['v'][1]} мм/с (критично > {spec['v'][2]})</p>
</div>
""", unsafe_allow_html=True)

# === 4. ПОКАЗАНИЯ ДАТЧИКОВ ===
st.subheader("4. Показания датчиков")

def get_gauge_html(name, val, norm_min, norm_max, crit_val, is_high_bad, unit):
    # Определяем цвет и ширину
    if is_high_bad: # Для температуры и вибрации (высокое = плохо)
        if val > crit_val: color, status = "#f87171", "КРИТИЧНО"
        elif val > norm_max: color, status = "#fbbf24", "ВНИМАНИЕ"
        else: color, status = "#4ade80", "НОРМА"
        # Ширина от 0 до crit_val
        width = min(100, max(0, (val / crit_val) * 100))
    else: # Для давления (низкое = плохо)
        if val < crit_val: color, status = "#f87171", "КРИТИЧНО"
        elif val < norm_min: color, status = "#fbbf24", "ВНИМАНИЕ"
        else: color, status = "#4ade80", "НОРМА"
        # Ширина от 0 до norm_max * 1.5
        width = min(100, max(0, (val / (norm_max * 1.5)) * 100))
        
    html = f"""
    <div class="gauge-container">
        <div class="gauge-header">
            <span>{name}</span>
            <span style="color: {color}">{val} {unit} ({status})</span>
        </div>
        <div class="gauge-bar-bg">
            <div class="gauge-bar-fill" style="width: {width}%; background-color: {color};"></div>
        </div>
        <div class="gauge-labels">
            <span>0</span>
            <span>Норма: {norm_min}–{norm_max}</span>
            <span>{crit_val if is_high_bad else (norm_max * 1.5):.1f}</span>
        </div>
    </div>
    """
    return html

val_t = st.number_input("Температура (°C)", value=float((spec['t'][0]+spec['t'][1])/2), key=f"t_{machine}_{mode}")
st.markdown(get_gauge_html("Температура", val_t, spec['t'][0], spec['t'][1], spec['t'][2], True, "°C"), unsafe_allow_html=True)

val_p = st.number_input("Давление масла (бар)", value=float((spec['p'][0]+spec['p'][1])/2), key=f"p_{machine}_{mode}")
st.markdown(get_gauge_html("Давление", val_p, spec['p'][0], spec['p'][1], spec['p'][2], False, "бар"), unsafe_allow_html=True)

val_v = st.number_input("Вибрация (мм/с)", value=float((spec['v'][0]+spec['v'][1])/2), key=f"v_{machine}_{mode}")
st.markdown(get_gauge_html("Вибрация", val_v, spec['v'][0], spec['v'][1], spec['v'][2], True, "мм/с"), unsafe_allow_html=True)

# === 5. РЕЗУЛЬТАТ ===
st.subheader("5. Результат диагностики")

if st.button("Выполнить диагностику", type="primary"):
    score = 0
    reasons = []
    actions = []
    links = set()

    # Анализ температуры
    if val_t > spec['t'][2]:
        score += 2
        reasons.append(f"Температура {val_t}°C критически высокая.")
        actions.append("Остановите двигатель, проверьте охлаждающую жидкость и радиатор.")
        links.add("cooling")
    elif val_t > spec['t'][1]:
        score += 1
        reasons.append(f"Температура {val_t}°C повышена.")
        actions.append("Снизьте нагрузку, проверьте термостат.")
        links.add("cooling")

    # Анализ давления
    if val_p < spec['p'][2]:
        score += 2
        reasons.append(f"Давление масла {val_p} бар критически низкое.")
        actions.append("Немедленно заглушите двигатель. Проверьте уровень масла и насос.")
        links.add("oil")
    elif val_p < spec['p'][0]:
        score += 1
        reasons.append(f"Давление масла {val_p} бар понижено.")
        actions.append("Проверьте уровень масла, возможна замена фильтра.")
        links.add("oil")

    # Анализ вибрации
    if val_v > spec['v'][2]:
        score += 2
        reasons.append(f"Вибрация {val_v} мм/с критическая.")
        actions.append("Проверьте крепления, подшипники и балансировку.")
        links.add("vibration")
    elif val_v > spec['v'][1]:
        score += 1
        reasons.append(f"Вибрация {val_v} мм/с повышена.")
        actions.append("Осмотрите вращающиеся узлы.")
        links.add("vibration")

    # Вывод
    if score == 0:
        st.markdown(f'''
        <div class="res-box res-ok">
            <div class="res-title" style="color: #4ade80;">НОРМА</div>
            <div class="res-text">Все показатели в пределах нормы для режима <b>{mode_map[mode]}</b>.</div>
        </div>''', unsafe_allow_html=True)
    else:
        if score <= 2:
            status_cls, status_title, status_color = "res-warn", "ВНИМАНИЕ", "#fbbf24"
        else:
            status_cls, status_title, status_color = "res-crit", "ТРЕБУЕТСЯ РЕМОНТ", "#f87171"

        reasons_html = "".join([f"<li>{r}</li>" for r in reasons])
        actions_html = "".join([f"<li>{a}</li>" for a in actions])

        st.markdown(f'''
        <div class="res-box {status_cls}">
            <div class="res-title" style="color: {status_color};">{status_title}</div>
            <div class="res-text">
                <b>Отклонения:</b><ul>{reasons_html}</ul>
                <b>Рекомендации:</b><ul>{actions_html}</ul>
            </div>
        </div>''', unsafe_allow_html=True)

    # Ссылки на решения
    link_data = {
        "cooling": ("Система охлаждения (учебник)", "https://barakud.ucoz.ru/news/rukovodstvo_po_remontu_traktora_mtz_80_i_mtz_82_1984_pdf_djvu_doc_rus/2012-03-12-2322"),
        "oil": ("Смазочная система (учебник)", "https://barakud.ucoz.ru/news/rukovodstvo_po_remontu_traktora_mtz_80_i_mtz_82_1984_pdf_djvu_doc_rus/2012-03-12-2322"),
        "vibration": ("ГОСТ по вибрации", "https://protect.gost.ru/gost/details/e2ddaae8-c27d-41e4-80e7-cca0de5fb059")
    }
    
    if links:
        st.markdown("**Полезные материалы:**")
        for k in links:
            if k in link_data:
                text, url = link_data[k]
                st.markdown(f'<a class="guide-link" href="{url}" target="_blank">🔗 {text}</a><br>', unsafe_allow_html=True)
