import streamlit as st
import time

st.set_page_config(page_title="АгроСервис Диагностика", page_icon="🌾", layout="wide")

# === ОФОРМЛЕНИЕ: ПРИРОДНЫЕ ЦВЕТА + ПЛАВНЫЕ ПОЛОСКИ ===
st.markdown("""
<style>
    /* Фон — глубокий хвойный с лёгким градиентом */
    .stApp {
        background-color: #121812;
        background-image: linear-gradient(180deg, #182019 0%, #0c100d 100%);
    }
    /* Основной текст — мягкий светлый, без резкости */
    html, body, [class*="css"], .stMarkdown, p, span, label, div {
        color: #dfe6d8 !important;
    }
    h1, h2, h3 { color: #f0f4ea !important; letter-spacing: 0.3px; }

    /* === НОВЫЙ РАЗДЕЛ ВЫБОРА ТЕХНИКИ === */
    .selection-panel {
        background-color: #1c241c;
        border: 1px solid #3e4d3a;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .panel-title {
        color: #b5c9a5;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 12px;
        display: block;
    }

    /* Стилизация выпадающего списка (закрытое состояние) */
    div[data-testid="stSelectbox"] label { 
        color: #b5c9a5 !important; 
        font-weight: 600 !important; 
        font-size: 0.95rem !important;
        margin-bottom: 6px;
    }
    div[data-baseweb="select"] > div {
        background-color: #2a3429 !important; 
        color: #f0f4ea !important;
        font-weight: 600 !important; 
        font-size: 1rem !important;
        border: 1px solid #4d6144 !important; 
        border-radius: 8px !important;
        transition: all 0.2s ease;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #7a9b68 !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div[role="button"] { 
        color: #f0f4ea !important; 
        font-weight: 600 !important; 
    }

    /* Выпадающее меню (портал) — цвета хвои и светлый текст */
    div[data-baseweb="popover"] ul,
    div[data-baseweb="menu"] ul,
    ul[role="listbox"] {
        background-color: #1c241c !important;
        border: 1px solid #4d6144 !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5) !important;
    }
    div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] li,
    ul[role="listbox"] li {
        color: #dfe6d8 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        background-color: #1c241c !important;
        padding: 10px 16px !important;
    }
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="menu"] li:hover,
    ul[role="listbox"] li:hover {
        background-color: #2a3429 !important;
        color: #ffffff !important;
    }
    div[data-baseweb="popover"] li[aria-selected="true"],
    div[data-baseweb="menu"] li[aria-selected="true"],
    ul[role="listbox"] li[aria-selected="true"] {
        background-color: #384832 !important;
        color: #ffffff !important;
    }

    /* Поля ввода */
    div[data-testid="stNumberInput"] label, div[data-testid="stTextInput"] label {
        color: #b5c9a5 !important; font-weight: 600 !important; font-size: 0.95rem !important;
    }
    div[data-testid="stNumberInput"] input, div[data-testid="stTextInput"] input {
        background-color: #e8ebe4 !important; color: #121812 !important;
        font-weight: 600 !important; font-size: 1.05rem !important;
        border: 1px solid #6a7f5e !important; border-radius: 6px !important;
    }

    /* Радиокнопки (для режима работы) — стилизуем как таблетки */
    div[data-testid="stRadio"] > label {
        color: #b5c9a5 !important; font-weight: 600 !important; font-size: 0.95rem !important;
        margin-bottom: 6px;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 8px;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background-color: #2a3429 !important; 
        border: 1px solid #4d6144 !important;
        border-radius: 8px !important; 
        padding: 8px 16px !important; 
        margin: 0 !important;
        transition: all 0.2s ease;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover { 
        border-color: #7a9b68 !important; 
        background-color: #384832 !important; 
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label p { 
        color: #dfe6d8 !important; 
        font-weight: 600 !important; 
        font-size: 0.95rem !important;
    }

    /* Карточки результатов */
    .result-card { 
        padding: 24px; border-radius: 10px; margin-top: 16px; 
        border-left: 6px solid #444; background-color: #1c241c; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.4); 
    }
    .result-card p { color: #dfe6d8 !important; font-size: 1.05rem; line-height: 1.5; }
    .status-ok { border-left-color: #81c784; background-color: #1c2a1d; }
    .status-warn { border-left-color: #e0b651; background-color: #2a2618; }
    .status-crit { border-left-color: #e57373; background-color: #2a1c1c; }
    .status-ok h2 { color: #81c784 !important; }
    .status-warn h2 { color: #e0b651 !important; }
    .status-crit h2 { color: #e57373 !important; }

    /* Блоки нормативов */
    .spec-box { 
        background-color: #1c241c; padding: 12px 16px; border-radius: 8px; 
        border: 1px solid #3e4d3a; margin-bottom: 8px; 
        font-size: 1rem; color: #dfe6d8 !important; line-height: 1.5; 
    }

    /* Зафиксированные параметры */
    .fixed-param { 
        background-color: #242e22; padding: 12px 16px; border-radius: 8px; 
        border: 1px solid #4d6144; margin-bottom: 8px; 
        color: #f0f4ea !important; font-size: 1rem; line-height: 1.5; 
    }
    .fixed-param strong { color: #b5c9a5 !important; }

    /* Ссылки-гайды */
    .guide-link { 
        display: inline-block; margin-top: 12px; padding: 12px 20px; 
        background-color: #384832; color: #f0f4ea !important; border-radius: 8px; 
        text-decoration: none; border: 1px solid #5c7052; font-size: 1rem; font-weight: 600; 
    }
    .guide-link:hover { background-color: #4d6144; border-color: #81c784; }
    .threshold-note { font-size: 0.85em; color: #8a9e7a !important; margin-top: 20px; }

    /* Кнопка */
    .stButton > button { 
        background-color: #4d6144 !important; color: #ffffff !important; 
        font-weight: 700 !important; font-size: 1.05rem !important; 
        border: 1px solid #6a7f5e !important; padding: 12px 24px !important; border-radius: 8px !important; 
        transition: all 0.2s ease;
    }
    .stButton > button:hover { background-color: #5c7052 !important; border-color: #81c784 !important; }
    hr { border-color: #3e4d3a !important; }

    /* === ПЛАВНЫЕ ИНТЕРАКТИВНЫЕ ПОЛОСКИ === */
    .gauge-container { margin-bottom: 20px; }
    .gauge-header { 
        display: flex; justify-content: space-between; margin-bottom: 6px; 
        font-weight: 600; font-size: 1rem; color: #dfe6d8; 
    }
    .gauge-bar-bg { 
        width: 100%; height: 22px; 
        background: linear-gradient(90deg, #e57373 0%, #81c784 20%, #81c784 60%, #e0b651 80%, #e57373 100%);
        border-radius: 11px; overflow: hidden; 
        border: 1px solid #3e4d3a;
        position: relative;
    }
    .gauge-bar-fill { 
        height: 100%; background: rgba(255, 255, 255, 0.2); 
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 11px; 
        box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
    }
    .gauge-pointer {
        position: absolute; top: -2px; width: 4px; height: 26px;
        background-color: #ffffff; border-radius: 2px;
        box-shadow: 0 0 6px rgba(0,0,0,0.8);
        transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        transform: translateX(-50%); z-index: 10;
    }
    .gauge-labels { 
        display: flex; justify-content: space-between; 
        font-size: 0.8rem; color: #8a9e7a; margin-top: 4px; 
    }
</style>
""", unsafe_allow_html=True)

