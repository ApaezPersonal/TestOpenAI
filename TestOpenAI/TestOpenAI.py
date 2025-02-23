import openai
import json
import os

# Initialize the OpenAI client with the API key from an environment variable or user input
api_key = os.getenv("OPENAI_API_KEY") or input("Enter your OpenAI API key: ").strip()
client = openai.OpenAI(api_key=api_key)

# Mock product catalog with product details
# Each product has a name, description, price, and stock quantity
products = {
    1: {"name": "EcoFriendly Water Bottle", "desc": "Reusable bottle.", "price": 15.99, "stock": 10},
    2: {"name": "Wireless Earbuds", "desc": "Noise-canceling earbuds.", "price": 59.99, "stock": 5},
    3: {"name": "Smartwatch", "desc": "Fitness tracking smartwatch.", "price": 199.99, "stock": 2},
    4: {"name": "Laptop Stand", "desc": "Ergonomic adjustable stand.", "price": 29.99, "stock": 8},
    5: {"name": "Gaming Mouse", "desc": "Customizable gaming mouse.", "price": 49.99, "stock": 12}
}

def get_product_info(name):
    """Retrieve product details based on the product name from the catalog."""
    for product in products.values():
        if name.lower() in product["name"].lower():
            return product
    return None

def check_stock(name):
    """Check the stock availability of a product based on its name."""
    for product in products.values():
        if name.lower() in product["name"].lower():
            return {"name": product["name"], "stock": product["stock"]}
    return None

def call_assistant(user_message, last_product):
    """Send the user's message to the AI assistant and retrieve a response."""
    if "available" in user_message.lower() and last_product:
        user_message += f" (Product: {last_product})"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "AI e-commerce assistant."},
                {"role": "user", "content": user_message}
            ],
            functions=[
                {
                    "name": "get_product_info",
                    "description": "Fetch details about a product.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "The name of the product"}
                        },
                        "required": ["name"]
                    }
                },
                {
                    "name": "check_stock",
                    "description": "Check stock availability of a product.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "The name of the product"}
                        },
                        "required": ["name"]
                    }
                }
            ],
            function_call="auto"
        )
        return response.choices[0].message
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def process_response(response, last_product):
    """Process the response from the AI assistant and return the relevant result."""
    # If the AI assistant makes a function call, determine which function to use
    if hasattr(response, "function_call") and response.function_call:
        func = response.function_call.name
        name = json.loads(response.function_call.arguments).get("name", last_product)
        if not name:
            return "Could you please specify which product you're referring to?", last_product
        
        # Determine if the request is for stock availability or product details
        product = check_stock(name) if func == "check_stock" else get_product_info(name)
        if not product:
            return "I'm sorry, but I couldn't find that product in our catalog.", last_product
        
        if func == "check_stock":
            # Instead of returning a hardcoded message, we request OpenAI to generate a natural response
            stock_status = f"{product['stock']} units available" if product["stock"] > 0 else "out of stock"

            ai_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an AI e-commerce assistant providing stock availability information in a natural way."},
                    {"role": "user", "content": f"Can you check the stock for {product['name']}?"},
                    {"role": "assistant", "content": f"The {product['name']} currently has {stock_status}."}
                ]
            )
            return ai_response.choices[0].message.content, name  # Maintain conversation context
        
        # Generate AI response dynamically for product details
        ai_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "AI e-commerce assistant."},
                {"role": "assistant", "content": f"Product details: {json.dumps(product)}"}
            ]
        )
        return ai_response.choices[0].message.content, name  # Maintain conversation context
    
    return response.content, last_product

def chat():
    """Initiate a chat session where users can interact with the AI assistant."""
    last_product = None  # Keep track of the last-mentioned product for context
    while True:
        msg = input("You: ")
        if msg.lower() in ["exit", "quit"]:
            break
        response = call_assistant(msg, last_product)
        if isinstance(response, dict) and "error" in response:
            print("Assistant:", response["error"])
            continue
        result, last_product = process_response(response, last_product)
        print("Assistant:", result)

# Run the chat application if the script is executed directly
if __name__ == "__main__":
    chat()
