
# Student Engagement Analysis System for Online Learning

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-v2.0.0-black)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![Svelte](https://img.shields.io/badge/Svelte-3-red)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

This repository contains the source code for the **Student Engagement Analysis System**, developed as part of an undergraduate thesis. The system is designed to analyze student engagement in real-time during online learning sessions by detecting emotional and behavioral cues from students using their webcam.

This project was published in: [this article (in Indonesian)](https://jurnalelektro.petra.ac.id/index.php/elk/article/view/25888/20824)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [System Architecture](#system-architecture)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This system provides teachers with insights into the engagement levels of students during online learning sessions by analyzing both **emotional** and **behavioral engagement**. It uses image processing and deep learning techniques to detect student emotions and presence during class, giving teachers valuable data to improve the learning experience.

---

## Features

- **Emotion Detection**: Classifies student emotions (happiness, sadness, anger, fear, surprise, disgust, and neutral) using their facial expressions in real-time.
- **Behavioral Engagement Monitoring**: Detects student presence during online learning sessions via face detection.
- **Real-time Data Processing**: The system processes images captured through a webcam and sends the engagement data to a server for teacher evaluation.
- **Teacher Dashboard**: A web interface where teachers can view student engagement statistics and attendance data.

---

## Technologies Used

- **Deep Learning (CNN)**: For emotion classification using the FER-2013 dataset.
- **Python**: The primary programming language used for backend logic and data processing.
  - **Flask**: API framework to handle requests between the desktop application, web server, and the database.
  - **TensorFlow**: Deep learning framework for emotion classification.
  - **OpenCV**: For image and video capture and processing.
  - **PyQt**: For building the desktop application GUI.
- **Web Technologies**:
  - **Svelte**: JavaScript framework used for building the web dashboard interface.
  - **SQLAlchemy**: Database toolkit for handling database queries and interaction with MySQL.

---

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)
- Virtual environment (optional but recommended)
- MySQL or any compatible SQL database server

### Clone the repository

```bash
git clone https://github.com/your-username/student-engagement-analysis-system.git
cd student-engagement-analysis-system
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Setup the database

1. Ensure MySQL (or any SQL database) is running.
2. Create a database for the project.
3. Update the database configuration in the `config.py` file.

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'
```

4. Run the migration to set up the database schema:

```bash
flask db upgrade
```

---

## Usage

### Running the desktop application

1. Start the Flask server:

```bash
flask run
```

2. Run the desktop application:

```bash
python desktop_app/main.py
```

### Accessing the teacher dashboard

1. Open your browser and navigate to `http://localhost:5000/` to access the teacher dashboard.

2. Log in as a teacher to view student engagement data.

---

## System Architecture

The system is composed of two main components:

1. **Desktop Application**:
   - Built using PyQt and OpenCV to capture images from the webcam.
   - Detects student presence using face detection.
   - Classifies student emotions using a CNN model.

2. **Teacher Dashboard**:
   - A web application built using Svelte for the frontend.
   - Flask API manages requests and communicates with the database.
   - Teachers can view engagement data on charts and tables.

```plaintext
+-------------+    +-------------+    +-------------+
| Desktop App |<-->| Flask API   |<-->| MySQL DB    |
+-------------+    +-------------+    +-------------+
       |                   ^                   |
       v                   |                   v
+-------------+    +-------------+    +-------------+
| OpenCV (FD) |    | TensorFlow  |    | Web Client  |
+-------------+    +-------------+    +-------------+
```

---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
