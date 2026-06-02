import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* ================================
SIDEBAR
================================ */

section[data-testid="stSidebar"] {
    background-color: #F8FAFC;
}

/* ================================
TITLE
================================ */

.main-title {

    font-size: 52px;

    font-weight: 800;

    color: #0F172A;

    margin-bottom: 5px;
}

.main-subtitle {

    font-size: 18px;

    color: #475569;

    margin-bottom: 25px;
}

/* ================================
SECTION TITLE
================================ */

.section-title {

    font-size: 32px;

    font-weight: 700;

    color: #0F172A;

    margin-top: 25px;

    margin-bottom: 15px;
}

/* ================================
KPI CARD
================================ */

.kpi-card {

    background: linear-gradient(
        135deg,
        #0F172A,
        #1E293B
    );

    padding: 28px;

    border-radius: 20px;

    text-align: center;

    box-shadow: 0 8px 20px rgba(0,0,0,0.25);

    height: 170px;
}

.kpi-title {

    color: #CBD5E1;

    font-size: 20px;

    font-weight: 600;

    margin-bottom: 20px;
}

.kpi-value {

    color: white;

    font-size: 42px;

    font-weight: 800;

    margin-top: 10px;
}

/* ================================
DATAFRAME
================================ */

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    r'C:\SKripsi\Skripsi Clustering\output\customer_segmentation_dpp.csv'
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📌 Navigation")

algorithm = st.sidebar.selectbox(

    "Pilih Algoritma Clustering",

    [
        "KMeans",
        "Agglomerative",
        "GMM",
        "DBSCAN"
    ]
)

# =========================================================
# CLUSTER COLUMN
# =========================================================

cluster_column = {

    "KMeans": "KMeans_Cluster",
    "Agglomerative": "Agglo_Cluster",
    "GMM": "GMM_Cluster",
    "DBSCAN": "DBSCAN_Cluster"

}[algorithm]

# =========================================================
# TITLE
# =========================================================

st.markdown("""
<div class='main-title'>
📊 Customer Segmentation Dashboard
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='main-subtitle'>
Dashboard visualisasi clustering customer berdasarkan data invoice perusahaan menggunakan beberapa algoritma clustering.
</div>
""", unsafe_allow_html=True)

# =========================================================
# FORMAT RUPIAH
# =========================================================

def format_rupiah(num):

    if num >= 1_000_000_000_000:
        return f"{num/1_000_000_000_000:.2f} T"

    elif num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f} B"

    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f} M"

    return f"{num:,.0f}"

# =========================================================
# KPI SECTION CLEAN FINAL
# =========================================================

total_customer = len(df)

total_transaksi = df['Total_DPP_Original'].sum()

avg_transaksi = df['Avg_DPP_Original'].mean()

jumlah_cluster = df[cluster_column].nunique()

if algorithm == "DBSCAN":
    jumlah_cluster = len(
        df[df[cluster_column] != -1][cluster_column].unique()
    )

# =========================================================
# FORMAT
# =========================================================

def format_rupiah(num):

    if num >= 1_000_000_000_000:
        return f"{num/1_000_000_000_000:.2f} T"

    elif num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f} B"

    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f} M"

    return f"{num:,.0f}"

# =========================================================
# CSS KPI
# =========================================================

