const fs = require('fs');
const path = require('path');

// Major Indian states for scheme generation
const MAJOR_STATES = [
  'Maharashtra', 'Karnataka', 'Gujarat', 'Punjab', 'Haryana',
  'Tamil Nadu', 'Uttar Pradesh', 'Bihar', 'Madhya Pradesh',
  'Andhra Pradesh', 'Telangana', 'West Bengal', 'Rajasthan',
  'Odisha', 'Jharkhand', 'Chhattisgarh', 'Kerala'
];

// Official URLs for Central Schemes
const CENTRAL_SCHEME_URLS = {
  'PM-KISAN: Pradhan Mantri Kisan Samman Nidhi': 'https://pmkisan.gov.in/',
  'Pradhan Mantri Fasal Bima Yojana': 'https://pmfby.gov.in/',
  'PM Kisan Samman Nidhi - Top-up Scheme': 'https://pmkisan.gov.in/',
  'Soil Health Card Scheme': 'https://soilhealth.dac.gov.in/',
  'Pradhan Mantri Krishi Sinchayee Yojana': 'https://pmksy.gov.in/',
  'Sub-Mission on Agricultural Mechanization': 'https://agrimech.dac.gov.in/',
  'Pradhan Mantri Annadata Aay Sanrakshan Abhiyaan (PM-AASHA)': 'https://pib.gov.in/',
  'National Mission for Sustainable Agriculture': 'https://nmsa.dac.gov.in/',
  'Paramparagat Krishi Vikas Yojana': 'https://pkvy.dac.gov.in/',
  'E-NAM: National Agriculture Market': 'https://www.enam.gov.in/'
};

// State Portal URLs
const STATE_PORTAL_URLS = {
  'Maharashtra': 'https://krishi.maharashtra.gov.in/',
  'Karnataka': 'https://raitamitra.karnataka.gov.in/',
  'Gujarat': 'https://ikhedut.gujarat.gov.in/',
  'Punjab': 'https://agriharyana.gov.in/',
  'Haryana': 'https://agriharyana.gov.in/',
  'Tamil Nadu': 'https://www.tn.gov.in/agriculture/',
  'Uttar Pradesh': 'https://agriculture.up.gov.in/',
  'Bihar': 'https://agriculture.bih.nic.in/',
  'Madhya Pradesh': 'https://dac.mp.gov.in/',
  'Andhra Pradesh': 'https://agriculture.ap.gov.in/',
  'Telangana': 'https://agriculture.telangana.gov.in/',
  'West Bengal': 'https://www.wbagrisnet.gov.in/',
  'Rajasthan': 'https://agriculture.rajasthan.gov.in/',
  'Odisha': 'https://agriculture.odisha.gov.in/',
  'Jharkhand': 'https://agriculture.jharkhand.gov.in/',
  'Chhattisgarh': 'https://agriculture.cg.gov.in/',
  'Kerala': 'https://agriculture.kerala.gov.in/'
};

const CATEGORIES = [
  'Subsidy', 'Loan', 'Insurance', 'Machinery',
  'Irrigation', 'Seeds', 'Crop Insurance', 'Fertilizer'
];

