![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![Event-logger](https://github.com/swe-students-spring2026/4-containers-ocean_pulse-2/actions/workflows/event-logger.yml/badge.svg)

# Containerized App Exercise

Our project is a study focus tracker. Do you have a hard time concentrating when nobody is around to keep you accountable? Have you ever felt like you've been working for hours and still havent gotten much done? Our project uses a machine learning client to record when the user has lost focus while working on their computer. With our project you can measure your study session, which can help with setting goals and noticing patterns in your own behavior.

## Ocean Pulse Team

[Hanxi Li](https://github.com/hanxili435)<br>
[Michael Miao](https://github.com/miaom-Konkon)<br>
[Grace Johnson](https://github.com/grace350)<br>
[Marcus Song](https://github.com/Marclous)<br>
[Rohan Ahmad](https://github.com/ra4059)<br>

## Steps To Run

Follow these steps to start the application:

### 1. build and start

```
docker compose up --build
```

### 2. open the web app

Open http://localhost:5000/ and allow camera access.

### 3. run the machine learning client

```
docker compose run --rm machine-learning-client
```

Refresh the page to see results!
