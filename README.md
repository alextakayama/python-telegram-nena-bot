# 👩 Nena - Python Telegram Bot

**This is a RAG (Retrieval-Augmented Generation) application that acts as a personal assistant, answering general questions and interacting with the user's personal mailbox.**

## ✨ Features
- 💬 Answer general questions
- 📬 List email messages in a mailbox
- 📖 Read an entire message
- 🗑️ Delete message from a mailbox
- ✨ Summarize messages

---

## 🚀 Tech Stack
- **Programming Language**: Python 3.11
- **Packages**: Langchain, OpenAI, python-telegram-bot, imaplib/smtplib, python-dotenv
- **Persistence**: Files

---

## 🏗️ Running the Application with Docker Compose

To quickly set up and run the application using Docker Compose, follow these steps:

1. **Ensure Docker and Docker Compose are installed**
   - [Install Docker](https://docs.docker.com/get-docker/)
   - [Install Docker Compose](https://docs.docker.com/compose/install/)

2. **Register a new Telegram bot using BotFather**
    - Open Telegram and search for "@BotFather"
    - Start a chat and use ``/newbot`` command
    - Follow prompts to set a name and username (must end in 'bot')
    - BotFather will provide you with an API token - keep this secure

3. **Clone the repository**
```sh
git clone https://github.com/alextakayama/python-telegram-nena-bot.git
cd python-telegram-nena-bot
```

3. **Copy and edit .env with your own values**
```sh
cp .env.example .env
vi .env
```

4. **Start the application**
```sh
docker-compose up -d
```

This will start the Telegram bot application in detached mode (`-d`).

**To stop the application:**
```sh
docker-compose stop
```

**And to delete the container:**
```sh
docker-compose down
```

---

## 🚀 Why I Built This
Recent advances in Artificial Intelligence and the widespread availability of generative AI services have made it feasible to develop intelligent applications with features such as text classification, information summarization, data extraction, editing and revision, reasoning and problem-solving, personalization and recommendations, moderation, and tutoring. This project demonstrates how leveraging LLMs with user-specific content can streamline everyday tasks—like accessing your emails—and make routine operations much faster.

---

## 🛠️ Future Improvements & TODOs
- Add command to send e-mails
- Add [run_webhook](https://docs.python-telegram-bot.org/en/stable/telegram.ext.application.html#telegram.ext.Application.run_webhook) support
- Add multi-modality support
- Add [function calling](https://platform.openai.com/docs/guides/function-calling)
- Add memory checks and token contraints
- Add tests

---

## 👋 About Me

<img alt="Foto de Alex Takayama" src="https://alextakayama.com/images/alex_takayama.jpg" style="border-radius: 50%; height: 100px; width: 100px">

Hi, I'm **Alex Takayama**, a builder at heart, passionate about technology and problem-solving. I have experience crafting scalable applications and driving innovation for enterprises and startups. Always eager to collaborate—let’s build something great together!

### 💻 Skills
- **Languages**: C++, C#, Java, JavaScript, Lua, Node.JS, Perl, PHP, Python, Rust, Typescript
- **Backend**: ASP.NET, Express, FastAPI, Flask, Laravel, Nest.JS, Phalcon, Play Framework, Slim, Spring Boot, Symfony
- **Frontend**: Angular, Next.js, React, Vue.js
- **Mobile**: React Native, Flutter
- **Databases**: DynamoDB, MariaDB, MongoDB, MySQL, SQL Server, PostgreSQL, SQLite
- **DevOps**: Apache, AWS, CI/CD, GCP, Docker, Memcached, NginX, RabbitMQ, Redis, Terraform, Varnish

### 🌐 Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/alextakayama) [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&labelColor=181717)](https://github.com/alextakayama)

### 📫 Contact

You can also reach me by email: [alex.takayama@gmail.com](mailto:alex.takayama@gmail.com).

---

## 📄 License

Distributed under the [MIT License](https://opensource.org/license/MIT).
