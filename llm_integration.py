import os
import requests
import json
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure API key
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("Warning: OpenRouter API key not found in environment variables")
    # Fallback to a placeholder - replace this with your actual API key
    api_key = "your-api-key-here"

# Simple canned responses for fallback
canned_responses = {
    "skincare": "For skincare questions, I recommend products with hyaluronic acid for hydration and niacinamide for skin barrier protection. We have various options depending on your specific skin concerns.",
    "pricing": "We offer several pricing plans: Basic ($9.99/month), Premium ($19.99/month), and Enterprise (custom pricing). Each offers different features tailored to business size and needs.",
    "shipping": "We offer standard shipping (3-5 business days), express shipping (1-2 business days), and overnight shipping options. Free shipping is available on orders over $50.",
    "returns": "Our return policy allows you to return unused items within 30 days of purchase for a full refund. Just include your order number with the return."
}

def get_fallback_response(query):
    """Provide a canned response based on keywords in the query"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["skin", "moisturizer", "lotion", "cream"]):
        return canned_responses["skincare"]
    elif any(word in query_lower for word in ["price", "cost", "plan", "subscription", "premium"]):
        return canned_responses["pricing"]
    elif any(word in query_lower for word in ["ship", "delivery", "arrive"]):
        return canned_responses["shipping"]
    elif any(word in query_lower for word in ["return", "refund", "money back"]):
        return canned_responses["returns"]
    
    return "I don't have specific information on that topic. Would you like me to forward your question to our product specialist?"

def _call_llm_api(user_query, conversation_history=None, user_name=None):
    """
    Get a response from the LLM based on the user's query and conversation history
    
    Args:
        user_query (str): The user's question or message
        conversation_history (list): Optional list of previous exchanges
        user_name (str): Optional name of the user for personalization
        
    Returns:
        str: The LLM's response
    """
    try:
        # Format system prompt based on our support bot's purpose
        system_prompt = """You are a helpful customer support assistant for a small business.
Your goal is to be helpful, concise, and friendly. If you don't know the answer to something, 
just say you don't have that information rather than making something up. 
If the user is looking for specific product information you don't have, offer to take their contact details
to have someone follow up with them."""

        # Add user name to personalize if available
        if user_name:
            system_prompt += f"\nThe customer's name is {user_name}."
            
        # Prepare the messages including conversation history if available
        messages = [{"role": "system", "content": system_prompt}]
        
        if conversation_history and isinstance(conversation_history, list):
            # Add up to the last 5 exchanges to provide context without making the prompt too long
            for exchange in conversation_history[-5:]:
                if isinstance(exchange, dict) and "user_input" in exchange and "bot_response" in exchange:
                    messages.append({"role": "user", "content": exchange["user_input"]})
                    messages.append({"role": "assistant", "content": exchange["bot_response"]})
        
        # Add the current user query
        messages.append({"role": "user", "content": user_query})
        
        # API request data for OpenRouter
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://your-website.com", # Replace with your website if needed
            "X-Title": "Support Bot" # Identify your application
        }
        
        payload = {
            "model": "openai/gpt-3.5-turbo", # Using OpenAI's model through OpenRouter
            "messages": messages,
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        # Make request to OpenRouter API
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            response_data = response.json()
            if "choices" in response_data and len(response_data["choices"]) > 0:
                if "message" in response_data["choices"][0] and "content" in response_data["choices"][0]["message"]:
                    return response_data["choices"][0]["message"]["content"].strip()
        
        # If we get here, there was an issue with the response format
        print(f"Unexpected API response: {response.text}")
        return None
    
    except Exception as e:
        print(f"Error calling LLM API: {e}")
        return None

def get_llm_response(user_query, conversation_history=None, user_name=None):
    """
    Get a response using LLM with fallback to canned responses if needed
    
    Args:
        user_query (str): The user's question or message
        conversation_history (list): Optional list of previous exchanges
        user_name (str): Optional name of the user for personalization
        
    Returns:
        str: The response
    """
    # Try to get a response from the LLM
    llm_response = _call_llm_api(user_query, conversation_history, user_name)
    
    # If we got a valid response from the LLM, return it
    if llm_response:
        return llm_response
    
    # Otherwise, fall back to canned responses
    return get_fallback_response(user_query)

# Test function
if __name__ == "__main__":
    test_response = get_llm_response("What are your store hours?")
    print(test_response)
    
    test_response = get_llm_response("Can you recommend skincare products for dry skin?")
    print(test_response) 