# MessageBox

This project is a messaging application that includes a FastAPI web server, a MongoDB database, Redis for caching, a Nginx web server and a Telegram bot using aiogram. The web server provides endpoints for creating and retrieving messages, while the Telegram bot allows users to interact with the messaging service directly from Telegram.

## Features

- FastAPI web server with endpoints:
  - `GET /api/v1/messages/` - Retrieve all messages
  - `POST /api/v1/message/` - Create a new message
- MongoDB for message storage
- Redis for caching messages
- Nginx as a reverse proxy
- Telegram bot for interacting with the messaging service


## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Belgrak/MessageBox.git
   cd MessageBox

2. Create a `.env` file in the root directory and add your Telegram bot token:
    ```sh 
    TELEGRAM_BOT_API_TOKEN=your_telegram_bot_api_token

### Running the Project

1. Build and start the Docker containers:
    ```sh
    docker-compose up --build

2. Interact with the Telegram bot by searching for your bot in the Telegram app and starting a conversation.


## FastAPI Endpoints

### GET /api/v1/messages/

- Description: Retrieve all messages.

- Response: JSON array of messages.

### POST /api/v1/message/

- Description: Create a new message.

- Request Body: JSON object with author and content fields.

- Response: JSON object of the created message.

## Telegram Bot Commands

### /start or /help
- Get a welcome message and a list of available commands.
### /messages 
- Retrieve and display all messages.