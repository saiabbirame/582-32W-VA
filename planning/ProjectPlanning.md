# Project Planning

## Project Name
**NextStop** *(working title - subject to change)*

---
## Project Idea
NextStop is a web application that helps users discover places in Montreal and organize them into personalized daily itineraries.

---
## Project Vision Statement
To provide a simple and user-friendly platform that makes planning a day in Montreal easier by combining place discovery and itinerary planning in one applicaiton.

---
## Simulated Client Quote
*"Our organization wants a web application that helps people discover restaurants, cafés, attractions, entertainment venues and other places of interest in Montreal. We want users to be able to organize these places into personalized daily itineraries within a single application. Our goal is to simplify the planning process by providing an easy-to-use platform for both visitors and local residents."*

---
## Client Quote Interpretation

### Client Need
The client wants a centralized platform where users can discover places in Montreal and organize them into personalized itineraries without relying on multiple applications.

### Proposed Solution
Develop NextStop, a web application that allows users to browse places, filter results by category and create personalized itineraries in one place.

---
## Problem
People planning a day in a city often have to use multiple apps to discover restaurants, cafés, attractions, entertainment venues and other places of interest. After finding places they like, they usually need another app to organize and write down their itinerary. Switching between different apps makes the planning process more time-consuming and less convenient.

---
## Solution
NextStop lets users browse a curated list of places, filter the results based on their interests and build personalized itineraries by adding selected places, organizing them into a daily schedule and keeping everything in one application.

---
## Target Users
- Tourists visiting Montreal
- New residents exploring Montreal
- Local residents planning a day out

---
## User Roles

### Guest
A guest can browse places, filter the results and view place details without creating an account.

### Registered User
A registered user can browse places, create personal itineraries, add places to an itinerary, organize places by visit time, add notes and edit or delete their own itineraries.

### Administrator
An administrator can add, edit and delete the places available in the application.

---
## Project Scope
The application will allow users to browse places, filter them by category and create, edit and manage their own itineraries after logging in. An administrator will manage the list of places available in the application.

To keep the project achievable within the five-week timeline, advanced features such as maps, reviews, ratings, itinerary sharing and support for multiple cities will not be included in the initial version.

---
## Must-Have Features

### User Authentication
- Users can register for an account.
- Users can log in.
- Users can log out.

### Place Discovery
- Browse a list of places.
- View detailed information about each place.
- Filter places by category.

### Itinerary Management
- Create a new itinerary.
- Add places to an itinerary.
- Assign a visit time to each place.
- Add personal notes.
- Edit an existing itinerary.
- Delete an itinerary.

### Place Management
- Add new places.
- Edit existing places.
- Delete places.

---
## Optional Features
- Search for places by name.
- Filter places by neighbourhood.
- Filter places by price range.
- Mark places as favourites.
- Reorder places within an itinerary.
- Share an itinerary with others.
- Display places on a map.
- Add ratings or reviews.
- Support additional cities.

---
## Frontend Track
Track A - Flask and JavaScript

---
## Route or Endpoint List

| Method | Route | Purpose|
|--------|-------|--------|
| GET | `/` | Display the home page. |
| GET | `/places` | Display all available places. |
| GET | `/places/<int:id>` | Display information about a selected place. |
| GET | `/itineraries` | Display the user's itineraries. |
| GET | `/account` | Display the user's account information. |

### User Authentication
| Method | Route | Purpose|
|--------|-------|--------|
| GET | `/register` | Display the registration page. |
| POST | `/register` | Register a new user. |
| GET | `/login` | Display the login page. |
| POST | `/login` | Log in a user. |
| POST | `/logout` | Log out the current user. |

### Itinerary Management
| Method | Route | Purpose|
|--------|-------|--------|
| GET | `/itineraries/new` | Display the create itinerary page. |
| POST | `/itineraries` | Create a new itinerary. |
| GET | `/itineraries/<int:id>` | Display a selected itinerary. |
| GET | `/itineraries/<int:id>/edit` | Display the edit itinerary page. |
| POST | `/itineraries/<int:id>/edit` | Update an existing itinerary. |
| POST | `/itineraries/<int:id>/places` | Add a place to an itinerary. |
| POST | `/itineraries/<int:id>/places/<int:place_id>/delete` | Remove a place from an itinerary. |
| POST | `/itineraries/<int:id>/delete` | Delete an itinerary. |

### Place Management
| Method | Route | Purpose|
|--------|-------|--------|
| GET | `/admin/places` | Display all places for administration. |
| GET | `/admin/places/new` | Display the add place page. |
| POST | `/admin/places` | Add a new place. |
| GET | `/admin/places/<int:id>/edit` | Display the edit place page. |
| POST | `/admin/places/<int:id>/edit` | Update an existing place. |
| POST | `/admin/places/<int:id>/delete` | Delete a place. |

---
## Project Structure
The project will include a `code/` folder in the root directory to store the Flask application and all source code. I expect this folder to contain an `app.py` file, the standard Flask `templates/` and `static/` folders, and a `routes/`folder to organize the application's routes.
