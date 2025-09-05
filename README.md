[README (3).md](https://github.com/user-attachments/files/22167160/README.3.md)
# 🏅 Olympic Games Analysis Web App

An **interactive Streamlit web application** to analyze and visualize **Olympic Games data**.  
The app provides insights into medal tallies, country-wise performance, athlete statistics, and historical trends.

## ✨ Features
- 📊 **Medal Tally** – Explore medal counts by country and year  
- 🌍 **Country-wise Analysis** – Track performance of nations across time  
- 🧑‍🤝‍🧑 **Athlete Insights** – Visualize trends in height, weight, and age  
- 🔥 **Top Athletes** – Discover the most successful Olympians by sport and country  
- 📈 **Visualizations** – Interactive charts using Plotly, Seaborn, and Matplotlib  

## 🛠️ Tech Stack
- [Python](https://www.python.org/)  
- [Streamlit](https://streamlit.io/) for web app  
- [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/) for data processing  
- [Plotly](https://plotly.com/) & [Seaborn](https://seaborn.pydata.org/) for visualization  

## 📂 Project Structure
```
Olympic-Analysis/
│── app.py             # Main Streamlit app
│── helper.py          # Utility functions
│── preprocess.py      # Preprocessing functions
│── requirements.txt   # Dependencies
│── Procfile           # For Render deployment
│── .streamlit/
│   └── config.toml    # Streamlit config
│── data/
    └── athlete_events.csv  # Olympic dataset
```

## 🚀 Deployment on Render
This app is deployed on [Render](https://render.com/).  
To deploy your own:
1. Fork/clone this repo  
2. Push to GitHub with `requirements.txt` and `Procfile`  
3. On Render → **New Web Service** → connect repo  
4. Use:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

## ▶️ Run Locally
Clone this repo:
```bash
git clone https://github.com/Sourabh2303/Olympic-Analysis.git
cd Olympic-Analysis
```

Create virtual environment and install dependencies:
```bash
python -m venv .venv
.venv\Scripts\activate    # On Windows
source .venv/bin/activate # On Linux/Mac
pip install -r requirements.txt
```

Run the Streamlit app:
```bash
streamlit run app.py
```

Then open 👉 `http://localhost:8501` in your browser.

## 📊 Dataset
The dataset used is **Olympic athlete events** (available on Kaggle).  
Make sure `athlete_events.csv` is inside the repo for the app to run.

---

## 🙌 Author
👤 **Sourabh Kumar**  
- GitHub: [Sourabh2303](https://github.com/Sourabh2303)

---

⭐ If you like this project, don’t forget to **star the repo**!
