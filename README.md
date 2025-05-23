# AI-Enhanced Support Bot for Small Business

A rule-based chatbot with LLM capabilities that serves as a customer support agent for a small business or website.

## Overview

This project provides a customizable chatbot that can:

- Greet users and respond to common queries
- Capture and remember user names
- Answer FAQs using rule-based matching or basic NLP
- Use advanced AI (LLM) for handling complex questions
- Log conversations for later analysis
- Allow adding new FAQ responses

The project includes both basic and advanced implementations, as well as command-line and web interfaces.

## Project Structure

- `chatbot.py` - Basic rule-based chatbot implementation
- `advanced_chatbot.py` - Enhanced version using NLTK and LLM integration
- `llm_integration.py` - Module for integrating with LLM API
- `chat_cli.py` - Command-line interface for interacting with the chatbot
- `app.py` - Flask web application for the chatbot
- `knowledge_base.json` - JSON file storing chatbot responses
- `templates/index.html` - HTML template for the web interface
- `setup.py` - Setup script for easy installation

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd support-bot
```

2. Run the setup script:
```
python setup.py
```

3. Or install dependencies manually:
```
pip install -r requirements.txt
```

4. Run the command-line version:
```
python chat_cli.py
```

5. Or run the web version:
```
python app.py
```
Then open your browser to http://127.0.0.1:5000/

## How It Works

### Rule-based Chatbot (`chatbot.py`)

The basic version uses simple pattern matching techniques:

1. **Keyword matching**: Identifies keywords in user input and maps them to predefined responses
2. **Regular expressions**: Extracts information like names
3. **Response templates**: Uses templates with placeholders for dynamic responses

```python
# Example of getting a response
bot = SupportBot()
response = bot.get_response("What are your store hours?")
print(response)  # Outputs information about store hours
```

### Advanced Chatbot (`advanced_chatbot.py`)

The advanced version enhances the basic chatbot with:

1. **Text preprocessing**: Tokenization, removing stopwords, lemmatization
2. **Similarity matching**: Calculates text similarity to find the best matching FAQ
3. **Context tracking**: Keeps track of conversation context
4. **LLM Integration**: Falls back to advanced AI for complex questions

```python
# Example of using the advanced features
bot = AdvancedSupportBot()
response = bot.get_response("Can you tell me about your return policy?")
print(response)  # Uses similarity matching to find the best response
```

### LLM Integration (`llm_integration.py`)

The LLM integration provides:

1. **Advanced AI responses**: Handles complex questions beyond the FAQ database
2. **Context-aware answers**: Takes conversation history into account
3. **Personalization**: Uses customer name if available

```python
# Example of getting an LLM response
from llm_integration import get_llm_response
response = get_llm_response("What products would you recommend for someone with sensitive skin?")
print(response)  # Generates a helpful, context-aware response
```

### Knowledge Base

All responses are stored in `knowledge_base.json` with the following structure:

```json
{
    "greeting": ["Hello! I'm {bot_name}, here to help you today."],
    "goodbye": ["Thank you for chatting with us today!"],
    "faq": {
        "hours": ["Our store is open Monday-Friday 9AM-6PM..."],
        "return policy": ["You can return any unused item..."]
    }
}
```

## LLM Configuration

The chatbot uses an LLM API for advanced responses. The API key is stored in a `.env` file:

1. Create a file named `.env` in the project root directory
2. Add your API key: `OPENROUTER_API_KEY=your-api-key-here`

The key is already included, but you can replace it with your own if needed.

## Customization

### Adding FAQs

You can add new FAQs through the command-line interface:

```
add faq delivery How long does delivery take? Usually 3-5 business days.
```

Or through the web interface using the "Add FAQ" tab.

### Modifying the Knowledge Base

Edit the `knowledge_base.json` file directly to add or modify responses:

1. Add new greeting variations
2. Modify existing FAQ answers
3. Add entirely new FAQ categories

## Web Interface

The web interface (`app.py` and `templates/index.html`) provides:

1. A chat window for interacting with the bot
2. An interface for adding new FAQ responses
3. Conversation history in the current session
4. Visual indication when the AI is thinking

## Learning from This Project

Key concepts to understand:

1. **Rule-based systems**: How simple if-else logic and pattern matching can create interactive experiences
2. **Natural Language Processing basics**: Using NLTK for text preprocessing and matching
3. **LLM integration**: How to integrate advanced AI models with simple rule-based systems
4. **Web development**: Building a simple Flask API and frontend
5. **Data persistence**: Saving and loading conversation logs and knowledge bases

## Advanced Enhancements (Future Ideas)

Some ways to extend this project:

1. Add fine-tuning for the LLM with your specific business data
2. Implement entity extraction to understand more complex queries
3. Create a database backend instead of JSON files
4. Add user authentication for the web interface
5. Implement multi-language support
6. Add a voice interface using speech-to-text and text-to-speech

## Troubleshooting

- If you see NLTK errors, make sure you've installed all dependencies and NLTK data
- If logs aren't being created, check permissions on the logs directory
- For web interface issues, check the Flask console for error messages
- If LLM responses aren't working, verify your API key in the `.env` file

## License

---

This project was created as a learning resource. Feel free to modify and extend it for your own use! 