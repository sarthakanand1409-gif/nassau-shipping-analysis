
│   └── .streamlit/
│       └── config.toml
├── reports/
│   ├── research_paper.md
│   └── executive_summary.md
├── requirements.txt
├── README.md
└── .gitignore
```
 
---
 
## ⚙️ Installation
 
```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/nassau-shipping-analysis.git
cd nassau-shipping-analysis
 
# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows
 
# 3. Install dependencies
pip install -r requirements.txt
```
 
### `requirements.txt`
 
```txt
pandas==2.2.0
numpy==1.26.4
plotly==5.18.0
streamlit==1.31.0
scikit-learn==1.4.0
folium==0.15.1
streamlit-folium==0.18.0
geopy==2.4.1
matplotlib==3.8.2
seaborn==0.13.2
openpyxl==3.1.2
jupyter==1.0.0
```
 
---
 
## 🚀 Usage
 
### Step 1 — Run the data pipeline (once)
 
```bash
# Run cleaning and feature engineering notebooks
cd notebooks
jupyter notebook
# Execute: 01_data_cleaning.ipynb → 02_feature_engineering.ipynb
 
# Generate geocoding and KPIs
cd ../src
python data_loader.py        # adds customer state coordinates
python kpi_calculator.py     # computes route-level KPIs
```
 
### Step 2 — Launch the dashboard
 
```bash
cd app
streamlit run streamlit_app.py
```
 
Open **http://localhost:8501** in your browser.
 
---
 
## 🔬 Analytical Methodology
 
### 1. Data Cleaning & Validation
- Validate date formats (DD-MM-YYYY)
- Remove invalid or negative lead times
- Handle missing shipment records
- Standardize geographic fields
### 2. Feature Engineering
- Calculate Shipping Lead Time (days)
- Categorize routes by `Factory → Customer Region` and `Factory → Customer State`
- Group shipments by Ship Mode
### 3. Route Definition & Aggregation
Each route is defined as `Factory Location → Customer State / Region`. For each route:
- Total shipments
- Average shipping lead time
- Lead time variability
### 4. Efficiency Benchmarking
- Rank routes from fastest to slowest
- Identify top 10 most efficient and bottom 10 least efficient routes
### 5. Geographic Bottleneck Analysis
- Identify regions with high average lead time
- Flag high shipment volume + poor performance
- Detect congestion-prone states or regions
### 6. Ship Mode Performance Analysis
- Compare efficiency across Standard / Expedited shipping
- Evaluate cost-time tradeoffs (descriptive)
---
 
## 📐 Key Performance Indicators (KPIs)
 
| KPI | Definition |
|---|---|
| **Shipping Lead Time** | Ship Date − Order Date |
| **Average Lead Time** | Mean shipping duration per route |
| **Route Volume** | Number of orders per route |
| **Delay Frequency** | % of shipments exceeding threshold |
| **Route Efficiency Score** | Normalized lead-time performance (0–100) |
| **Lead Time Variability** | Standard deviation of lead time per route |
| **Profit Margin %** | Gross Profit ÷ Sales × 100 |
 
---
 
## 📊 Dashboard Modules
 
### 🏠 Home
KPI overview cards + global sidebar filters (date range, region, ship mode, delay threshold).
 
### 🛣️ Route Overview
- Average lead time by route
- Route performance leaderboard (top/bottom routes)
- Factory performance comparison
### 🗺️ Geographic Shipping Map
- US choropleth heatmap of shipping efficiency
- Route network visualization
- Regional bottleneck detection
### 🚚 Ship Mode Comparison
- Lead time comparison by shipping method
- Ship Mode × Region heatmap
### 🔎 Route Drill-Down
- State-level performance insights
- Order-level shipment timelines
- Product breakdown per route
**User Capabilities:** Date range filter · Region/State selector · Ship mode filter · Lead-time threshold slider · CSV export
 
---
 
## ☁️ Deployment
 
### Push to GitHub
 
```bash
git init
git add .
git commit -m "Initial commit: shipping route efficiency analysis"
git remote add origin https://github.com/YOUR_USERNAME/nassau-shipping-analysis.git
git branch -M main
git push -u origin main
```
 
### Deploy to Streamlit Community Cloud
 
1. Go to **https://share.streamlit.io**
2. Sign in with GitHub
3. Click **New app**
4. Repository: `YOUR_USERNAME/nassau-shipping-analysis`
5. Branch: `main`
6. Main file path: `app/streamlit_app.py`
7. Click **Deploy**
> **Live App:** `https://YOUR-APP-URL.streamlit.app`
 
### `.streamlit/config.toml`
 
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
 
[server]
maxUploadSize = 200
```
 
---
 
## 💡 Results & Insights
 
> Replace the placeholders below with your actual computed numbers from the analysis.
 
- **Lead time:** Median X days; Same Day class is ~Y% faster than Standard Class
- **Most efficient routes:** [Top 3 routes with metrics]
- **Critical bottlenecks:** [N] states account for [X]% of volume but [Y]% of all delays
- **Geographic gap:** Sugar Shack (Minnesota) shows the longest reach into the Pacific region
### Recommendations
1. Open a Pacific-region distribution hub to reduce Sugar Shack → CA/OR/WA lead times
2. Apply a ship-mode upgrade policy for high-value orders to bottleneck states
3. Audit carriers on the 5 worst-performing routes
4. Pre-position Q4 inventory in high-volume states
---
 
## 📦 Deliverables
 
| Deliverable | Location |
|---|---|
| Research paper (EDA, insights, recommendations) | `reports/research_paper.md` |
| Streamlit dashboard (live analytics) | Streamlit Cloud URL |
| Executive summary for stakeholders | `reports/executive_summary.md` |
| Source code | This repository |
| Visualizations | `reports/*.html`, `reports/*.png` |
 
---
 
## 🗺️ Roadmap
 
- [x] Data cleaning & feature engineering
- [x] Route-level KPI computation
- [x] Geographic bottleneck analysis
- [x] Ship mode performance analysis
- [x] Interactive Streamlit dashboard
- [x] Research paper & executive summary
- [ ] Predictive lead-time model (regression)
- [ ] Delay-risk classification model
- [ ] Time-series volume forecasting (Prophet)
---
 
## 📄 License
 
This project is licensed under the MIT License — see the `LICENSE` file for details.
 
---
 
## 🙏 Acknowledgments
 
- Dataset: Nassau Candy Distributor shipment records
- Built with Python, Streamlit, and Plotly
---
 
<div align="center">
**⭐ If you found this project useful, consider giving it a star!**
 
</div>