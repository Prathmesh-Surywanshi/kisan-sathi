# Government Schemes - Official Portal Redirect Feature

## Overview

This feature enables users to redirect from scheme cards to official government portals. Each scheme card displays the official portal link and opens it securely in a new tab.

## Architecture

### 1. **Data Layer** (`data/governmentSchemes.json`)

Each scheme object now includes an `officialUrl` field:

```json
{
  "id": "CENTRAL-1771716517499-0",
  "schemeName": "PM-KISAN: Pradhan Mantri Kisan Samman Nidhi",
  "description": "Direct income support scheme...",
  "type": "Central",
  "state": "All",
  "category": "Subsidy",
  "benefitAmount": 6000,
  "eligibility": "Small and marginal farmers...",
  "applicationMode": "Online",
  "officialDepartment": "Ministry of Agriculture & Farmers Welfare",
  "officialUrl": "https://pmkisan.gov.in/",
  "lastUpdated": "2026-02-21"
}
```

### 2. **Dataset Generator** (`scripts/generateSchemes.js`)

The generator automatically maps scheme names to official portals:

**Central Schemes Mapping:**
- PM-KISAN → `https://pmkisan.gov.in/`
- Pradhan Mantri Fasal Bima Yojana → `https://pmfby.gov.in/`
- Soil Health Card Scheme → `https://soilhealth.dac.gov.in/`
- E-NAM → `https://www.enam.gov.in/`
- Pradhan Mantri Krishi Sinchayee Yojana → `https://pmksy.gov.in/`

**State Schemes Mapping:**
Each state gets its official agriculture department portal:
- Maharashtra → `https://krishi.maharashtra.gov.in/`
- Karnataka → `https://raitamitra.karnataka.gov.in/`
- Gujarat → `https://ikhedut.gujarat.gov.in/`
- etc.

### 3. **Component Architecture**

#### SchemeCard Component (`frontend/src/components/SchemeCard.jsx`)

**Responsibilities:**
- Renders individual scheme card
- Handles secure URL validation and redirection
- Displays domain badge
- Manages fallback UI for missing URLs

**Key Functions:**

```javascript
// Secure redirect with validation
const handleRedirect = (url, schemeName) => {
  // Validates URL protocol
  // Opens in new tab with: noopener,noreferrer
  // Logs action for debugging
};

// Extract domain for display
const getDomainFromUrl = (url) => {
  // Extracts hostname from URL
  // Removes www prefix
  // Returns domain name for badge display
};
```

**Security Features:**
- ✅ URL validation (must start with http/https)
- ✅ `window.open(_blank, 'noopener,noreferrer')` - prevents cross-tab access
- ✅ Error handling with user-friendly messages
- ✅ Console logging for debugging

#### SchemeSection Component (`frontend/src/components/SchemeSection.jsx`)

**Responsibilities:**
- Manages filtering, search, sorting, pagination
- Passes scheme data to SchemeCard
- Handles recommended schemes logic

### 4. **Styling**

#### SchemeCard Styles (`frontend/src/styles/SchemeCard.css`)

**Portal Domain Badge:**
```css
.portal-domain {
  font-size: 0.85em;
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  padding: 6px 10px;
  border-radius: 4px;
  display: flex;
  gap: 6px;
}
```

**Learn More Button:**
```css
.learn-more-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.learn-more-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.3);
}

.learn-more-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  opacity: 0.7;
}
```

## User Flow

```
1. User browses Government Schemes page
                ↓
2. User sees scheme cards with:
   - Scheme details
   - Benefit amount
   - Eligibility criteria
   - Portal domain badge (e.g., "🌐 pmkisan.gov.in")
                ↓
3. User clicks "Learn More →" button
                ↓
4. Component validates officialUrl
                ↓
5. Opens https://pmkisan.gov.in/ in new tab
   (with noopener,noreferrer for security)
                ↓
6. User views official government portal
```

## Fallback Behavior

If `officialUrl` is missing:

```jsx
<button 
  className="learn-more-btn"
  disabled={!scheme.officialUrl}
>
  No Link Available
</button>
<p className="no-link-message">
  Contact your local agriculture department for details
</p>
```

## Data Flow

