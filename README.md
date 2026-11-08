# Proyek Analisis Data: E-Commerce Public Dataset (Olist)

Submission akhir untuk kelas **Belajar Fundamental Analisis Data** - Dicoding Indonesia.

- **Nama:** Gian Abi Firdaus
- **ID Dicoding:** gianabif14

---

## Ringkasan Proyek

Proyek ini bertujuan untuk menganalisis performa bisnis e-commerce berbasis data transaksi riil dari platform Olist di Brasil. Analisis berfokus pada dua pertanyaan bisnis strategis menggunakan framework **SMART**:
1. **Pertanyaan 1 (Performa Produk & Revenue):** Kategori produk apa saja yang menghasilkan total pendapatan (*revenue*) tertinggi dan terendah sepanjang tahun 2017, serta bagaimana tren pertumbuhannya per kuartal?
2. **Pertanyaan 2 (Demografi Wilayah & Biaya Logistik):** Wilayah/negara bagian (*customer_state*) mana saja yang menyumbang nilai transaksi (GMV) terbesar sepanjang Semester 1 tahun 2018, dan berapa rata-rata biaya ongkos kirim (*freight value*) di wilayah tersebut?
3. **Analisis Lanjutan:** Segmentasi perilaku pelanggan menggunakan model **RFM Analysis** (*Recency, Frequency, Monetary*).

---

## Struktur Direktori

```text
submission/
├── dashboard/
│   ├── dashboard.py         # Skrip aplikasi dashboard Streamlit
│   └── main_data.csv        # Data bersih gabungan untuk dashboard
├── data/
│   ├── customers_dataset.csv
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   └── products_dataset.csv
├── notebook.ipynb           # Notebook Jupyter untuk Data Wrangling, EDA, dan Visualisasi
├── README.md                # Dokumentasi proyek
├── requirements.txt         # Daftar dependensi library Python
└── url.txt                  # URL deployment dashboard di Streamlit Community Cloud
```

---

## Panduan Menjalankan Proyek di Komputer Lokal

### 1. Masuk ke Direktori Proyek
Buka terminal / PowerShell dan arahkan ke direktori `submission`:
```bash
cd submission
```

### 2. Membuat dan Mengaktifkan Virtual Environment (Disarankan)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Menginstal Dependensi
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Dashboard Streamlit
Jalankan perintah berikut:
```bash
streamlit run dashboard/dashboard.py
```
Aplikasi dashboard akan terbuka secara otomatis di browser Anda pada alamat `http://localhost:8501`.

### 5. Url Ke Streamlit Cloud
https://d6zbgvvxcapqshwbcp6tc4.streamlit.app/
