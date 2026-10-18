import streamlit as st
import time

st.set_page_config(page_title="АгроСервис Диагностика", page_icon="🌾", layout="wide")

# === ОФОРМЛЕНИЕ: СЕЛЬХОЗ ИНДУСТРИЯ, СЕРЬЁЗНЫЙ СТИЛЬ ===
st.markdown("""
<style>
    /* Фон — тёмная земля с зеленоватым оттенком */
    .stApp {
        background-color: #141a10;
        background-image: linear-gradient(180deg, #1c2416 0%, #10150c 100%);
    }
    html, body, [class*="css"], .stMarkdown, p, span, label, div {
        color: #e6ebd8 !important;
    }
    h1, h2, h3 { color: #f2f5ea !important; letter-spacing: 0.3px; }

    /* Поле выбора техники — цвет спелой пшеницы */
    div[data-testid="stSelectbox"] label {
        color: #c9d6a8 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #d9c68a !important;
        color: #2b2410 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border: 2px solid #a3841f !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div[role="button"] {
        color: #2b2410 !important;
        font-weight: 700 !important;
    }

    /* ИСПРАВЛЕНИЕ: Открытое выпадающее меню — тёмный фон, светлый текст */
    ul[role="listbox"] {
        background-color: #1f2718 !important;
        border: 1px solid #a3841f !important;
    }
    ul[role="listbox"] li {
        color: #f2f5ea !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        background-color: #1f2718 !important;
    }
    ul[role="listbox"] li:hover {
        background-color: #3f4d33 !important;
        color: #ffffff !important;
    }
    ul[role="listbox"] li[aria-selected="true"] {
        background-color: #4d6b2a !important;
        color: #ffffff !important;
    }

    /* Поля ввода — светлый фон, тёмный текст */
    div[data-testid="stNumberInput"] label,
    div[data-testid="stTextInput"] label {
        color: #c9d6a8 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input {
        background-color: #eef0e4 !important;
        color: #1c2416 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }

    /* Радиокнопки режима работы — тёмные карточки с зелёным акцентом */
    div[data-testid="stRadio"] label {
        color: #c9d6a8 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background-color: #222b1b !important;
        border: 1px solid #3f4d33 !important;
        border-radius: 8px !important;
        padding: 8px 14px !important;
        margin-right: 8px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        border-color: #7a8f3c !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label p {
        color: #e6ebd8 !important;
        font-weight: 600 !important;
    }

    /* Карточки */
    .result-card {
        padding: 24px; border-radius: 10px; margin-top: 16px;
        border-left: 6px solid #444; background-color: #1f2718;
        box-shadow: 0 2px 10px rgba(0,0,0,0.4);
    }
    .result-card p { color: #e6ebd8 !important; font-size: 1.05rem; line-height: 1.5; }
    .status-ok { border-left-color: #6a9a3a; }
    .status-warn { border-left-color: #c99a2e; }
    .status-crit { border-left-color: #b3402e; }
    .status-ok h2 { color: #9cc46a !important; }
    .status-warn h2 { color: #e0b651 !important; }
    .status-crit h2 { color: #e07864 !important; }

    /* Блоки нормативов */
    .spec-box {
        background-color: #1f2718; padding: 12px 16px; border-radius: 8px;
        border: 1px solid #3f4d33; margin-bottom: 8px;
        font-size: 1rem; color: #e6ebd8 !important; line-height: 1.5;
    }

    /* Зафиксированные параметры */
    .fixed-param {
        background-color: #26301d; padding: 12px 16px; border-radius: 8px;
        border: 1px solid #4d5c3c; margin-bottom: 8px;
        color: #d4e0bc !important; font-size: 1rem; line-height: 1.5;
    }
    .fixed-param strong { color: #b7cf8e !important; }

    /* Ссылки-гайды */
    .guide-link {
        display: inline-block; margin-top: 12px; padding: 10px 18px;
        background-color: #2c3824; color: #b7cf8e !important; border-radius: 6px;
        text-decoration: none; border: 1px solid #4d5c3c; font-size: 1rem;
        font-weight: 600;
    }
    .guide-link:hover { background-color: #3a4a2e; color: #cfe0a6 !important; }

    .threshold-note { font-size: 0.85em; color: #9aa884 !important; margin-top: 20px; }

    /* Кнопка — цвет поля */
    .stButton > button {
        background-color: #4d6b2a !important; color: #f2f5ea !important;
        font-weight: 700 !important; font-size: 1.05rem !important;
        border: 1px solid #6a8a3e !important; padding: 12px 20px !important;
    }
    .stButton > button:hover { background-color: #5c7d34 !important; }

    hr { border-color: #3f4d33 !important; }
</style>
""", unsafe_allow_html=True)

st.title("АгроСервис: Диагностика техники")
st.markdown('<p style="font-size:1.1rem; color:#c9d6a8;">Выберите машину и режим работы — нормативы подставятся автоматически</p>', unsafe_allow_html=True)

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
    st.markdown('<p style="color:#c9d6a8; font-size:1rem;">Выберите тип техники — нормативы для всех режимов подставятся автоматически и будут зафиксированы</p>', unsafe_allow_html=True)

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
        f'<p style="color:#9aa884; font-size:0.9rem;">Диапазоны: '
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
        <div class="result-card" style="border-left-color: #3f4d33;">
            <h2 style="color: #7d8b6a !important;">—</h2>
            <p>Нажмите кнопку для анализа показаний.</p>
        </div>''', unsafe_allow_html=True)

st.markdown('---')
st.markdown('<p class="threshold-note">Пороги зависят от выбранной техники и режима работы. Пользовательские нормативы сохраняются в рамках сессии.</p>', unsafe_allow_html=True)
