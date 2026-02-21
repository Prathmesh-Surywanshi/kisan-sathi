import json
from app import whatsapp_webhook, app
import logging

logging.basicConfig(level=logging.DEBUG)

# Simulate a test message through the Flask app context
with app.test_request_context(
    '/webhook', 
    method='POST',
    json={
        'entry': [{
            'changes': [{
                'value': {
                    'messages': [{
                        'from': '1234567890',
                        'text': {'body': 'hi'}
                    }]
                }
            }]
        }]
    }
):
    print("Testing webhook with 'hi' message...")
    try:
        response = whatsapp_webhook()
        print(f'Response: {response}')
        print("✓ Webhook processed successfully!")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
