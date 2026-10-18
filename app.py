import streamlit as st
import time

st.set_page_config(page_title="ИИ-Диагностика", page_icon="🚜", layout="centered")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
.result-card { padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); margin-top: 20px; text-align: center; font-weight: bold; }
.status-ok { background-color: #d4edda; color: #155724; border-left: 8px solid #28a745; }
.status-warn { background-color: #fff3cd; color: #856404; border-left: 8px solid #ffc107; }
.status-crit { background-color: #f8d7da; color: #721c24; border-left: 8px solid #dc3545; }
</style>
""", unsafe_allow_html=True)

st.title("🚜 ИИ-Диагностика сельхозтехники")
st.write("Введите показатели датчиков — система определит состояние узла")

st.header("📊 Показатели датчиков")

col1, col2, col3 = st.columns(3)

with col1:
    temp = st.slider("🌡️ Температура двигателя (°C)", 40.0, 130.0, 85.0, 0.5)

with col2:
    pressure = st.slider("🛢️ Давление масла (бар)", 0.5, 10.0, 4.5, 0.1)

with col3:
    vibration = st.slider("📳 Вибрация (мм/с)", 0.0, 25.0, 3.0, 0.1)


def diagnose(temp, pressure, vibration):
    score = 0
    reasons = []
    advice = []

    if temp > 105:
        score += 2
        reasons.append(f"температура {temp}°C критически высокая")
        advice.append("остановите двигатель и дайте остыть")
    elif temp > 95:
        score += 1
        reasons.append(f"температура {temp}°C повышена")
        advice.append("проверьте систему охлаждения")

    if pressure < 1.5:
        score += 2
        reasons.append(f"давление масла {pressure} бар критически низкое")
        advice.append("немедленно заглушите двигатель")
    elif pressure < 2.5:
        score += 1
        reasons.append(f"давление масла {pressure} бар понижено")
        advice.append("проверьте уровень и состояние масла")

    if vibration > 7.1:
        score += 2
        reasons.append(f"вибрация {vibration} мм/с критическая")
        advice.append("проверьте подшипники и крепления")
    elif vibration > 4.5:
        score += 1
        reasons.append(f"вибрация {vibration} мм/с повышена")
        advice.append("осмотрите вращающиеся узлы")

    if score == 0:
        return "ok", "Все показатели в норме.", "Продолжайте работу."
    elif score <= 2:
        return "warn", "Обнаружены отклонения: " + ", ".join(reasons) + ".", \
               "Рекомендация: " + "; ".join(advice) + "."
    else:
        return "crit", "Критические показатели: " + ", ".join(reasons) + "!", \
               "Требуется ремонт: " + "; ".join(advice) + "."


if st.button("🔍 Запустить диагностику", type="primary", use_container_width=True):
    with st.spinner("Анализ данных..."):
        time.sleep(0.5)
        status, explanation, recommendation = diagnose(temp, pressure, vibration)

    if status == "ok":
        st.markdown(f'<div class="result-card status-ok"><h2>✅ ВСЁ В НОРМЕ</h2><p>{explanation}</p><p><strong>{recommendation}</strong></p></div>', unsafe_allow_html=True)
    elif status == "warn":
        st.markdown(f'<div class="result-card status-warn"><h2>⚠️ НА ГРАНИ</h2><p>{explanation}</p><p><strong>{recommendation}</strong></p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="result-card status-crit"><h2>🚨 ТРЕБУЕТСЯ РЕМОНТ</h2><p>{explanation}</p><p><strong>{recommendation}</strong></p></div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Прототип. Пороги: температура 95/105°C, давление 2.5/1.5 бар, вибрация 4.5/7.1 мм/с.")