const CENTRAL_SCHEMES = [
  {
    name: 'PM-KISAN: Pradhan Mantri Kisan Samman Nidhi',
    category: 'Subsidy',
    description: 'Direct income support scheme providing ₹6000 annually to eligible farmers',
    benefitAmount: 6000,
    eligibility: 'Small and marginal farmers holding up to 2 hectares',
    officialDepartment: 'Ministry of Agriculture & Farmers Welfare'
  },
  {
    name: 'Pradhan Mantri Fasal Bima Yojana',
    category: 'Crop Insurance',
    description: 'Comprehensive crop insurance coverage against crop failure',
    benefitAmount: 50000,
    eligibility: 'All farmers including tenant farmers',
    officialDepartment: 'Ministry of Agriculture & Farmers Welfare'
  },
  {
    name: 'PM Kisan Samman Nidhi - Top-up Scheme',
    category: 'Subsidy',
    description: 'Additional financial support to PM-KISAN beneficiaries',
    benefitAmount: 2000,
    eligibility: 'Registered PM-KISAN beneficiaries',
    officialDepartment: 'Ministry of Agriculture & Farmers Welfare'
  },
  {
    name: 'Soil Health Card Scheme',
    category: 'Subsidy',
    description: 'Free soil testing and computerized soil health cards',
    benefitAmount: 0,
    eligibility: 'All farmers',
    officialDepartment: 'Ministry of Agriculture & Farmers Welfare'
  },
  {
    name: 'Pradhan Mantri Krishi Sinchayee Yojana',
    category: 'Irrigation',
    description: 'Subsidy for irrigation infrastructure development',
    benefitAmount: 100000,
    eligibility: 'Farmers with cultivable land',
    officialDepartment: 'Ministry of Agriculture & Farmers Welfare'
  },
  {
    name: 'Sub-Mission on Agricultural Mechanization',
    category: 'Machinery',
    description: 'Subsidy up to 50% for farm machinery purchase',
    benefitAmount: 75000,
    eligibility: 'Individual and group farmers',
    officialDepartment: 'Ministry of Agriculture & Farmers Welfare'
  },
  {
    name: 'Pradhan Mantri Annadata Aay Sanrakshan Abhiyaan (PM-AASHA)',
    category: 'Subsidy',
    description: 'Price support for agricultural commodities',
    benefitAmount: 45000,
    eligibility: 'Producers of notified commodities',
    officialDepartment: 'Ministry of Consumer Affairs'
  },
  {
    name: 'National Mission for Sustainable Agriculture',
    category: 'Subsidy',
    description: 'Support for sustainable farming practices and infrastructure',
    benefitAmount: 50000,
    eligibility: 'Farmers adopting sustainable practices',
    officialDepartment: 'Ministry of Agriculture & Farmers Welfare'
  },
  {
    name: 'Paramparagat Krishi Vikas Yojana',
    category: 'Subsidy',
    description: 'Promotion of organic farming and cluster formation',
    benefitAmount: 20000,
    eligibility: 'Organic farming enthusiasts',
    officialDepartment: 'Ministry of Agriculture & Farmers Welfare'
  },
  {
    name: 'E-NAM: National Agriculture Market',
    category: 'Subsidy',
    description: 'Online agricultural commodity trading platform access',
    benefitAmount: 0,
    eligibility: 'All registered traders and farmers',
    officialDepartment: 'Ministry of Agriculture & Farmers Welfare'
  }
];