st.title("АгроСервис: Диагностика техники")
st.markdown('<p style="font-size:1.05rem; color:#8a9e7a;">Выберите машину и режим работы — нормативы подставятся автоматически</p>', unsafe_allow_html=True)

# === БАЗА НОРМАТИВОВ ===
DEFAULT_MACHINES = {
    "МТЗ-80/82 (Д-240)": {
        "temp": {
            "idle":     {"min": 70, "max": 85, "crit_high": 95,  "label": "Температура ОЖ (°C)", "note": "Холостой ход: 70–85°C, критично выше 95°C"},
            "drive":    {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)", "note": "Езда: 80–95°C, критично выше 105°C"},
            "load":     {"min": 85, "max": 100, "crit_high": 108, "label": "Температура ОЖ (°C)", "note": "Под нагрузкой: 85–100°C, критично выше 108°C"},
        },
        "pressure": {
            "idle":     {"min": 0.8, "max": 2.0, "crit_low": 0.5, "label": "Давление масла (бар)", "note": "Холостой ход: 0.8–2.0 бар, мин. 0.5 бар"},
            "drive":    {"min": 2.0, "max": 3.5, "crit_low": 1.0, "label": "Давление масла (бар)", "note": "Езда: 2.0–3.5 бар, мин. 1.0 бар"},
            "load":     {"min": 2.5, "max": 4.5, "crit_low": 1.5, "label": "Давление масла (бар)", "note": "Под нагрузкой: 2.5–4.5 бар, мин. 1.5 бар"},
        },
        "vibration": {
            "idle":     {"min": 0, "max": 3.0, "crit_high": 5.0, "label": "Вибрация (мм/с)", "note": "Холостой ход: до 3.0 мм/с, критично выше 5.0 мм/с"},
            "drive":    {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)", "note": "Езда: до 4.5 мм/с, критично выше 7.1 мм/с"},
            "load":     {"min": 0, "max": 5.5, "crit_high": 8.0, "label": "Вибрация (мм/с)", "note": "Под нагрузкой: до 5.5 мм/с, критично выше 8.0 мм/с"},
        }
    },
    "John Deere PowerTech": {
        "temp": {
            "idle":     {"min": 70, "max": 85, "crit_high": 95,  "label": "Температура ОЖ (°C)", "note": "Холостой ход: 70–85°C, критично выше 95°C"},
            "drive":    {"min": 82, "max": 94, "crit_high": 104, "label": "Температура ОЖ (°C)", "note": "Езда: 82–94°C, критично выше 104°C"},
            "load":     {"min": 85, "max": 100, "crit_high": 108, "label": "Температура ОЖ (°C)", "note": "Под нагрузкой: 85–100°C, критично выше 108°C"},
        },
        "pressure": {
            "idle":     {"min": 1.4, "max": 2.9, "crit_low": 0.8, "label": "Давление масла (бар)", "note": "Холостой ход: 1.4–2.9 бар, мин. 0.8 бар"},
            "drive":    {"min": 2.9, "max": 4.5, "crit_low": 1.4, "label": "Давление масла (бар)", "note": "Езда: 2.9–4.5 бар, мин. 1.4 бар"},
            "load":     {"min": 3.5, "max": 5.5, "crit_low": 2.0, "label": "Давление масла (бар)", "note": "Под нагрузкой: 3.5–5.5 бар, мин. 2.0 бар"},
        },
        "vibration": {
            "idle":     {"min": 0, "max": 3.0, "crit_high": 5.0, "label": "Вибрация (мм/с)", "note": "Холостой ход: до 3.0 мм/с, критично выше 5.0 мм/с"},
            "drive":    {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)", "note": "Езда: до 4.5 мм/с, критично выше 7.1 мм/с"},
            "load":     {"min": 0, "max": 5.5, "crit_high": 8.0, "label": "Вибрация (мм/с)", "note": "Под нагрузкой: до 5.5 мм/с, критично выше 8.0 мм/с"},
        }
    },
    "ХТЗ-181 (Т-150)": {
        "temp": {
            "idle":     {"min": 70, "max": 85, "crit_high": 95,  "label": "Температура ОЖ (°C)", "note": "Холостой ход: 70–85°C, критично выше 95°C"},
            "drive":    {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)", "note": "Езда: 80–95°C, критично выше 105°C"},
            "load":     {"min": 85, "max": 100, "crit_high": 108, "label": "Температура ОЖ (°C)", "note": "Под нагрузкой: 85–100°C, критично выше 108°C"},
        },
        "pressure": {
            "idle":     {"min": 2.0, "max": 4.0, "crit_low": 1.5, "label": "Давление масла (бар)", "note": "Холостой ход: 2.0–4.0 бар, мин. 1.5 бар"},
            "drive":    {"min": 4.0, "max": 7.0, "crit_low": 2.0, "label": "Давление масла (бар)", "note": "Езда: 4.0–7.0 бар, мин. 2.0 бар"},
            "load":     {"min": 5.0, "max": 8.0, "crit_low": 3.0, "label": "Давление масла (бар)", "note": "Под нагрузкой: 5.0–8.0 бар, мин. 3.0 бар"},
        },
        "vibration": {
            "idle":     {"min": 0, "max": 3.0, "crit_high": 5.0, "label": "Вибрация (мм/с)", "note": "Холостой ход: до 3.0 мм/с, критично выше 5.0 мм/с"},
            "drive":    {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)", "note": "Езда: до 4.5 мм/с, критично выше 7.1 мм/с"},
            "load":     {"min": 0, "max": 5.5, "crit_high": 8.0, "label": "Вибрация (мм/с)", "note": "Под нагрузкой: до 5.5 мм/с, критично выше 8.0 мм/с"},
        }
    },
    "Комбайн Дон-1500": {
        "temp": {
            "idle":     {"min": 70, "max": 85, "crit_high": 95,  "label": "Температура ОЖ (°C)", "note": "Холостой ход: 70–85°C, критично выше 95°C"},
            "drive":    {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)", "note": "Езда: 80–95°C, критично выше 105°C"},
            "load":     {"min": 85, "max": 100, "crit_high": 108, "label": "Температура ОЖ (°C)", "note": "Под нагрузкой: 85–100°C, критично выше 108°C"},
        },
        "pressure": {
            "idle":     {"min": 2.0, "max": 4.0, "crit_low": 1.5, "label": "Давление масла (бар)", "note": "Холостой ход: 2.0–4.0 бар, мин. 1.5 бар"},
            "drive":    {"min": 4.0, "max": 7.0, "crit_low": 2.0, "label": "Давление масла (бар)", "note": "Езда: 4.0–7.0 бар, мин. 2.0 бар"},
            "load":     {"min": 5.0, "max": 8.0, "crit_low": 3.0, "label": "Давление масла (бар)", "note": "Под нагрузкой: 5.0–8.0 бар, мин. 3.0 бар"},
        },
        "vibration": {
            "idle":     {"min": 0, "max": 3.0, "crit_high": 5.0, "label": "Вибрация (мм/с)", "note": "Холостой ход: до 3.0 мм/с, критично выше 5.0 мм/с"},
            "drive":    {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)", "note": "Езда: до 4.5 мм/с, критично выше 7.1 мм/с"},
            "load":     {"min": 0, "max": 5.5, "crit_high": 8.0, "label": "Вибрация (мм/с)", "note": "Под нагрузкой: до 5.5 мм/с, критично выше 8.0 мм/с"},
        }
    }
}

