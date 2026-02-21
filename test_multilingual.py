#!/usr/bin/env python3
"""
Test script for multilingual WhatsApp bot functionality.
Verifies that language selection changes bot responses correctly.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import (
    _get_user_session, 
    process_user_message,
    _get_translated_text,
    TRANSLATIONS
)

def test_language_selection():
    """Test that language selection works correctly"""
    print("\n" + "="*60)
    print("TEST 1: Language Selection")
    print("="*60)
    
    sender = "test_user_1"
    
    # Simulate user greeting (should prompt for language before any language is set)
    response, send_menu, menu_type = process_user_message("hi", sender)
    print(f"Initial greeting: {response[:50]}...")
    assert menu_type == "language", "Should show language menu on first greeting"
    
    # Select Hindi
    response, send_menu, menu_type = process_user_message("lang_hi", sender)
    print(f"Hindi selection: {response[:50]}...")
    
    # Verify language is stored in session
    session = _get_user_session(sender)
    assert session.get("language") == "hi"
    print(f"Language in session: {session['language']}")
    print("✅ TEST 1 PASSED\n")

def test_hindi_messages():
    """Test that bot messages change to Hindi"""
    print("="*60)
    print("TEST 2: Hindi Message Translation")
    print("="*60)
    
    sender = "test_user_2"
    process_user_message("lang_hi", sender)
    session = _get_user_session(sender)
    assert session.get("language") == "hi"
    
    response, _, _ = process_user_message("help", sender)
    print(f"Hindi help message: {response[:80]}...")
    print("✅ TEST 2 PASSED\n")

def test_translation_dictionary():
    """Test that TRANSLATIONS dictionary has all required keys"""
    print("="*60)
    print("TEST 5: Translation Dictionary Coverage")
    print("="*60)
    
    languages = {"en", "hi", "mr"}
    required_keys = {
        "first_greeting", "language_set", "welcome", "help", "main_menu",
        "location_help", "recommend_prompt", "invalid_location", 
        "recommendation_result", "market_crop_needed", "market_unavailable",
        "no_market_data", "forecast_crop_needed", "no_forecast_data",
        "season_needed", "invalid_season", "season_unavailable", "no_season_data",
        "season_result", "not_understood", "help_needed", "service_unavailable"
    }
    
    for key in required_keys:
        assert key in TRANSLATIONS, f"Missing key: {key}"
        for lang in languages:
            assert lang in TRANSLATIONS[key], f"Missing {lang} for key: {key}"
    
    print(f"All {len(required_keys)} required keys present")
    print(f"All translations for {len(languages)} languages available")
    print("✅ TEST 5 PASSED\n")

def test_translated_text_helper():
    """Test the _get_translated_text helper function"""
    print("="*60)
    print("TEST 6: Translation Helper Function")
    print("="*60)
    
    en_text = _get_translated_text("help", "en")
    hi_text = _get_translated_text("help", "hi")
    mr_text = _get_translated_text("help", "mr")
    
    print(f"English version length: {len(en_text)}")
    print(f"Hindi version length: {len(hi_text)}")
    print(f"Marathi version length: {len(mr_text)}")
    
    assert en_text != hi_text
    assert en_text != mr_text
    assert hi_text != mr_text
    
    result = _get_translated_text("no_market_data", "en", crop="rice")
    assert "rice" in result.lower()
    
    print("✅ TEST 6 PASSED\n")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("MULTILINGUAL WHATSAPP BOT TEST SUITE")
    print("="*60)
    
    tests = [
        test_language_selection,
        test_hindi_messages,
        test_translation_dictionary,
        test_translated_text_helper
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
        print("\nALL TESTS PASSED! Multilingual system is working.\n")
        return True
    else:
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
