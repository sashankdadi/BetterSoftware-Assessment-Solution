# app.py
from flask import Flask
from flask_cors import CORS
# Note: db is now imported from models, but we keep SQLAlchemy import here for clarity if needed
from flask_sqlalchemy import SQLAlchemy 
from comments_api import comments_bp 
from models import db, Task, Comment 

def create_app():
    # 1. Create the Flask app
    app = Flask(__name__)

    # 2. Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. Initialize extensions
    db.init_app(app)
    # Enable CORS for the API endpoints
    CORS(app, resources={r"/api/*": {"origins": "*"}}) 

    # 4. Register Blueprints
    app.register_blueprint(comments_bp)

    # 5. Add a default home route
    @app.route('/')
    def home():
        return {"message": "Flask API is running! Access the API at /api/tasks"}

    # 6. Create database tables and seed example data
    with app.app_context():
        db.create_all()

        # FIX: Replace Task.query.get(1) with db.session.get(Task, 1) to remove LegacyAPIWarning
        if db.session.get(Task, 1) is None:
            sample_task = Task(id=1, title='Initial Test Task (ID 1)')
            db.session.add(sample_task)
            db.session.commit()

        print("Registered routes:")
        print(app.url_map)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)