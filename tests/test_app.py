import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    from src.app import activities
    initial_state = {
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
    
    # Clear and reset
    activities.clear()
    activities.update(initial_state)
    yield
    
    # Cleanup after test
    activities.clear()
    activities.update(initial_state)


class TestActivitiesEndpoint:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Basketball" in data
    
    def test_get_activities_has_required_fields(self, client, reset_activities):
        """Test that activities have required fields"""
        response = client.get("/activities")
        data = response.json()
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "location" in activity
        assert "max_participants" in activity
        assert "participants" in activity
    
    def test_get_activities_participants_format(self, client, reset_activities):
        """Test that participants are returned as a list"""
        response = client.get("/activities")
        data = response.json()
        activity = data["Basketball"]
        assert isinstance(activity["participants"], list)
        assert "james@mergington.edu" in activity["participants"]


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_for_activity_success(self, client, reset_activities):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Basketball/signup?email=newstudent@mergington.edu",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
    
    def test_signup_adds_participant_to_activity(self, client, reset_activities):
        """Test that signup actually adds the participant"""
        email = "newstudent@mergington.edu"
        client.post(f"/activities/Chess Club/signup?email={email}")
        
        response = client.get("/activities")
        data = response.json()
        assert email in data["Chess Club"]["participants"]
    
    def test_signup_duplicate_email_rejected(self, client, reset_activities):
        """Test that duplicate signup is rejected"""
        response = client.post(
            "/activities/Basketball/signup?email=james@mergington.edu"
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]
    
    def test_signup_to_nonexistent_activity(self, client, reset_activities):
        """Test signup to an activity that doesn't exist"""
        response = client.post(
            "/activities/NonexistentActivity/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]


class TestDeleteParticipantEndpoint:
    """Tests for DELETE /activities/{activity_name}/participant endpoint"""
    
    def test_delete_participant_success(self, client, reset_activities):
        """Test successful removal of a participant"""
        response = client.delete(
            "/activities/Basketball/participant?email=james@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
    
    def test_delete_removes_participant_from_activity(self, client, reset_activities):
        """Test that delete actually removes the participant"""
        client.delete("/activities/Basketball/participant?email=james@mergington.edu")
        
        response = client.get("/activities")
        data = response.json()
        assert "james@mergington.edu" not in data["Basketball"]["participants"]
    
    def test_delete_nonexistent_participant(self, client, reset_activities):
        """Test deletion of a participant who hasn't signed up"""
        response = client.delete(
            "/activities/Basketball/participant?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
        data = response.json()
        assert "not found" in data["detail"].lower() or "not signed up" in data["detail"].lower()
    
    def test_delete_from_nonexistent_activity(self, client, reset_activities):
        """Test deletion from an activity that doesn't exist"""
        response = client.delete(
            "/activities/NonexistentActivity/participant?email=student@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]


class TestRootEndpoint:
    """Tests for GET / endpoint"""
    
    def test_root_redirects_to_static_index(self, client):
        """Test that root endpoint redirects to static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]
