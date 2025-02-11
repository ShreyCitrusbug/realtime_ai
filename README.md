# Realtime AI POC

This project is a Proof of Concept (POC) for a Real-Time AI application built with Python, FastAPI, OpenAI's Realtime API, and PostgreSQL. The application allows live interaction through AI and stores the data in a PostgreSQL database.

## Table of Contents
- [Installation](#installation)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Technologies](#technologies)

## Installation

Follow these steps to set up the project locally.

## Prerequisites

Ensure you have the following installed on your machine:
- Python (version 3.10.11)
- PostgreSQL

### Steps to Install

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/realtime-ai-poc.git
   cd realtime-ai-poc

2. Create a virtual environment:
   ```bash
    python3 -m venv venv
    source venv/bin/activate 

3. Install the required dependencies::
   ```bash
    pip install -r requirements.txt

4. Set up PostgreSQL:
    - Create a PostgreSQL database and update the database connection string in the .env file.

5. Set up your OpenAI Realtime API credentials:
    - Obtain the API key from OpenAI and store it in the .env file as OPENAI_API_KEY.

6. Run database migrations (if applicable): 
    ```bash
    alembic revision --autogenerate -m "Your Message"
    alembic upgrade head

## Usage

### Running the API Server
To start the FastAPI server, run:
```bash
uvicorn main:app --reload
```
This will start the server in development mode with live reloading enabled.

### Accessing the API
- Open your browser and go to http://localhost:8000/docs to interact with the API and view available endpoints.

### Environment Variables
Create a .env file in the root directory and refer ```env.sample``` file.

## Technologies
This project uses the following technologies:

 - Python 3.10.11: The programming language.
 - FastAPI: Web framework for building the API.
 - OpenAI Realtime API: For live AI interaction.
 - PostgreSQL: Database for storing interactions and data.
 - SQLAlchemy & Alembic: For ORM and database migrations.