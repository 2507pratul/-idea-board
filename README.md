
# 💡 IdeaBoard

IdeaBoard is a full-stack web application where users can create, view, update, and delete ideas.

## 🚀 Features

- Create new ideas
- View all saved ideas
- Edit existing ideas
- Delete ideas
- PostgreSQL database integration
- REST API using FastAPI
- React frontend
- Docker containerization

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| React | Frontend |
| Python | Backend language |
| FastAPI | REST API |
| PostgreSQL | Database |
| Docker | Containerization |
| Docker Compose | Multi-container management |

## 🏗️ Project Architecture

React Frontend
      |
      v
FastAPI Backend
      |
      v
PostgreSQL Database

Docker Compose manages the application containers.

## 📁 Project Structure

idea-board/
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       └── main.jsx
│
├── backend/
│   ├── main.py
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md

## ⚙️ Run Locally

### 1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL

### 2. Open the project folder

cd idea-board

### 3. Build and start containers

docker compose up --build -d

### 4. Open the application

Frontend:
http://localhost:3000

Backend API:
http://localhost:8000

API Documentation:
http://localhost:8000/docs

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/ideas | Get all ideas |
| POST | /api/ideas | Create an idea |
| PUT | /api/ideas/{id} | Update an idea |
| DELETE | /api/ideas/{id} | Delete an idea |

## 🐳 Docker Commands

Start containers:

docker compose up -d

Rebuild containers:

docker compose up --build -d

View running containers:

docker compose ps

View logs:

docker compose logs

Stop containers:

docker compose down

## 👨‍💻 Author

Pratul Gurjar
