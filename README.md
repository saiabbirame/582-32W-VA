# NextStop
NextStop is a dynamic web application that helps users discover places to visit in Montreal and organize them into personalized daily itineraries.

## Client Need
The client needs a simple platform that allows visitors and residents of Montreal to discover interesting places around the city and organize their plans in one place. Instead of searching for places separately and keeping track of plans elsewhere, NextStop allows users to browse destinations and add them directly to personalized itineraries.

## Target User
NextStop is designed for people who want to explore Montreal and plan a day in the city, including tourists, visitors and local residents looking for places to visit.

## Features
- Browse places to visit in Montreal
- Search places by name
- Filter places by category
- View detailed information about each place
- View place locations on an interactive map
- Register and log in to a user account
- Create, edit and delete personalized itineraries
- Add places to an itinerary with a visit time and optional note
- Edit and remove places from an itinerary
- View all itinerary locations together on an interactive map
- Administrator tools for adding, editing and deleting places
- Responsive layouts for desktop and mobile devices
- Success and error feedback through flash messages

## Technologies
- Python 
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite
- Jinja
- HTML
- CSS
- JavaScript
- Leaflet
- OpenStreetMap
- python-dotenv
- Git
- GitHub

## Project Structure
The repository is organized into separate folders for the different parts of the project.

- `journal/` - daily development journal
- `planning/` - project planning and documentation
- `design/` - design files and related assets
- `code/` - Flask web application and source code
- `README.md` - project overview and setup instructions

Inside the `code/` folder:
- `app.py` - Flask routes, configuration and application logic
- `models.py` - SQLAlchemy database models
- `templates/` - Jinja HTML templates
- `static/css/` - application styles
- `static/js/` - JavaScript functionality
- `static/images/` - images used throughout the website
- `requirements.txt` - Python dependencies

## Installation
1. Clone the repository.

2. Navigate to the application folder:
```bash
cd code
```

3. Create a virtual environment:
```bash
python3 -m venv venv
```

4. Activate the virtual environment:
```bash
source venv/bin/activate
```

5. Install the required dependencies:
```bash
pip install -r requirements.txt
```

If `pip` is not recognized, use:
```bash
python3 -m pip install -r requirements.txt
```

6. Verify Flask is installed:
```bash
flask --version
```

## Environment Variables
The application uses an environment variable for the Flask secret key.

Create a `.env` file inside the `code/` folder:
```env
SECRET_KEY=your_secret_key
```

The `.env` file is excluded from Git through `.gitignore` and should not be committed to the repository.

## Database Setup
NextStop uses SQLite with Flask-SQLAlchemy.

The application is configured to use:
```text
sqlite:///nextstop.db
```

The required database tables are automatically created when the application starts using `db.create_all()`.

The SQLite database is stored locally in Flask's `instance/` folder and is excluded from Git.

A new database will initially be empty, so place data and user accounts must be created manually when setting up a fresh copy of the project.

## Running the Application
From inside the `code/` folder with the virtual environment activated, run:
```bash
flask --app app run --debug
```

Then open the local address displayed in the terminal in a web browser.

## Testing
The application was manually tested across its main user workflows.

Testing included:

- Guest navigation
- User registration and login
- Invalid login and form validation
- Place browsing, searching and filtering
- Place details and interactive map display
- Creating, editing and deleting itineraries
- Adding places to itineraries
- Editing visit times and notes
- Removing places from itineraries
- Itinerary map markers and popups
- Administrator place management
- Admin authorization
- Success and error flash messages
- Responsive layouts

## Known Limitations
- NextStop currently focuses only on places located in Montreal.
- Place information is entered and managed manually by an administrator.
- A fresh database does not automatically include demo places or test users.
- The itinerary map displays the locations in an itinerary but does not calculate or display a route between them.

## Documentation
- Project Planning (`planning/ProjectPlanning.md`)
- Trello Board: https://trello.com/b/U9FnhejE/nextstop-web-project-1
- Journal (`journal/`)

## External Resources
- Leaflet Documentation: https://leafletjs.com/index.html
- OpenStreetMap: https://www.openstreetmap.org/#map=3/66.16/-121.11 

## Project Status
NextStop is complete for Web Project 1.