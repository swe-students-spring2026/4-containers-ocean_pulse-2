![Lint](https://github.com/swe-students-spring2026/4-containers-ocean_pulse-2/actions/workflows/lint.yml/badge.svg)
![Event Logger](https://github.com/swe-students-spring2026/4-containers-ocean_pulse-2/actions/workflows/event-logger.yml/badge.svg)

# Ocean Pulse — Study Focus Tracker

Our project is a study focus tracker. Do you have a hard time concentrating when nobody is around to keep you accountable? Have you ever felt like you've been working for hours and still havent gotten much done? Our project uses a machine learning client to record when the user has lost focus while working on their computer. With our project you can measure your study session, which can help with setting goals and noticing patterns in your own behavior.

**Ocean Pulse** is a containerized study focus tracker that uses machine learning to detect when you lose focus while working at your computer. The system captures webcam frames from your browser, analyzes head pose with MediaPipe FaceMesh, and presents focus statistics on a live dashboard — helping you measure study sessions, set goals, and notice patterns in your own behavior.

[Hanxi Li](https://github.com/hanxili435)<br>
[Michael Miao](https://github.com/miaom-Konkon)<br>
[Grace Johnson](https://github.com/grace350)<br>
[Marcus Song](https://github.com/Marclous)<br>
[Rohan Ahmad](https://github.com/ra4059)<br>

## Steps To Run

Follow these steps to start the application:

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) (v2+)
- A webcam-equipped device with a modern browser (Chrome, Firefox, Edge)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/swe-students-spring2026/4-containers-ocean_pulse-2.git
cd 4-containers-ocean_pulse-2
```

### 2. Build and start all services

```bash
docker compose up --build
```

This starts three containers:

- `mongodb` on port **27017**
- `web-app` on port **5000**
- `machine-learning-client` (runs in background, polling for images)

### 3. Open the web app

Navigate to [http://localhost:5000](http://localhost:5000) in your browser and **allow camera access** when prompted.

### 4. Run a focus session

Click **Start Session** on the dashboard. The browser will begin capturing webcam frames every 10 seconds and sending them to the server. The machine learning client picks up the images, analyzes them, and writes results to MongoDB. The dashboard auto-refreshes to show your focus statistics.

### 5. Run the ML client manually (optional)

If the ML client container has exited, you can re-run it:

```bash
docker compose run --rm machine-learning-client
```

### 6. Stop all services

```bash
docker compose down
```

To also remove the persisted database volume:

```bash
docker compose down -v
```

## Environment Variables

All environment variables are pre-configured in `docker-compose.yml`. No `.env` file is required.

| Variable | Default | Used By | Description |
|---|---|---|---|
| `MONGO_URI` | `mongodb://mongodb:27017` | web-app, ml-client | MongoDB connection string. Inside Docker Compose the hostname `mongodb` resolves to the database container. |
| `MONGO_DB` | `ocean_pulse` | web-app, ml-client | Name of the MongoDB database where results are stored. |

If you need to override these (e.g. connecting to an external MongoDB), you can either edit `docker-compose.yml` or create a `.env` file in the project root:

```env
MONGO_URI=mongodb://your-host:27017
MONGO_DB=ocean_pulse
```

## Continuous Integration

GitHub Actions workflows run automatically on every push and pull request:

- **Lint** (`lint.yml`) — runs `pylint` and `black --check` on both subsystems (web-app and machine-learning-client)
- **Event Logger** (`event-logger.yml`) — logs GitHub events for course tracking
