# Government Schemes Feature - Implementation Guide

## Overview

The Government Schemes Section is a production-ready, fully offline feature that displays Central and State government agricultural schemes with advanced filtering, search, and recommendations.

**Status:** ✅ Ready for Hackathon Demo

---

## 📊 Dataset Statistics

- **Total Schemes Generated:** 129
- **Central Schemes:** ~40% (51 schemes)
- **State Schemes:** ~60% (78 schemes)
- **States Covered:** 17 major Indian states
- **Categories:** Subsidy, Loan, Insurance, Machinery, Irrigation, Seeds, Crop Insurance, Fertilizer

**File Sizes:**
- Dataset: `68.23 KB` (efficiently compressed)
- No API dependency - completely offline

---

## 🏗️ Architecture

### Directory Structure

```
kisan-sathi-main/
├── data/
│   └── governmentSchemes.json (129 schemes, 68 KB)
├── scripts/
│   └── generateSchemes.js (Generator tool)
├── utils/
│   └── schemeFilter.js (Filter engine)
├── frontend/
│   ├── public/
│   │   └── governmentSchemes.json (copy for frontend)
│   ├── src/
│   │   ├── components/
│   │   │   └── SchemeSection.jsx
│   │   ├── pages/
│   │   │   └── GovernmentSchemesPage.jsx
│   │   ├── styles/
│   │   │   └── SchemeSection.css
│   │   ├── utils/
│   │   │   ├── schemeFilter.js (for frontend)
│   │   │   └── schemeDataLoader.js
│   │   └── App.jsx (updated with route)
```

---

## 🔧 Core Components

### 1. **Data Generator** (`scripts/generateSchemes.js`)

**Purpose:** Programmatically generates 100+ realistic scheme data

**Features:**
- Central schemes (PM-KISAN, PMFBY, etc.)
- State-specific schemes (17 states)
- Realistic benefit amounts (₹10,000 - ₹100,000)
- Automatic metadata (departments, eligibility, application mode)

**Usage:**
```bash
node scripts/generateSchemes.js
```

**Output:** `/data/governmentSchemes.json` with 129 schemes

**No manual editing required** - scheme data is auto-generated!

---

### 2. **Filter Engine** (`utils/schemeFilter.js`)

**Core Functions:**

#### `filterSchemes(options)`
Filters schemes by state, category, and search term

```javascript
const filtered = filterSchemes({
  schemes: allSchemes,
  selectedState: 'Maharashtra',
  selectedCategory: 'Subsidy',
  searchTerm: 'irrigation'
});
```

**Rules:**
- Central schemes appear for **all states**
- State schemes appear **only for their state**
- Search is **case-insensitive** (name, description, department)
- No mutation of original dataset

#### `getRecommendedSchemes(options)`
Recommends top 5 schemes based on farmer profile

```javascript
const recommended = getRecommendedSchemes({
  schemes: allSchemes,
  selectedCrop: 'wheat',
  selectedState: 'Maharashtra',
  isDroughtProne: true
});
```

**Priority Logic:**
1. Insurance schemes (+50 points)
2. Machinery subsidy (+40 points)
3. Irrigation for drought-prone areas (+45 points)
4. Seed & fertilizer (+30 points)
5. General subsidy (+25 points)
6. Central schemes boost (+10 points)

#### `getAllStates(schemes)`
Returns sorted list of unique states

#### `getAllCategories(schemes)`
Returns sorted list of scheme categories

#### `getSchemeStats(schemes)`
Returns statistics:
- Total schemes
- Central vs State split
- Category distribution
- Average benefit amount

#### `createMemoizedFilter(schemes)`
React-optimized memoized filter with LRU cache (max 50 entries)

---

### 3. **Frontend Component** (`components/SchemeSection.jsx`)

**Key Features:**

✨ **Filtering & Search**
- State dropdown (auto-populated)
- Category dropdown (auto-populated)
- Real-time search bar (name + description + department)
- Clear filters button

