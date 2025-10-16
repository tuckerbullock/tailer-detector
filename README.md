# Tailer Detector - Sports Betting Project

Detects groups of users who tail (copy) sharp bettors and simulates actions (alerts / prop pulls / limits). Designed as a demo project with simulated betting logs to avoid needing access to proprietary sportsbook user databases.

Features:
- Synthetic betting log generator (realistic timestamps, amounts, props)
- Rule-based and ML detection pipelines for tailing behavior
- REST API exposing detection results
- Streamlit dashboard for visualization and replay simulation
- Unit tests and evaluation metrics (precision/recall, detection latency)

Tech stack: Python, FastAPI, PostgreSQL (or SQLite for demos), Pandas, scikit-learn, Streamlit, Docker.

Getting started:
1. `git clone ...`
2. Create venv, `pip install -r requirements.txt`
3. `python synth/generate_data.py`  # creates sample logs
4. `uvicorn app.main:app --reload`  # run API
5. `streamlit run ui/dashboard.py`  # open dashboard

Future ideas:
- Add alerts when a tailer is flagged
- Visualize lag times in charts
- Use an actual database instead of CSV files
- Add machine learning for smarter detection
  
