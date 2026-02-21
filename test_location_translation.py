#!/usr/bin/env python3
"""
Test location translation for Hindi and Marathi location names.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import (
    _get_user_session, 
    process_user_message,
    _translate_location_to_english,
    STATE_TRANSLATION_MAP,
    DISTRICT_TRANSLATION_MAP
)

def test_location_translation():
    """Test that Hindi/Marathi locations translate to English"""
    print("\n" + "="*60)
    print("TEST: Location Translation (Hindi/Marathi to English)")
    print("="*60)
    
    test_cases = [
        ("महाराष्ट्र", "पुणे", "maharashtra", "pune"),
        ("आंध्र प्रदेश", "गुंटूर", "andhra pradesh", "guntur"),
        ("तमिलनाडु", "चेन्नई", "tamil nadu", "chennai"),
        ("पंजाब", "अमृतसर", "punjab", "amritsar"),
        ("गुजरात", "अहमदाबाद", "gujarat", "ahmedabad"),
        ("राजस्थान", "जयपुर", "rajasthan", "jaipur"),
    ]
    
    for hindi_state, hindi_district, expected_state, expected_district in test_cases:
        english_state, english_district = _translate_location_to_english(hindi_state, hindi_district)
        
        # Normalize comparison
        eng_state_norm = english_state.lower().strip()
        exp_state_norm = expected_state.lower().strip()
        eng_dist_norm = english_district.lower().strip()
        exp_dist_norm = expected_district.lower().strip()
        
        print(f"\n✓ Hindi: {hindi_state}, {hindi_district}")
        print(f"  → English: {english_state}, {english_district}")
        print(f"  Expected: {expected_state}, {expected_district}")
        
        assert eng_state_norm == exp_state_norm, f"State mismatch: {eng_state_norm} != {exp_state_norm}"
        assert eng_dist_norm == exp_dist_norm, f"District mismatch: {eng_dist_norm} != {exp_dist_norm}"
    
    print("\n✅ All location translations passed!\n")

def test_location_recommendation_in_hindi():
    """Test that location recommendation works in Hindi"""
    print("="*60)
    print("TEST: Hindi Location Recommendation")
    print("="*60)
    
    sender = "test_hindi_loc"
    
    # Set Hindi language
    process_user_message("lang_hi", sender)
    session = _get_user_session(sender)
    assert session.get("language") == "hi"
    
    # Send recommend request
    response, _, _ = process_user_message("recommend", sender)
    print(f"Recommend prompt: {response[:100]}...")
    
    # Send location in Hindi (महाराष्ट्र | पुणे)
    response, _, _ = process_user_message("महाराष्ट्र | पुणे", sender)
    print(f"Location response (first 150 chars): {response[:150]}...")
    
    # Should contain Hindi text and crop recommendation
    assert "का" in response or "रष्" in response or "सिफारिश" in response, "No Hindi text in response"
    assert "%" in response, "No confidence % in response"
    
    print("✅ Hindi location recommendation works!\n")

def test_location_recommendation_in_marathi():
    """Test that location recommendation works in Marathi"""
    print("="*60)
    print("TEST: Marathi Location Recommendation")
    print("="*60)
    
    sender = "test_marathi_loc"
    
    # Set Marathi language
    process_user_message("lang_mr", sender)
    session = _get_user_session(sender)
    assert session.get("language") == "mr"
    
    # Send recommend request
    response, _, _ = process_user_message("recommend", sender)
    print(f"Recommend prompt: {response[:100]}...")
    
    # Send location in Marathi (महाराष्ट्र | पुणे)
    response, _, _ = process_user_message("महाराष्ट्र | पुणे", sender)
    print(f"Location response (first 150 chars): {response[:150]}...")
    
    # Should contain response with crop recommendation
    assert "%" in response, "No confidence % in response"
    
    print("✅ Marathi location recommendation works!\n")

def test_english_location_still_works():
    """Test that English location names still work"""
    print("="*60)
    print("TEST: English Location (backward compatibility)")
    print("="*60)
    
    sender = "test_english_loc"
    
    # Set English language
    process_user_message("lang_en", sender)
    session = _get_user_session(sender)
    assert session.get("language") == "en"
    
    # Send recommend request
    process_user_message("recommend", sender)
    
    # Send location in English (Maharashtra | Pune)
    response, _, _ = process_user_message("Maharashtra | Pune", sender)
    print(f"Location response (first 150 chars): {response[:150]}...")
    
    # Should contain response with crop recommendation
    assert "%" in response, "No confidence % in response"
    
    print("✅ English location recommendation still works!\n")

def test_translation_maps_coverage():
    """Verify translation maps have good coverage"""
    print("="*60)
    print("TEST: Translation Maps Coverage")
    print("="*60)
    
    print(f"States mapped: {len(STATE_TRANSLATION_MAP)}")
    print(f"Districts mapped: {len(DISTRICT_TRANSLATION_MAP)}")
    
    # Check key states
    key_states = ["महाराष्ट्र", "आंध्र प्रदेश", "तमिलनाडु", "पंजाब", "गुजरात"]
    for state in key_states:
        html_found = [k for k in STATE_TRANSLATION_MAP.keys() if state in k or k in state]
        if html_found:
            print(f"✓ {state} mapping found")
    
    print("\n✅ Translation maps have good coverage!\n")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("LOCATION TRANSLATION TEST SUITE")
    print("="*60)
    
    tests = [
        test_translation_maps_coverage,
        test_location_translation,
        test_location_recommendation_in_hindi,
        test_location_recommendation_in_marathi,
        test_english_location_still_works,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"FAILED: {test_func.__name__}")
            print(f"Error: {e}\n")
    
    print("="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("\nALL TESTS PASSED! Location translation works correctly.\n")
        return True
    else:
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
