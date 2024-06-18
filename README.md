# A User-Adaptive Educational Device Powered by Generative AI

## Overview

This repository contains the source code for the project "A User-Adaptive Educational Device Powered by Generative AI". The project is structured to provide a backend server and a frontend graphical user interface (GUI).

## Repository Structure

- **App/Backend/main.py**: The main backend application file.
- **App/GUI**: The frontend application directory.

## Installation

### Backend

1. Navigate to the `App/Backend` directory:
    ```bash
    cd App/Backend
    ```
2. Install the required dependencies using `pip`:
    ```bash
    pip install -r requirements.txt
    ```
3. Download the necessary spaCy models:
    ```bash
    python -m spacy download en_core_web_sm
    python -m spacy download en_core_web_md
    ```
4. Run the backend server:
    ```bash
    python main.py
    ```

### Frontend

1. Navigate to the `App/GUI` directory:
    ```bash
    cd App/GUI
    ```
2. Install the required dependencies using `npm`:
    ```bash
    npm install
    ```
3. Start the frontend application:
    ```bash
    npm start
    ```

## Usage

1. Ensure the backend server is running beforehand by following the backend setup instructions.
2. Start the frontend application by following the frontend setup instructions.

## Notes

- Ensure you have Python 3 and Node.js installed on your system before running the installation commands.
