from advanced_chatbot import AdvancedSupportBot

# Create a bot with LLM capabilities
bot = AdvancedSupportBot(name="TestBot", use_llm=True)

# Test with a simple greeting
print(f"Bot: {bot.get_response('Hello')}")

# Test with a FAQ that should be in the knowledge base
print(f"\nBot: {bot.get_response('What are your store hours?')}")

# Test with a more complex question that would need LLM
print(f"\nBot: {bot.get_response('Can you recommend skincare products for dry skin?')}")

# Test with another complex query
print(f"\nBot: {bot.get_response('What are the differences between your basic and premium plans?')}")

# Test with a user providing their name
print(f"\nBot: {bot.get_response('My name is Alice')}")
print(f"Bot: {bot.get_response('What do you think would be good for me?')}") 