#!/usr/bin/env python3
"""
Test location translation functionality.
Demonstrates that Hindi/Marathi location names are correctly translated to English.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import (
    _translate_location_to_english,
    STATE_TRANSLATION_MAP,
    DISTRICT_TRANSLATION_MAP
)

def test_state_translations():
    """Test that all state translations work"""
    print("\n" + "="*70)
    print("STATE TRANSLATION TEST")
    print("="*70)
    
    test_cases = [
        ("महाराष्ट्र", "maharashtra"),
        ("आंध्र प्रदेश", "andhra pradesh"),
        ("तमिलनाडु", "tamil nadu"),
        ("पंजाब", "punjab"),
        ("गुजरात", "gujarat"),
        ("राजस्थान", "rajasthan"),
        ("हरियाणा", "haryana"),
        ("मध्य प्रदेश", "madhya pradesh"),
        ("कर्नाटक", "karnataka"),
    ]
    
    passed = 0
    for hindi, expected in test_cases:
        result, _ = _translate_location_to_english(hindi, "")
        result_norm = result.lower().strip()
        expected_norm = expected.lower().strip()
        
        if result_norm == expected_norm:
            print(f"✓ {hindi:20} → {result:20} (expected: {expected})")
            passed += 1
        else:
            print(f"✗ {hindi:20} → {result:20} (expected: {expected})")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

def test_district_translations():
    """Test that all district translations work"""
    print("\n" + "="*70)
    print("DISTRICT TRANSLATION TEST")
    print("="*70)
    
    test_cases = [
        ("पुणे", "pune"),
        ("मुंबई", "mumbai"),
        ("नागपूर", "nagpur"),
        ("अहमदनगर", "ahmadnagar"),
        ("औरंगाबाद", "aurangabad"),
        ("ठाणे", "thane"),
        ("गुंटूर", "guntur"),
        ("चेन्नई", "chennai"),
        ("अमृतसर", "amritsar"),
        ("जयपुर", "jaipur"),
        ("अहमदाबाद", "ahmedabad"),
    ]
    
    passed = 0
    for hindi, expected in test_cases:
        _, result = _translate_location_to_english("", hindi)
        result_norm = result.lower().strip()
        expected_norm = expected.lower().strip()
        
        if result_norm == expected_norm:
            print(f"✓ {hindi:20} → {result:20} (expected: {expected})")
            passed += 1
        else:
            print(f"✗ {hindi:20} → {result:20} (expected: {expected})")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

def test_combined_location():
    """Test combined state and district translation"""
    print("\n" + "="*70)
    print("COMBINED LOCATION TEST (State | District)")
    print("="*70)
    
    test_cases = [
        ("महाराष्ट्र", "पुणे", "maharashtra", "pune"),
        ("आंध्र प्रदेश", "गुंटूर", "andhra pradesh", "guntur"),
        ("तमिलनाडु", "चेन्नई", "tamil nadu", "chennai"),
        ("पंजाब", "अमृतसर", "punjab", "amritsar"),
        ("राजस्थान", "जयपुर", "rajasthan", "jaipur"),
    ]
    
    passed = 0
    for h_state, h_dist, exp_state, exp_dist in test_cases:
        eng_state, eng_dist = _translate_location_to_english(h_state, h_dist)
        
        eng_state_norm = eng_state.lower().strip()
        eng_dist_norm = eng_dist.lower().strip()
        exp_state_norm = exp_state.lower().strip()
        exp_dist_norm = exp_dist.lower().strip()
        
        if eng_state_norm == exp_state_norm and eng_dist_norm == exp_dist_norm:
            print(f"✓ {h_state:20} | {h_dist:20}")
            print(f"  → {eng_state:20} | {eng_dist:20}")
            passed += 1
        else:
            print(f"✗ {h_state:20} | {h_dist:20}")
            print(f"  → {eng_state:20} | {eng_dist:20}")
            print(f"  Expected: {exp_state:20} | {exp_dist:20}")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

def test_map_coverage():
    """Verify translation map coverage"""
    print("\n" + "="*70)
    print("TRANSLATION MAP COVERAGE")
    print("="*70)
    
    print(f"\nStates in translation map: {len(STATE_TRANSLATION_MAP)}")
    print(f"Districts in translation map: {len(DISTRICT_TRANSLATION_MAP)}")
    
    # Count unique English values
    unique_states = set(STATE_TRANSLATION_MAP.values())
    unique_districts = set(DISTRICT_TRANSLATION_MAP.values())
    
    print(f"Unique English states: {len(unique_states)}")
    print(f"Unique English districts: {len(unique_districts)}")
    
    # Show sample coverage
    print("\nSample states covered:")
    states_sample = sorted(list(unique_states))[:10]
    for state in states_sample:
        print(f"  • {state}")
    
    print("\nSample districts covered:")
    districts_sample = sorted(list(unique_districts))[:10]
    for district in districts_sample:
        print(f"  • {district}")
    
    return True

def main():
    print("\n" + "="*70)
    print("🌍 LOCATION TRANSLATION SYSTEM TEST")
    print("="*70)
    print("\nThis test verifies that Hindi and Marathi location names")
    print("are correctly translated to English for database queries.\n")
    
    results = []
    results.append(("States", test_state_translations()))
    results.append(("Districts", test_district_translations()))
    results.append(("Combined", test_combined_location()))
    results.append(("Coverage", test_map_coverage()))
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name:20} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("="*70)
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nLocation names in Hindi/Marathi are now correctly translated")
        print("to English before database queries. Users can provide locations")
        print("in any language and get correct recommendations!\n")
    else:
        print("\n⚠️ Some tests failed. Review the output above.\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
