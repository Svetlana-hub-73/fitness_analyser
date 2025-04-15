# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Фитнес Анализ", page_icon="🏃", layout="centered")

st.title("🏃‍♀️ Фитнес Анализатор")
st.write("Загрузи CSV-файл и получи быстрый анализ!")

uploaded_file = st.file_uploader("fit_data.csv", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Очистка
    df['Duration'] = pd.to_numeric(df['Duration'].str.replace('min', '').str.strip())
    df['Calories'] = pd.to_numeric(df['Calories'].str.replace('kcal', '').str.strip())
    df['Activity'] = df['Activity'].str.lower().str.strip()
    df['Activity'] = df['Activity'].replace({'swimm': 'swimming', 'yoga': 'yoga'})
    df = df.dropna(subset=['Username']).drop_duplicates()

    # Аналитика
    avg_duration = df['Duration'].mean()
    mood_mode = df['Mood'].mode()[0]
    cal_std = df['Calories'].std()
    age_iqr = df['Age'].quantile(0.75) - df['Age'].quantile(0.25)

    # Вывод
    st.metric("📏 Средняя длительность (мин)", f"{avg_duration:.2f}")
    st.metric("🔥 Стандартное отклонение калорий", f"{cal_std:.2f} ккал")
    st.metric("🧓 IQR по возрасту", f"{age_iqr} лет")
    st.metric("😊 Самое частое настроение", mood_mode)

    # Дополнительно: показать таблицу
    with st.expander("📊 Посмотреть таблицу"):
        st.dataframe(df)
else:
    st.info("⬆️ Загрузите файл для начала.")
