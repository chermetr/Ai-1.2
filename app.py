import streamlit as st
import time

st.set_page_config(page_title="Сервис-Диагностика", page_icon="⚙️", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #e6e6e6; }
    .result-card {
        padding: 24px; border-radius: 8px; margin-top: 16px;
        border-left: 6px solid #444; background-color: #1a1d24;
    }
    .status-ok { border-left-color: #2e7d32; }
    .status-warn { border-left-color: #f9a825; }
    .status-crit { border-left-color: #c62828; }
    .status-ok h2 { color: #66bb6a; }
    .status-warn h2 { color: #ffca28; }
    .status-crit h2 { color: #ef5350; }
    h1, h2, h3 { color: #ffffff !important; }
    .guide-link {
        display: inline-block; margin-top: 12px; padding: 10px 18px;
        background-color: #2a2d35; color: #64b5f6; border-radius: 6px;
        text-decoration: none; border: 1px solid #3a3d45; font-size: 0.95em;
    }
    .guide-link:hover { background-color: #3a3d45; color: #90caf9; }
    .threshold-note { font-size: 0.8em; color: #888; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("⚙️ Сервисная диагностика сельхозтехники")
st.caption("Выберите технику и введите текущие показания датчиков")

# --- БАЗА НОРМАТИВОВ ПО ТЕХНИКЕ ---
MACHINES = {
    "МТЗ-80/82 (Д-240)": {
        "temp": {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)",
                 "note": "Рабочая норма 80–95°C, кратковременно до 105°C [citation:4][citation:15]"},
        "pressure": {"min": 2.0, "max": 3.5, "crit_low": 1.0, "label": "Давление масла (бар)",
                     "note": "Норма 2.0–3.5 бар на номинальных оборотах, минимум 1.0 бар [citation:13][citation:15]"},
        "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                      "note": "Общая норма для с/х техники: до 4.5 мм/с, критично выше 7.1 мм/с"}
    },
    "John Deere (PowerTech)": {
        "temp": {"min": 82, "max": 94, "crit_high": 104, "label": "Температура ОЖ (°C)",
                 "note": "Норма 82–94°C, при >104°C снизить нагрузку [citation:3][citation:8]"},
        "pressure": {"min": 2.41, "max": 4.48, "crit_low": 1.03, "label": "Давление масла (бар)",
                     "note": "Мин. 1.03 бар на холостом, 2.41+ бар под нагрузкой [citation:3][citation:16]"},
        "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                      "note": "Общая норма для с/х техники: до 4.5 мм/с, критично выше 7.1 мм/с"}
    },
    "ХТЗ-181 (Т-150)": {
        "temp": {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)",
                 "note": "Норма 80–95°C, кратковременно до 105°C [citation:1]"},
        "pressure": {"min": 4.0, "max": 7.3, "crit_low": 3.0, "label": "Давление масла (бар)",
                     "note": "Норма 4.0–7.3 бар на номинале, после износа допускается от 3.0 бар [citation:1]"},
        "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                      "note": "Общая норма для с/х техники: до 4.5 мм/с, критично выше 7.1 мм/с"}
    },
    "Комбайн Дон-1500": {
        "temp": {"min": 80, "max": 95, "crit_high": 105, "label": "Температура ОЖ (°C)",
                 "note": "Норма 80–95°C, при перегреве — остановка"},
        "pressure": {"min": 4.0, "max": 7.3, "crit_low": 2.0, "label": "Давление масла (бар)",
                     "note": "Не менее 4.0 МПа (40 бар) при номинале — уточните по паспорту двигателя [citation:2]"},
        "vibration": {"min": 0, "max": 4.5, "crit_high": 7.1, "label": "Вибрация (мм/с)",
                      "note": "Общая норма для с/х техники: до 4.5 мм/с, критично выше 7.1 мм/с"}
    }
}

# --- ВЫБОР ТЕХНИКИ ---
machine_name = st.selectbox("🚜 Выберите технику", list(MACHINES.keys()))
spec = MACHINES[machine_name]

st.markdown(f"**Нормативы для {machine_name}:**")
st.caption(f"🌡️ {spec['temp']['note']}")
st.caption(f"🛢️ {spec['pressure']['note']}")
st.caption(f"📳 {spec['vibration']['note']}")

st.divider()

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("Показания датчиков")
    temp = st.number_input(spec["temp"]["label"], min_value=0.0, max_value=150.0,
                           value=float((spec["temp"]["min"] + spec["temp"]["max"]) / 2), step=0.5)
    pressure = st.number_input(spec["pressure"]["label"], min_value=0.0, max_value=15.0,
                               value=float((spec["pressure"]["min"] + spec["pressure"]["max"]) / 2), step=0.1)
    vibration = st.number_input(spec["vibration"]["label"], min_value=0.0, max_value=30.0,
                                value=3.0, step=0.1)


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
        reasons.append(f"Температура {temp}°C — вне рабочего диапазона {t['min']}–{t['max']}°C")
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
        advice.append("проверьте уровень масла и состояние масляного насоса")
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
        advice.append("осмотрите вращающиеся узлы и крепления")
        guide_key = "vibration"

    if score == 0:
        return "ok", "Все показатели в пределах нормы для выбранной техники.", "Продолжайте эксплуатацию.", None
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
        <div class="result-card" style="border-left-color: #444;">
            <h2 style="color: #888;">—</h2>
            <p>Нажмите кнопку для анализа показаний.</p>
        </div>''', unsafe_allow_html=True)

st.markdown('---')
st.markdown('<p class="threshold-note">Пороги зависят от выбранной техники. Данные основаны на открытых руководствах и могут уточняться по паспорту конкретной машины.</p>', unsafe_allow_html=True)
