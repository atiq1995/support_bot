from flask import Flask, request, jsonify, render_template
from advanced_chatbot import AdvancedSupportBot
import os
import sys

app = Flask(__name__)

# Create a single bot instance for the whole application
# Use the advanced bot with LLM capabilities
bot = AdvancedSupportBot(name="AI-Enhanced Support", use_llm=True)

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chat interaction"""
    data = request.json
    user_message = data.get('message', '')
    
    # Get response from the bot
    response = bot.get_response(user_message)
    
    # Log the conversation
    bot.log_conversation(user_message, response)
    
    return jsonify({
        'response': response,
        'userName': bot.user_name
    })

@app.route('/api/add-faq', methods=['POST'])
def add_faq():
    """API endpoint to add new FAQ responses"""
    data = request.json
    keyword = data.get('keyword', '').lower()
    response = data.get('response', '')
    
    if not keyword or not response:
        return jsonify({'error': 'Both keyword and response are required'}), 400
    
    result = bot.add_faq(keyword, response)
    return jsonify({'message': result})

# Create templates directory if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')

if __name__ == '__main__':
    app.run(debug=True) 