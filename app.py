import streamlit as st
import time

st.set_page_config(page_title="АгроСервис Диагностика", page_icon="🌾", layout="wide")

# === ОФОРМЛЕНИЕ: ЯРКИЙ СЕЛЬХОЗ СТИЛЬ ===
st.markdown("""
<style>
    /* Фон — насыщенный тёмно-зелёный */
    .stApp {
        background-color: #0d1a0f;
        background-image: linear-gradient(180deg, #142b17 0%, #081209 100%);
    }
    html, body, [class*="css"], .stMarkdown, p, span, label, div {
        color: #eaffea !important;
    }
    h1, h2, h3 { color: #ffffff !important; letter-spacing: 0.3px; }

    /* Поле выбора техники — яркое золото */
    div[data-testid="stSelectbox"] label {
        color: #a8e6a0 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffd54f !important;
        color: #1a1a1a !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border: 2px solid #ffb300 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div[role="button"] {
        color: #1a1a1a !important;
        font-weight: 700 !important;
    }

    /* Открытое выпадающее меню — тёмный фон, яркий текст */
    ul[role="listbox"] {
        background-color: #1b3a1e !important;
        border: 2px solid #ffb300 !important;
    }
    ul[role="listbox"] li {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        background-color: #1b3a1e !important;
    }
    ul[role="listbox"] li:hover {
        background-color: #2e7d32 !important;
        color: #ffffff !important;
    }
    ul[role="listbox"] li[aria-selected="true"] {
        background-color: #43a047 !important;
        color: #ffffff !important;
    }

    /* Поля ввода — светлый фон, тёмный текст */
    div[data-testid="stNumberInput"] label,
    div[data-testid="stTextInput"] label {
        color: #a8e6a0 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input {
        background-color: #ffffff !important;
        color: #0d1a0f !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border: 2px solid #43a047 !important;
        border-radius: 6px !important;
    }

    /* Радиокнопки режима работы — яркие карточки */
    div[data-testid="stRadio"] label {
        color: #a8e6a0 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background-color: #1b3a1e !important;
        border: 2px solid #2e7d32 !important;
        border-radius: 8px !important;
        padding: 8px 14px !important;
        margin-right: 8px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        border-color: #ffb300 !important;
        background-color: #2e7d32 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Карточки результатов */
    .result-card {
        padding: 24px; border-radius: 10px; margin-top: 16px;
        border-left: 8px solid #444; background-color: #1b3a1e;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .result-card p { color: #ffffff !important; font-size: 1.05rem; line-height: 1.5; }
    .status-ok { border-left-color: #00e676; background-color: #143a1a; }
    .status-warn { border-left-color: #ffb300; background-color: #3e2c0a; }
    .status-crit { border-left-color: #ff1744; background-color: #3e0e12; }
    .status-ok h2 { color: #69f0ae !important; }
    .status-warn h2 { color: #ffd54f !important; }
    .status-crit h2 { color: #ff5252 !important; }

    /* Блоки нормативов */
    .spec-box {
        background-color: #1b3a1e; padding: 12px 16px; border-radius: 8px;
        border: 2px solid #2e7d32; margin-bottom: 8px;
        font-size: 1rem; color: #ffffff !important; line-height: 1.5;
    }

    /* Зафиксированные параметры */
    .fixed-param {
        background-color: #234a28; padding: 12px 16px; border-radius: 8px;
        border: 2px solid #43a047; margin-bottom: 8px;
        color: #ffffff !important; font-size: 1rem; line-height: 1.5;
    }
    .fixed-param strong { color: #ffd54f !important; }

    /* Ссылки-гайды */
    .guide-link {
        display: inline-block; margin-top: 12px; padding: 12px 20px;
        background-color: #2e7d32; color: #ffffff !important; border-radius: 8px;
        text-decoration: none; border: 2px solid #43a047; font-size: 1rem;
        font-weight: 700;
    }
    .guide-link:hover { background-color: #43a047; border-color: #ffb300; }

    .threshold-note { font-size: 0.85em; color: #a8e6a0 !important; margin-top: 20px; }

    /* Кнопка — яркая, заметная */
    .stButton > button {
        background-color: #ffb300 !important; color: #1a1a1a !important;
        font-weight: 800 !important; font-size: 1.1rem !important;
        border: 2px solid #ffd54f !important; padding: 14px 24px !important;
        border-radius: 8px !important;
    }
    .stButton > button:hover { background-color: #ffd54f !important; border-color: #ffffff !important; }

    hr { border-color: #2e7d32 !important; }
</style>
""", unsafe_allow_html=True)

st.title("АгроСервис: Диагностика техники")
st.markdown('<p style="font-size:1.1rem; color:#a8e6a0;">Выберите машину и режим работы — нормативы подставятся автоматически</p>', unsafe_allow_html=True)

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
    st.markdown('<p style="color:#a8e6a0; font-size:1rem;">Выберите тип техники — нормативы для всех режимов подставятся автоматически и будут зафиксированы</p>', unsafe_allow_html=True)

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

    st.markdown(
        f'<p style="color:#a8e6a0; font-size:0.9rem;">Диапазоны: '
        f'темп. {cur_temp["min"]}–{cur_temp["max"]}°C · '
        f'давл. {cur_pressure["min"]}–{cur_pressure["max"]} бар · '
        f'вибр. {cur_vibration["min"]}–{cur_vibration["max"]} мм/с</p>',
        unsafe_allow_html=True
    )


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
                cur_temp, cur_pressure, cur_vibration, MODE_LABELS[mode_key], temp, pressure, vibration
            )

        if status == "ok":
            st.markdown(f'''
            <div class="result-card status-ok">
                <h2>НОРМА</h2>
                <p>{explanation}</p>
                <p><strong>{recommendation}</strong></p>
            </div>''', unsafe_allow_html=True)
        elif status == "warn":
            st.markdown(f'''
            <div class="result-card status-warn">
                <h2>НА ГРАНИ</h2>
                <p>{explanation}</p>
                <p><strong>{recommendation}</strong></p>
            </div>''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="result-card status-crit">
                <h2>ТРЕБУЕТСЯ РЕМОНТ</h2>
                <p>{explanation}</p>
                <p><strong>{recommendation}</strong></p>
            </div>''', unsafe_allow_html=True)

        if guide_key and guide_key in GUIDES:
            label, url = GUIDES[guide_key]
            st.markdown(f'<a class="guide-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    else:
        st.markdown('''
        <div class="result-card" style="border-left-color: #2e7d32;">
            <h2 style="color: #a8e6a0 !important;">—</h2>
            <p>Нажмите кнопку для анализа показаний.</p>
        </div>''', unsafe_allow_html=True)

st.markdown('---')
st.markdown('<p class="threshold-note">Пороги зависят от выбранной техники и режима работы. Пользовательские нормативы сохраняются в рамках сессии.</p>', unsafe_allow_html=True)
