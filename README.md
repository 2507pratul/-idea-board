\# 💡 IdeaBoard — AI-Ready, Cloud-Agnostic DevOps Platform



IdeaBoard is a full-stack application for creating, viewing, editing, and deleting ideas. It uses React, FastAPI, and PostgreSQL, with Docker-based containerization and a GitHub Actions CI/CD pipeline that builds and publishes application images to Docker Hub.



The project establishes a foundation for an AI-assisted, cloud-agnostic DevOps platform.



> \*\*Implementation status:\*\* The full-stack application, Docker containerization, and Docker Hub image publishing pipeline are implemented. AI-assisted automation, Infrastructure as Code, Kubernetes orchestration, and multi-cloud deployments are planned extensions and are not yet implemented.



\## 1. Features



\- Create, view, update, and delete ideas.

\- REST API built with FastAPI.

\- React-based frontend.

\- PostgreSQL database integration.

\- Dockerfiles for frontend and backend.

\- Docker Compose orchestration for local development.

\- GitHub Actions workflow for automated Docker image builds.

\- Automated publishing of frontend and backend images to Docker Hub.

\- Database health checks before backend startup.



\## 2. Technology Stack



| Technology | Purpose |

|---|---|

| React | Frontend application |

| Python | Backend programming language |

| FastAPI | REST API |

| PostgreSQL 16 | Persistent database |

| Docker | Application containerization |

| Docker Compose | Local multi-container orchestration |

| GitHub Actions | CI/CD automation |

| Docker Hub | Container image registry |

| Nginx | Frontend web server |



\## 3. Architecture



\### Current application architecture



```text

&#x20;                User

&#x20;                  |

&#x20;                  v

&#x20;           React Frontend

&#x20;             (Nginx)

&#x20;                  |

&#x20;                  v

&#x20;            FastAPI Backend

&#x20;                  |

&#x20;                  v

&#x20;             PostgreSQL

```



Docker Compose manages the three services:



\- `frontend`: Serves the React production build through Nginx.

\- `backend`: Runs the FastAPI application.

\- `db`: Stores application data in PostgreSQL.



\### Current CI/CD architecture



```text

&#x20;      Developer pushes code

&#x20;                |

&#x20;                v

&#x20;            GitHub

&#x20;                |

&#x20;                v

&#x20;         GitHub Actions

&#x20;                |

&#x20;         Docker Buildx

&#x20;                |

&#x20;         +------+------+

&#x20;         |             |

&#x20;         v             v

&#x20;     Backend        Frontend

&#x20;      Build           Build

&#x20;         |             |

&#x20;         +------+------+

&#x20;                |

&#x20;                v

&#x20;            Docker Hub

```



Pull requests trigger image builds without publishing. Pushes to `main` trigger builds and publish both images.



\## 4. Project Structure



```text

idea-board/

│

├── .github/

│   └── workflows/

│       └── ci.yml

│

├── backend/

│   ├── main.py

│   └── Dockerfile

│

├── frontend/

│   ├── src/

│   │   ├── App.jsx

│   │   ├── App.css

│   │   └── main.jsx

│   └── Dockerfile

│

├── docker-compose.yml

└── README.md

```



\## 5. Run Locally



\### Prerequisites



\- Git

\- Docker Desktop

\- Docker Compose



\### Clone the repository



```bash

git clone https://github.com/2507pratul/-idea-board.git

cd -idea-board

```



\### Build and start the application



```bash

docker compose up --build -d

```



\### Access the application



| Service | URL |

|---|---|

| Frontend | http://localhost:3000 |

| Backend API | http://localhost:8000 |

| FastAPI Swagger documentation | http://localhost:8000/docs |



\### Verify containers



```bash

docker compose ps

```



\### View logs



```bash

docker compose logs

```



\### Stop the application



```bash

docker compose down

```



To remove containers and the persistent database volume as well:



```bash

docker compose down -v

```



\*\*Warning:\*\* The `-v` option deletes the local PostgreSQL data stored in the Compose volume.



\## 6. REST API



| Method | Endpoint | Description |

|---|---|---|

| GET | `/api/ideas` | Retrieve all ideas |

| POST | `/api/ideas` | Create a new idea |

| PUT | `/api/ideas/{id}` | Update an existing idea |

| DELETE | `/api/ideas/{id}` | Delete an idea |



Interactive API documentation is available at:



http://localhost:8000/docs



\## 7. Docker Images



The application images are published to Docker Hub.



| Component | Docker Image |

|---|---|

| Backend | `pratulgurjar/ideaboard-backend:latest` |

| Frontend | `pratulgurjar/ideaboard-frontend:latest` |



Pull

