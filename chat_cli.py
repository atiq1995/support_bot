from chatbot import SupportBot
import sys

def print_colored(text, color_code):
    """Print text with color for better UI"""
    print(f"\033[{color_code}m{text}\033[0m")

def main():
    print_colored("="*50, "1;34")
    print_colored("Welcome to the Support Bot CLI", "1;32")
    print_colored("Type 'exit', 'quit', or 'bye' to end the conversation", "1;33")
    print_colored("Type 'help' to see available commands", "1;33")
    print_colored("="*50, "1;34")
    
    # Initialize the chatbot
    bot = SupportBot(name="SupportBot")
    
    # Print a greeting
    print_colored(f"Bot: {bot.get_response('hello')}", "1;36")
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        # Check if user wants to exit
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print_colored(f"Bot: {bot.get_response('goodbye')}", "1;36")
            break
            
        # Handle special commands
        elif user_input.lower() == 'help':
            print_colored("Available commands:", "1;33")
            print_colored("  help - Show this help message", "1;33")
            print_colored("  add faq <keyword> <response> - Add a new FAQ response", "1;33")
            print_colored("  exit/quit/bye - End the conversation", "1;33")
            continue
            
        elif user_input.lower().startswith('add faq '):
            try:
                # Format: add faq keyword response text here
                parts = user_input[8:].strip().split(' ', 1)
                if len(parts) != 2:
                    print_colored("Error: Format should be 'add faq <keyword> <response>'", "1;31")
                    continue
                    
                keyword, response = parts
                result = bot.add_faq(keyword.lower(), response)
                print_colored(f"Bot: {result}", "1;36")
            except Exception as e:
                print_colored(f"Error: {str(e)}", "1;31")
            continue
        
        # Get bot response for normal queries
        response = bot.get_response(user_input)
        print_colored(f"Bot: {response}", "1;36")
        
        # Log the conversation
        bot.log_conversation(user_input, response)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0) 