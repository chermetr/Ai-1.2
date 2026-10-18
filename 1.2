import streamlit as st
from google import genai
import time

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(
    page_title="ИИ-Диагностика сельхозтехники",
    page_icon="🚜",
    layout="centered"
)

# --- КАСТОМНЫЕ СТИЛИ ДЛЯ КРАСОТЫ ---
st.markdown("""
<style>
    /* Основной фон и шрифты */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    /* Карточка результата */
    .result-card {
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-top: 20px;
        text-align: center;
        font-weight: bold;
    }
    .status-ok { background-color: #d4edda; color: #155724; border-left: 8px solid #28a745; }
    .status-warn { background-color: #fff3cd; color: #856404; border-left: 8px solid #ffc107; }
    .status-crit { background-color: #f8d7da; color: #721c24; border-left: 8px solid #dc3545; }
    /* Заголовки */
    h1 { color: #2c3e50; text-align: center; }
    .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 30px; font-size: 1.1em; }
    /* Стили для слайдеров */
    .stSlider > label { font-weight: 600 !important; color: #34495e; }
</style>
""", unsafe_allow_html=True)

# --- ЗАГОЛОВОК ---
st.title("🚜 ИИ-Диагностика сельхозтехники")
st.markdown('<p class="subtitle">Введите показатели датчиков, и ИИ определит состояние узла</p>', unsafe_allow_html=True)

# --- ВВОД ДАННЫХ С ДАТЧИКОВ ---
st.header("📊 Показатели датчиков")

col1, col2, col3 = st.columns(3)

with col1:
    temp = st.slider(
        "🌡️ Температура двигателя (°C)",
        min_value=40.0,
        max_value=130.0,
        value=85.0,
        step=0.5,
        help="Норма для большинства дизельных двигателей: 80–95 °C"
    )

with col2:
    pressure = st.slider(
        "🛢️ Давление масла (бар)",
        min_value=0.5,
        max_value=10.0,
        value=4.5,
        step=0.1,
        help="Норма на холостых оборотах: 2–5 бар, под нагрузкой выше"
    )

with col3:
    vibration = st.slider(
        "📳 Вибрация (мм/с)",
        min_value=0.0,
        max_value=25.0,
        value=3.0,
        step=0.1,
        help="Норма: до 4.5 мм/с. Выше 7.1 мм/с — требует внимания"
    )

# --- ИНИЦИАЛИЗАЦИЯ КЛИЕНТА GEMINI ---
# ВАЖНО: Замените строку ниже на ваш реальный API-ключ из Google AI Studio
API_KEY = "ВАШ_API_КЛЮЧ"

if API_KEY == "ВАШ_API_КЛЮЧ":
    st.warning("⚠️ Пожалуйста, вставьте ваш API-ключ Gemini в код (переменная API_KEY).")
    st.stop()

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Ошибка инициализации ИИ: {e}")
    st.stop()

# --- ЛОГИКА ДИАГНОСТИКИ С ПОМОЩЬЮ ИИ ---
if st.button("🔍 Запустить ИИ-диагностику", type="primary", use_container_width=True):
    
    with st.spinner("ИИ анализирует данные датчиков..."):
        time.sleep(1) # Небольшая пауза для визуального эффекта
        
        # Формируем промпт для ИИ
        prompt = f"""
        Ты — эксперт по диагностике сельскохозяйственной техники.
        Проанализируй показания датчиков и дай вердикт по одному из трёх вариантов:
        1. "В норме" (зелёный) — все показатели в пределах допустимого.
        2. "На грани" (жёлтый) — есть отклонения, требуется повышенное внимание или скорое ТО.
        3. "Требуется ремонт" (красный) — критические значения, эксплуатация опасна.

        Данные датчиков:
        - Температура двигателя: {temp} °C
        - Давление масла: {pressure} бар
        - Вибрация: {vibration} мм/с

        Ответь СТРОГО в формате:
        СТАТУС: [В норме / На грани / Требуется ремонт]
        ОБЪЯСНЕНИЕ: [Краткое пояснение, 1-2 предложения]
        РЕКОМЕНДАЦИЯ: [Что делать, 1 предложение]
        """

        try:
            # Вызов Gemini (используем актуальную модель flash для скорости)
            response = client.models.generate_content(
                model="gemini-2.5-flash", # или gemini-3-flash, если доступна
                contents=prompt
            )
            ai_text = response.text
            
            # Парсим ответ (простой парсинг по ключевым словам)
            status =
