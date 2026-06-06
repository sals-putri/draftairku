import streamlit as st
import pandas as pd

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Evaluasi Kualitas Air Kelas I",
    page_icon="💧",
    layout="wide"
)

# =========================
# JUDUL
# =========================
st.title("💧 Evaluasi Kualitas Air Kelas I")
st.subheader("Berdasarkan PP No. 22 Tahun 2021")
st.write(
    """
    Aplikasi ini digunakan untuk mengevaluasi kualitas air terhadap
    baku mutu Air Kelas I (air baku untuk air minum).
    """
)

st.divider()

# =========================
# INPUT DATA
# =========================
st.header("📋 Input Data Sampel")

nama_sampel = st.text_input(
    "Nama Sampel",
    placeholder="Contoh: Sungai Ciliwung Titik 1"
)

col1, col2 = st.columns(2)

with col1:
    ph = st.number_input(
        "pH",
        min_value=0.0,
        max_value=14.0,
        value=7.0,
        step=0.1
    )

    bod = st.number_input(
        "BOD (mg/L)",
        min_value=0.0,
        value=1.0,
        step=0.1
    )

    cod = st.number_input(
        "COD (mg/L)",
        min_value=0.0,
        value=5.0,
        step=0.1
    )

with col2:
    do = st.number_input(
        "DO (mg/L)",
        min_value=0.0,
        value=7.0,
        step=0.1
    )

    tss = st.number_input(
        "TSS (mg/L)",
        min_value=0.0,
        value=20.0,
        step=0.1
    )

    tds = st.number_input(
        "TDS (mg/L)",
        min_value=0.0,
        value=500.0,
        step=1.0
    )

# =========================
# TOMBOL ANALISIS
# =========================
if st.button("🔍 Evaluasi Kualitas Air"):

    hasil = []

    # pH
    status_ph = "Memenuhi" if 6 <= ph <= 9 else "Tidak Memenuhi"
    hasil.append(["pH", ph, "6 - 9", status_ph])

    # BOD
    status_bod = "Memenuhi" if bod <= 2 else "Tidak Memenuhi"
    hasil.append(["BOD", bod, "≤ 2", status_bod])

    # COD
    status_cod = "Memenuhi" if cod <= 10 else "Tidak Memenuhi"
    hasil.append(["COD", cod, "≤ 10", status_cod])

    # DO
    status_do = "Memenuhi" if do >= 6 else "Tidak Memenuhi"
    hasil.append(["DO", do, "≥ 6", status_do])

    # TSS
    status_tss = "Memenuhi" if tss <= 40 else "Tidak Memenuhi"
    hasil.append(["TSS", tss, "≤ 40", status_tss])

    # TDS
    status_tds = "Memenuhi" if tds <= 1000 else "Tidak Memenuhi"
    hasil.append(["TDS", tds, "≤ 1000", status_tds])

    # =========================
    # DATAFRAME HASIL
    # =========================
    df = pd.DataFrame(
        hasil,
        columns=[
            "Parameter",
            "Hasil",
            "Baku Mutu",
            "Status"
        ]
    )

    st.divider()

    st.header("📊 Hasil Evaluasi")

    st.dataframe(
        df,
        use_container_width=True
    )

    # =========================
    # PERHITUNGAN
    # =========================
    jumlah_memenuhi = (
        df["Status"] == "Memenuhi"
    ).sum()

    jumlah_tidak = (
        df["Status"] == "Tidak Memenuhi"
    ).sum()

    total_parameter = len(df)

    persentase = (
        jumlah_memenuhi /
        total_parameter
    ) * 100

    # =========================
    # METRIK
    # =========================
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Parameter Memenuhi",
        jumlah_memenuhi
    )

    c2.metric(
        "Parameter Tidak Memenuhi",
        jumlah_tidak
    )

    c3.metric(
        "Persentase Kepatuhan",
        f"{persentase:.1f}%"
    )

    st.divider()

    # =========================
    # KESIMPULAN
    # =========================
    st.header("📝 Kesimpulan")

    if jumlah_tidak == 0:
        st.success(
            f"""
            Sampel '{nama_sampel}'
            MEMENUHI Baku Mutu Air Kelas I
            berdasarkan PP No. 22 Tahun 2021.
            """
        )
    else:
        st.error(
            f"""
            Sampel '{nama_sampel}'
            TIDAK MEMENUHI Baku Mutu Air Kelas I
            berdasarkan PP No. 22 Tahun 2021.
            """
        )

        gagal = df[
            df["Status"] == "Tidak Memenuhi"
        ]["Parameter"].tolist()

        st.warning(
            "Parameter yang tidak memenuhi: "
            + ", ".join(gagal)
        )

    # =========================
    # GRAFIK
    # =========================
    st.divider()
    st.header("📈 Ringkasan Status Parameter")

    grafik = (
        df["Status"]
        .value_counts()
    )

    st.bar_chart(grafik)
