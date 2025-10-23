# comments_api.py

from flask import Blueprint, request, jsonify
import models 

# Correct way to access attributes directly from the imported module
db = models.db
Comment = models.Comment 
Task = models.Task

# Blueprint with API prefix
# ... (rest of the file)

# Blueprint with API prefix
comments_bp = Blueprint('comments', __name__, url_prefix='/api')

# ==================== TASK ROUTES ====================

# GET: List all tasks
@comments_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = db.session.execute(db.select(Task)).scalars().all() # SQLAlchemy 2.0 select
    return jsonify([{'id': t.id, 'title': t.title} for t in tasks]), 200

# POST: Add a new task
@comments_bp.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'message': 'Missing task title'}), 400
        
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id, 'title': new_task.title}), 201

# PUT/PATCH: Update an existing task
@comments_bp.route('/tasks/<int:task_id>', methods=['PUT', 'PATCH'])
def edit_task(task_id):
    # FIX: Replace Task.query.get() with db.session.get()
    task = db.session.get(Task, task_id) 
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    data = request.get_json()
    if 'title' in data:
        task.title = data['title']
        db.session.commit()
        return jsonify({'message': 'Task updated', 'id': task.id, 'title': task.title}), 200
    else:
        return jsonify({'message': 'Missing update content (title)'}), 400

# DELETE: Delete a task
@comments_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # FIX: Replace Task.query.get() with db.session.get()
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Task {task_id} deleted'}), 204 # 204 No Content


# ==================== COMMENT ROUTES ====================

# POST: Add a new comment
@comments_bp.route('/tasks/<int:task_id>/comments', methods=['POST'])
def add_comment(task_id):
    # FIX: Replace Task.query.get() with db.session.get()
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'message': 'Missing comment content'}), 400

    new_comment = Comment(task_id=task_id, content=data['content'])
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({
        'id': new_comment.id,
        'content': new_comment.content,
        'created_at': new_comment.created_at.isoformat()
    }), 201


# GET: List all comments for a task
@comments_bp.route('/tasks/<int:task_id>/comments', methods=['GET'])
def list_comments(task_id):
    # FIX: Replace Task.query.get() with db.session.get()
    if not db.session.get(Task, task_id):
        return jsonify({'message': 'Task not found'}), 404

    # Use SQLAlchemy 2.0 style select for comments filtering
    stmt = db.select(Comment).filter_by(task_id=task_id)
    comments = db.session.execute(stmt).scalars().all()

    return jsonify([{
        'id': c.id,
        'content': c.content,
        'created_at': c.created_at.isoformat()
    } for c in comments]), 200


# PUT/PATCH: Update an existing comment
@comments_bp.route('/comments/<int:comment_id>', methods=['PUT', 'PATCH'])
def edit_comment(comment_id):
    # FIX: Replace Comment.query.get() with db.session.get()
    comment = db.session.get(Comment, comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404

    data = request.get_json()
    if 'content' in data:
        comment.content = data['content']
        db.session.commit()
        return jsonify({'message': 'Comment updated', 'content': comment.content}), 200
    else:
        return jsonify({'message': 'Missing update content'}), 400


# DELETE: Delete a comment
@comments_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    # FIX: Replace Comment.query.get() with db.session.get()
    comment = db.session.get(Comment, comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'}), 204