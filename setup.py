import os
import subprocess
import sys

def setup():
    """Setup the chatbot project with all dependencies"""
    print("Setting up the AI Support Bot project...")
    
    # Create necessary directories
    if not os.path.exists('logs'):
        os.makedirs('logs')
        print("Created logs directory")
    
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("Created templates directory")
    
    # Install dependencies
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("Error installing dependencies. Please try manually: pip install -r requirements.txt")
    
    # Setup NLTK data
    print("\nDownloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        print("NLTK data downloaded successfully!")
    except ImportError:
        print("NLTK not installed. Please run: pip install nltk")
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")
    
    # Create .env file for API key if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("# Add your OpenRouter API key here\n")
            f.write("OPENROUTER_API_KEY=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\n")
        print("\nCreated .env file with API key")
    
    print("\nSetup complete! You can now run the bot using:")
    print("   - Command line interface: python chat_cli.py")
    print("   - Web interface: python app.py")
    print("\nNote: To use the LLM capabilities, make sure your API key is correct in the .env file.")

if __name__ == "__main__":
    setup() 