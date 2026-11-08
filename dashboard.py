import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ==============================================================================
# KONFIGURASI HALAMAN STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="E-Commerce Performance Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Set visual theme
sns.set_theme(style="whitegrid")

# ==============================================================================
# MEMUAT DATASET DENGAN CACHING
# ==============================================================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    
    # Fallback jika dijalankan dari root folder
    if not os.path.exists(file_path):
        file_path = "main_data.csv"
        
    df = pd.read_csv(file_path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

main_df = load_data()

# ==============================================================================
# HELPER FUNCTIONS UNTUK AGREGASI DATA
# ==============================================================================
def create_category_revenue_df(df):
    cat_rev = df.groupby("product_category_name")["price"].sum().reset_index()
    return cat_rev.sort_values(by="price", ascending=False)

def create_monthly_trend_df(df):
    monthly_trend = df.resample(rule="ME", on="order_purchase_timestamp").agg({
        "order_id": "nunique",
        "price": "sum"
    }).reset_index()
    monthly_trend.rename(columns={
        "order_id": "order_count",
        "price": "total_revenue"
    }, inplace=True)
    return monthly_trend

def create_state_summary_df(df):
    state_df = df.groupby("customer_state").agg(
        total_gmv=("total_price", "sum"),
        avg_freight=("freight_value", "mean"),
        order_count=("order_id", "nunique")
    ).reset_index().sort_values(by="total_gmv", ascending=False)
    return state_df

def create_rfm_df(df):
    snapshot_date = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("customer_unique_id").agg(
        recency=("order_purchase_timestamp", lambda x: (snapshot_date - x.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("total_price", "sum")
    ).reset_index()
    rfm["short_id"] = rfm["customer_unique_id"].str[:8] + "..."
    return rfm

# ==============================================================================
# SIDEBAR: FILTER RENTANG WAKTU
# ==============================================================================
min_date = main_df["order_purchase_timestamp"].min().date()
max_date = main_df["order_purchase_timestamp"].max().date()

with st.sidebar:
    st.title("🛒 Filter Analisis")
    
    # Input filter tanggal
    date_range = st.date_input(
        label="Pilih Rentang Waktu:",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    st.markdown("---")
    st.markdown("**Informasi Pengembang:**")
    st.markdown("- **Nama:** Gian Abi Firdaus")
    st.markdown("- **ID Dicoding:** gianabif14")
    st.markdown("- **Dataset:** Brazilian E-Commerce (Olist)")

# Validasi filter tanggal
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# Filter data berdasarkan rentang waktu terpilih
filtered_df = main_df[
    (main_df["order_purchase_timestamp"].dt.date >= start_date) & 
    (main_df["order_purchase_timestamp"].dt.date <= end_date)
].copy()

# ==============================================================================
# HEADER UTAMA
# ==============================================================================
st.title("📊 Brazilian E-Commerce Performance Dashboard")
st.markdown("Dashboard interaktif untuk memonitor performa penjualan, disparitas logistik wilayah, dan segmentasi pelanggan.")
st.markdown("---")

# ==============================================================================
# RINGKASAN METRIK KINERJA (KPI CARDS)
# ==============================================================================
col1, col2, col3, col4 = st.columns(4)

total_orders = filtered_df["order_id"].nunique()
total_revenue = filtered_df["price"].sum()
total_gmv = filtered_df["total_price"].sum()
avg_freight = filtered_df["freight_value"].mean()

with col1:
    st.metric("Total Pesanan Sukses", f"{total_orders:,}")
with col2:
    st.metric("Total Pendapatan (Revenue)", f"R$ {total_revenue:,.2f}")
with col3:
    st.metric("Total GMV (Barang + Ongkir)", f"R$ {total_gmv:,.2f}")
with col4:
    st.metric("Rata-rata Ongkos Kirim", f"R$ {avg_freight:,.2f}")

st.markdown("---")

# ==============================================================================
# SECTION 1: PERTANYAAN 1 - KATEGORI PRODUK & TREN PENDAPATAN
# ==============================================================================
st.subheader("📦 1. Performa Pendapatan Kategori Produk & Tren Waktu")

cat_revenue_df = create_category_revenue_df(filtered_df)
monthly_trend_df = create_monthly_trend_df(filtered_df)

col_cat1, col_cat2 = st.columns(2)

with col_cat1:
    st.markdown("##### Top 5 Kategori Produk (Revenue Tertinggi)")
    top_5 = cat_revenue_df.head(5)
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(
        x="price", 
        y="product_category_name", 
        data=top_5, 
        hue="product_category_name", 
        palette="Blues_r", 
        legend=False, 
        ax=ax
    )
    ax.set_xlabel("Pendapatan (BRL)", fontsize=10)
    ax.set_ylabel(None)
    for p in ax.patches:
        ax.annotate(f"R$ {p.get_width():,.0f}", (p.get_width() * 0.65, p.get_y() + p.get_height() / 2.),
                    ha="center", va="center", color="white", fontweight="bold", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_cat2:
    st.markdown("##### Bottom 5 Kategori Produk (Revenue Terendah)")
    bottom_5 = cat_revenue_df.tail(5)
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(
        x="price", 
        y="product_category_name", 
        data=bottom_5, 
        hue="product_category_name", 
        palette="Reds_r", 
        legend=False, 
        ax=ax
    )
    ax.set_xlabel("Pendapatan (BRL)", fontsize=10)
    ax.set_ylabel(None)
    ax.invert_xaxis()
    ax.yaxis.tick_right()
    for p in ax.patches:
        ax.annotate(f"R$ {p.get_width():,.2f}", (p.get_width() * 0.5, p.get_y() + p.get_height() / 2.),
                    ha="center", va="center", color="black", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Tren Pendapatan Berkala
st.markdown("##### Tren Pendapatan Bulanan")
fig_line, ax_line = plt.subplots(figsize=(12, 4))
ax_line.plot(
    monthly_trend_df["order_purchase_timestamp"].dt.strftime("%b %Y"),
    monthly_trend_df["total_revenue"],
    marker="o",
    linewidth=2.5,
    color="#1f77b4"
)
ax_line.set_xlabel("Bulan", fontsize=10)
ax_line.set_ylabel("Total Pendapatan (BRL)", fontsize=10)
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
st.pyplot(fig_line)
plt.close()

st.markdown("---")

# ==============================================================================
# SECTION 2: PERTANYAAN 2 - DEMOGRAFI WILAYAH & DISPARITAS ONGKOS KIRIM
# ==============================================================================
st.subheader("🗺️ 2. Distribusi GMV dan Biaya Ongkos Kirim per Wilayah (Negara Bagian)")

state_df = create_state_summary_df(filtered_df)
top_10_states = state_df.head(10).copy()

col_geo1, col_geo2 = st.columns(2)

with col_geo1:
    st.markdown("##### Top 10 Negara Bagian Penyumbang GMV Terbesar")
    colors_gmv = ["#1f77b4" if s == "SP" else "#a6c8e0" for s in top_10_states["customer_state"]]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        x="total_gmv", 
        y="customer_state", 
        data=top_10_states, 
        palette=colors_gmv, 
        hue="customer_state", 
        legend=False, 
        ax=ax
    )
    ax.set_xlabel("Total GMV (BRL)", fontsize=10)
    ax.set_ylabel("Negara Bagian", fontsize=10)
    for p in ax.patches:
        ax.annotate(f"R$ {p.get_width():,.0f}", (p.get_width() * 0.7, p.get_y() + p.get_height() / 2.),
                    ha="center", va="center", color="white" if p.get_width() > 1000000 else "black", 
                    fontweight="bold", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_geo2:
    st.markdown("##### Rata-rata Ongkos Kirim di 10 Wilayah Teratas")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        x="avg_freight", 
        y="customer_state", 
        data=top_10_states, 
        palette="flare", 
        hue="customer_state", 
        legend=False, 
        ax=ax
    )
    ax.set_xlabel("Rata-rata Ongkos Kirim (BRL)", fontsize=10)
    ax.set_ylabel(None)
    for p in ax.patches:
        ax.annotate(f"R$ {p.get_width():.2f}", (p.get_width() * 0.7, p.get_y() + p.get_height() / 2.),
                    ha="center", va="center", color="white", fontweight="bold", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ==============================================================================
# SECTION 3: ANALISIS LANJUTAN - RFM ANALYSIS
# ==============================================================================
st.subheader("👥 3. Analisis Lanjutan: Segmentasi Pelanggan (Model RFM)")

rfm_df = create_rfm_df(filtered_df)

col_rfm1, col_rfm2, col_rfm3 = st.columns(3)

with col_rfm1:
    avg_recency = round(rfm_df["recency"].mean(), 1)
    st.metric("Rata-rata Recency", f"{avg_recency} Hari")

with col_rfm2:
    avg_frequency = round(rfm_df["frequency"].mean(), 2)
    st.metric("Rata-rata Frequency", f"{avg_frequency} Pesanan")

with col_rfm3:
    avg_monetary = rfm_df["monetary"].mean()
    st.metric("Rata-rata Monetary", f"R$ {avg_monetary:,.2f}")

fig_rfm, ax_rfm = plt.subplots(nrows=1, ncols=3, figsize=(18, 5))

# Top Recency
top_rec = rfm_df.sort_values(by="recency", ascending=True).head(5)
sns.barplot(x="recency", y="short_id", data=top_rec, hue="short_id", palette="Greens_r", legend=False, ax=ax_rfm[0])
ax_rfm[0].set_title("Top 5 Customers by Recency (Days)", fontsize=12, fontweight="bold")
ax_rfm[0].set_xlabel("Hari Sejak Pembelian Terakhir", fontsize=10)
ax_rfm[0].set_ylabel("Customer ID", fontsize=10)

# Top Frequency
top_freq = rfm_df.sort_values(by="frequency", ascending=False).head(5)
sns.barplot(x="frequency", y="short_id", data=top_freq, hue="short_id", palette="Blues_r", legend=False, ax=ax_rfm[1])
ax_rfm[1].set_title("Top 5 Customers by Frequency", fontsize=12, fontweight="bold")
ax_rfm[1].set_xlabel("Total Pesanan", fontsize=10)
ax_rfm[1].set_ylabel(None)

# Top Monetary
top_mon = rfm_df.sort_values(by="monetary", ascending=False).head(5)
sns.barplot(x="monetary", y="short_id", data=top_mon, hue="short_id", palette="Oranges_r", legend=False, ax=ax_rfm[2])
ax_rfm[2].set_title("Top 5 Customers by Monetary (BRL)", fontsize=12, fontweight="bold")
ax_rfm[2].set_xlabel("Total Belanja (BRL)", fontsize=10)
ax_rfm[2].set_ylabel(None)

plt.tight_layout()
st.pyplot(fig_rfm)
plt.close()

# ==============================================================================
# FOOTER
# ==============================================================================
st.caption("Proyek Analisis Data - Dicoding 'Belajar Fundamental Analisis Data' © 2026 Gian Abi Firdaus")
