import streamlit as st
from datetime import datetime, timedelta
import barcode
from barcode.writer import ImageWriter
import io

st.set_page_config(
    page_title="Склад",
    page_icon="📦",
    layout="centered"
)

st.title("📦 Складской помощник")
st.caption("Мобильный режим 📱")

# ---------------- СРОК В ДНЯХ ----------------
st.subheader("⏳ Срок (в днях)")

product = st.text_input("Товар")
st.subheader("⏳ Быстрый выбор срока")

col1, col2, col3 = st.columns(3)

if col1.button("7 дней"):
    st.session_state.days = 7

if col2.button("14 дней"):
    st.session_state.days = 14

if col3.button("30 дней"):
    st.session_state.days = 30

col4, col5, col6 = st.columns(3)

if col4.button("90 дней"):
    st.session_state.days = 90

if col5.button("180 дней"):
    st.session_state.days = 180

if col6.button("365 дней"):
    st.session_state.days = 365

days = st.number_input(
    "Срок (дней)",
    min_value=1,
    value=st.session_state.get("days", 30)
)

if st.button("📅 Посчитать дату"):
    expiry = datetime.today() + timedelta(days=days)

    st.success("Готово")
    st.write(f"Товар: {product}")
    st.write(f"Годен до: {expiry.date()}")

st.divider()

# ---------------- СРОК ПО ДАТАМ ----------------
st.subheader("📅 По датам")

prod = st.date_input("Производство")
exp = st.date_input("Окончание")

if st.button("⏳ Посчитать срок"):
    if exp < prod:
        st.error("Даты перепутаны 😄")
    else:
        st.success(f"Срок: {(exp - prod).days} дней")

st.divider()

# ---------------- ШТРИХКОД ----------------
st.subheader("🏷️ Штрихкод")

code = st.text_input("Артикул / ID/ Паспорт")

if st.button("📦 Создать штрихкод"):
    if not code.strip():
        st.warning("Введи данные")
    else:
        barcode128 = barcode.get("code128", code, writer=ImageWriter())

        buffer = io.BytesIO()
        barcode128.write(buffer)

        st.image(buffer.getvalue())
