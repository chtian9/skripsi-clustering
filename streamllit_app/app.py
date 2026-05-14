import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================================
# LOAD DATA
# =========================================

df = pd.read_csv(
    'output/customer_segmentation_complete.csv'
)

evaluation_df = pd.read_csv(
    'output/evaluation_result.csv'
)

# =========================================
# TITLE
# =========================================

st.title("📊 Customer Segmentation Dashboard")

st.markdown("""
Dashboard visualisasi hasil clustering customer
berdasarkan data invoice perusahaan menggunakan:

- K-Means
- DBSCAN
- Agglomerative Clustering
""")

# =========================================
# SIDEBAR
# =========================================

st.sidebar.title("Navigation")

selected_cluster = st.sidebar.selectbox(
    "Filter KMeans Cluster",
    sorted(df['KMeans_Cluster'].unique())
)

# =========================================
# KPI SECTION
# =========================================

total_customer = df['Nama'].nunique()

total_transaksi = df['Total_Transaksi'].sum()

jumlah_cluster = df['KMeans_Cluster'].nunique()

avg_transaksi = df['Avg_Transaksi'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customer",
    total_customer
)

col2.metric(
    "Total Transaksi",
    f"Rp {total_transaksi:,.0f}"
)

col3.metric(
    "Jumlah Cluster",
    jumlah_cluster
)

col4.metric(
    "Rata-rata Transaksi",
    f"Rp {avg_transaksi:,.0f}"
)

# =========================================
# TABS
# =========================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "K-Means",
    "DBSCAN",
    "Agglomerative",
    "Evaluation"
])

# =========================================
# OVERVIEW TAB
# =========================================

with tab1:

    st.subheader("Distribusi Customer per Cluster")

    cluster_count = (
        df['KMeans_Cluster']
        .value_counts()
        .reset_index()
    )

    cluster_count.columns = [
        'Cluster',
        'Jumlah Customer'
    ]

    fig_cluster = px.bar(
        cluster_count,
        x='Cluster',
        y='Jumlah Customer',
        color='Cluster',
        text='Jumlah Customer'
    )

    st.plotly_chart(
        fig_cluster,
        use_container_width=True
    )

    st.subheader("Top 10 Customer")

    top_customer = df.sort_values(
        by='Total_Transaksi',
        ascending=False
    ).head(10)

    st.dataframe(
        top_customer[
            [
                'Nama',
                'Total_Transaksi',
                'Frekuensi_Invoice'
            ]
        ],
        use_container_width=True
    )

# =========================================
# KMEANS TAB
# =========================================

with tab2:

    st.subheader("K-Means PCA Visualization")

    fig_kmeans = px.scatter(
        df,
        x='PCA1',
        y='PCA2',
        color='KMeans_Cluster',
        hover_data=['Nama'],
        title='K-Means Clustering'
    )

    st.plotly_chart(
        fig_kmeans,
        use_container_width=True
    )

    st.subheader("K-Means Cluster Profiling")

    kmeans_profile = df.groupby(
        'KMeans_Cluster'
    ).mean(numeric_only=True)

    st.dataframe(
        kmeans_profile,
        use_container_width=True
    )

# =========================================
# DBSCAN TAB
# =========================================

with tab3:

    st.subheader("DBSCAN PCA Visualization")

    fig_dbscan = px.scatter(
        df,
        x='PCA1',
        y='PCA2',
        color='DBSCAN_Cluster',
        hover_data=['Nama'],
        title='DBSCAN Clustering'
    )

    st.plotly_chart(
        fig_dbscan,
        use_container_width=True
    )

    st.subheader("DBSCAN Cluster Distribution")

    dbscan_count = (
        df['DBSCAN_Cluster']
        .value_counts()
        .reset_index()
    )

    dbscan_count.columns = [
        'Cluster',
        'Jumlah'
    ]

    fig_dbscan_bar = px.pie(
        dbscan_count,
        names='Cluster',
        values='Jumlah'
    )

    st.plotly_chart(
        fig_dbscan_bar,
        use_container_width=True
    )

# =========================================
# AGGLOMERATIVE TAB
# =========================================

with tab4:

    st.subheader("Agglomerative PCA Visualization")

    fig_agglo = px.scatter(
        df,
        x='PCA1',
        y='PCA2',
        color='Agglo_Cluster',
        hover_data=['Nama'],
        title='Agglomerative Clustering'
    )

    st.plotly_chart(
        fig_agglo,
        use_container_width=True
    )

    st.subheader("Agglomerative Cluster Profiling")

    agglo_profile = df.groupby(
        'Agglo_Cluster'
    ).mean(numeric_only=True)

    st.dataframe(
        agglo_profile,
        use_container_width=True
    )

# =========================================
# EVALUATION TAB
# =========================================

with tab5:

    st.subheader("Perbandingan Algoritma")

    st.dataframe(
        evaluation_df,
        use_container_width=True
    )

    st.subheader("Silhouette Score Comparison")

    fig_eval = px.bar(
        evaluation_df,
        x='Algoritma',
        y='Silhouette Score',
        color='Algoritma',
        text='Silhouette Score'
    )

    st.plotly_chart(
        fig_eval,
        use_container_width=True
    )

    st.subheader("Davies-Bouldin Index Comparison")

    fig_dbi = px.bar(
        evaluation_df,
        x='Algoritma',
        y='Davies-Bouldin Index',
        color='Algoritma',
        text='Davies-Bouldin Index'
    )

    st.plotly_chart(
        fig_dbi,
        use_container_width=True
    )

# =========================================
# FILTERED DATA
# =========================================

st.subheader("Filtered Customer Data")

filtered_df = df[
    df['KMeans_Cluster'] == selected_cluster
]

st.dataframe(
    filtered_df,
    use_container_width=True
)