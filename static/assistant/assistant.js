class ChatApp {
    constructor(chatContainerId, inputId) {
        this.chatContainer = document.getElementById(chatContainerId);
        this.inputField   = document.getElementById(inputId);
        this.counter      = 0;

        // załaduj zapisane tematy
        const stored = localStorage.getItem('topics');
        if (stored) {
            try {
                const topics = JSON.parse(stored);
                for (let i = 1; i <= 3; i++) {
                    const tEl = document.getElementById(`topicTitle${i}`);
                    const dEl = document.getElementById(`topicDesc${i}`);
                    if (topics[i-1] && tEl && dEl) {
                        tEl.innerText = topics[i-1].title;
                        dEl.innerText = topics[i-1].description;
                    }
                }
            } catch {}
        }

        // kliknięcia na bloki tematów
        document.querySelectorAll('.topic-card').forEach(card => {
            card.addEventListener('click', () => {
                const title = card.querySelector('h3').innerText;
                this.sendTopicRequest(title);
            });
        });

        this.inputField.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                this.sendMessage();
            }
        });
    }

    sendMessage() {
        const message = this.inputField.value.trim();
        if (!message) return;
        this.addMessage(message, 'user');
        this._sendToGemini(message);
        this.inputField.value = '';
    }

    sendTopicRequest(topicTitle) {
        const prompt = `Hey, I've got a problem related to this topic: ${topicTitle}. Can you help me?`;
        this.addMessage(prompt, 'user');
        this._sendToGemini(prompt);
    }


    _sendToGemini(message) {
        this.counter++;
        fetch('/get_response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        })
        .then(res => res.json())
        .then(data => {
            // 1) normal chat
            const chatText = data.chat_response ?? data.response;
            this.addMessage(chatText, 'ai');

            // 2) update co 3 wiadomości
            if (this.counter % 3 === 0
                && data.problem_title
                && data.problem_description) {
                // sliding window
                for (let i = 3; i > 1; i--) {
                    const prevT = document.getElementById(`topicTitle${i-1}`);
                    const prevD = document.getElementById(`topicDesc${i-1}`);
                    const curT  = document.getElementById(`topicTitle${i}`);
                    const curD  = document.getElementById(`topicDesc${i}`);
                    if (prevT && prevD && curT && curD) {
                        curT.innerText = prevT.innerText;
                        curD.innerText = prevD.innerText;
                    }
                }
                // nowy na górę
                const t1 = document.getElementById("topicTitle1");
                const d1 = document.getElementById("topicDesc1");
                t1.innerText = data.problem_title;
                d1.innerText = data.problem_description;

                // zapisz stan
                const topics = [];
                for (let i = 1; i <= 3; i++) {
                    const title = document.getElementById(`topicTitle${i}`).innerText;
                    const desc  = document.getElementById(`topicDesc${i}`).innerText;
                    topics.push({ title, description: desc });
                }
                localStorage.setItem('topics', JSON.stringify(topics));
            }
        })
        .catch(err => {
            console.error(err);
            this.addMessage("Error: Unable to connect to AI.", 'ai');
        });
    }

    addMessage(text, sender) {
        const msg = document.createElement('div');
        msg.className = `message ${sender}-message`;
        msg.innerHTML = text;
        this.chatContainer.appendChild(msg);
        this.chatContainer.scrollTo({ top: this.chatContainer.scrollHeight, behavior: 'smooth' });
    }
}

const chatApp = new ChatApp("chatMessages", "userInput");