# === SESSION STATE ===
if "custom_machines" not in st.session_state:
    st.session_state.custom_machines = {}

all_machines = {**DEFAULT_MACHINES, **st.session_state.custom_machines}

# === НОВЫЙ КОМПАКТНЫЙ РАЗДЕЛ ВЫБОРА ===
st.markdown('<div class="selection-panel">', unsafe_allow_html=True)
st.markdown('<span class="panel-title">Параметры диагностики</span>', unsafe_allow_html=True)

col_sel1, col_sel2 = st.columns([1, 1])

with col_sel1:
    machine_options = list(all_machines.keys()) + ["Добавить свою технику"]
    selected = st.selectbox("Техника", machine_options)

with col_sel2:
    if selected != "Добавить свою технику":
        MODE_LABELS = {
            "idle": "Работа на холостых",
            "drive": "Езда",
            "load": "Работа с нагрузкой",
        }
        mode_key = st.radio(
            "Режим работы",
            options=list(MODE_LABELS.keys()),
            format_func=lambda k: MODE_LABELS[k],
            horizontal=True,
        )
    else:
        mode_key = "drive"
        MODE_LABELS = {"idle": "Холостой", "drive": "Езда", "load": "Нагрузка"}

st.markdown('</div>', unsafe_allow_html=True)

