
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify, Response
from openai import OpenAI









# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(handlers=[RotatingFileHandler('hello_world.log', maxBytes=10000, backupCount=1)],
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Log a message
logging.info('Hello, World!')


# Configure logging
#handler = RotatingFileHandler('flask_app.log', maxBytes=10000, backupCount=1)
#handler.setLevel(logging.INFO)
#formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#handler.setFormatter(formatter)
#app.logger.addHandler(handler)

# Test log message
app.logger.info("Flask application starting up...")

# Global dictionary to store session contexts
session_contexts = {}

# http://127.0.0.1:5000/hello
@app.route('/hello', methods=['GET'])
def get_stock_data():
    app.logger.info("Received request to /hello")
    return 'hello hello'  # Simple response for testing

# curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d '{"text": "Hello, how are you?"}'
# curl -X POST http://54.185.52.192:5000/chat -H "Content-Type: application/json" -d '{"text": "Hello, how are you?"}'
@app.route('/chat', methods=['POST'])
def chat():
    try:
        app.logger.info("Received request to /chat")

        data = request.json
        user_input = data.get('text')
        user_id = data.get('user_id', 'default_user')

        app.logger.info(f"User Input: {user_input}")
        app.logger.info(f"User ID: {user_id}")

        conversation_history = session_contexts.get(user_id, [])
        app.logger.info(f"Conversation History: {conversation_history}")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")

        client = OpenAI(api_key=api_key)
        app.logger.info("Making request to OpenAI API")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": user_input}]
        )

        app.logger.info("Received response from OpenAI API")
        response_text = response.choices[0].message.content

        app.logger.info(f"Response Text: {response_text}")
        return jsonify({'response': response_text})

    except Exception as e:
        app.logger.error("Error during /chat processing", exc_info=True)
        return Response(str(e), status=500)


#@app.route('/whatsapp-webhook', methods=['POST'])
#def whatsapp_webhook():


# Existing code for your WhatsApp webhook
# ...

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