📊 **Display & Stats**
- Scheme cards with rich information
- Statistics bar (total, central, state, avg benefit)
- Recommended schemes banner
- Pagination (10 items per page)

🎨 **Card Content**
- Scheme name with type badge (Central/State)
- Category badge
- Benefit amount (₹)
- Application mode (Online/Offline)
- Eligibility summary
- Department information
- Last updated date
- "Learn More" button

⚡ **Performance**
- `useMemo` for filters (no unnecessary re-renders)
- `useMemo` for pagination calculations
- Pagination resets on filter change
- Efficient sorting (name, benefit, date)

📱 **Responsive Design**
- Mobile-first CSS Grid
- Works on tablets and desktops
- Touch-friendly buttons
- Readable on all screen sizes

---

### 4. **Data Loader** (`utils/schemeDataLoader.js`)

**Smart Loading Strategy:**
1. Tries `/governmentSchemes.json` (public root)
2. Falls back to `/data/governmentSchemes.json`
3. Caches results for performance
4. Provides helper functions

```javascript
import { loadSchemesData } from '../utils/schemeDataLoader';

const schemes = await loadSchemesData();
```

**Additional Functions:**
- `getSchemeById(schemeId)` - Get single scheme
- `searchSchemes(criteria)` - Search by name/state/category
- `clearSchemesCache()` - Force fresh load

---

## 🚀 How to Run

### 1. **Generate/Regenerate Schemes Data**

```bash
cd kisan-sathi-main
node scripts/generateSchemes.js
```

This creates:
- `/data/governmentSchemes.json` (129 schemes)
- Auto-copies to frontend via build process

### 2. **Start Frontend**

```bash
cd frontend
npm install
npm start
```

The app loads at `http://localhost:3000`

### 3. **Access Government Schemes**

Navigate to:
```
http://localhost:3000/government-schemes
```

---

## 💡 Usage Examples

### Basic Filtering

```jsx
import SchemeSection from './components/SchemeSection';
import { loadSchemesData } from './utils/schemeDataLoader';

export default function Page() {
  const [schemes, setSchemes] = useState([]);
  
  useEffect(() => {
    loadSchemesData().then(setSchemes);
  }, []);
  
  return <SchemeSection allSchemes={schemes} />;
}
```

### With Farmer Profile (Recommendations)

```jsx
const farmerProfile = {
  state: 'Maharashtra',
  crop: 'wheat',
  isDroughtProne: true
};

<SchemeSection allSchemes={schemes} farmerProfile={farmerProfile} />
```

### Direct Filter Usage

```javascript
import { filterSchemes, getRecommendedSchemes } from '../utils/schemeFilter';

// Filter by state and category
const filtered = filterSchemes({
  schemes,
  selectedState: 'Punjab',
  selectedCategory: 'Insurance'
});

// Get recommendations
const recommended = getRecommendedSchemes({
  schemes,
  selectedState: 'Punjab',
  isDroughtProne: false
});
```

---

## 🎨 UI Features

### Search Bar
- Real-time filtering
- Searches scheme name, description, and department
- Case-insensitive

### Dropdowns
- Auto-populated from data
- No hardcoded values
- Sortable options

### Scheme Cards
- Clean, modern design
- Gradient backgrounds
- Hover animations
- Click-to-action buttons

### Stats Bar
- Shows total schemes available
- Displays central vs state split
- Shows average benefit amount
- Updates in real-time with filters

### Pagination
- 10 schemes per page
- Previous/Next buttons
- Page indicator
- Resets when filters change

### Empty State
- Friendly message
- Reset button
- Encouraging icon

---

## ⚡ Performance Optimizations

1. **Memoization** - `useMemo` prevents unnecessary re-renders
2. **Caching** - Data loader caches schemes after first load
3. **Lazy Pagination** - Only renders visible items
4. **Filter Cache** - LRU cache for filter combinations
5. **Efficient Sorting** - Single-pass sort algorithms
6. **Responsive Images** - CSS-based layouts (no image downloads)

**Result:** Handles 100+ schemes with near-instant filtering

