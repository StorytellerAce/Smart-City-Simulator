# Smart City Simulator

> A turn-based city-building game developed as a Final Year Project, featuring AI-assisted gameplay through machine learning and Google Gemini integration.

---

## Overview

Smart City Simulator is a grid-based city-building game where players strategically develop a city by placing residential, supply, factory, and service buildings.

Unlike traditional city builders, the game incorporates a Python-based AI backend that analyzes player behaviour, predicts future city performance, and generates personalized in-game advice using Google Gemini.

The project demonstrates the integration of game development, backend services, machine learning, and AI into a single gameplay experience.

---

## Features

### Gameplay
- Grid-based building placement
- Road placement system
- Turn-based gameplay
- Population and satisfaction management
- Resource management

### AI Assistant
- AI-generated gameplay advice
- Dynamic city reactions
- Personalized objectives
- Google Gemini integration

### Machine Learning
- Player behaviour clustering using K-Means
- Population prediction using Linear Regression
- Gameplay data collection and analysis

### Backend
- FastAPI server
- REST API communication
- WebSocket support
- Session management

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Game Engine | Unity |
| Language | C# |
| Backend | FastAPI |
| Machine Learning | Python, Scikit-learn |
| AI | Google Gemini API |
| Database | PostgreSQL |
| Communication | REST API, WebSocket |

---

## Project Structure

```

```

---

## System Architecture

```
                 +----------------+
                 | Unity Client   |
                 +----------------+
                         |
            REST API / WebSocket
                         |
                         v
                +----------------+
                | FastAPI Server |
                +----------------+
                 |            |
                 |            |
         Machine Learning     |
                 |            |
                 v            v
          Scikit-learn    Google Gemini
                 |
                 v
            PostgreSQL
```

---

## Gameplay Flow

<img width="569" height="744" alt="image" src="https://github.com/user-attachments/assets/a2fc1ce5-a88a-42a1-9dd2-0f973766b797" />

---

## Machine Learning Pipeline

The game continuously records player actions and city statistics during gameplay.

At predefined turns, gameplay data is processed through a machine learning pipeline:

1. Extract gameplay features.
2. Classify player strategy using K-Means clustering.
3. Predict future population using Linear Regression.
4. Generate contextual prompts.
5. Request gameplay advice from Google Gemini.
6. Display personalized feedback to the player.

---

## How to Launch Server

cd GamewebAPI
python -m uvicorn app.main:app --reload

--- 

## Screenshots

### Main Menu

*Coming soon*

### Gameplay

*Coming soon*

### AI Assistant

*Coming soon*

---

## Future Improvements

- NPC simulation
- Traffic system
- Smarter city events
- More machine learning models
- Save/load improvements
- Enhanced AI conversations

---

## Learning Outcomes

This project provided practical experience in:

- Unity game development
- FastAPI backend development
- Machine learning integration
- AI prompt engineering
- REST API design
- WebSocket communication
- Software architecture
- Data-driven game design

---

## License

This project was developed as a Final Year Project for educational and portfolio purposes.
