import streamlit as st
import time

st.set_page_config(page_title="АгроСервис Диагностика", page_icon="🌾", layout="wide")

# === ОФОРМЛЕНИЕ В СТИЛЕ СЕЛЬХОЗ ИНДУСТРИИ ===
st.markdown("""
<style>
    .stApp {
        background-color: #1a1f16;
        background-image: linear-gradient(180deg, #1e2a1a 0%, #141a11 100%);
    }
    h1, h2, h3 { color: #d4e8c2 !important; }
    .result-card {
        padding: 24px; border-radius: 10px; margin-top: 16px;
        border-left: 6px solid #444; background-color: #252d20;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .status-ok { border-left-color: #4caf50; }
    .status-warn { border-left-color: #ff9800; }
    .status-crit { border-left-color: #f44336; }
    .status-ok h2 { color: #81c784; }
    .status-warn h2 { color: #ffb74d; }
    .status-crit h2 { color: #ef5350; }
    .guide-link {
        display: inline-block; margin-top: 12px; padding: 10px 18px;
        background-color: #2e3a28; color: #a5d6a7; border-radius: 6px;
        text-decoration: none; border: 1px solid #3a4a32; font-size: 0.95em;
    }
    .guide-link:hover { background-color: #3a4a32; color: #c8e6c9; }
    .threshold-note { font-size: 0.8em; color: #8a9a7a; margin-top: 20px; }
    .spec-box {
        background-color: #1e261a; padding: 12px 16px; border-radius: 8px;
        border: 1px solid #2e3a28; margin-bottom: 8px; font-size: 0.9em;
        color: #b0c4a0;
    }
    div[data-testid="stSelectbox"] label { color: #a5d6a7 !important; }
    div[data-testid="stNumberInput"] label { color: #c8e6c9 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🌾 АгроСервис: Диагностика техники")
st.caption("Выберите машину или создайте свою, укажите показания датчиков — система оценит состояние")

# === БАЗА НОРМАТИВОВ ===
DEFAULT_MACHINES = {
    "МТЗ-80/82 (Д-240)": {
        "temp": {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)",
                 "note": "Норма 80–95°C, критично выше 105°C"},
        "pressure": {"min": 2.0, "max": 3.5, "crit_low": 0.8, "label": "Давление масла (бар)",
                     "note": "Норма 2.0–3.5 бар на номинале, мин. 0.8 бар на холостых [citation:21]"},
        "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                      "note": "Норма до 4.5 мм/с (зона B), критично выше 7.1 мм/с (зона D) [citation:22]"}
    },
    "John Deere PowerTech": {
        "temp": {"min": 82, "max": 94, "crit_high": 104, "label": "Температура ОЖ (°C)",
                 "note": "Норма 82–94°C, при >104°C снизить нагрузку"},
        "pressure": {"min": 2.9, "max": 4.5, "crit_low": 1.4, "label": "Давление масла (бар)",
                     "note": "Норма 2.9 бар на номинале (масло 105°C), мин. 1.4 бар на холостом [citation:11][citation:26]"},
        "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                      "note": "Норма до 4.5 мм/с, критично выше 7.1 мм/с [citation:22]"}
    },
    "ХТЗ-181 (Т-150)": {
        "temp": {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)",
                 "note": "Норма 80–95°C, критично выше 105°C"},
        "pressure": {"min": 4.0, "max": 7.0, "crit_low": 2.0, "label": "Давление масла (бар)",
                     "note": "Норма 4.0–7.0 кгс/см² на номинале, мин. 2.0 на холостых [citation:15]"},
        "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                      "note": "Норма до 4.5 мм/с, критично выше 7.1 мм/с [citation:22]"}
    },
    "Комбайн Дон-1500": {
        "temp": {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)",
                 "note": "Норма 80–95°C, критично выше 105°C"},
        "pressure": {"min": 4.0, "max": 7.0, "crit_low": 2.0, "label": "Давление масла (бар)",
                     "note": "Уточните по паспорту двигателя СМД"},
        "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                      "note": "Норма до 4.5 мм/с, критично выше 7.1 мм/с [citation:22]"}
    }
}

# === ИНИЦИАЛИЗАЦИЯ СВОЕЙ ТЕХНИКИ В SESSION STATE ===
if "custom_machines" not in st.session_state:
    st.session_state.custom_machines = {}

# Объединяем стандартные и пользовательские
all_machines = {**DEFAULT_MACHINES, **st.session_state.custom_machines}

# === ВЫБОР ТЕХНИКИ ===
col_select, col_add = st.columns([3, 1])

with col_select:
    machine_options = list(all_machines.keys()) + ["➕ Добавить свою технику"]
    selected = st.selectbox("🚜 Выберите технику", machine_options)

with col_add:
    st.write("")
    st.write("")

# === ФОРМА ДЛЯ ДОБАВЛЕНИЯ СВОЕЙ ТЕХНИКИ ===
if selected == "➕ Добавить свою технику":
    st.subheader("Добавление своей техники")
    st.caption("Укажите название и нормативные диапазоны для каждого показателя")

    with st.form("add_machine_form"):
        new_name = st.text_input("Название техники", placeholder="Например: К-701 (ЯМЗ-240)")

        st.markdown("**Температура двигателя**")
        c1, c2, c3 = st.columns(3)
        with c1:
            t_min = st.number_input("Норма min (°C)", value=80.0, step=1.0, key="t_min")
        with c2:
            t_max = st.number_input("Норма max (°C)", value=95.0, step=1.0, key="t_max")
        with c3:
            t_crit = st.number_input("Критично выше (°C)", value=105.0, step=1.0, key="t_crit")

        st.markdown("**Давление масла**")
        c4, c5, c6 = st.columns(3)
        with c4:
            p_min = st.number_input("Норма min (бар)", value=2.0, step=0.1, key="p_min")
        with c5:
            p_max = st.number_input("Норма max (бар)", value=4.0, step=0.1, key="p_max")
        with c6:
            p_crit = st.number_input("Критично ниже (бар)", value=1.0, step=0.1, key="p_crit")

        st.markdown("**Вибрация**")
        c7, c8, c9 = st.columns(3)
        with c7:
            v_min = st.number_input("Норма min (мм/с)", value=0.0, step=0.1, key="v_min")
        with c8:
            v_max = st.number_input("Норма max (мм/с)", value=4.5, step=0.1, key="v_max")
        with c9:
            v_crit = st.number_input("Критично выше (мм/с)", value=7.1, step=0.1, key="v_crit")

        submitted = st.form_submit_button("💾 Сохранить технику", type="primary")

        if submitted:
            if not new_name.strip():
                st.error("Введите название техники")
            elif new_name in DEFAULT_MACHINES or new_name in st.session_state.custom_machines:
                st.error("Техника с таким названием уже существует")
            else:
                st.session_state.custom_machines[new_name] = {
                    "temp": {"min": t_min, "max": t_max, "crit_high": t_crit,
                             "label": "Температура ОЖ (°C)", "note": f"Норма {t_min}–{t_max}°C"},
                    "pressure": {"min": p_min, "max": p_max, "crit_low": p_crit,
                                 "label": "Давление масла (бар)", "note": f"Норма {p_min}–{p_max} бар"},
                    "vibration": {"min": v_min, "max": v_max, "crit_high": v_crit,
                                  "label": "Вибрация (мм/с)", "note": f"Норма до {v_max} мм/с"}
                }
                st.success(f"Техника «{new_name}» добавлена! Выберите её в списке выше.")
                st.rerun()

    st.stop()

# === ОСНОВНОЙ ИНТЕРФЕЙС ДЛЯ ВЫБРАННОЙ ТЕХНИКИ ===
spec = all_machines[selected]

# Показываем нормативы
st.markdown(f"**Нормативы для {selected}:**")
st.markdown(f'<div class="spec-box">🌡️ {spec["temp"]["note"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="spec-box">🛢️ {spec["pressure"]["note"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="spec-box">📳 {spec["vibration"]["note"]}</div>', unsafe_allow_html=True)

st.divider()

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("Показания датчиков")
    temp = st.number_input(spec["temp"]["label"], min_value=0.0, max_value=200.0,
                           value=float((spec["temp"]["min"] + spec["temp"]["max"]) / 2), step=0.5)
    pressure = st.number_input(spec["pressure"]["label"], min_value=0.0, max_value=20.0,
                               value=float((spec["pressure"]["min"] + spec["pressure"]["max"]) / 2), step=0.1)
    vibration = st.number_input(spec["vibration"]["label"], min_value=0.0, max_value=30.0,
                                value=float((spec["vibration"]["min"] + spec["vibration"]["max"]) / 2), step=0.1)


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
            <h2 style="color: #6b7a5a;">—</h2>
            <p style="color: #8a9a7a;">Нажмите кнопку для анализа показаний.</p>
        </div>''', unsafe_allow_html=True)

st.markdown('---')
st.markdown('<p class="threshold-note">Пороги зависят от выбранной техники. Пользовательские нормативы сохраняются в рамках сессии.</p>', unsafe_allow_html=True)
