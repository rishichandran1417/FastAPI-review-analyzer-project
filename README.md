# Amazon Review Analysis Dashboard

A powerful, full-stack web application designed to scrape, analyze, and visualize Amazon product reviews. This project leverages **FastAPI** for the backend, **BeautifulSoup4** for web scraping, **TextBlob** for sentiment analysis, and **Matplotlib/Chart.js** for advanced data visualization.

## 🚀 Features

- **Automated Web Scraping**: Extracts review titles, text, and ratings directly from Amazon product pages.
- **Sentiment Analysis**: Uses Natural Language Processing (NLP) to categorize reviews as Positive, Neutral, or Negative.
- **Dynamic Analytics Dashboard**:
    - Real-time statistics (Total reviews, Average rating).
    - interactive distribution charts (Chart.js).
    - Statistical correlations (Rating vs. Sentiment, Rating vs. Length).
- **Advanced Matplotlib Visualizations**:
    - Review length distribution histograms.
    - Sentiment polarity density plots.
    - Comparative box plots (Length by Rating).
- **Dark Mode UI**: A premium, modern interface with smooth animations and responsive design.

## 🛠 Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite3
- **Scraping**: BeautifulSoup4, Requests
- **NLP**: TextBlob, NLTK
- **Analysis**: Scipy, NumPy
- **Visualization**: Matplotlib, Chart.js
- **Frontend**: Jinja2 Templates, Vanilla CSS

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gayurajeev/FastAPI-review-analyzer-project.git
   cd FastAPI-review-analyzer-project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

4. Open your browser at `http://127.0.0.1:8000`.

## 📸 Screenshots

*(Add your screenshots here after pushing to GitHub)*

---
*Created as part of a Next-Generation Web Scraping & Machine Learning project.*
