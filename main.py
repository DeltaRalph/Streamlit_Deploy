import streamlit as st
import pandas as pd

st.title("Veri Dashboard - Hava Kalitesi")

uploaded_file = st.file_uploader("Excel formatında verinizi yükleyin", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)


    # Tarih sütununu datetime formatına çevir
    date_col = "Tarih"
    if date_col not in df.columns:
        st.error(f"Veri setinde '{date_col}' adlı bir tarih kolonu bulunamadı!")
    else:
        df[date_col] = pd.to_datetime(df[date_col])

        st.subheader("Zaman Aralığı Seçiniz")
        start_date = st.date_input("Başlangıç Tarihi", df[date_col].min().date())
        end_date = st.date_input("Bitiş Tarihi", df[date_col].max().date())

        # Tarihe göre filtreleme
        filtered_df = df[(df[date_col] >= pd.to_datetime(start_date)) & (df[date_col] <= pd.to_datetime(end_date))]

        # Filtrelenmiş veriyi göster
        st.subheader("Filtrelenmiş Veri")
        st.write(filtered_df)

        # Grafik için seçimler
        st.subheader("Veri Görselleştirme")
        x_column = st.selectbox("X ekseni için bir kolon seçin", [date_col])
        y_columns = st.multiselect("Y ekseni için bir veya birden fazla kolon seçin", [col for col in df.columns if col != date_col])

        if st.button("Grafiği Çiz"):
            if y_columns:
                st.line_chart(filtered_df.set_index(x_column)[y_columns])
            else:
                st.warning("Lütfen en az bir Y ekseni kolonu seçin.")