---

## 🔄 Update Mechanism

To update scheme data:

```bash
# Simply run the generator again
node scripts/generateSchemes.js
```

This:
- ✅ Generates new scheme data with fresh IDs
- ✅ Updates `lastUpdated` timestamps
- ✅ Maintains data consistency
- ✅ No manual editing required
- ✅ Auto-copies to frontend

---

## 📋 Scheme Data Structure

Each scheme object contains:

```javascript
{
  id: "CENTRAL-1702345678-0",
  schemeName: "PM-KISAN: Pradhan Mantri Kisan Samman Nidhi",
  description: "Direct income support scheme...",
  type: "Central" | "State",
  state: "All" | "Maharashtra" | "Punjab" | etc...
  category: "Subsidy" | "Loan" | "Insurance" | "Machinery" | "Irrigation" | "Seeds" | "Crop Insurance" | "Fertilizer",
  benefitAmount: 6000,
  eligibility: "Small and marginal farmers holding up to 2 hectares",
  applicationMode: "Online" | "Offline",
  officialDepartment: "Ministry of Agriculture & Farmers Welfare",
  lastUpdated: "2025-02-22"
}
```

---

## 🗺️ Filter Logic

### State Filtering

```
If selectedState is empty:
  → Show ALL schemes

If selectedState is "All":
  → Show only central schemes

If selectedState is "Maharashtra":
  → Show central schemes
  → Show Maharashtra state schemes
  → Hide schemes from other states
```

### Category Filtering

```
If selectedCategory is empty:
  → Show all categories

If selectedCategory is "Subsidy":
  → Show only subsidy schemes
  → Applies after state filter
```

### Search Filtering

```
If searchTerm is empty:
  → Show all matching schemes

If searchTerm is "irrigation":
  → Match against:
     - Scheme name (case-insensitive)
     - Description
     - Department
  → Return matching schemes
```

---

## 🎯 Hackathon Demo Points

✅ **Fully Offline** - No API calls, works without internet
✅ **Auto-Generated Data** - 129 realistic schemes, programmatically generated
✅ **Scalable** - Handles hundreds of schemes efficiently
✅ **User-Friendly** - Intuitive filtering and search
✅ **Production-Ready** - Clean code, error handling, responsive design
✅ **Recommended Schemes** - Smart recommendations based on farmer profile
✅ **Statistics** - Real-time analytics on filtered results
✅ **No Manual Work** - Scheme data auto-generated, never manually edited

---

## 🔍 Testing Checklist

- [x] Generator creates 100+ schemes
- [x] Filter engine handles all combinations
- [x] State filtering works correctly
- [x] Category filtering works correctly  
- [x] Search works case-insensitive
- [x] Pagination displays correctly
- [x] Recommended schemes populate
- [x] Mobile responsive
- [x] No console errors
- [x] Data loads from public folder
- [x] Navigation link works
- [x] CSS styles apply correctly

---

## 🚀 Future Enhancements

1. **API Integration** - Replace JSON with backend API
2. **Favorites** - Save favorite schemes to localStorage
3. **Share** - Share scheme details via WhatsApp/Email
4. **Eligibility Checker** - Interactive eligibility wizard
5. **Application Links** - Direct links to apply
6. **Notifications** - Alert for new schemes
7. **Scheme Calendar** - Application deadlines
8. **PDF Export** - Download scheme details

---

## 📞 Support

For issues or questions:
1. Check that `/data/governmentSchemes.json` exists
2. Verify `/frontend/public/governmentSchemes.json` is copied
3. Check browser console for errors
4. Regenerate data: `node scripts/generateSchemes.js`
5. Clear browser cache and reload

---

## ✨ Credits

Built as a production-ready feature for the KISAN SATHI farmer platform.

**Technology Stack:**
- React (Hooks, Context, Memoization)
- Modern CSS (Grid, Flexbox, Animations)
- JavaScript (ES6+)
- Node.js (Generator)

**Ready for deployment and scaling! 🚀**
