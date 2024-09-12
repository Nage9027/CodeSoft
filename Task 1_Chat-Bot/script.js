const chatMessages = document.querySelector('.chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// Define the rules and responses
const rules = {
    "hello|hi|hey": "Hello! How can I assist you today?",
    "how are you|what's up": "I'm doing well, thanks! How about you?",
    "what's your name": "I'm a chatbot, nice to meet you!",
    "help|assist": "I can help with math, coding, and general questions. What do you need help with?",
    "goodbye|bye|see you": "Goodbye! It was nice chatting with you.",
    "default": "I didn't understand that. Can you please rephrase?"
};

function respond(user_input) {
    // Convert the user input to lowercase for case-insensitive matching
    user_input = user_input.toLowerCase();

    // Iterate through the rules and check if the user input matches any of them
    for (const [pattern, response] of Object.entries(rules)) {
        if (pattern.split("|").some(word => user_input.includes(word))) {
            return response;
        }
    }

    // If no rule matches, return the default response
    return rules["default"];
}

function sendMessage() {
    const userMessage = userInput.value;
    if (userMessage.trim() !== '') {
        chatMessages.innerHTML += `<div class="user-message">${userMessage}</div>`;
        const chatbotResponse = respond(userMessage);
        chatMessages.innerHTML += `<div class="chatbot-message">${chatbotResponse}</div>`;
        userInput.value = '';
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to the bottom
    }
}

// Event listener for the 'Send' button
sendButton.addEventListener('click', () => {
    sendMessage();
});

// Event listener for pressing 'Enter' key
userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();  // Prevent form submission (if applicable)
        sendMessage();
    }
});