# === ФОРМА ДОБАВЛЕНИЯ СВОЕЙ ТЕХНИКИ ===
if selected == "Добавить свою технику":
    st.subheader("Добавление своей техники")
    st.markdown('<p style="color:#8a9e7a; font-size:1rem;">Выберите тип техники — нормативы для всех режимов подставятся автоматически и будут зафиксированы</p>', unsafe_allow_html=True)

    TEMPLATES = {
        "Трактор (классический дизель)": DEFAULT_MACHINES["МТЗ-80/82 (Д-240)"],
        "Трактор (тяжёлый, промышленный)": DEFAULT_MACHINES["ХТЗ-181 (Т-150)"],
        "Комбайн (самоходный)": DEFAULT_MACHINES["Комбайн Дон-1500"],
        "Импортный трактор (John Deere / CNH)": DEFAULT_MACHINES["John Deere PowerTech"],
    }

    with st.form("add_machine_form"):
        new_name = st.text_input("Название техники", placeholder="Например: К-701 (ЯМЗ-240)")
        template_name = st.selectbox("Тип техники (шаблон нормативов)", list(TEMPLATES.keys()))
        template = TEMPLATES[template_name]

        st.markdown("**Выбранные нормативы (зафиксированы для всех режимов):**")
        for m in ["idle", "drive", "load"]:
            st.markdown(f'<div class="fixed-param"><strong>{MODE_LABELS[m]}:</strong><br>'
                        f'Температура: {template["temp"][m]["note"]}<br>'
                        f'Давление масла: {template["pressure"][m]["note"]}<br>'
                        f'Вибрация: {template["vibration"][m]["note"]}</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("Сохранить технику", type="primary")

        if submitted:
            if not new_name.strip():
                st.error("Введите название техники")
            elif new_name in all_machines:
                st.error("Техника с таким названием уже существует")
            else:
                st.session_state.custom_machines[new_name] = template
                st.success(f"Техника «{new_name}» добавлена! Выбираем её...")
                st.rerun()

    st.stop()

# === ОСНОВНОЙ ИНТЕРФЕЙС ===
spec = all_machines[selected]
cur_temp = spec["temp"][mode_key]
cur_pressure = spec["pressure"][mode_key]
cur_vibration = spec["vibration"][mode_key]

st.markdown(f"### Нормативы для: {selected} — {MODE_LABELS[mode_key]}")
st.markdown(f'<div class="spec-box">Температура: {cur_temp["note"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="spec-box">Давление масла: {cur_pressure["note"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="spec-box">Вибрация: {cur_vibration["note"]}</div>', unsafe_allow_html=True)

st.divider()

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("Показания датчиков")

    temp = st.number_input(
        cur_temp["label"],
        min_value=0.0, max_value=200.0,
        value=float((cur_temp["min"] + cur_temp["max"]) / 2),
        step=0.5,
        key=f"temp_{selected}_{mode_key}"
    )
    pressure = st.number_input(
        cur_pressure["label"],
        min_value=0.0, max_value=20.0,
        value=float((cur_pressure["min"] + cur_pressure["max"]) / 2),
        step=0.1,
        key=f"pressure_{selected}_{mode_key}"
    )
    vibration = st.number_input(
        cur_vibration["label"],
        min_value=0.0, max_value=30.0,
        value=float((cur_vibration["min"] + cur_vibration["max"]) / 2),
        step=0.1,
        key=f"vibration_{selected}_{mode_key}"
    )

    # --- ФУНКЦИЯ ДЛЯ ОТРИСОВКИ ПЛАВНОГО ИНДИКАТОРА ---
    def render_gauge(label, value, spec, unit, is_pressure=False):
        if is_pressure:
            max_scale = spec["max"] * 1.5
        else:
            max_scale = spec["crit_high"] * 1.2
        
        if max_scale == 0: max_scale = 10
        
        fill_pct = min(100, max(0, (value / max_scale) * 100))
        
        if is_pressure:
            if value < spec["crit_low"]:
                zone_text = "КРИТИЧНО (низкое)"
                color = "#e57373"
            elif value < spec["min"]:
                zone_text = "ВНИМАНИЕ (низкое)"
                color = "#e0b651"
            elif value > spec["max"]:
                zone_text = "ВНИМАНИЕ (высокое)"
                color = "#e0b651"
            else:
                zone_text = "НОРМА"
                color = "#81c784"
        else:
            if value > spec["crit_high"]:
                zone_text = "КРИТИЧНО"
                color = "#e57373"
            elif value > spec["max"]:
                zone_text = "ВНИМАНИЕ"
                color = "#e0b651"
            elif value < spec["min"]:
                zone_text = "ВНИМАНИЕ (низкое)"
                color = "#e0b651"
            else:
                zone_text = "НОРМА"
                color = "#81c784"

        st.markdown(f'''
        <div class="gauge-container">
            <div class="gauge-header">
                <span>{label}</span>
                <span style="color: {color};">{value} {unit} — {zone_text}</span>
            </div>
            <div class="gauge-bar-bg">
                <div class="gauge-bar-fill" style="width: {fill_pct}%;"></div>
                <div class="gauge-pointer" style="left: {fill_pct}%;"></div>
            </div>
            <div class="gauge-labels">
                <span style="color:#e57373;">0</span>
                <span style="color:#81c784;">Норма: {spec["min"]}–{spec["max"]}</span>
                <span style="color:#e57373;">{max_scale:.1f}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    render_gauge("Температура", temp, cur_temp, "°C")
    render_gauge("Давление масла", pressure, cur_pressure, "бар", is_pressure=True)
    render_gauge("Вибрация", vibration, cur_vibration, "мм/с")


def diagnose(temp_spec, pressure_spec, vibration_spec, mode_label, temp, pressure, vibration):
    score = 0
    reasons = []
    advice = []
    guide_key = None

    t = temp_spec
    if temp > t["crit_high"]:
        score += 2
        reasons.append(f"Температура {temp}°C — критическая для режима «{mode_label}» (норма {t['min']}–{t['max']}°C)")
        advice.append("остановите двигатель и дайте остыть")
        guide_key = "cooling"
    elif temp > t["max"] or temp < t["min"]:
        score += 1
        reasons.append(f"Температура {temp}°C — вне диапазона {t['min']}–{t['max']}°C для режима «{mode_label}»")
        advice.append("проверьте систему охлаждения и термостат")
        guide_key = "cooling"

    p = pressure_spec
    if pressure < p["crit_low"]:
        score += 2
        reasons.append(f"Давление масла {pressure} бар — критически низкое для режима «{mode_label}» (мин. {p['crit_low']} бар)")
        advice.append("немедленно заглушите двигатель")
        guide_key = "oil"
    elif pressure < p["min"] or pressure > p["max"]:
        score += 1
        reasons.append(f"Давление масла {pressure} бар — вне нормы {p['min']}–{p['max']} бар для режима «{mode_label}»")
        advice.append("проверьте уровень масла и масляный насос")
        guide_key = "oil"

    v = vibration_spec
    if vibration > v["crit_high"]:
        score += 2
        reasons.append(f"Вибрация {vibration} мм/с — критическая для режима «{mode_label}» (норма до {v['max']} мм/с)")
        advice.append("проверьте подшипники, крепления, балансировку")
        guide_key = "vibration"
    elif vibration > v["max"]:
        score += 1
        reasons.append(f"Вибрация {vibration} мм/с — повышена для режима «{mode_label}» (норма до {v['max']} мм/с)")
        advice.append("осмотрите вращающиеся узлы")
        guide_key = "vibration"

    if score == 0:
        return "ok", f"Все показатели в пределах нормы для режима «{mode_label}».", "Продолжайте эксплуатацию.", None
    elif score <= 2:
        return "warn", "Отклонения: " + "; ".join(reasons) + ".", "Рекомендация: " + "; ".join(advice) + ".", guide_key
    else:
        return "crit", "К