```
generateSchemes.js (Node)
         ↓
    (generates)
         ↓
data/governmentSchemes.json
         ↓
    (copy to)
         ↓
frontend/public/governmentSchemes.json
         ↓
    (fetch via)
         ↓
schemeDataLoader.js
         ↓
    (loads into)
         ↓
SchemeSection.jsx
         ↓
    (passes to)
         ↓
SchemeCard.jsx
         ↓
    (renders with redirect)
         ↓
window.open(officialUrl, '_blank', 'noopener,noreferrer')
```

## Security Measures

### 1. **URL Validation**
- Must start with `http://` or `https://`
- Invalid URLs show error message

### 2. **Window Opening Security**
```javascript
window.open(url, '_blank', 'noopener,noreferrer');
```
- `_blank`: Opens in new tab
- `noopener`: New window can't access `window.opener`
- `noreferrer`: Referrer header not sent

### 3. **Error Handling**
- Try-catch wrapper for URL parsing
- User-friendly fallback messages
- Console logging for debugging

### 4. **Content Validation**
- Data comes from generated JSON (trusted source)
- URL mapping hardcoded in generator (not user input)

## File Structure

```
kisan-sathi-main/
├── scripts/
│   └── generateSchemes.js          # Generator with URL mappings
├── data/
│   └── governmentSchemes.json      # Generated data file
├── frontend/
│   ├── public/
│   │   └── governmentSchemes.json  # Copy for frontend fetch
│   └── src/
│       ├── components/
│       │   ├── SchemeCard.jsx      # Individual card component
│       │   └── SchemeSection.jsx   # Container component
│       └── styles/
│           ├── SchemeCard.css      # Card styling
│           └── SchemeSection.css   # Section styling
```

## Implementation Checklist

- [x] Update dataset structure with `officialUrl` field
- [x] Create central scheme URLs mapping
- [x] Create state scheme URLs mapping
- [x] Update generator script
- [x] Regenerate dataset with officialUrl
- [x] Create SchemeCard component
- [x] Add redirect handler with validation
- [x] Add domain badge display
- [x] Implement security measures
- [x] Add CSS styling
- [x] Update SchemeSection to use SchemeCard
- [x] Handle fallback cases

## Testing the Feature

### Manual Testing

1. **Navigate to Government Schemes Page**
```bash
http://localhost:3000/government-schemes
```

2. **Verify Portal Badges Display**
   - Each card should show domain badge (e.g., "🌐 pmkisan.gov.in")

3. **Click "Learn More" Button**
   - Should open official portal in new tab
   - No errors in browser console

4. **Test Fallback (if any schemes missing URL)**
   - Button should show "No Link Available"
   - Message should appear: "Contact your local agriculture department for details"

5. **Verify Security**
   - Open DevTools → Network
   - Click "Learn More"
   - New tab should open without errors
   - No CORS issues should appear

### Browser Console Testing

```javascript
// Test URL validation
const testUrl = "https://pmkisan.gov.in/";
console.log(testUrl.startsWith('https://')); // true

// Test domain extraction
new URL(testUrl).hostname.replace('www.', ''); // "pmkisan.gov.in"
```

## Future Enhancements

1. **Analytics Tracking**
   - Track clicks to official portals
   - Measure engagement by scheme type

2. **Scheme-Specific Resources**
   - Add downloadable eligibility forms
   - Add FAQ links
   - Add helpline numbers

3. **URL Verification**
   - Regular health checks on URLs
   - Fallback to backup URLs

4. **Localization**
   - Translate portal links by language
   - Region-specific portal URLs

5. **Deep Linking**
   - Direct links to application forms
   - Pre-populated application redirects

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Button shows "No Link Available" | URL is missing from dataset. Regenerate with `node scripts/generateSchemes.js` |
| Link opens but shows 404 | Official portal URL is outdated. Update mapping in `generateSchemes.js` |
| Error: "Cannot read property of undefined" | Check if `officiialUrl` field exists in JSON |
| Browser blocks popup | Configure popup settings or use Firefox for testing |

## References

- [MDN: Window.open()](https://developer.mozilla.org/en-US/docs/Web/API/Window/open)
- [OWASP: Opening External Links Securely](https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html)
- [Government of India Agriculture Portal](https://agriculture.gov.in/)
