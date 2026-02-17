"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "location": "Room 204",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Basketball": {
        "description": "Team sport focusing on basketball skills and competitive play",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "location": "Gymnasium",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Outdoor soccer league and training sessions",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "location": "Soccer Field",
        "max_participants": 20,
        "participants": ["lucas@mergington.edu", "noah@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and mixed media creative expression",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "location": "Room 101",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater performance, acting techniques, and stage design",
        "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
        "location": "Auditorium",
        "max_participants": 25,
        "participants": ["emily@mergington.edu", "grace@mergington.edu"]
    },
    "Debate Team": {
        "description": "Competitive debate, public speaking, and argumentation",
        "schedule": "Tuesdays, Wednesdays, Fridays, 3:30 PM - 4:30 PM",
        "location": "Room 305",
        "max_participants": 16,
        "participants": ["alexander@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments, research projects, and STEM exploration",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "location": "Lab Room",
        "max_participants": 20,
        "participants": ["aiden@mergington.edu", "mia@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities




@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

# Validate student is not already signed up
    if email in activity["participants"]:        
        raise HTTPException(status_code=400, detail="Student already signed up")

  
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
