# Roro Airlines Backend

## Description
This is the backend for the Roro Airlines Management System. It provides APIs for managing airlines, flights, passengers, bookings, and seat reservations.

## Technologies Used
- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Render (for deployment)

## Setup Instructions

### Prerequisites
- Python installed on your system
- PostgreSQL database setup

### Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:RomeOtieno501/roro-airlines-full-stack.git
   cd roro-airlines-full-stack
   ```
2. Create and activate a virtual environment:
   ```bash
   pipenv install && pipenv shell
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
1. Apply database migrations:
   ```bash
   flask db upgrade
   ```
2. (Optional) Seed the database with initial data:
   ```bash
   python seed.py
   ```
3. Start the Flask application:
   ```bash
   flask run
   ```

### API Endpoints
| Method | Endpoint         | Description |
|--------|-----------------|-------------|
| GET    | `/flights`      | Get all flights |
| POST   | `/flights`      | Create a new flight |
| PATCH  | `/flights/<id>` | Update flight details |
| DELETE | `/flights/<id>` | Delete a flight |
| GET    | `/passengers`   | Get all passengers |
| ...    | ...             | More API endpoints |

### Deployment
The backend is deployed on Render: [Backend Deployment Link](https://roro-airlines-full-stack-1.onrender.com)

### Frontend Repository
[Frontend GitHub Repository](https://github.com/RomeOtieno501/roro-airlines-frontend.git)

## License
This project is licensed under the MIT License.
