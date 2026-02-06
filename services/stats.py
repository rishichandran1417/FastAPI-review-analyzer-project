def calculate_stats(reviews):
    total = len(reviews)
    pos = sum(1 for r in reviews if r.get("sentiment", "").lower() == "positive")
    neg = sum(1 for r in reviews if r.get("sentiment", "").lower() == "negative")
    neu = sum(1 for r in reviews if r.get("sentiment", "").lower() == "neutral")

    avg_rating = round(sum(r["rating"] for r in reviews) / total, 2) if total else 0

    stars = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in reviews:
        try:
            rating = int(round(r.get("rating", 0)))
            if 1 <= rating <= 5:
                stars[rating] += 1
        except:
            pass

    return {
        "total": total,
        "positive": pos,
        "negative": neg,
        "neutral": neu,
        "avg_rating": avg_rating,
        "stars": [stars[1], stars[2], stars[3], stars[4], stars[5]]
    }

def calculate_correlations(reviews):
    if not reviews:
        default_val = {"r": 0, "p": 0, "text": "No data available"}
        return {
            "rating_sentiment": default_val,
            "rating_length": default_val
        }
    
    from scipy.stats import pearsonr
    def get_description(r):
        if abs(r) > 0.7: return "Strong"
        if abs(r) > 0.4: return "Moderate"
        if abs(r) > 0.1: return "Weak"
        return "Negligible"

    try:
        ratings = [r["rating"] for r in reviews]
        polarities = [r["polarity"] for r in reviews]
        lengths = [len(r["review_text"]) for r in reviews]
        
        # Rating vs Sentiment
        if len(set(ratings)) > 1 and len(set(polarities)) > 1:
            r_s, p_s = pearsonr(ratings, polarities)
            rating_sentiment = {
                "r": round(r_s, 2),
                "p": round(p_s, 4),
                "text": f"{get_description(r_s)} {'positive' if r_s > 0 else 'negative'} relationship"
            }
        else:
            rating_sentiment = {"r": 0, "p": 0, "text": "Insufficient variance"}

        # Rating vs Length
        if len(set(ratings)) > 1 and len(set(lengths)) > 1:
            r_l, p_l = pearsonr(ratings, lengths)
            rating_length = {
                "r": round(r_l, 2),
                "p": round(p_l, 4),
                "text": f"{get_description(r_l)} {'positive' if r_l > 0 else 'negative'} relationship"
            }
        else:
            rating_length = {"r": 0, "p": 0, "text": "Insufficient variance"}

        return {
            "rating_sentiment": rating_sentiment,
            "rating_length": rating_length
        }
    except Exception as e:
        print(f"Correlation error: {e}")
        err_val = {"r": 0, "p": 0, "text": "Calculation error"}
        return {
            "rating_sentiment": err_val,
            "rating_length": err_val
        }

def calculate_detailed_sentiment_distribution(reviews):
    """Calculate detailed sentiment distribution with 5 levels"""
    if not reviews:
        return {
            "very_positive": 0,
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "very_negative": 0
        }
    
    very_positive = sum(1 for r in reviews if r.get("polarity", 0) > 0.5)
    positive = sum(1 for r in reviews if 0.1 < r.get("polarity", 0) <= 0.5)
    neutral = sum(1 for r in reviews if -0.1 <= r.get("polarity", 0) <= 0.1)
    negative = sum(1 for r in reviews if -0.5 <= r.get("polarity", 0) < -0.1)
    very_negative = sum(1 for r in reviews if r.get("polarity", 0) < -0.5)
    
    return {
        "very_positive": very_positive,
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "very_negative": very_negative
    }

def calculate_advanced_metrics(reviews):
    """Calculate advanced disagreement metrics"""
    if not reviews:
        return {
            "rating": {"mean": 0, "median": 0, "std": 0, "variance": 0, "skewness": 0, "kurtosis": 0},
            "polarity": {"mean": 0, "median": 0, "std": 0, "variance": 0, "skewness": 0, "kurtosis": 0}
        }
    
    import numpy as np
    from scipy import stats as scipy_stats
    
    ratings = [r["rating"] for r in reviews if r.get("rating") is not None]
    polarities = [r["polarity"] for r in reviews if r.get("polarity") is not None]
    
    def calc_metrics(data):
        if not data or len(data) < 2:
            return {"mean": 0, "median": 0, "std": 0, "variance": 0, "skewness": 0, "kurtosis": 0}
        arr = np.array(data)
        return {
            "mean": round(float(np.mean(arr)), 6),
            "median": round(float(np.median(arr)), 6),
            "std": round(float(np.std(arr, ddof=1)), 6),
            "variance": round(float(np.var(arr, ddof=1)), 6),
            "skewness": round(float(scipy_stats.skew(arr)), 6),
            "kurtosis": round(float(scipy_stats.kurtosis(arr)), 6)
        }
    
    return {
        "rating": calc_metrics(ratings),
        "polarity": calc_metrics(polarities)
    }

def get_sentiment_by_rating(reviews):
    """Calculate average sentiment polarity for each star rating (1-5)"""
    # Initialize buckets
    rating_buckets = {1: [], 2: [], 3: [], 4: [], 5: []}
    
    for r in reviews:
        try:
            rating = int(round(r.get("rating", 0)))
            if 1 <= rating <= 5:
                # Use polarity if available, else 0
                polarity = r.get("polarity", 0)
                if polarity is None: polarity = 0
                rating_buckets[rating].append(polarity)
        except:
            continue
            
    # Calculate averages
    averages = []
    for star in range(1, 6):
        vals = rating_buckets[star]
        if vals:
            avg = sum(vals) / len(vals)
            # Normalize to 0-100 scale for chart (approx) or keep -1 to 1?
            # Chart usually expects percentage or similar. Let's map -1..1 to 0..100% 
            # where 0 is -1, 50 is 0, 100 is +1.
            # actually better to just return the polarity avg and let frontend handle or pre-process.
            # But specific dashboard chart seems to range 0-100%.
            # Let's start with mapping: (val + 1) * 50
            normalized = (avg + 1) * 50
            averages.append(round(normalized, 1))
        else:
            averages.append(0)
            
    return averages