const STATE_SCHEMES = {
  Maharashtra: [
    { name: 'Marathwada Intensified Mission for Accelerated Development Yojana', category: 'Irrigation' },
    { name: 'Pradhan Mantri Ojasvi Gram Yatra Yojana (Maharashtra)', category: 'Subsidy' },
    { name: 'Sugarcane Subsidy Scheme', category: 'Subsidy' },
    { name: 'Cotton Seed Subsidy', category: 'Seeds' },
  ],
  Karnataka: [
    { name: 'Karnataka Nursery Road Scheme', category: 'Subsidy' },
    { name: 'Krishna Bhagya Channeling Abhiyaan', category: 'Irrigation' },
    { name: 'Coffee Subsidy Scheme', category: 'Subsidy' },
    { name: 'Plantation Assistance Scheme', category: 'Subsidy' },
  ],
  Gujarat: [
    { name: 'Kanya Kelavni Pathak Scheme', category: 'Loan' },
    { name: 'Gujarat Flood Relief Scheme', category: 'Insurance' },
    { name: 'Cotton and Groundnut Subsidy', category: 'Subsidy' },
    { name: 'Dairy Development Loan Scheme', category: 'Loan' },
  ],
  Punjab: [
    { name: 'Paddy Procurement Support Scheme', category: 'Subsidy' },
    { name: 'Agricultural Infrastructure Fund', category: 'Loan' },
    { name: 'Crop Diversification Subsidy', category: 'Subsidy' },
    { name: 'Dairy Subsidy Scheme', category: 'Subsidy' },
  ],
  Haryana: [
    { name: 'Haryana Solar Energy Pump Scheme', category: 'Subsidy' },
    { name: 'Haryana Crop Insurance Scheme', category: 'Insurance' },
    { name: 'Maize Cultivation Support', category: 'Subsidy' },
    { name: 'Vegetable Cultivation Assistance', category: 'Subsidy' },
  ],
  'Tamil Nadu': [
    { name: 'Rainfed Area Development Scheme', category: 'Irrigation' },
    { name: 'Tamil Nadu Agricultural Insurance Scheme', category: 'Insurance' },
    { name: 'Coconut Cultivation Subsidy', category: 'Subsidy' },
    { name: 'Sugarcane Farmer Assistance', category: 'Loan' },
  ],
  'Uttar Pradesh': [
    { name: 'UP Bijli Harvesters Scheme', category: 'Machinery' },
    { name: 'Har Khet Ko Pani Scheme', category: 'Irrigation' },
    { name: 'Cooperative Farming Scheme', category: 'Loan' },
    { name: 'Wheat Support Scheme', category: 'Subsidy' },
  ],
  Bihar: [
    { name: 'Bihar Agricultural Infrastructure Fund', category: 'Loan' },
    { name: 'Integrated Crop Management Scheme', category: 'Subsidy' },
    { name: 'Bihar Krishi Input Subsidy', category: 'Subsidy' },
    { name: 'Vegetable Seeds Subsidy', category: 'Seeds' },
  ],
  'Madhya Pradesh': [
    { name: 'Mukhya Mantri Soya Subsidy Scheme', category: 'Subsidy' },
    { name: 'MP Microshed Scheme', category: 'Irrigation' },
    { name: 'Cotton Procurement Scheme', category: 'Subsidy' },
    { name: 'Farming Equipment Loan', category: 'Loan' },
  ],
  'Andhra Pradesh': [
    { name: 'Rythu Bandhu Scheme', category: 'Subsidy' },
    { name: 'Riddhigalor Padi Procurement', category: 'Subsidy' },
    { name: 'Mango Orchards Subsidy', category: 'Subsidy' },
    { name: 'Aquaculture Support Scheme', category: 'Loan' },
  ],
  Telangana: [
    { name: 'Telangana Rajathu Barosa Yojana', category: 'Subsidy' },
    { name: 'Rythu Bandhu (Telangana)', category: 'Subsidy' },
    { name: 'Seed Replacement Scheme', category: 'Seeds' },
    { name: 'Agricultural Loan Assistance', category: 'Loan' },
  ],
  'West Bengal': [
    { name: 'Kanyashree Prakalpa (Women Farmer Scheme)', category: 'Subsidy' },
    { name: 'Tea Garden Development Scheme', category: 'Subsidy' },
    { name: 'Rice Subsidy Program', category: 'Subsidy' },
    { name: 'Organic Farming Alternative', category: 'Subsidy' },
  ],
  Rajasthan: [
    { name: 'Rajasthan Bhamashah Kharid Mela', category: 'Subsidy' },
    { name: 'Ground Water Subsidy Scheme', category: 'Irrigation' },
    { name: 'Maize and Bajra Support', category: 'Subsidy' },
    { name: 'Livestock Sheep Rearing Loan', category: 'Loan' },
  ],
  Odisha: [
    { name: 'Odisha Krishi Teertha Scheme', category: 'Irrigation' },
    { name: 'ORMAS Scheme', category: 'Subsidy' },
    { name: 'Rice Farmer Assistance', category: 'Subsidy' },
    { name: 'Vegetable Cultivation Support', category: 'Subsidy' },
  ],
  Jharkhand: [
    { name: 'Jharkhand Agricultural Input Subsidy', category: 'Subsidy' },
    { name: 'Millet Cultivation Bonus', category: 'Subsidy' },
    { name: 'Farm Irrigation Scheme', category: 'Irrigation' },
    { name: 'Agricultural Loan Assistance', category: 'Loan' },
  ],
  Chhattisgarh: [
    { name: 'Chhattisgarh Paddy Procurement Scheme', category: 'Subsidy' },
    { name: 'Milk Production Encouragement Scheme', category: 'Loan' },
    { name: 'Rice Farmer Support', category: 'Subsidy' },
    { name: 'Horticulture Development Scheme', category: 'Subsidy' },
  ],
  Kerala: [
    { name: 'Kerala Spice Garden Scheme', category: 'Subsidy' },
    { name: 'Rubber Board Subsidy', category: 'Subsidy' },
    { name: 'Coconut Board Assistance', category: 'Subsidy' },
    { name: 'Integrated Pest Management Program', category: 'Subsidy' },
  ]
};

