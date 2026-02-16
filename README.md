# KAISAN - Crop Recommendation & Decision Support System

![KAISAN Banner](https://img.shields.io/badge/Version-1.0.0-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-18.2.0-61dafb)
![Flask](https://img.shields.io/badge/Flask-2.3.2-black)

## 🌾 **Project Overview**

KAISAN is an intelligent agricultural decision support system designed to help Indian farmers make data-driven decisions about crop selection. The system recommends the best crops to grow based on:

- **Soil Conditions**: Nitrogen (N), Phosphorus (P), Potassium (K) levels
- **Environmental Factors**: Temperature, humidity, pH, and rainfall
- **Market Trends**: Local demand, pricing, and global market access
- **Risk Assessment**: Weather, market, and disease risk analysis
- **Seasonal Guidance**: Optimal crops for each season

### Key Features

✅ **99.09% Accurate Crop Classification** - Using Random Forest ML model  
✅ **95% Yield Prediction Accuracy** - Estimated yield predictions  
✅ **22 Supported Crops** - Comprehensive coverage of major Indian crops  
✅ **Beautiful Farmer-Centric UI** - Mobile-responsive, easy-to-use interface  
✅ **Market Insights** - Real-time market trends and seasonal recommendations  
✅ **Risk Management** - Comprehensive risk assessment for informed decisions  
✅ **Real-time Recommendations** - Instant crop suggestions based on input conditions  

---

## 🏗️ **System Architecture**

```
KAISAN/
├── backend/
│   ├── app.py                    # Flask API server
│   ├── requirements.txt           # Python dependencies
│   └── data/
│       ├── models/               # Pre-trained ML models
│       └── processed/            # Cleaned datasets
│
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── pages/                # Page components
│   │   ├── styles/               # CSS modules
│   │   └── App.jsx               # Main app component
│   ├── public/
│   │   └── index.html            # HTML entry point
│   └── package.json              # React dependencies
│
└── README.md
```

---

## 🚀 **Quick Start Guide**

### Prerequisites

- **Python** 3.8+ (for backend)
- **Node.js** 14+ (for frontend)
- **npm** or **yarn**
- **Git**

### 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd kaisan
```

### 2️⃣ Setup Backend

#### Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Run Flask Server

```bash
# Make sure you're in the project root directory
python app.py
```

The backend will start on `http://localhost:5000`

**API Health Check:**
```bash
curl http://localhost:5000/api/health
```

### 3️⃣ Setup Frontend

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Run React Development Server

```bash
npm start
```

The frontend will open on `http://localhost:3000`

---

## 📊 **API Endpoints**

### Health Check
```http
GET /api/health
```

### Get Available Crops
```http
GET /api/crops/list
```

### Get Crop Recommendations
```http
POST /api/recommend-crop
Content-Type: application/json

{
  "nitrogen": 50.0,
  "phosphorus": 40.0,
  "potassium": 60.0,
  "temperature": 25.0,
  "humidity": 75.0,
  "ph": 6.5,
  "rainfall": 150.0
}
```

**Response:**
```json
{
  "status": "success",
  "primary_recommendation": "rice",
  "confidence": 94.5,
  "top_recommendations": [
    {
      "crop": "rice",
      "confidence": 94.5,
      "estimated_yield": 45.3,
      "unit": "kg/ha"
    },
    ...
  ]
}
```

### Predict Yield
```http
POST /api/yield-prediction
Content-Type: application/json

{
  "nitrogen": 50.0,
  "phosphorus": 40.0,
  "potassium": 60.0,
  "temperature": 25.0,
  "humidity": 75.0,
  "ph": 6.5,
  "rainfall": 150.0,
  "crop": "rice"
}
```

### Get Market Insights
```http
GET /api/market-insights/{crop}
```

### Get Seasonal Recommendations
```http
GET /api/seasonal-recommendations/{season}
```

Seasons: `summer`, `winter`, `rainy`, `spring`

### Get Model Information
```http
GET /api/model-info
```

### Get Feature Importance
```http
GET /api/feature-importance
```

---

## 🎨 **Frontend Pages**

### 🏠 **Home Page**
- Feature showcase with 6 key capabilities
- How it works step-by-step guide
- Statistics about the system
- CTA buttons for recommendations and insights

### 🌾 **Get Recommendations Page**
- Interactive form for soil and environmental conditions
- Real-time input validation
- Form sections:
  - Soil Nutrients (NPK)
  - Soil pH
  - Environmental Conditions (temperature, humidity, rainfall)
- Tips section for farmers

### 📊 **Results Page**
- Top crop recommendation with confidence score
- Priority yield prediction
- Alternative crop options
- Risk assessment
- Market insights specific to selected crop
- Optimal growing conditions
- Seasonal information

### 📈 **Market Insights Page**
- Season selection (Summer, Winter, Rainy, Spring)
- Seasonal crop recommendations
- Market trends and price stability
- Risk assessment dashboard
- Optimal growing conditions
- Growing timeline
- Farmer tips and best practices

---

## 🤖 **Machine Learning Models**

### Crop Classifier
- **Algorithm**: Random Forest Classifier
- **Features**: 14 engineered features (NPK, climate, soil properties)
- **Training Accuracy**: 99.09%
- **F1-Score**: 0.9908
- **Cross-Validation**: 0.9926 ± 0.0058

### Yield Predictor
- **Algorithm**: Random Forest Regressor
- **Features**: Same 14 features as classifier
- **R² Score**: 0.954 (95.4% variance explained)
- **RMSE**: 3.41 kg/ha
- **MAE**: 1.64 kg/ha

### Supported Crops (22 Total)

apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean, muskmelon, orange, papaya, pigeonpeas, pomegranate, rice, watermelon

---

## 📈 **Data Pipeline**

1. **Data Collection**: Multiple agricultural datasets
2. **Data Cleaning**: Missing value handling, outlier detection
3. **Feature Engineering**: 
   - Derived features (NPK score, temperature favorability, pH suitability, etc.)
   - Data normalization and scaling
4. **Model Training**: 80-20 train-test split with cross-validation
5. **Model Deployment**: Saved models via joblib

---

## 🎯 **UI/UX Highlights**

### Design Principles
- **Farmer-Centric**: Large text, clear labels, intuitive navigation
- **Mobile-First**: Fully responsive design
- **Accessibility**: WCAG compliant color contrasts and keyboard navigation
- **Performance**: Optimized assets and lazy loading

### Color Palette
- **Primary Green** (#2ecc71): Growth and nature
- **Dark Green** (#27ae60): Trust and stability
- **Blue Accents** (#3498db): Information and reliability
- **Orange Warnings** (#e67e22): Caution and risk

### Components
- **Cards**: Information containers with hover effects
- **Buttons**: Clear CTAs with loading states
- **Forms**: Validated inputs with error messaging
- **Charts**: Visualizations for trends and insights

---

## 🔧 **Troubleshooting**

### Backend Issues

**Problem**: Port 5000 already in use
```bash
# Use different port
python -c "import os; os.environ['FLASK_PORT'] = '5001'; exec(open('app.py').read())"
```

**Problem**: Models not found
```bash
# Ensure you're in the project root directory
# Check that data/models/ contains the .pkl files
ls data/models/
```

### Frontend Issues

**Problem**: CORS errors
- Backend CORS is already enabled in app.py
- Ensure Flask is running on http://localhost:5000

**Problem**: npm install fails
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📦 **Deployment**

### Docker Setup (Optional)

```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

```dockerfile
# Frontend Dockerfile
FROM node:14
WORKDIR /app
COPY frontend/package.json .
RUN npm install
COPY frontend/ .
RUN npm run build
CMD ["npm", "start"]
```

### Production Deployment

**Backend** (using Gunicorn):
```bash
gunicorn -b 0.0.0.0:5000 --workers 4 app:app
```

**Frontend** (using Vercel or Netlify):
```bash
cd frontend
npm run build
# Deploy the build/ folder
```

---

## 📝 **Project Structure Details**

### Backend
- **app.py**: Main Flask application with 9 API endpoints
- **requirements.txt**: All Python dependencies pinned to versions
- **data/models/**: Pre-trained models (crop_classifier.pkl, yield_predictor.pkl)
- **data/processed/**: Cleaned datasets for reference

### Frontend
- **src/App.jsx**: Main app with routing
- **src/components/**: Reusable components (Header, Navbar)
- **src/pages/**: Routed page components (Home, Recommendation, Results, Market Insights)
- **src/styles/**: Component-specific CSS with responsive design

---

## 🎓 **Learning Outcomes**

This project demonstrates:
- ✅ Full-stack web development (Python Flask + React)
- ✅ Machine learning model integration
- ✅ RESTful API design
- ✅ Responsive UI/UX design
- ✅ Real-world agricultural problem solving
- ✅ Data pipeline and feature engineering

---

## 🤝 **Contributing**

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 **License**

This project is open source and available under the MIT License.

---

## 👥 **Team**

Built for the Hackathon with focus on:
- Solving real agricultural problems
- Maximizing UI/UX for farmers
- Ensuring ML accuracy and reliability
- Creating an accessible and scalable solution

---

## 📞 **Support**

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team

---

## 🌱 **Future Enhancements**

- [ ] Real-time weather API integration
- [ ] Multi-language support (Hindi, Tamil, etc.)
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Farmer community forum
- [ ] Government scheme recommendations
- [ ] Pest and disease identification
- [ ] Supply chain marketplace integration

---

**Happy Farming! 🌾**

*KAISAN - Making Agriculture Intelligent*
