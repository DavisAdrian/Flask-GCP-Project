# Flask Task Manager

A simple task management web application built with Flask and SQLite, designed for deployment on Google Cloud Platform App Engine.

## Features

- Create, read, update, and delete tasks
- Mark tasks as completed
- View task statistics (total, completed, pending)
- Clean and responsive user interface
- SQLite database for data persistence
- Ready for GCP App Engine deployment

## Tech Stack

- **Backend**: Flask (Python 3.12)
- **Database**: SQLite3
- **Server**: Gunicorn
- **Deployment**: Google Cloud Platform App Engine
- **Frontend**: HTML templates with Jinja2

## Project Structure

```
flask-gcp-project/
├── app.py              # Main application file
├── app.yaml            # GCP App Engine configuration
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── index.html     # Main task list page
│   └── stats.html     # Statistics page
└── .gitignore         # Git ignore rules
```

## Local Development

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/DavisAdrian/flask-gcp-project.git
cd flask-gcp-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:8080
```

## Deployment to Google Cloud Platform

### Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- GCP project with billing enabled
- App Engine initialized in your project

### Deploy Steps

1. Authenticate with Google Cloud:
```bash
gcloud auth login
```

2. Set your project ID:
```bash
gcloud config set project YOUR_PROJECT_ID
```

3. Deploy to App Engine:
```bash
gcloud app deploy
```

4. View your deployed application:
```bash
gcloud app browse
```

## API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Display all tasks |
| `/add` | POST | Add a new task |
| `/complete/<id>` | GET | Mark task as completed |
| `/delete/<id>` | GET | Delete a task |
| `/stats` | GET | View task statistics |

## Database Schema

**tasks** table:
- `id` (INTEGER, PRIMARY KEY): Unique task identifier
- `title` (TEXT, NOT NULL): Task title
- `description` (TEXT): Task description
- `completed` (BOOLEAN): Completion status
- `created_at` (TIMESTAMP): Creation timestamp

## Configuration

The application uses the following configuration:
- **Runtime**: Python 3.12
- **Instance Class**: F1 (smallest App Engine instance)
- **Database Location**: `/tmp/tasks.db` (for App Engine compatibility)
- **Port**: 8080 (configurable via PORT environment variable)

## Notes

- The database is stored in `/tmp/` directory to work with App Engine's read-only filesystem
- In production, consider using Cloud SQL for persistent data storage
- Change the `secret_key` in `app.py` before deploying to production

## License

This project is open source and available for educational purposes.
