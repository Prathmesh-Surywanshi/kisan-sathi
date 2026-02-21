import { useEffect, useState } from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import MarketInsights from './pages/MarketInsights';
import RecommendationPage from './pages/RecommendationPage';
import ResultsPage from './pages/ResultsPage';

function App() {
  const [crops, setCrops] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch available crops on app load
    const fetchCrops = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/crops/list');
        const data = await response.json();
        if (data.status === 'success') {
          setCrops(data.crops);
        }
      } catch (error) {
        console.error('Error fetching crops:', error);
      }
    };

    fetchCrops();
  }, []);

  return (
    <Router>
      <div className="App">
        <Navbar />
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/recommend" element={<RecommendationPage crops={crops} />} />
          <Route path="/result" element={<ResultsPage />} />
          <Route path="/results" element={<ResultsPage />} />
          <Route path="/market-insights" element={<MarketInsights crops={crops} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
