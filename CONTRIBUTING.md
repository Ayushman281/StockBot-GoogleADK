# Contributing to StockBot

Thank you for your interest in contributing to StockBot! This document provides guidelines and instructions to help you get started.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## Development Setup

### Prerequisites

- Python 3.10+
- Node.js 16+
- npm or yarn

### Setting Up the Development Environment

1. Fork and clone the repository:
   ```
   git clone https://github.com/yourusername/StockBot.git
   cd StockBot
   ```

2. Set up the backend:
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```
   cd ../frontend
   npm install
   ```

4. Create `.env` files:
   - Backend: Copy `.env.example` to `.env` and add your API keys
   - Frontend: Copy `.env.example` to `.env` with appropriate values

## Project Structure

- `frontend/`: React application using Vite
- `backend/`: FastAPI server with multi-agent architecture
  - `agents/`: Specialized agents for different tasks
  - `api/`: API clients for financial data sources
  - `utils/`: Helper functions and utilities

## Making Changes

1. Create a new branch for your feature:
   ```
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test them:
   - Backend: Run with `python main.py`
   - Frontend: Run with `npm run dev`

3. Commit your changes with clear messages:
   ```
   git commit -m "Add feature: description of changes"
   ```

## Submitting a Pull Request

1. Push your changes to your fork:
   ```
   git push origin feature/your-feature-name
   ```

2. Open a pull request against the main repository
3. Provide a clear description of the changes and any relevant issue numbers
4. Wait for maintainers to review your PR

## Coding Standards

### Backend (Python)

- Follow PEP 8 style guide
- Write docstrings for all functions and classes
- Include type hints where appropriate
- Write unit tests for new functionality

### Frontend (JavaScript/React)

- Follow the project's ESLint configuration
- Use functional components and hooks
- Keep components small and focused
- Use descriptive variable and function names

## Reporting Bugs

Please report bugs by opening an issue with:
- A clear description of the bug
- Steps to reproduce
- Expected vs. actual behavior
- Screenshots if applicable
- Environment details (OS, browser, etc.)

## Feature Requests

Feature requests are welcome! Please include:
- A clear description of the feature
- Any relevant use cases or examples
- How the feature would benefit the project

## Questions?

Feel free to open an issue for any questions about contributing.

Thank you for helping improve StockBot!
