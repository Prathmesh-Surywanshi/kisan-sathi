"""
KISAN - Crop Recommendation & Decision Support System
Flask Backend API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import joblib
import json
from pathlib import Path
import logging
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Model paths
MODEL_DIR = Path("data/models")
PROCESSED_DATA_DIR = Path("data/processed")

# Global variables for models
crop_classifier = None
yield_predictor = None
feature_scaler = None
encoders_info = None
model_metadata = None
training_data = None
market_prices = None
market_model_cache = {}
location_data = None
soil_defaults = None

SEASON_MONTHS = {
    "summer": [3, 4, 5, 6],
    "rainy": [7, 8, 9, 10],
    "winter": [11, 12, 1, 2],
    "spring": [2, 3, 4]
}

def load_models():
    """Load trained ML models and scalers"""
    global crop_classifier, yield_predictor, feature_scaler, encoders_info, model_metadata, training_data, market_prices, location_data, soil_defaults
    
    try:
        logger.info("Loading models...")
        crop_classifier = joblib.load(MODEL_DIR / "crop_classifier.pkl")
        yield_predictor = joblib.load(MODEL_DIR / "yield_predictor.pkl")
        feature_scaler = joblib.load(MODEL_DIR / "feature_scaler.pkl")
        
        with open(MODEL_DIR / "encoders_info.json", 'r') as f:
            encoders_info = json.load(f)
        
        with open(MODEL_DIR / "model_metadata.json", 'r') as f:
            model_metadata = json.load(f)
        
        # Load sample training data for market insights
        training_data = pd.read_csv(PROCESSED_DATA_DIR / "merged_training_data.csv")

        # Load market price data for dynamic insights
        market_prices = pd.read_csv(
            PROCESSED_DATA_DIR / "cleaned_Agriculture_price_dataset.csv",
            low_memory=False
        )
        market_prices.columns = [col.strip().lower() for col in market_prices.columns]
        market_prices.rename(
            columns={
                "district_name": "district",
                "market_name": "market"
            },
            inplace=True
        )

        market_prices["commodity"] = (
            market_prices["commodity"].astype(str).str.strip().str.lower()
        )
        market_prices["state"] = market_prices["state"].astype(str).str.strip().str.lower()
        market_prices["district"] = market_prices["district"].astype(str).str.strip().str.lower()
        market_prices["market"] = market_prices["market"].astype(str).str.strip().str.lower()
        market_prices["modal_price"] = pd.to_numeric(
            market_prices["modal_price"],
            errors="coerce"
        )
        market_prices["price_date"] = pd.to_datetime(
            market_prices["price_date"],
            errors="coerce"
        )
        market_prices = market_prices.dropna(
            subset=["commodity", "modal_price", "price_date"]
        )

        market_prices["date_ordinal"] = market_prices["price_date"].map(datetime.toordinal)
        market_prices["month"] = market_prices["price_date"].dt.month
        market_prices["dayofyear"] = market_prices["price_date"].dt.dayofyear

        # Load location data from ICRISAT dataset
        try:
            location_data = pd.read_csv(PROCESSED_DATA_DIR / "cleaned_ICRISAT-District Level Data.csv")
            logger.info(f"✓ Location data loaded: {location_data.shape[0]} records")
        except Exception as e:
            logger.warning(f"Could not load location data: {e}")
            location_data = None

        # Load soil defaults from crop recommendation data
        try:
            soil_defaults = pd.read_csv(PROCESSED_DATA_DIR / "cleaned_Crop_recommendation.csv")
            logger.info(f"✓ Soil defaults loaded: {soil_defaults.shape[0]} samples")
        except Exception as e:
            logger.warning(f"Could not load soil defaults: {e}")
            soil_defaults = None
        
        logger.info("✓ All models loaded successfully!")
        return True
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        return False

def normalize_text(value: str) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()

def filter_market_prices(crop: str, state: str = None, district: str = None, market: str = None):
    if market_prices is None:
        return pd.DataFrame()

    df = market_prices
    crop_key = normalize_text(crop)
    if crop_key:
        df = df[df["commodity"] == crop_key]

    state_key = normalize_text(state)
    if state_key:
        df = df[df["state"] == state_key]

    district_key = normalize_text(district)
    if district_key:
        df = df[df["district"] == district_key]

    market_key = normalize_text(market)
    if market_key:
        df = df[df["market"] == market_key]

    return df.copy()

def apply_season_filter(df: pd.DataFrame, season: str = None):
    season_key = normalize_text(season)
    if not season_key or season_key not in SEASON_MONTHS:
        return df, False

    filtered = df[df["month"].isin(SEASON_MONTHS[season_key])].copy()
    return filtered, True

def classify_trend(df: pd.DataFrame) -> str:
    if df.shape[0] < 10:
        return "stable"

    df_sorted = df.sort_values("price_date")
    x = df_sorted["date_ordinal"].values
    y = df_sorted["modal_price"].values
    slope = np.polyfit(x, y, 1)[0]
    mean_price = float(np.mean(y)) if len(y) else 0
    if mean_price <= 0:
        return "stable"

    normalized_slope = slope / mean_price
    if normalized_slope > 0.0005:
        return "increasing"
    if normalized_slope < -0.0005:
        return "decreasing"
    return "stable"

def classify_stability(df: pd.DataFrame) -> str:
    if df.shape[0] < 10:
        return "stable"

    mean_price = df["modal_price"].mean()
    if mean_price == 0:
        return "stable"

    cv = df["modal_price"].std() / mean_price
    if cv < 0.05:
        return "stable"
    if cv < 0.15:
        return "moderate"
    return "volatile"

def forecast_price_ml(df: pd.DataFrame, cache_key: str):
    if df.shape[0] < 30:
        return None

    latest_date = df["price_date"].max()
    cached = market_model_cache.get(cache_key)
    if cached and cached["last_date"] == latest_date:
        model = cached["model"]
    else:
        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        df_sorted = df.sort_values("price_date")
        X = df_sorted[["date_ordinal", "month", "dayofyear"]]
        y = df_sorted["modal_price"]
        model.fit(X, y)
        market_model_cache[cache_key] = {
            "model": model,
            "last_date": latest_date
        }

    future_dates = pd.date_range(latest_date + timedelta(days=1), periods=30)
    future_features = pd.DataFrame({
        "date_ordinal": future_dates.map(datetime.toordinal),
        "month": future_dates.month,
        "dayofyear": future_dates.dayofyear
    })
    preds = model.predict(future_features)
    return {
        "avg": float(np.mean(preds)),
        "min": float(np.min(preds)),
        "max": float(np.max(preds)),
        "days": 30,
        "model": "RandomForestRegressor"
    }

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "crops": len(encoders_info['target_encoder']['classes']),
        "models": ["crop_classifier", "yield_predictor"]
    })

@app.route('/api/crops/list', methods=['GET'])
def get_crop_list():
    """Get list of all available crops"""
    crops = encoders_info['target_encoder']['classes']
    return jsonify({
        "status": "success",
        "crops": sorted(crops),
        "total": len(crops)
    })

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Get all available states and districts from location data"""
    try:
        if location_data is None or location_data.empty:
            return jsonify({
                "status": "error",
                "message": "Location data not available"
            }), 404
        
        locations = {}
        if 'state_name' in location_data.columns and 'dist_name' in location_data.columns:
            for state in location_data['state_name'].dropna().unique():
                districts = location_data[location_data['state_name'] == state]['dist_name'].dropna().unique().tolist()
                locations[state] = sorted([d for d in districts if d])
        
        return jsonify({
            "status": "success",
            "locations": locations,
            "total_states": len(locations)
        })
    except Exception as e:
        logger.error(f"Error getting locations: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/soil-data', methods=['GET'])
def get_soil_data():
    """Get average soil parameters based on location"""
    try:
        state = request.args.get('state', '').strip()
        district = request.args.get('district', '').strip()
        
        if not state:
            return jsonify({"status": "error", "message": "State is required"}), 400
        
        # Use soil defaults from crop recommendation data (averaged values)
        if soil_defaults is None or soil_defaults.empty:
            return jsonify({
                "status": "error",
                "message": "Soil data not available"
            }), 404
        
        # Get average NPK and pH values from the dataset
        # For now, provide typical values - in production, this could be location-specific
        n_avg = float(soil_defaults['n'].mean())
        p_avg = float(soil_defaults['p'].mean())
        k_avg = float(soil_defaults['k'].mean())
        ph_avg = float(soil_defaults['ph'].mean())
        
        # Add some variation based on state (simplified approach)
        state_variations = {
            'punjab': {'n': 1.1, 'p': 1.0, 'k': 0.9, 'ph': 1.0},
            'haryana': {'n': 1.1, 'p': 1.0, 'k': 0.9, 'ph': 1.0},
            'uttar pradesh': {'n': 1.0, 'p': 0.95, 'k': 1.0, 'ph': 1.0},
            'maharashtra': {'n': 0.9, 'p': 1.0, 'k': 1.1, 'ph': 0.98},
            'karnataka': {'n': 0.95, 'p': 1.05, 'k': 1.0, 'ph': 0.99},
            'tamil nadu': {'n': 0.9, 'p': 1.1, 'k': 1.0, 'ph': 0.97},
        }
        
        state_key = normalize_text(state)
        variation = state_variations.get(state_key, {'n': 1.0, 'p': 1.0, 'k': 1.0, 'ph': 1.0})
        
        soil_params = {
            'nitrogen': round(n_avg * variation['n'], 2),
            'phosphorus': round(p_avg * variation['p'], 2),
            'potassium': round(k_avg * variation['k'], 2),
            'ph': round(ph_avg * variation['ph'], 2),
            'state': state,
            'district': district,
            'data_source': 'aggregated_crop_data'
        }
        
        return jsonify({
            "status": "success",
            "soil_data": soil_params,
            "message": f"Average soil data for {state}"
        })
    except Exception as e:
        logger.error(f"Error getting soil data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/testing-centers', methods=['GET'])
def get_testing_centers():
    """Get nearby soil testing centers"""
    try:
        state = request.args.get('state', '').strip()
        
        # Mock data - can be replaced with real database
        testing_centers_db = {
            'andhra pradesh': [
                {'name': 'Agri Research Station, Guntur', 'location': 'Guntur', 'phone': '0863-2346789'},
                {'name': 'Soil Testing Lab', 'location': 'Vijayawada', 'phone': '0866-2478965'}
            ],
            'karnataka': [
                {'name': 'Dept of Agriculture', 'location': 'Bangalore', 'phone': '080-22250000'},
                {'name': 'Krishi Vigyan Kendra', 'location': 'Mysore', 'phone': '0821-2419876'}
            ],
            'maharashtra': [
                {'name': 'Agri Technology Mgmt', 'location': 'Pune', 'phone': '020-24537890'},
                {'name': 'Soil Health Card Center', 'location': 'Nashik', 'phone': '0253-2576543'}
            ],
            'punjab': [
                {'name': 'PAU Soil Testing Lab', 'location': 'Ludhiana', 'phone': '0161-2401960'},
                {'name': 'Dept of Agriculture', 'location': 'Amritsar', 'phone': '0183-2227845'}
            ],
            'tamil nadu': [
                {'name': 'Tamil Nadu Agri Univ', 'location': 'Coimbatore', 'phone': '0422-6611200'},
                {'name': 'Soil Testing Lab', 'location': 'Chennai', 'phone': '044-28524624'}
            ],
            'uttar pradesh': [
                {'name': 'Krishi Bhawan', 'location': 'Lucknow', 'phone': '0522-2286532'},
                {'name': 'Soil Testing Center', 'location': 'Meerut', 'phone': '0121-2764219'}
            ],
            'haryana': [
                {'name': 'HAU Soil Lab', 'location': 'Hisar', 'phone': '01662-289239'},
                {'name': 'Agri Dept Testing Center', 'location': 'Karnal', 'phone': '0184-2252600'}
            ]
        }
        
        state_key = normalize_text(state)
        centers = testing_centers_db.get(state_key, [])
        
        return jsonify({
            "status": "success",
            "centers": centers,
            "helpline": "1800-180-1551",
            "helpline_name": "Kisan Call Centre (Toll Free)",
            "message": f"Testing centers for {state}" if centers else "Contact Kisan Call Centre for nearest center"
        })
    except Exception as e:
        logger.error(f"Error getting testing centers: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/recommend-crop', methods=['POST'])
def recommend_crop():
    """
    Recommend crops based on soil and environmental conditions
    
    Request body:
    {
        "nitrogen": float,
        "phosphorus": float,
        "potassium": float,
        "temperature": float,
        "humidity": float,
        "ph": float,
        "rainfall": float
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 
                         'humidity', 'ph', 'rainfall']
        missing_fields = [f for f in required_fields if f not in data]
        
        if missing_fields:
            return jsonify({
                "status": "error",
                "message": f"Missing fields: {', '.join(missing_fields)}"
            }), 400
        
        # Extract features (must match training order)
        features = np.array([[
            data['nitrogen'],      # n
            data['phosphorus'],    # p
            data['potassium'],     # k
            data['temperature'],   # temperature
            data['humidity'],      # humidity
            data['ph'],            # ph
            data['rainfall'],      # rainfall
            data.get('rainfall_deviation_pct', 10),  # rainfall_deviation_pct
            data.get('npk_score', (data['nitrogen'] + data['phosphorus'] + data['potassium']) / 3),  # npk_score
            data.get('temp_favorability', data['temperature'] / 30),  # temp_favorability
            data.get('humidity_favorability', data['humidity'] / 100),  # humidity_favorability
            data.get('ph_suitability', 1 - abs(data['ph'] - 7) / 7),  # ph_suitability
            data.get('growth_potential', 0.5),  # growth_potential
            data.get('water_stress', 50)  # water_stress
        ]])
        
        # Scale features
        features_scaled = feature_scaler.transform(features)
        
        # Get probabilities for all crops
        probabilities = crop_classifier.predict_proba(features_scaled)[0]
        crop_names = encoders_info['target_encoder']['classes']
        
        # Get top recommendations
        top_indices = np.argsort(probabilities)[-5:][::-1]
        recommendations = []
        
        for idx in top_indices:
            crop = crop_names[idx]
            confidence = float(probabilities[idx]) * 100
            
            # Get yield prediction for this crop
            yield_pred = yield_predictor.predict(features_scaled)[0]
            
            recommendations.append({
                "crop": crop,
                "confidence": round(confidence, 2),
                "estimated_yield": round(float(yield_pred), 2),
                "unit": "kg/ha"
            })
        
        return jsonify({
            "status": "success",
            "primary_recommendation": recommendations[0]['crop'],
            "confidence": recommendations[0]['confidence'],
            "top_recommendations": recommendations,
            "input_conditions": {
                "nitrogen": data['nitrogen'],
                "phosphorus": data['phosphorus'],
                "potassium": data['potassium'],
                "temperature": data['temperature'],
                "humidity": data['humidity'],
                "ph": data['ph'],
                "rainfall": data['rainfall']
            }
        })
    
    except Exception as e:
        logger.error(f"Error in crop recommendation: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/yield-prediction', methods=['POST'])
def predict_yield():
    """
    Predict crop yield based on conditions
    
    Request body:
    {
        "nitrogen": float,
        "phosphorus": float,
        "potassium": float,
        "temperature": float,
        "humidity": float,
        "ph": float,
        "rainfall": float,
        "crop": string (optional)
    }
    """
    try:
        data = request.json
        
        # Extract features
        features = np.array([[
            data['nitrogen'],
            data['phosphorus'],
            data['potassium'],
            data['temperature'],
            data['humidity'],
            data['ph'],
            data['rainfall'],
            data.get('rainfall_deviation_pct', 10),
            data.get('npk_score', (data['nitrogen'] + data['phosphorus'] + data['potassium']) / 3),
            data.get('temp_favorability', data['temperature'] / 30),
            data.get('humidity_favorability', data['humidity'] / 100),
            data.get('ph_suitability', 1 - abs(data['ph'] - 7) / 7),
            data.get('growth_potential', 0.5),
            data.get('water_stress', 50)
        ]])
        
        # Scale features
        features_scaled = feature_scaler.transform(features)
        
        # Predict yield
        yield_pred = yield_predictor.predict(features_scaled)[0]
        
        return jsonify({
            "status": "success",
            "estimated_yield": round(float(yield_pred), 2),
            "unit": "kg/ha",
            "crop": data.get('crop', 'selected crop'),
            "confidence": "high"
        })
    
    except Exception as e:
        logger.error(f"Error in yield prediction: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/market-insights/<crop>', methods=['GET'])
def market_insights(crop):
    """Get market insights for a specific crop"""
    try:
        state = request.args.get("state")
        district = request.args.get("district")
        market = request.args.get("market")
        season = request.args.get("season")

        crop_data_all = filter_market_prices(crop, state=state, district=district, market=market)
        season_filtered_data, season_filter_applied = apply_season_filter(crop_data_all, season)
        crop_data = season_filtered_data if not season_filtered_data.empty else crop_data_all

        if crop_data.empty:
            return jsonify({
                "status": "success",
                "crop": crop,
                "has_market_data": False,
                "market_data": {
                    "demand_trend": "no data",
                    "price_stability": "no data",
                    "global_demand": "no data",
                    "recommendation": f"No price records found for {crop} in current market dataset."
                },
                "optimal_conditions": {
                    "temperature_range": "20-30°C",
                    "humidity_range": "60-80%",
                    "ph_range": "6.0-7.5",
                    "rainfall_range": "400-800mm"
                },
                "risk_assessment": {
                    "weather_risk": "medium",
                    "market_risk": "medium",
                    "disease_risk": "medium",
                    "overall_risk": "medium"
                },
                "seasonal_info": {
                    "best_season": season or "rainy season",
                    "growing_period": "100-150 days",
                    "harvest_time": "varies by region"
                }
            })

        crop_data = crop_data.sort_values("price_date")
        latest_row = crop_data.iloc[-1]
        latest_date = latest_row["price_date"]
        latest_price = float(latest_row["modal_price"])

        last_30 = crop_data[crop_data["price_date"] >= latest_date - timedelta(days=30)]
        last_90 = crop_data[crop_data["price_date"] >= latest_date - timedelta(days=90)]
        avg_30 = float(last_30["modal_price"].mean()) if not last_30.empty else latest_price
        avg_90 = float(last_90["modal_price"].mean()) if not last_90.empty else avg_30

        price_change_90 = 0.0
        if avg_90:
            price_change_90 = ((avg_30 - avg_90) / avg_90) * 100

        trend = classify_trend(last_90 if not last_90.empty else crop_data)
        stability = classify_stability(last_90 if not last_90.empty else crop_data)

        cache_key = f"{normalize_text(crop)}|{normalize_text(state)}|{normalize_text(district)}|{normalize_text(market)}"
        forecast = forecast_price_ml(crop_data, cache_key)

        if stability == "volatile":
            market_risk = "high"
        elif stability == "moderate":
            market_risk = "medium"
        else:
            market_risk = "low"

        demand_trend = "high" if trend == "increasing" else "moderate" if trend == "stable" else "low"

        recommendation = f"{crop.title()} prices are {trend}."
        if forecast:
            recommendation += f" 30-day expected average is about {forecast['avg']:.1f}."

        insights = {
            "status": "success",
            "crop": crop,
            "has_market_data": True,
            "market_data": {
                "demand_trend": demand_trend,
                "price_stability": stability,
                "global_demand": trend,
                "latest_price": {
                    "value": round(latest_price, 2),
                    "unit": "INR/quintal",
                    "date": latest_date.strftime("%Y-%m-%d")
                },
                "recent_average": {
                    "value": round(avg_30, 2),
                    "unit": "INR/quintal",
                    "days": 30
                },
                "price_change_90d_pct": round(price_change_90, 2),
                "forecast_30d": {
                    "avg": round(forecast["avg"], 2) if forecast else None,
                    "min": round(forecast["min"], 2) if forecast else None,
                    "max": round(forecast["max"], 2) if forecast else None,
                    "model": forecast["model"] if forecast else None,
                    "days": forecast["days"] if forecast else None
                },
                "recommendation": recommendation
            },
            "optimal_conditions": {
                "temperature_range": "20-30°C",
                "humidity_range": "60-80%",
                "ph_range": "6.0-7.5",
                "rainfall_range": "400-800mm"
            },
            "risk_assessment": {
                "weather_risk": "medium",
                "market_risk": market_risk,
                "disease_risk": "medium",
                "overall_risk": "medium"
            },
            "seasonal_info": {
                "best_season": season or "rainy season",
                "growing_period": "100-150 days",
                "harvest_time": "varies by region"
            },
            "data_coverage": {
                "records": int(crop_data.shape[0]),
                "from": crop_data["price_date"].min().strftime("%Y-%m-%d"),
                "to": latest_date.strftime("%Y-%m-%d"),
                "season_filter_applied": season_filter_applied
            }
        }
        
        return jsonify(insights)
    
    except Exception as e:
        logger.error(f"Error getting market insights: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/seasonal-recommendations/<season>', methods=['GET'])
def seasonal_recommendations(season):
    """Get crop recommendations for a specific season"""
    try:
        season_key = normalize_text(season)
        if season_key not in SEASON_MONTHS:
            return jsonify({
                "status": "error",
                "message": f"Invalid season '{season}'. Use summer, rainy, winter, or spring."
            }), 400

        if market_prices is None or market_prices.empty:
            return jsonify({
                "status": "success",
                "season": season,
                "recommended_crops": [],
                "reason": "Market dataset not loaded."
            })

        seasonal_df = market_prices[market_prices["month"].isin(SEASON_MONTHS[season_key])]

        if seasonal_df.empty:
            return jsonify({
                "status": "success",
                "season": season,
                "recommended_crops": [],
                "reason": f"No market records available for {season} season."
            })

        commodity_rank = (
            seasonal_df.groupby("commodity")
            .agg(records=("commodity", "count"), avg_price=("modal_price", "mean"))
            .sort_values(["records", "avg_price"], ascending=[False, False])
            .head(6)
            .reset_index()
        )

        crops = [item.title() for item in commodity_rank["commodity"].tolist()]

        return jsonify({
            "status": "success",
            "season": season,
            "recommended_crops": crops,
            "reason": f"Top commodities in {season} based on available market records",
            "data_source": "processed/cleaned_Agriculture_price_dataset.csv"
        })

    except Exception as e:
        logger.error(f"Error in seasonal recommendations: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/feature-importance', methods=['GET'])
def feature_importance():
    """Get feature importance from the model"""
    try:
        with open(MODEL_DIR / "feature_importance.json", 'r') as f:
            importance = json.load(f)
        
        feature_names = model_metadata['feature_names']
        detailed_importance = []
        
        for item in importance:
            if item['feature'] < len(feature_names):
                detailed_importance.append({
                    "feature": feature_names[item['feature']],
                    "importance": round(item['importance'], 4)
                })
        
        return jsonify({
            "status": "success",
            "feature_importance": sorted(detailed_importance, key=lambda x: x['importance'], reverse=True)
        })
    
    except Exception as e:
        logger.error(f"Error getting feature importance: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get information about the trained models"""
    return jsonify({
        "status": "success",
        "models": {
            "crop_classifier": {
                "type": model_metadata['crop_classifier']['model_type'],
                "accuracy": round(model_metadata['crop_classifier']['test_accuracy'], 4),
                "f1_score": round(model_metadata['crop_classifier']['f1_score'], 4)
            },
            "yield_predictor": {
                "type": model_metadata['yield_predictor']['model_type'],
                "r2_score": round(model_metadata['yield_predictor']['r2_score'], 4),
                "rmse": round(model_metadata['yield_predictor']['test_rmse'], 4)
            }
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    # Load models on startup
    if load_models():
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        logger.error("Failed to load models. Exiting...")
