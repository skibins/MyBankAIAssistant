class ChatApp {
    constructor(chatContainerId, inputId) {
        this.chatContainer = document.getElementById(chatContainerId);
        this.inputField = document.getElementById(inputId);

        // Bind event listeners
        this.inputField.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                this.sendMessage();
            }
        });
    }

    sendMessage() {
        const message = this.inputField.value.trim();

        if (message) {
            this.addMessage(message, 'user');

            // Send to the backend
            fetch('/get_response', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                this.addMessage(data.response, 'ai');
            })
            .catch(error => {
                console.error("Error:", error);
                this.addMessage("Error: Unable to connect to AI.", 'ai');
            });

            this.inputField.value = '';
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerHTML = text;
        this.chatContainer.appendChild(messageDiv);

        this.chatContainer.scrollTo({
            top: this.chatContainer.scrollHeight,
            behavior: 'smooth'
        });
    }
}

// Initialize the chat app
const chatApp = new ChatApp("chatMessages", "userInput");
