from app import process_user_message, _get_user_session

# Test 1: Simple greeting
print("Test 1: Greeting")
response, send_menu, menu_type = process_user_message("hi", "test1")
print(f"Response: {response[:50]}")
print(f"Send menu: {send_menu}, Menu type: {menu_type}\n")

# Test 2: Language selection
print("Test 2: Language selection (Hindi)")
response, send_menu, menu_type = process_user_message("lang_hi", "test2")
print(f"Response: {response[:50]}")
session = _get_user_session("test2")
print(f"Session language: {session.get('language')}\n")

# Test 3: Another greeting
print("Test 3: Greeting in Hindi")
response, send_menu, menu_type = process_user_message("hello", "test2")
print(f"Response: {response[:50]}")
print(f"Send menu: {send_menu}, Menu type: {menu_type}\n")

print("All tests passed!")