// Generate unique ID
function generateId(prefix, index) {
  return `${prefix}-${Date.now()}-${index}`;
}

// Generate schemes
function generateSchemes() {
  const schemes = [];
  let index = 0;

  // Generate Central Schemes (40%)
  CENTRAL_SCHEMES.forEach((scheme) => {
    // Get official URL from mapping, fallback to ministry portal
    const officialUrl = CENTRAL_SCHEME_URLS[scheme.name] || 'https://agriculture.gov.in/';
    
    schemes.push({
      id: generateId('CENTRAL', index),
      schemeName: scheme.name,
      description: scheme.description,
      type: 'Central',
      state: 'All',
      category: scheme.category,
      benefitAmount: scheme.benefitAmount,
      eligibility: scheme.eligibility,
      applicationMode: Math.random() > 0.5 ? 'Online' : 'Offline',
      officialDepartment: scheme.officialDepartment,
      officialUrl: officialUrl,
      lastUpdated: new Date().toISOString().split('T')[0]
    });
    index++;
  });

  // Generate State Schemes (60%)
  MAJOR_STATES.forEach((state) => {
    const stateSchemes = STATE_SCHEMES[state] || [];
    const statePortalUrl = STATE_PORTAL_URLS[state] || 'https://agriculture.gov.in/';
    
    // Base state-specific schemes
    stateSchemes.forEach((scheme, stateIndex) => {
      const benefitAmounts = [15000, 25000, 35000, 50000, 75000, 100000];
      schemes.push({
        id: generateId(`STATE-${state}`, index),
        schemeName: scheme.name,
        description: `State-level ${scheme.category.toLowerCase()} scheme for agricultural development in ${state}`,
        type: 'State',
        state: state,
        category: scheme.category,
        benefitAmount: benefitAmounts[Math.floor(Math.random() * benefitAmounts.length)],
        eligibility: `Registered farmers in ${state} with minimum 0.5 hectares of land`,
        applicationMode: Math.random() > 0.4 ? 'Online' : 'Offline',
        officialDepartment: `${state} Department of Agriculture`,
        officialUrl: statePortalUrl,
        lastUpdated: new Date().toISOString().split('T')[0]
      });
      index++;
    });

    // Add additional random state schemes for variety
    for (let i = 0; i < 3; i++) {
      const randomCategory = CATEGORIES[Math.floor(Math.random() * CATEGORIES.length)];
      const benefitAmounts = [10000, 20000, 30000, 45000, 60000, 80000];
      const schemeTypes = ['Support', 'Assistance', 'Subsidy', 'Development', 'Promotion', 'Aid'];
      const schemeType = schemeTypes[Math.floor(Math.random() * schemeTypes.length)];

      schemes.push({
        id: generateId(`STATE-${state}`, index),
        schemeName: `${state} ${schemeType} Scheme for ${randomCategory}`,
        description: `Specialized ${randomCategory.toLowerCase()} support program for farmers in ${state}`,
        type: 'State',
        state: state,
        category: randomCategory,
        benefitAmount: benefitAmounts[Math.floor(Math.random() * benefitAmounts.length)],
        eligibility: `Eligible farmers in ${state} meeting land and income criteria`,
        applicationMode: Math.random() > 0.4 ? 'Online' : 'Offline',
        officialDepartment: `${state} Department of Agriculture`,
        officialUrl: statePortalUrl,
        lastUpdated: new Date().toISOString().split('T')[0]
      });
      index++;
    }
  });

  return schemes;
}

// Main execution
function main() {
  try {
    const schemes = generateSchemes();
    const dataDir = path.join(__dirname, '../data');
    const filePath = path.join(dataDir, 'governmentSchemes.json');

    // Ensure data directory exists
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true });
    }

    // Write to file
    fs.writeFileSync(
      filePath,
      JSON.stringify({ schemes, generatedAt: new Date().toISOString() }, null, 2)
    );

    console.log(`✓ Generated ${schemes.length} government schemes`);
    console.log(`✓ Saved to: ${filePath}`);
    console.log(`✓ File size: ${(fs.statSync(filePath).size / 1024).toFixed(2)} KB`);
  } catch (error) {
    console.error('Error generating schemes:', error);
    process.exit(1);
  }
}

main();
