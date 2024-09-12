# Define a dictionary to store the rules and responses
rules = {
    "hello|hi|hey": "Hello! How can I assist you today?",
    "how are you|what's up": "I'm doing well, thanks! How about you?",
    "what's your name": "I'm a chatbot, nice to meet you!",
    "help|assist": "I can help with math, coding, and general questions. What do you need help with?",
    "goodbye|bye|see you": "Goodbye! It was nice chatting with you.",
    "default": "I didn't understand that. Can you please rephrase?"
}

def respond(user_input):
    # Convert the user input to lowercase for case-insensitive matching
    user_input = user_input.lower()

    # Iterate through the rules and check if the user input matches any of them
    for pattern, response in rules.items():
        if any(word in user_input for word in pattern.split("|")):
            return response

    # If no rule matches, return the default response
    return rules["default"]

# Test the chatbot
while True:
    user_input = input("You: ")
    response = respond(user_input)
    print("Chatbot:", response)