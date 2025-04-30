class ChatApp {
  /**
   * Single-class object-oriented chat application managing UI, API calls, and topics.
   * @param {string} chatContainerId - ID of the chat messages container.
   * @param {string} inputId - ID of the user input field.
   * @param {string} apiEndpoint - URL endpoint for fetching AI responses.
   */
  constructor(chatContainerId, inputId, apiEndpoint = '/get_response') {
    // UI elements
    this.chatContainer = document.getElementById(chatContainerId);
    this.inputField = document.getElementById(inputId);

    // API setup
    this.apiEndpoint = apiEndpoint;
    this.counter = 0;

    // Topic state
    this.maxTopics = 3;
    this.topicIds = Array.from({ length: this.maxTopics }, (_, i) => i + 1);
    this._loadTopics();

    // Event bindings
    this._bindInput();
    this._bindTopicClicks();
  }

  /**
   * Bind Enter key on input to send messages.
   */
  _bindInput() {
    this.inputField.addEventListener('keydown', event => {
      if (event.key === 'Enter') {
        event.preventDefault();
        this.sendMessage();
      }
    });
  }

  /**
   * Attach click handlers to topic cards to trigger topic requests.
   */
  _bindTopicClicks() {
    document.querySelectorAll('.topic-card').forEach(card => {
      card.addEventListener('click', () => {
        const title = card.querySelector('h3').innerText;
        this.sendTopicRequest(title);
      });
    });
  }

  /**
   * Send user-typed message.
   */
  async sendMessage() {
    const message = this.inputField.value.trim();
    if (!message) return;
    this._addMessage(message, 'user');
    this.inputField.value = '';
    await this._processMessage(message);
  }

  /**
   * Send a predefined topic-based prompt.
   * @param {string} topicTitle
   */
  async sendTopicRequest(topicTitle) {
    const prompt = `Hey, I've got a problem related to this topic: ${topicTitle}. Can you help me?`;
    this._addMessage(prompt, 'user');
    await this._processMessage(prompt);
  }

  /**
   * Core handler: calls API, updates chat UI, and topics every third message.
   * @param {string} message
   */
  async _processMessage(message) {
    this.counter++;
    try {
      const data = await this._fetchResponse(message);
      const chatText = data.chat_response || data.response || 'No response';
      this._addMessage(chatText, 'ai');

      if (this.counter % 3 === 0 && data.problem_title && data.problem_description) {
        this._rotateTopics(data.problem_title, data.problem_description);
      }
    } catch (error) {
      console.error(error);
      this._addMessage('Error: Unable to connect to AI.', 'ai');
    }
  }

  /**
   * Fetch AI response from backend.
   * @param {string} message
   * @returns {Promise<object>}
   */
  async _fetchResponse(message) {
    const res = await fetch(this.apiEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json();
  }

  /**
   * Add a chat message to the UI.
   * @param {string} text
   * @param {'user'|'ai'} sender
   */
  _addMessage(text, sender) {
    const msg = document.createElement('div');
    msg.className = `message ${sender}-message`;
    msg.innerHTML = text;
    this.chatContainer.appendChild(msg);
    this.chatContainer.scrollTo({ top: this.chatContainer.scrollHeight, behavior: 'smooth' });
  }

  /**
   * Load saved topics from localStorage and render them.
   */
  _loadTopics() {
    const stored = localStorage.getItem('topics');
    if (!stored) return;
    try {
      const topics = JSON.parse(stored);
      this.topicIds.forEach(i => {
        const tEl = document.getElementById(`topicTitle${i}`);
        const dEl = document.getElementById(`topicDesc${i}`);
        if (topics[i - 1] && tEl && dEl) {
          tEl.innerText = topics[i - 1].title;
          dEl.innerText = topics[i - 1].description;
        }
      });
    } catch (e) {
      console.warn('Failed to load topics:', e);
    }
  }

  /**
   * Rotate topic cards downward and insert a new topic at the top, then persist.
   * @param {string} title
   * @param {string} description
   */
  _rotateTopics(title, description) {
    for (let i = this.maxTopics; i > 1; i--) {
      const prevT = document.getElementById(`topicTitle${i - 1}`);
      const prevD = document.getElementById(`topicDesc${i - 1}`);
      const curT = document.getElementById(`topicTitle${i}`);
      const curD = document.getElementById(`topicDesc${i}`);
      if (prevT && prevD && curT && curD) {
        curT.innerText = prevT.innerText;
        curD.innerText = prevD.innerText;
      }
    }
    const firstT = document.getElementById('topicTitle1');
    const firstD = document.getElementById('topicDesc1');
    if (firstT && firstD) {
      firstT.innerText = title;
      firstD.innerText = description;
    }
    this._saveTopics();
  }

  /**
   * Persist current topics in localStorage.
   */
  _saveTopics() {
    const topics = this.topicIds.map(i => ({
      title: document.getElementById(`topicTitle${i}`).innerText,
      description: document.getElementById(`topicDesc${i}`).innerText
    }));
    localStorage.setItem('topics', JSON.stringify(topics));
  }
}

// Initialize the single ChatApp class
const chatApp = new ChatApp('chatMessages', 'userInput');
