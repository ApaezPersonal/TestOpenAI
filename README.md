# AI E-Commerce Assistant

## Description

This application is an AI-powered e-commerce assistant built using OpenAI's API. It provides product details and checks stock availability based on user queries.

## Requirements

- Python 3.8+
- OpenAI Python SDK
- Visual Studio (optional but recommended for development)

## Installation

1. **Install Python** (if not already installed):
   - Download and install from [python.org](https://www.python.org/downloads/)
2. **Install dependencies:**
   ```sh
   pip install openai
   ```
3. **Set up your OpenAI API key as an environment variable:**
   ```sh
   export OPENAI_API_KEY="your_api_key_here"  # Linux/macOS
   set OPENAI_API_KEY="your_api_key_here"  # Windows (Command Prompt)
   $env:OPENAI_API_KEY="your_api_key_here"  # Windows (PowerShell)
   ```

## Running the Application

1. **Open a terminal or command prompt.**
2. **Navigate to the project directory.**
3. **Run the script:**
   ```sh
   python TestOpenAI.py
   ```
4. **Start chatting with the assistant!**

## Usage Example

```
You: Tell me about the Wireless Earbuds.
Assistant: The Wireless Earbuds are noise-canceling earbuds available for $59.99.
You: Is it available?
Assistant: The Wireless Earbuds are in stock with 5 units available.
```

## Features

- Provides detailed product information.
- Checks stock availability.
- Maintains context for follow-up queries.
- Uses OpenAI's `gpt-4o` model for intelligent responses.

## License

This project is for educational purposes only and follows OpenAI's API usage guidelines.
