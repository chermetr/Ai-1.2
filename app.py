import streamlit as st
import time

st.set_page_config(page_title="АгроСервис Диагностика", page_icon="🌾", layout="wide")

# === ОФОРМЛЕНИЕ: ВЫСОКИЙ КОНТРАСТ + ПЛАВНЫЕ ПОЛОСКИ ===
st.markdown("""
<style>
    /* Фон — глубокий тёмный, чтобы светлый текст читался идеально */
    .stApp {
        background-color: #0f1410;
        background-image: linear-gradient(180deg, #161d17 0%, #0a0d0a 100%);
    }
    /* Весь основной текст — светлый и яркий */
    html, body, [class*="css"], .stMarkdown, p, span, label, div {
        color: #f0f4ea !important;
    }
    h1, h2, h3 { color: #ffffff !important; letter-spacing: 0.3px; }

    /* Поле выбора техники — яркий читаемый контраст */
    div[data-testid="stSelectbox"] label { 
        color: #b8d4a8 !important; font-weight: 700 !important; font-size: 1.1rem !important; 
    }
    div[data-baseweb="select"] > div {
        background-color: #2c3a28 !important; 
        color: #f0f4ea !important;
        font-weight: 700 !important; font-size: 1.05rem !important;
        border: 2px solid #6a9a3a !important; border-radius: 8px !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div[role="button"] { 
        color: #f0f4ea !important; font-weight: 700 !important; 
    }

    /* Выпадающий список (портал) — контрастный */
    div[data-baseweb="popover"] ul,
    div[data-baseweb="menu"] ul,
    ul[role="listbox"] {
        background-color: #1a241a !important;
        border: 2px solid #6a9a3a !important;
    }
    div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] li,
    ul[role="listbox"] li {
        color: #f0f4ea !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        background-color: #1a241a !important;
    }
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="menu"] li:hover,
    ul[role="listbox"] li:hover {
        background-color: #3a5a2e !important;
        color: #ffffff !important;
    }
    div[data-baseweb="popover"] li[aria-selected="true"],
    div[data-baseweb="menu"] li[aria-selected="true"],
    ul[role="listbox"] li[aria-selected="true"] {
        background-color: #4d7c3a !important;
        color: #ffffff !important;
    }

    /* Поля ввода — белый фон, тёмный текст */
    div[data-testid="stNumberInput"] label, div[data-testid="stTextInput"] label {
        color: #b8d4a8 !important; font-weight: 600 !important; font-size: 1rem !important;
    }
    div[data-testid="stNumberInput"] input, div[data-testid="stTextInput"] input {
        background-color: #ffffff !important; color: #0f1410 !important;
        font-weight: 700 !important; font-size: 1.05rem !important;
        border: 2px solid #6a9a3a !important; border-radius: 6px !important;
    }

    /* Радиокнопки — читаемые карточки */
    div[data-testid="stRadio"] label { color: #b8d4a8 !important; font-weight: 600 !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background-color: #1a241a !important; border: 2px solid #4d6b3a !important;
        border-radius: 8px !important; padding: 8px 14px !important; margin-right: 8px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover { 
        border-color: #9ccc65 !important; background-color: #2c3a28 !important; 
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label p { 
        color: #ffffff !important; font-weight: 700 !important; 
    }

    /* Карточки результатов */
    .result-card { 
        padding: 24px; border-radius: 10px; margin-top: 16px; 
        border-left: 8px solid #444; background-color: #1a241a; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.5); 
    }
    .result-card p { color: #f0f4ea !important; font-size: 1.05rem; line-height: 1.5; }
    .status-ok { border-left-color: #66bb6a; background-color: #1b2e1b; }
    .status-warn { border-left-color: #ffca28; background-color: #2e2a1a; }
    .status-crit { border-left-color: #ef5350; background-color: #2e1a1a; }
    .status-ok h2 { color: #81c784 !important; }
    .status-warn h2 { color: #ffd54f !important; }
    .status-crit h2 { color: #e57373 !important; }

    /* Блоки нормативов */
    .spec-box { 
        background-color: #1a241a; padding: 12px 16px; border-radius: 8px; 
        border: 2px solid #4d6b3a; margin-bottom: 8px; 
        font-size: 1rem; color: #f0f4ea !important; line-height: 1.5; 
    }

    /* Зафиксированные параметры */
    .fixed-param { 
        background-color: #22301f; padding: 12px 16px; border-radius: 8px; 
        border: 2px solid #5a7d42; margin-bottom: 8px; 
        color: #f0f4ea !important; font-size: 1rem; line-height: 1.5; 
    }
    .fixed-param strong { color: #b8d4a8 !important; }

    /* Ссылки-гайды */
    .guide-link { 
        display: inline-block; margin-top: 12px; padding: 12px 20px; 
        background-color: #4d6b3a; color: #ffffff !important; border-radius: 8px; 
        text-decoration: none; border: 2px solid #6a9a3a; font-size: 1rem; font-weight: 700; 
    }
    .guide-link:hover { background-color: #5a7d42; border-color: #9ccc65; }
    .threshold-note { font-size: 0.85em; color: #b8d4a8 !important; margin-top: 20px; }

    /* Кнопка */
    .stButton > button { 
        background-color: #4d6b3a !important; color: #ffffff !important; 
        font-weight: 800 !important; font-size: 1.1rem !important; 
        border: 2px solid #6a9a3a !important; padding: 14px 24px !important; border-radius: 8px !important; 
    }
    .stButton > button:hover { background-color: #5a7d42 !important; border-color: #9ccc65 !important; }
    hr { border-color: #4d6b3a !important; }

    /* === ПЛАВНЫЕ ИНТЕРАКТИВНЫЕ ПОЛОСКИ (КРАСНЫЙ-ЗЕЛЁНЫЙ-ЖЁЛТЫЙ-КРАСНЫЙ) === */
    .gauge-container { margin-bottom: 20px; }
    .gauge-header { 
        display: flex; justify-content: space-between; margin-bottom: 6px; 
        font-weight: 700; font-size: 1.05rem; color: #ffffff; 
    }
    /* Фон полоски — шкала с зонами (красный → зелёный → жёлтый → красный) */
    .gauge-bar-bg { 
        width: 100%; height: 24px; 
        background: linear-gradient(90deg, #ef5350 0%, #66bb6a 20%, #66bb6a 60%, #ffca28 80%, #ef5350 100%);
        border-radius: 12px; overflow: hidden; 
        border: 1px solid #4d6b3a;
        position: relative;
    }
    /* Заполнение — полупрозрачный белый слой поверх шкалы, чтобы было видно, куда смотрит стрелка */
    .gauge-bar-fill { 
        height: 100%; background: rgba(255, 255, 255, 0.3); 
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1); /* Плавная анимация */
        border-radius: 12px; 
        box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
    }
    /* Указатель (стрелка) на полоске */
    .gauge-pointer {
        position: absolute;
        top: -2px;
        width: 4px;
        height: 28px;
        background-color: #ffffff;
        border-radius: 2px;
        box-shadow: 0 0 8px rgba(0,0,0,0.8);
        transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1); /* Плавное движение */
        transform: translateX(-50%);
        z-index: 10;
    }
    .gauge-labels { 
        display: flex; justify-content: space-between; 
        font-size: 0.8rem; color: #b8d4a8; margin-top: 4px; 
    }
</style>
""", unsafe_allow_html=True)

