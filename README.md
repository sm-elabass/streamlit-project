# Interactive CSV Data Explorer

A generic data exploration app built with **Streamlit**. Upload any CSV file and the app automatically detects column types, applies filters, and generates distribution, temporal, and geographic visualizations — no configuration required.

Tested with the **Titanic** and **Amazon Prime** datasets included in the repo.

---

## Features

- **Auto-detection** of categorical, temporal, and geographic columns
- **Sidebar filters**: year range slider and category selector (auto-detected)
- **4 analysis tabs**:
  - Overview — shape, column types, missing values, raw preview
  - Distribution — pie chart and bar chart of categorical columns
  - Temporal analysis — yearly trend line and top-5 years
  - Detailed analysis — geographic breakdown or per-column exploration
- **Full-text search** across any column
- Works with any CSV — no schema assumed

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Streamlit | Web app framework |
| Pandas | Data loading and filtering |
| Matplotlib | Pie charts |
| Python 3.x | Core language |

---

## Project Structure

```
csv-data-explorer/
├── amazon_analysis.py      # Main app — generic multi-tab CSV analyzer
├── streamlit_app.py        # Simple Titanic survivor explorer
├── duckdb_ex.py            # DuckDB query experiments
├── data/
│   ├── titanic.csv
│   └── amazon_prime_titles.csv
└── README.md
```

---

## Getting Started

### 1. Install dependencies

```bash
pip install streamlit pandas matplotlib
```

### 2. Run the generic CSV explorer

```bash
streamlit run amazon_analysis.py
```

### 3. (Optional) Run the basic Titanic app

```bash
streamlit run streamlit_app.py
```

The app opens at `http://localhost:8501`. Upload any CSV to start exploring.

---

## Sample Datasets

| File | Description |
|---|---|
| `data/titanic.csv` | Titanic passenger survival data |
| `data/amazon_prime_titles.csv` | Amazon Prime Video catalog (titles, genres, countries, years) |

Both files are included in the repo and can be used directly after launching the app.
