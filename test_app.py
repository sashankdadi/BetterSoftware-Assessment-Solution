# test_app.py
import pytest
from app import create_app, db
from models import Task, Comment
import json

# ------------------- FIXTURES -------------------

@pytest.fixture
def test_app():
    """Setup and teardown test Flask app with in-memory DB."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()   # Create tables for each test
        yield app
        db.session.remove()
        db.drop_all()     # Clean up after each test

@pytest.fixture
def client(test_app):
    """A test client for making requests."""
    return test_app.test_client()

@pytest.fixture
def sample_task(test_app):
    """Creates and commits a sample task to the DB for testing."""
    with test_app.app_context():
        task = Task(title="Sample Task to Modify")
        db.session.add(task)
        db.session.commit()
        
        # FIX: Read the ID while the object is still attached to the session
        task_id = task.id
        
        # Ensure the task is detached from the session before returning the ID
        db.session.expunge(task)
        
        return task_id

@pytest.fixture
def sample_comment(test_app, sample_task):
    """Creates and commits a sample comment linked to sample_task."""
    with test_app.app_context():
        comment = Comment(task_id=sample_task, content="Sample Comment to Delete")
        db.session.add(comment)
        db.session.commit()
        
        # FIX: Read the ID while the object is still attached to the session
        comment_id = comment.id
        
        db.session.expunge(comment)
        
        return comment_id

# ------------------- TESTS -------------------

# ==================== TASK TESTS ====================

def test_create_task(client):
    response = client.post("/api/tasks", json={"title": "New Task from Test"})
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data["title"] == "New Task from Test"

def test_get_tasks(client, sample_task):
    response = client.get("/api/tasks")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert isinstance(data, list)
    assert any(task["id"] == sample_task for task in data)

def test_update_task(client, sample_task):
    """Tests the PUT/PATCH /api/tasks/<id> route."""
    new_title = "Updated Task Title"
    response = client.put(f"/api/tasks/{sample_task}", json={"title": new_title})
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data["message"] == "Task updated"

    # Verify the update by fetching the task list
    get_response = client.get("/api/tasks")
    tasks = json.loads(get_response.data)
    updated_task = next(t for t in tasks if t["id"] == sample_task)
    assert updated_task["title"] == new_title

def test_delete_task(client, sample_task):
    """Tests the DELETE /api/tasks/<id> route."""
    response = client.delete(f"/api/tasks/{sample_task}")
    
    # Check for 204 No Content status code
    assert response.status_code == 204 
    
    # Verify deletion by trying to fetch the task list
    get_response = client.get("/api/tasks")
    tasks = json.loads(get_response.data)
    assert not any(t["id"] == sample_task for t in tasks)

# ==================== COMMENT TESTS ====================

def test_add_comment(client, sample_task):
    response = client.post(f"/api/tasks/{sample_task}/comments", json={"content": "A comment from test"})
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data["content"] == "A comment from test"
    assert "created_at" in data

def test_get_comments(client, sample_comment, sample_task):
    response = client.get(f"/api/tasks/{sample_task}/comments")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert isinstance(data, list)
    assert any(comment["id"] == sample_comment for comment in data)

def test_update_comment(client, sample_comment):
    """Tests the PUT/PATCH /api/comments/<id> route."""
    new_content = "Revised Comment Content"
    response = client.put(f"/api/comments/{sample_comment}", json={"content": new_content})
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["message"] == "Comment updated"
    assert data["content"] == new_content

def test_delete_comment(client, sample_comment, sample_task):
    """Tests the DELETE /api/comments/<id> route."""
    response = client.delete(f"/api/comments/{sample_comment}")
    
    # Check for 204 No Content status code
    assert response.status_code == 204 

    # Verify deletion by fetching comments for the task
    get_response = client.get(f"/api/tasks/{sample_task}/comments")
    comments = json.loads(get_response.data)
    assert not any(c["id"] == sample_comment for c in comments)