st.title("АгроСервис: Диагностика техники")
st.markdown('<p style="font-size:1.1rem; color:#b8d4a8;">Выберите машину и режим работы — нормативы подставятся автоматически</p>', unsafe_allow_html=True)

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

# === ВЫБОР ТЕХНИКИ ===
machine_options = list(all_machines.keys()) + ["Добавить свою технику"]
selected = st.selectbox("Выберите технику", machine_options)

# === ВЫБОР РЕЖИМА РАБОТЫ ===
MODE_LABELS = {
    "idle": "Работа на холостых",
    "drive": "Езда",
    "load": "Работа с нагрузкой",
}
if selected != "Добавить свою технику":
    mode_key = st.radio(
        "Режим работы",
        options=list(MODE_LABELS.keys()),
        format_func=lambda k: MODE_LABELS[k],
        horizontal=True,
    )
else:
    mode_key = "drive"

# === ФОРМА ДОБАВЛЕНИЯ СВОЕЙ ТЕХНИКИ ===
if selected == "Добавить свою технику":
    st.subheader("Добавление своей техники")
    st.markdown('<p style="color:#b8d4a8; font-size:1rem;">Выберите тип техники — нормативы для всех режимов подставятся автоматически и будут зафиксированы</p>', unsafe_allow_html=True)

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
        # Определяем максимум шкалы (немного больше критического значения для наглядности)
        if is_pressure:
            max_scale = spec["max"] * 1.5
        else:
            max_scale = spec["crit_high"] * 1.2
        
        if max_scale == 0: max_scale = 10
        
        # Вычисляем процент заполнения и позицию указателя
        fill_pct = min(100, max(0, (value / max_scale) * 100))
        
        # Визуальное определение зоны (для текста/подсказки)
        if is_pressure:
            if value < spec["crit_low"]:
                zone_text = "КРИТИЧНО (низкое)"
            elif value < spec["min"]:
                zone_text = "ВНИМАНИЕ (низкое)"
            elif value > spec["max"]:
                zone_text = "ВНИМАНИЕ (высокое)"
            else:
                zone_text = "НОРМА"
        else:
            if value > spec["crit_high"]:
                zone_text = "КРИТИЧНО"
            elif value > spec["max"]:
                zone_text = "ВНИМАНИЕ"
            elif value < spec["min"]:
                zone_text = "ВНИМАНИЕ (низкое)"
            else:
                zone_text = "НОРМА"

        st.markdown(f'''
        <div class="gauge-container">
            <div class="gauge-header">
                <span>{label}</span>
                <span style="color: {'#ef5350' if 'КРИТИЧНО' in zone_text else '#ffca28' if 'ВНИМАНИЕ' in zone_text else '#66bb6a'};">
                    {value} {unit} — {zone_text}
                </span>
            </div>
            <div class="gauge-bar-bg">
                <div class="gauge-bar-fill" style="width: {fill_pct}%;"></div>
                <div class="gauge-pointer" style="left: {fill_pct}%;"></div>
            </div>
            <div class="gauge-labels">
                <span style="color:#ef5350;">0</span>
                <span style="color:#66bb6a;">Норма: {spec["min"]}–{spec["max"]}</span>
                <span style="color:#ef5350;">{max_scale:.1f}</span>
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
        return "crit", "Критические показатели: " + "; ".join(reasons) + "!", "Требуется вмешательство: " + "; ".join(advice) + ".", guide_key


GUIDES = {
    "cooling": ("Руководство: Система охлаждения МТЗ", "https://barakud.ucoz.ru/news/rukovodstvo_po_remontu_traktora_mtz_80_i_mtz_82_1984_pdf_djvu_doc_rus/2012-03-12-2322"),
    "oil": ("Руководство: Смазочная система и давление масла", "https://barakud.ucoz.ru/news/rukovodstvo_po_remontu_traktora_mtz_80_i_mtz_82_1984_pdf_djvu_doc_rus/2012-03-12-2322"),
    "vibration": ("ГОСТ Р ИСО 20816-1-2021: Оценка вибрации", "https://protect.gost.ru/gost/details/e2ddaae8-c27d-41e4-80e7-cca0de5fb059"),
}

with col_right:
    st.subheader("Результат диагностики")

    if st.button("Выполнить анализ", type="primary", use_container_width=True):
        with st.spinner("Обработка данных..."):
            time.sleep(0.4)
            status, explanation, recommendation, guide_key = diagnose(
                cur_temp, cur_pressure, cur_vibration, MODE_LABELS
