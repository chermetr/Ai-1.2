import streamlit as st
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="ИИ Диагностика", page_icon="🌾", layout="wide")

# === СТИЛЬ (МЯГКИЙ СЕЛЬХОЗ) ===
st.markdown("""
<style>
    .stApp { background-color: #141a14; background-image: linear-gradient(180deg, #182018 0%, #101510 100%); }
    html, body, [class*="css"], .stMarkdown, p, span, label, div { color: #d4dec8 !important; font-family: 'Segoe UI', sans-serif; }
    h1, h2, h3 { color: #e8ede1 !important; font-weight: 600; }
    
    /* Убираем лишние рамки у блоков, оставляем только отступы */
    div[data-testid="stVerticalBlock"] > div { background-color: transparent; border: none; padding: 0; margin-bottom: 0; }
    
    /* Поля ввода */
    div[data-testid="stNumberInput"] label, div[data-testid="stTextInput"] label { color: #8a9e7a !important; font-size: 0.9rem; }
    div[data-testid="stNumberInput"] input, div[data-testid="stTextInput"] input {
        background-color: #101510 !important; color: #e8ede1 !important; border: 1px solid #3d4a3d !important; font-weight: 600;
    }
    
    /* Выпадающий список */
    div[data-testid="stSelectbox"] label { color: #8a9e7a !important; }
    div[data-baseweb="select"] > div { background-color: #263026 !important; color: #d4dec8 !important; border: 1px solid #3d4a3d !important; }
    div[data-baseweb="select"] span { color: #d4dec8 !important; }
    ul[role="listbox"] { background-color: #263026 !important; }
    ul[role="listbox"] li { color: #d4dec8 !important; }
    ul[role="listbox"] li:hover { background-color: #324032 !important; }
    
    /* Радиокнопки */
    div[data-testid="stRadio"] label { color: #8a9e7a !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] label { background-color: #263026 !important; border: 1px solid #3d4a3d !important; border-radius: 6px !important; padding: 6px 12px !important; margin-right: 8px !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] label p { color: #d4dec8 !important; }
    
    /* Кнопка */
    .stButton > button { background-color: #3d4a3d !important; color: #e8ede1 !important; border: 1px solid #4d5c4d !important; font-weight: 600 !important; width: 100%; transition: all 0.2s; }
    .stButton > button:hover { background-color: #4d5c4d !important; border-color: #8a9e7a !important; }
    
    /* Результаты */
    .res-box { padding: 16px; border-radius: 6px; margin-bottom: 12px; border-left: 4px solid #3d4a3d; background-color: #1a221a; }
    .res-ok { border-left-color: #81c784; background-color: #172417; }
    .res-warn { border-left-color: #d4b651; background-color: #241f14; }
    .res-crit { border-left-color: #d1685a; background-color: #241414; }
    .res-title { font-size: 1.2rem; font-weight: 700; margin-bottom: 8px; }
    .res-text { font-size: 0.95rem; line-height: 1.5; color: #d4dec8; }
    
    /* Ссылки */
    .guide-link { display: inline-block; margin-top: 12px; color: #81c784 !important; text-decoration: none; font-weight: 600; font-size: 0.9rem; }
    .guide-link:hover { text-decoration: underline; color: #a5d6a7 !important; }
    
    /* Полоски */
    .gauge-container { margin-bottom: 16px; }
    .gauge-header { display: flex; justify-content: space-between; font-size: 0.9rem; font-weight: 600; margin-bottom: 4px; }
    .gauge-bar-bg { width: 100%; height: 16px; background: #101510; border-radius: 8px; overflow: hidden; border: 1px solid #2e382e; position: relative; }
    .gauge-bar-fill { height: 100%; transition: width 0.4s ease; border-radius: 8px; }
    .gauge-labels { display: flex; justify-content: space-between; font-size: 0.75rem; color: #6b7d6b; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

# === ИНИЦИАЛИЗАЦИЯ ДАННЫХ (СЕССИЯ) ===
if "custom_machines" not in st.session_state:
    st.session_state.custom_machines = {}
if "history" not in st.session_state:
    st.session_state.history = []

# Базовые техники
DEFAULT_MACHINES = {
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
all_machines = {**DEFAULT_MACHINES, **st.session_state.custom_machines}

# === ЗАГОЛОВОК ===
st.title("🌾 ИИ Диагностика")
st.markdown("---")

# === ВКЛАДКИ ===
tab_diag, tab_history = st.tabs(["🔧 Диагностика", "📊 История и графики"])

# ==========================================
# РАЗДЕЛ 1: ДИАГНОСТИКА
# ==========================================
with tab_diag:
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("1. Выбор техники")
        machine_options = list(all_machines.keys()) + ["➕ Добавить свою технику"]
        machine = st.selectbox("Техника", machine_options, label_visibility="collapsed")

        # Форма добавления своей техники
        if machine == "➕ Добавить свою технику":
            with st.form("add_machine"):
                st.markdown("**Название техники**")
                new_name = st.text_input("Название", label_visibility="collapsed", placeholder="Например: К-701")
                st.markdown("**Нормативы (Температура / Давление / Вибрация)**")
                st.markdown("*(Значения для холостого хода, езды и нагрузки будут усреднены)*")
                
                c1, c2, c3 = st.columns(3)
                with c1: t_min, t_max, t_crit = st.number_input("T min", 0.0, 200.0, 80.0), st.number_input("T max", 0.0, 200.0, 95.0), st.number_input("T крит", 0.0, 200.0, 105.0)
                with c2: p_min, p_max, p_crit = st.number_input("P min", 0.0, 20.0, 2.0), st.number_input("P max", 0.0, 20.0, 4.0), st.number_input("P крит", 0.0, 20.0, 1.0)
                with c3: v_min, v_max, v_crit = st.number_input("V min", 0.0, 50.0, 0.0), st.number_input("V max", 0.0, 50.0, 4.5), st.number_input("V крит", 0.0, 50.0, 7.1)
                
                if st.form_submit_button("Сохранить технику"):
                    if new_name.strip():
                        new_spec = {
                            "idle": {"t": (t_min, t_max, t_crit), "p": (p_min, p_max, p_crit), "v": (v_min, v_max, v_crit)},
                            "drive": {"t": (t_min, t_max, t_crit), "p": (p_min, p_max, p_crit), "v": (v_min, v_max, v_crit)},
                            "load": {"t": (t_min, t_max, t_crit), "p": (p_min, p_max, p_crit), "v": (v_min, v_max, v_crit)}
                        }
                        st.session_state.custom_machines[new_name] = new_spec
                        st.rerun()
            st.stop()

        # Выбор режима
        st.subheader("2. Режим использования")
        mode_map = {"idle": "Холостой ход", "drive": "Езда", "load": "Рабочая нагрузка"}
        mode = st.radio("Режим", list(mode_map.keys()), format_func=lambda x: mode_map[x], horizontal=True, label_visibility="collapsed")
        
        spec = all_machines[machine][mode]

        # Нормативы
        st.subheader("3. Нормативы (справочно)")
        st.markdown(f"""
        <div style="background-color: #1a221a; padding: 12px 16px; border-radius: 8px; border: 1px solid #2e382e; margin-bottom: 20px;">
            <p style="margin: 4px 0;"><b>Температура:</b> {spec['t'][0]} — {spec['t'][1]} °C (критично > {spec['t'][2]})</p>
            <p style="margin: 4px 0;"><b>Давление масла:</b> {spec['p'][0]} — {spec['p'][1]} бар (критично < {spec['p'][2]})</p>
            <p style="margin: 4px 0;"><b>Вибрация:</b> до {spec['v'][1]} мм/с (критично > {spec['v'][2]})</p>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.subheader("4. Показания датчиков")
        
        val_t = st.number_input("Температура (°C)", value=float((spec['t'][0]+spec['t'][1])/2), key=f"t_{machine}_{mode}")
        val_p = st.number_input("Давление масла (бар)", value=float((spec['p'][0]+spec['p'][1])/2), key=f"p_{machine}_{mode}")
        val_v = st.number_input("Вибрация (мм/с)", value=float((spec['v'][0]+spec['v'][1])/2), key=f"v_{machine}_{mode}")

        st.subheader("5. Результат диагностики")
        
        if st.button("Выполнить диагностику", type="primary"):
            with st.spinner("Анализ данных..."):
                time.sleep(0.5)
                
                score = 0
                reasons = []
                actions = []
                links = set()

                # Логика проверки
                if val_t > spec['t'][2]:
                    score += 2; reasons.append(f"Температура {val_t}°C критически высокая."); actions.append("Остановите двигатель, проверьте охлаждающую жидкость."); links.add("cooling")
                elif val_t > spec['t'][1]:
                    score += 1; reasons.append(f"Температура {val_t}°C повышена."); actions.append("Снизьте нагрузку, проверьте термостат."); links.add("cooling")

                if val_p < spec['p'][2]:
                    score += 2; reasons.append(f"Давление масла {val_p} бар критически низкое."); actions.append("Немедленно заглушите двигатель."); links.add("oil")
                elif val_p < spec['p'][0]:
                    score += 1; reasons.append(f"Давление масла {val_p} бар понижено."); actions.append("Проверьте уровень масла."); links.add("oil")

                if val_v > spec['v'][2]:
                    score += 2; reasons.append(f"Вибрация {val_v} мм/с критическая."); actions.append("Проверьте подшипники и крепления."); links.add("vibration")
                elif val_v > spec['v'][1]:
                    score += 1; reasons.append(f"Вибрация {val_v} мм/с повышена."); actions.append("Осмотрите вращающиеся узлы."); links.add("vibration")

                # Сохранение в историю
                history_entry = {
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "machine": machine,
                    "mode": mode_map[mode],
                    "temp": val_t,
                    "pressure": val_p,
                    "vibration": val_v,
                    "status": "Норма" if score == 0 else ("Внимание" if score <= 2 else "Ремонт")
                }
                st.session_state.history.append(history_entry)

                # Вывод
                if score == 0:
                    st.markdown(f'''
                    <div class="res-box res-ok">
                        <div class="res-title" style="color: #81c784;">✅ НОРМА</div>
                        <div class="res-text">Все показатели в пределах нормы для режима <b>{mode_map[mode]}</b>.</div>
                    </div>''', unsafe_allow_html=True)
                else:
                    if score <= 2:
                        status_cls, status_title, status_color = "res-warn", "⚠️ ВНИМАНИЕ", "#d4b651"
                    else:
                        status_cls, status_title, status_color = "res-crit", "🚨 ТРЕБУЕТСЯ РЕМОНТ", "#d1685a"

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

                link_data = {
                    "cooling": ("Система охлаждения", "https://barakud.ucoz.ru/news/rukovodstvo_po_remontu_traktora_mtz_80_i_mtz_82_1984_pdf_djvu_doc_rus/2012-03-12-2322"),
                    "oil": ("Смазочная система", "https://barakud.ucoz.ru/news/rukovodstvo_po_remontu_traktora_mtz_80_i_mtz_82_1984_pdf_djvu_doc_rus/2012-03-12-2322"),
                    "vibration": ("ГОСТ по вибрации", "https://protect.gost.ru/gost/details/e2ddaae8-c27d-41e4-80e7-cca0de5fb059")
                }
                if links:
                    st.markdown("**Полезные материалы:**")
                    for k in links:
                        if k in link_data:
                            text, url = link_data[k]
                            st.markdown(f'<a class="guide-link" href="{url}" target="_blank">🔗 {text}</a><br>', unsafe_allow_html=True)

# ==========================================
# РАЗДЕЛ 2: ИСТОРИЯ И ГРАФИКИ
# ==========================================
with tab_history:
    st.subheader("📊 История проверок")
    
    if not st.session_state.history:
        st.info("История пуста. Проведите первую диагностику во вкладке «Диагностика».")
    else:
        df = pd.DataFrame(st.session_state.history)
        
        # Фильтр по технике для графиков
        selected_machine = st.selectbox("Выберите технику для анализа", df["machine"].unique())
        df_filtered = df[df["machine"] == selected_machine].copy()
        
        # Графики
        st.markdown("### Сравнение показателей по времени")
        st.line_chart(df_filtered.set_index("timestamp")[["temp", "pressure", "vibration"]])
        
        st.markdown("### Таблица последних проверок")
        st.dataframe(df_filtered.tail(10), use_container_width=True)
        
        # Кнопка сброса
        st.markdown("---")
        if st.button("🗑️ Сбросить всю историю и добавленную технику"):
            st.session_state.history = []
            st.session_state.custom_machines = {}
            st.rerun()