st.markdown("""
<style>

.kpi-card{
    background: linear-gradient(135deg,#0F172A,#1E293B);
    border-radius:20px;
    padding:30px;
    text-align:center;
    box-shadow:0 8px 20px rgba(0,0,0,0.25);
}

.kpi-title{
    color:#CBD5E1;
    font-size:20px;
    font-weight:600;
    margin-bottom:18px;
}

.kpi-number{
    color:white;
    font-size:40px;
    font-weight:800;
    line-height:1.2;
}

.kpi-money{
    color:white;
    font-size:32px;
    font-weight:800;
    line-height:1.2;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# KPI LAYOUT
# =========================================================

col1, col2, col3, col4 = st.columns(4)

# =========================================================
# CARD 1
# =========================================================

with col1:

    html = f"""
    <div class="kpi-card">
        <div class="kpi-title">👥 Total Customer</div>
        <div class="kpi-number">{total_customer}</div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# CARD 2
# =========================================================

with col2:

    html = f"""
    <div class="kpi-card">
        <div class="kpi-title">💰 Total Pendapatan</div>
        <div class="kpi-money">Rp {format_rupiah(total_transaksi)}</div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# CARD 3
# =========================================================

with col3:

    html = f"""
    <div class="kpi-card">
        <div class="kpi-title">📈 Avg Pendapatan</div>
        <div class="kpi-money">Rp {format_rupiah(avg_transaksi)}</div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

# =========================================================
# CARD 4
# =========================================================

with col4:

    html = f"""
    <div class="kpi-card">
        <div class="kpi-title">🧩 Jumlah Cluster</div>
        <div class="kpi-number">{jumlah_cluster}</div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

st.write("")
st.divider()
# =========================================================
# EVALUATION METRICS
# =========================================================

st.markdown("""
<div class='section-title'>
📈 Evaluation Metrics
</div>
""", unsafe_allow_html=True)

evaluation_df = pd.DataFrame({

    "Algorithm": [

        "KMeans",
        "Agglomerative",
        "GMM",
        "DBSCAN"
    ],

    "Silhouette Score": [

        0.464,
        0.427,
        0.131,
        None
    ],

    "Davies Bouldin Index": [

        0.757,
        0.638,
        1.765,
        None
    ],

    "Calinski Harabasz Index": [

        336.337,
        300.680,
        112.775,
        None
    ],

    "Status": [

        "Good",
        "Best Overall",
        "Overlap High",
        "Failed Density Separation"
    ]
})

st.dataframe(
    evaluation_df,
    use_container_width=True
)

st.divider()

# =========================================================
# PCA VISUALIZATION
# =========================================================

st.markdown(f"""
<div class='section-title'>
📍 PCA Visualization - {algorithm}
</div>
""", unsafe_allow_html=True)

fig_pca = px.scatter(

    df,

    x="PCA1",
    y="PCA2",

    color=cluster_column,

    hover_data=[

        "Nama",
        "Total_DPP_Original",
        "Frekuensi_Invoice"
    ],

    title=f"PCA Scatter Plot - {algorithm}",

    height=650,

    template="plotly_dark"
)

st.plotly_chart(
    fig_pca,
    use_container_width=True
)

st.divider()

# =========================================================
# DISTRIBUSI CLUSTER
# =========================================================

st.markdown("""
<div class='section-title'>
📊 Distribusi Cluster
</div>
""", unsafe_allow_html=True)

cluster_dist = (

    df[cluster_column]
    .value_counts()
    .reset_index()
)

cluster_dist.columns = [

    "Cluster",
    "Jumlah Customer"
]

fig_bar = px.bar(

    cluster_dist,

    x="Cluster",
    y="Jumlah Customer",

    color="Cluster",

    text_auto=True,

    template="plotly_dark",

    height=500
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)

# =========================================================
# DONUT CHART
# =========================================================

st.markdown("""
<div class='section-title'>
🍩 Persentase Cluster
</div>
""", unsafe_allow_html=True)

fig_pie = px.pie(

    cluster_dist,

    names="Cluster",
    values="Jumlah Customer",

    hole=0.5,

    template="plotly_dark"
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)

st.divider()

# =========================================================
# CLUSTER PROFILING
# =========================================================

st.markdown("""
<div class='section-title'>
🧠 Cluster Profiling
</div>
""", unsafe_allow_html=True)

cluster_profile = (

    df.groupby(cluster_column)[

        [
            "Total_DPP_Original",
            "Avg_DPP_Original",
            "Frekuensi_Invoice",
            "Tahun_Aktif"
        ]

    ]
    .mean()
    .round(2)
)

st.dataframe(

    cluster_profile,

    use_container_width=True
)

st.divider()

# =========================================================
# TOP CUSTOMER
# =========================================================

st.markdown("""
<div class='section-title'>
🏆 Top 10 Customer
</div>
""", unsafe_allow_html=True)

top_customer = (

    df.sort_values(
        by="Total_DPP_Original",
        ascending=False
    )

    [[

        "Nama",
        "Total_DPP_Original",
        "Avg_DPP_Original",
        "Frekuensi_Invoice"
    ]]

    .head(10)
)

st.dataframe(

    top_customer,

    use_container_width=True
)

st.divider()

# =========================================================
# FILTER CLUSTER
# =========================================================

st.markdown("""
<div class='section-title'>
🔎 Filter Customer by Cluster
</div>
""", unsafe_allow_html=True)

cluster_option = st.selectbox(

    "Pilih Cluster",

    sorted(df[cluster_column].unique())
)

filtered_df = df[
    df[cluster_column] == cluster_option
]

st.dataframe(

    filtered_df,

    use_container_width=True
)

# =========================================================
# DOWNLOAD CSV
# =========================================================

st.download_button(

    label="⬇ Download Filtered Data CSV",

    data=filtered_df.to_csv(index=False),

    file_name=f"{algorithm}_cluster_{cluster_option}.csv",

    mime="text/csv"
)

# =========================================================
# BUSINESS INSIGHT
# =========================================================

st.divider()

st.markdown("""
<div class='section-title'>
💡 Business Insight
</div>
""", unsafe_allow_html=True)

if algorithm == "KMeans":

    st.info("""

    K-Means menghasilkan clustering yang cukup stabil
    dengan pemisahan cluster yang baik.

    Cocok digunakan untuk segmentasi customer umum.

    """)

elif algorithm == "Agglomerative":

    st.success("""

    Agglomerative Clustering memberikan struktur
    cluster terbaik secara keseluruhan berdasarkan
    DBI dan interpretasi hierarchical customer.

    """)

elif algorithm == "GMM":

    st.warning("""

    GMM menghasilkan overlap cluster yang cukup tinggi,
    menunjukkan distribusi customer tidak mengikuti
    Gaussian distribution secara optimal.

    """)

elif algorithm == "DBSCAN":

    st.error("""

    DBSCAN gagal membentuk multiple cluster yang meaningful
    karena dataset customer invoice tidak memiliki
    density separation yang kuat.

    """)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Customer Segmentation Dashboard © 2026"
)