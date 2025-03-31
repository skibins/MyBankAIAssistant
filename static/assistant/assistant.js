function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();

            if(message) {
                // Add user message
                addMessage(message, 'user');

                // Simulate AI response (replace with actual API call)
                setTimeout(() => {
                    addMessage("Thank you for your question. Our virtual assistant is processing your request...", 'ai');
                }, 1000);

                input.value = '';
            }
        }

        function addMessage(text, sender) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            messageDiv.textContent = text;
            messagesDiv.appendChild(messageDiv);

            messagesDiv.scrollTo({
                top: messagesDiv.scrollHeight,
                behavior: 'smooth'
            });
        }

    document.getElementById("userInput").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
