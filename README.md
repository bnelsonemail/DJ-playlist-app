# Playlists Manager

Playlists Manager is a web application built with Flask that allows users to manage playlists and songs easily. Users can create playlists, add songs, and organize their favorite tracks seamlessly. 

## Table of Contents
- [Playlists Manager](#playlists-manager)
  - [Table of Contents](#table-of-contents)
  - [Purpose](#purpose)
  - [Features](#features)
  - [Tech Stack](#tech-stack)
  - [Installation](#installation)
  - [Database Migration](#database-migration)
  - [Usage](#usage)
  - [Testing](#testing)
  - [License](#license)

## Purpose

The purpose of the Playlists Manager app is to provide users with an intuitive platform to manage and organize their music playlists. Whether you're curating songs for a party or just organizing your favorite tracks, this app simplifies the process with a user-friendly interface and powerful backend functionality.

---

## Features

- **User Authentication**:
  - Register and log in with secure password storage.
  - Personalized playlists for each user.

- **Playlist Management**:
  - Create, edit, and delete playlists.
  - Add or remove songs from playlists.

- **Song Management**:
  - Add new songs to the database.
  - View a list of all available songs.
  - Delete songs from the database.

- **Responsive Design**:
  - Optimized for desktop and mobile devices with Bootstrap.

- **SEO & Social Media Friendly**:
  - Includes meta tags for search engines and social media platforms.

---

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, Bootstrap, Jinja2
- **Database**: PostgreSQL
- **Authentication**: Flask-Login, Flask-WTF (for CSRF protection)

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/playlists-manager.git
    cd playlists-manager
    ```

2. Set up a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate     # For Windows
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environmental variables:
   - Create a `.env` file in the root directory:

    ```plaintext
    SECRET_KEY=your-secret-key
    DATABASE_URL=your-database-url
    ```

5. Initialize the database (details in the next section).

6. Run the application:

    ```bash
    flask run
    ```

7. Access the app at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Database Migration

To set up or update the database schema, follow these steps:

1. **Generate Migration Scripts**:
   Run this command to generate a new migration script based on your models:

    ```bash
    flask db migrate -m "Initial migration"
    ```

2. **Apply Migrations**:
   Apply the generated migrations to your database:

    ```bash
    flask db upgrade
    ```

3. **Rollback Migrations** (if needed):
   Rollback to a previous state if something goes wrong:

    ```bash
    flask db downgrade
    ```

4. **Verify Schema**:
   Check your database to ensure all tables and relationships are created correctly.

---

## Usage
- Register a new account or log in with an existing user.
- Create playlists and add songs.
- View, edit, or delete playlists and songs.
- Enjoy a streamlined playlist management experience.

---

## Testing
Here are the details for a test user you can use to log in and explore the app:

| **Username** | **Email**         | **Password**   |
|--------------|-------------------|----------------|
| DogLover     | dog@example.com   | password456    |

**To create additional test users**:
- Register new users directly from the `/register` page.

---

## License
This project is licensed under the MIT License.
