***More detailed version of this app can be found at skibins/MyBankAIAssistant2.0 (Java/Spring, solo project)***

***For now please use 'dev' branch, as 'main' is currently experiencing some merge conflicts, Sebastian is responsible for the fix***

# MyBank AI Assistant Documentation

## Table of Contents

- [Project Authors](#project-authors)  
- [Program Description](#program-description)  
- [Technologies Used](#technologies-used)  
- [Installation](#installation)  
- [System Architecture](#system-architecture)  
- [List of System Components](#list-of-system-components)  
- [Testing](#testing)  
- [Development Opportunities](#development-opportunities)

---

## Project Authors

- Jan Skibiński  
- Sebastian Paszek  
- Michał Bujok  

---

## Program Description

**MyBank AI Assistant** is an intelligent system supporting online banking customer service, integrated with the bank’s website. The application runs in a client-server model and allows users to interact with the chatbot in real time through a web browser. After logging into their account, users gain access to personalized functions such as checking their balance, viewing transaction history, or making transfers.

The bot processes user queries in natural language, analyzes their content, and performs actions based on account data. This allows users to solve many issues that previously required contact with a bank employee, providing a fast, secure, and automated support channel.

---

## Technologies Used

| Technology               | Purpose                                        |
|--------------------------|------------------------------------------------|
| HTML, CSS                | Page layout and design                         |
| JavaScript               | Frontend-backend integration, UI handling     |
| Google GenAI SDK         | Communication with the Gemini model           |
| Flask                    | Hosting, routing, session management          |
| Python                   | Backend logic                                 |
| Regex & JSON             | Data parsing and cleaning                     |
| Git & GitHub             | Team project management                       |

---

## Installation

This guide was designed for PyCharm IDE. The application will run in any Python environment, though the library import process may vary.

1. Go to the interpreter settings and click "+" to add the following packages:

```
Flask  
generativeai  
google  
google-ai-generativelanguage  
google-api-core  
google-api-python-client  
google-auth  
google-auth-httplib2  
google-genai  
google-generativeai  
googleapis-common-protos  
```

2. Generate an API key in Google AI Studio and paste it into a file named `apiKey.txt` placed in the project’s root directory.

3. Run the file `run.py`.

4. Open the address link shown in the console (default: http://127.0.0.1:5000/) to access the MyBank site.

---

## System Architecture

### 1. Presentation Layer

- Renders dynamic pages using server-side HTML templates.  
- Manages frontend routing and navigation between sections.  
- Performs asynchronous API calls (fetch/xhr) for message sending and receiving.  
- Maintains UI state (chat history, local storage of hot topics).  

### 2. Application Logic Layer

- Built on a web framework handling HTTP(S) requests.  
- Maps URL paths to controller logic.  
- Handles user validation and authorization.  
- Returns HTML pages or JSON responses.  

### 3. Domain and Integration Layer

- Manages users, sessions, and communication with the conversational AI service.  
- Handles registration, login, data verification.  
- Builds enriched prompts for Gemini API.  
- Processes streamed responses from Gemini API.  

### 4. Data Access Layer

- Stores data locally using JSON files.  
- Reads and writes user records.  
- Manages chat history and user preferences.  
- Future improvements may involve switching to a relational DB or ORM for scalability.  

### 5. Security and Secret Management

- API keys and secrets (e.g., session key) are stored in hidden text files.  
- Uses session-based HTTP authentication.  
- Future improvements: CSRF protection, password encryption, input sanitization.  

### 6. Deployment and Scalability

- Can be launched as a single WSGI service with a web server (e.g., Gunicorn) and reverse proxy (e.g., Nginx).  
- Static files (CSS, JS, images) served directly from file server.  

**Future scalability options:**

- Docker containerization & Kubernetes orchestration  
- Unit and integration tests for core components  
- Monitoring and logging in production environment  

---

## List of System Components

### Python Files (.py)

- `run.py` – Initializes and runs the app in debug mode using `create_app()`.  
- `config.py` – Loads the API key, custom instructions, file paths, and session key.  
- `__init__.py` – Initializes Flask app, loads config, registers routes.  
- `gemini.py` – Builds prompt, sends queries, processes Gemini responses.  
- `routes.py` – Handles login, registration, logout, page rendering, and Gemini API communication.  
- `user.py` – Manages user data: save/load, register, login, email checking.  
- `utils.py` – Helper functions for reading/writing JSON files.  

### HTML Files (.html)

- `footer.html`  
- `header.html`  
- `about.html`  
- `assistant.html`  
- `base.html`  
- `login.html`  
- `main.html`  
- `services.html`  
- `creditcards.html`  
- `insurance.html`  
- `investments.html`  
- `loans.html`  
- `savings.html`

### CSS Files (.css)

- `about.css`  
- `assistant.css`  
- `global.css`  
- `footer.css`  
- `header.css`  
- `login.css`  
- `main.css`  
- `services.css`  
- `services_subpage.css`

### JavaScript Files (.js)

- `Assistant.js` – Handles chat UI, user message sending, Gemini API calls, and rotating chat topics via `localStorage`.  
- `BankRoute.js` – Manages page navigation, assigning actions to buttons like "home", "login", "services", and "about".  

### Image Files (.jpg, .png)

- `security.jpg`  
- `speed.jpg`  
- `support.jpg`  
- `bank.png`  
- `bank-account.png`  
- `bank-transfer.png`  
- `credit-card.png`  
- `piggy-bank.png`  
- `background.jpg`  
- `logo.png`

### Data and Text Files (.json, .txt)

- `users.json` – Stores user account data.  
- `additional_prompt.txt` – Extra instructions for the AI assistant.  
- `custom_instructions.txt` – Custom instructions for Gemini model.  
- `apiKey.txt` – Contains API key for Gemini access.  

### Config and Helper Files

- `.gitignore`  
- `.gitattributes`  
- `LICENSE`  
- `README.md`

---

## Testing

The program underwent detailed security testing, including end-to-end encryption to ensure user data confidentiality. All transmitted data is protected via SSL/TLS. Bot interaction analysis was also conducted to test prompt correctness and error detection, ensuring stable chatbot performance across various scenarios.

---

## Development Opportunities

Potential future enhancements include:

- **Two-Factor Authentication** – Adds a security layer to protect user accounts.  
- **Advanced Activity Monitoring** – Detects threats or abnormal behavior based on user interactions.  
- **Sentiment Analysis** – Adapts bot responses based on conversation tone.  
- **AI System Integration** – Real-time error detection and prompt adjustment.  
- **Extended Personalization** – Tailored responses based on user's history and preferences.
