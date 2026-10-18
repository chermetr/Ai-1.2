import streamlit as st
import time

st.set_page_config(page_title="АгроСервис Диагностика", page_icon="🌾", layout="wide")

# === ОФОРМЛЕНИЕ: СЕЛЬХОЗ ИНДУСТРИЯ, ВЫСОКИЙ КОНТРАСТ ===
st.markdown("""
<style>
    .stApp {
        background-color: #12160e;
        background-image: linear-gradient(180deg, #182014 0%, #0e120b 100%);
    }
    html, body, [class*="css"], .stMarkdown, p, span, label, div {
        color: #e8f0e0 !important;
    }
    h1, h2, h3 { color: #ffffff !important; letter-spacing: 0.3px; }
    /* Читаемый выпадающий список техники — НОВЫЙ ЦВЕТ */
    div[data-testid="stSelectbox"] label {
        color: #d4e8c2 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #fff8e1 !important;
        color: #3e2723 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border: 2px solid #ff9800 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div[role="button"] {
        color: #3e2723 !important;
        font-weight: 700 !important;
    }
    /* Выпадающее меню — НОВЫЙ ЦВЕТ */
    ul[role="listbox"] {
        background-color: #fff8e1 !important;
    }
    ul[role="listbox"] li {
        color: #3e2723 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    ul[role="listbox"] li:hover {
        background-color: #ffe0b2 !important;
    }
    /* Поля ввода — светлый фон, тёмный текст */
    div[data-testid="stNumberInput"] label,
    div[data-testid="stTextInput"] label {
        color: #d4e8c2 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input {
        background-color: #f5f7f0 !important;
        color: #1a1f16 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    /* Карточки */
    .result-card {
        padding: 24px; border-radius: 10px; margin-top: 16px;
        border-left: 6px solid #444; background-color: #1e261a;
        box-shadow: 0 2px 10px rgba(0,0,0,0.4);
    }
    .result-card p { color: #e8f0e0 !important; font-size: 1.05rem; line-height: 1.5; }
    .status-ok { border-left-color: #4caf50; }
    .status-warn { border-left-color: #ff9800; }
    .status-crit { border-left-color: #f44336; }
    .status-ok h2 { color: #81c784 !important; }
    .status-warn h2 { color: #ffb74d !important; }
    .status-crit h2 { color: #ef5350 !important; }
    /* Блоки нормативов */
    .spec-box {
        background-color: #1e261a; padding: 12px 16px; border-radius: 8px;
        border: 1px solid #3a4a32; margin-bottom: 8px;
        font-size: 1rem; color: #e8f0e0 !important; line-height: 1.5;
    }
    /* Зафиксированные параметры */
    .fixed-param {
        background-color: #252d20; padding: 12px 16px; border-radius: 8px;
        border: 1px solid #4a5a42; margin-bottom: 8px;
        color: #c8e6c9 !important; font-size: 1rem; line-height: 1.5;
    }
    .fixed-param strong { color: #a5d6a7 !important; }
    /* Ссылки-гайды */
    .guide-link {
        display: inline-block; margin-top: 12px; padding: 10px 18px;
        background-color: #2e3a28; color: #a5d6a7 !important; border-radius: 6px;
        text-decoration: none; border: 1px solid #4a5a42; font-size: 1rem;
        font-weight: 600;
    }
    .guide-link:hover { background-color: #3a4a32; color: #c8e6c9 !important; }
    .threshold-note { font-size: 0.85em; color: #a0b090 !important; margin-top: 20px; }
    /* Кнопка */
    .stButton > button {
        background-color: #2e7d32 !important; color: #ffffff !important;
        font-weight: 700 !important; font-size: 1.05rem !important;
        border: none !important; padding: 12px 20px !important;
    }
    .stButton > button:hover { background-color: #388e3c !important; }
    hr { border-color: #3a4a32 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🌾 АгроСервис: Диагностика техники")
st.markdown('<p style="font-size:1.1rem; color:#d4e8c2;">Выберите машину — её нормативы подставятся автоматически</p>', unsafe_allow_html=True)

# === БАЗА НОРМАТИВОВ ===
DEFAULT_MACHINES = {
    "МТЗ-80/82 (Д-240)": {
        "temp": {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)",
                 "note": "Норма 80–95°C, критично выше 105°C"},
        "pressure": {"min": 2.0, "max": 3.5, "crit_low": 0.8, "label": "Давление масла (бар)",
                     "note": "Норма 2.0–3.5 бар на номинале, мин. 0.8 бар на холостых"},
        "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                      "note": "Норма до 4.5 мм/с, критично выше 7.1 мм/с"}
    },
    "John Deere PowerTech": {
        "temp": {"min": 82, "max": 94, "crit_high": 104, "label": "Температура ОЖ (°C)",
                 "note": "Норма 82–94°C, при >104°C снизить нагрузку"},
        "pressure": {"min": 2.9, "max": 4.5, "crit_low": 1.4, "label": "Давление масла (бар)",
                     "note": "Норма 2.9 бар на номинале, мин. 1.4 бар на холостом"},
        "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                      "note": "Норма до 4.5 мм/с, критично выше 7.1 мм/с"}
    },
    "ХТЗ-181 (Т-150)": {
        "temp": {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)",
                 "note": "Норма 80–95°C, критично выше 105°C"},
        "pressure": {"min": 4.0, "max": 7.0, "crit_low": 2.0, "label": "Давление масла (бар)",
                     "note": "Норма 4.0–7.0 кгс/см², мин. 2.0 на холостых"},
        "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                      "note": "Норма до 4.5 мм/с, критично выше 7.1 мм/с"}
    },
    "Комбайн Дон-1500": {
        "temp": {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)",
                 "note": "Норма 80–95°C, критично выше 105°C"},
        "pressure": {"min": 4.0, "max": 7.0, "crit_low": 2.0, "label": "Давление масла (бар)",
                     "note": "Уточните по паспорту двигателя СМД"},
        "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                      "note": "Норма до 4.5 мм/с, критично выше 7.1 мм/с"}
    }
}

# === SESSION STATE ===
if "custom_machines" not in st.session_state:
    st.session_state.custom_machines = {}

all_machines = {**DEFAULT_MACHINES, **st.session_state.custom_machines}

# === ВЫБОР ТЕХНИКИ ===
machine_options = list(all_machines.keys()) + ["➕ Добавить свою технику"]
selected = st.selectbox("🚜 Выберите технику", machine_options)

# === ФОРМА ДОБАВЛЕНИЯ СВОЕЙ ТЕХНИКИ ===
if selected == "➕ Добавить свою технику":
    st.subheader("Добавление своей техники")
    st.markdown('<p style="color:#d4e8c2; font-size:1rem;">Выберите тип техники — нормативы подставятся автоматически и будут зафиксированы</p>', unsafe_allow_html=True)

    TEMPLATES = {
        "Трактор (классический дизель)": {
            "temp": {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)",
                     "note": "Норма 80–95°C, критично выше 105°C"},
            "pressure": {"min": 2.0, "max": 3.5, "crit_low": 0.8, "label": "Давление масла (бар)",
                         "note": "Норма 2.0–3.5 бар, мин. 0.8 бар на холостых"},
            "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                          "note": "Норма до 4.5 мм/с, критично выше 7.1 мм/с"}
        },
        "Трактор (тяжёлый, промышленный)": {
            "temp": {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)",
                     "note": "Норма 80–95°C, критично выше 105°C"},
            "pressure": {"min": 4.0, "max": 7.0, "crit_low": 2.0, "label": "Давление масла (бар)",
                         "note": "Норма 4.0–7.0 бар, мин. 2.0 на холостых"},
            "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                          "note": "Норма до 4.5 мм/с, критично выше 7.1 мм/с"}
        },
        "Комбайн (самоходный)": {
            "temp": {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)",
                     "note": "Норма 80–95°C, критично выше 105°C"},
            "pressure": {"min": 4.0, "max": 7.0, "crit_low": 2.0, "label": "Давление масла (бар)",
                         "note": "Уточните по паспорту двигателя"},
            "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                          "note": "Норма до 4.5 мм/с, критично выше 7.1 мм/с"}
        },
        "Импортный трактор (John Deere / CNH)": {
            "temp": {"min": 82, "max": 94, "crit_high": 104, "label": "Температура ОЖ (°C)",
                     "note": "Норма 82–94°C, при >104°C снизить нагрузку"},
            "pressure": {"min": 2.9, "max": 4.5, "crit_low": 1.4, "label": "Давление масла (бар)",
                         "note": "Норма 2.9 бар на номинале, мин. 1.4 бар на холостом"},
            "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                          "note": "Норма до 4.5 мм/с, критично выше 7.1 мм/с"}
        },
    }

    with st.form("add_machine_form"):
        new_name = st.text_input("Название техники", placeholder="Например: К-701 (ЯМЗ-240)")

        template_name = st.selectbox("Тип техники (шаблон нормативов)", list(TEMPLATES.keys()))
        template = TEMPLATES[template_name]

        st.markdown("**Выбранные нормативы (зафиксированы):**")
        st.markdown(f'<div class="fixed-param">🌡️ <strong>Температура:</strong> {template["temp"]["note"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="fixed-param">🛢️ <strong>Давление масла:</strong> {template["pressure"]["note"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="fixed-param">📳 <strong>Вибрация:</strong> {template["vibration"]["note"]}</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("💾 Сохранить технику", type="primary")

        if submitted:
            if not new_name.strip():
                st.error("Введите название техники")
            elif new_name in all_machines:
                st.error("Техника с таким названием уже существует")
            else:
                st.session_state.custom_machines[new_name] = template
                st.success(f"Техника «{new_name}» добавлена! Выбираем её...")
                st.session_state.selected_machine = new_name
                st.rerun()

    st.stop()

# === ОСНОВНОЙ ИНТЕРФЕЙС ===
spec = all_machines[selected]

st.markdown(f"### Нормативы для: {selected}")
st.markdown(f'<div class="spec-box">🌡️ {spec["temp"]["note"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="spec-box">🛢️ {spec["pressure"]["note"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="spec-box">📳 {spec["vibration"]["note"]}</div>', unsafe_allow_html=True)

st.divider()

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("Показания датчиков")

    temp = st.number_input(
        spec["temp"]["label"],
        min_value=0.0, max_value=200.0,
        value=float((spec["temp"]["min"] + spec["temp"]["max"]) / 2),
        step=0.5,
        key=f"temp_{selected}"
    )
    pressure = st.number_input(
        spec["pressure"]["label"],
        min_value=0.0, max_value=20.0,
        value=float((spec["pressure"]["min"] + spec["pressure"]["max"]) / 2),
        step=0.1,
        key=f"pressure_{selected}"
    )
    vibration = st.number_input(
        spec["vibration"]["label"],
        min_value=0.0, max_value=30.0,
        value=float((spec["vibration"]["min"] + spec["vibration"]["max"]) / 2),
        step=0.1,
        key=f"vibration_{selected}"
    )

    st.markdown(
        f'<p style="color:#a0b090; font-size:0.9rem;">Диапазоны: '
        f'темп. {spec["temp"]["min"]}–{spec["temp"]["max"]}°C · '
        f'давл. {spec["pressure"]["min"]}–{spec["pressure"]["max"]} бар · '
        f'вибр. {spec["vibration"]["min"]}–{spec["vibration"]["max"]} мм/с</p>',
        unsafe_allow_html=True
    )


def diagnose(spec, temp, pressure, vibration):
    score = 0
    reasons = []
    advice = []
    guide_key = None

    t = spec["temp"]
    if temp > t["crit_high"]:
        score += 2
        reasons.append(f"Температура {temp}°C — критическая (норма {t['min']}–{t['max']}°C)")
        advice.append("остановите двигатель и дайте остыть")
        guide_key = "cooling"
    elif temp > t["max"] or temp < t["min"]:
        score += 1
        reasons.append(f"Температура {temp}°C — вне диапазона {t['min']}–{t['max']}°C")
        advice.append("проверьте систему охлаждения и термостат")
        guide_key = "cooling"

    p = spec["pressure"]
    if pressure < p["crit_low"]:
        score += 2
        reasons.append(f"Давление масла {pressure} бар — критически низкое (мин. {p['crit_low']} бар)")
        advice.append("немедленно заглушите двигатель")
        guide_key = "oil"
    elif pressure < p["min"] or pressure > p["max"]:
        score += 1
        reasons.append(f"Давление масла {pressure} бар — вне нормы {p['min']}–{p['max']} бар")
        advice.append("проверьте уровень масла и масляный насос")
        guide_key = "oil"

    v = spec["vibration"]
    if vibration > v["crit_high"]:
        score += 2
        reasons.append(f"Вибрация {vibration} мм/с — критическая (норма до {v['max']} мм/с)")
        advice.append("проверьте подшипники, крепления, балансировку")
        guide_key = "vibration"
    elif vibration > v["max"]:
        score += 1
        reasons.append(f"Вибрация {vibration} мм/с — повышена (норма до {v['max']} мм/с)")
        advice.append("осмотрите вращающиеся узлы")
        guide_key = "vibration"

    if score == 0:
        return "ok", "Все показатели в пределах нормы.", "Продолжайте эксплуатацию.", None
    elif score <= 2:
        return "warn", "Отклонения: " + "; ".join(reasons) + ".", "Рекомендация: " + "; ".join(advice) + ".", guide_key
    else:
        return "crit", "Критические показатели: " + "; ".join(reasons) + "!", "Требуется вмешательство: " + "; ".join(advice) + ".", guide_key


GUIDES = {
    "cooling": ("📖 Руководство: Система охлаждения МТЗ", "https://barakud.ucoz.ru/news/rukovodstvo_po_remontu_traktora_mtz_80_i_mtz_82_1984_pdf_djvu_doc_rus/2012-03-12-2322"),
    "oil": ("📖 Руководство: Смазочная система и давление масла", "https://barakud.ucoz.ru/news/rukovodstvo_po_remontu_traktora_mtz_80_i_mtz_82_1984_pdf_djvu_doc_rus/2012-03-12-2322"),
    "vibration": ("📖 ГОСТ Р ИСО 20816-1-2021: Оценка вибрации", "https://protect.gost.ru/gost/details/e2ddaae8-c27d-41e4-80e7-cca0de5fb059"),
}

with col_right:
    st.subheader("Результат диагностики")

    if st.button("Выполнить анализ", type="primary", use_container_width=True):
        with st.spinner("Обработка данных..."):
            time.sleep(0.4)
            status, explanation, recommendation, guide_key = diagnose(spec, temp, pressure, vibration)

        if status == "ok":
            st.markdown(f'''
            <div class="result-card status-ok">
                <h2>✅ НОРМА</h2>
                <p>{explanation}</p>
                <p><strong>{recommendation}</strong></p>
            </div>''', unsafe_allow_html=True)
        elif status == "warn":
            st.markdown(f'''
            <div class="result-card status-warn">
                <h2>⚠️ НА ГРАНИ</h2>
                <p>{explanation}</p>
                <p><strong>{recommendation}</strong></p>
            </div>''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="result-card status-crit">
                <h2>🚨 ТРЕБУЕТСЯ РЕМОНТ</h2>
                <p>{explanation}</p>
                <p><strong>{recommendation}</strong></p>
            </div>''', unsafe_allow_html=True)

        if guide_key and guide_key in GUIDES:
            label, url = GUIDES[guide_key]
            st.markdown(f'<a class="guide-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    else:
        st.markdown('''
        <div class="result-card" style="border-left-color: #3a4a32;">
            <h2 style="color: #8a9a7a !important;">—</h2>
            <p>Нажмите кнопку для анализа показаний.</p>
        </div>''', unsafe_allow_html=True)

st.markdown('---')
st.markdown('<p class="threshold-note">Пороги зависят от выбранной техники. Пользовательские нормативы сохраняются в рамках сессии.</p>', unsafe_allow_html=True)
