// client/src/components/TaskManager.jsx
import React, { useState, useEffect } from "react";

const API_BASE_URL = "http://127.0.0.1:5000/api";

function TaskManager() {
  const [tasks, setTasks] = useState([]);
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [comments, setComments] = useState({});
  const [newComment, setNewComment] = useState({});
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [editingTaskTitle, setEditingTaskTitle] = useState("");
  const [editingCommentId, setEditingCommentId] = useState(null);
  const [editingCommentContent, setEditingCommentContent] = useState("");
  const [error, setError] = useState(null);

  // -------------------- TASK CRUD --------------------
  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/tasks`);
      if (!res.ok) throw new Error("Failed to fetch tasks");
      const data = await res.json();
      setTasks(data);
    } catch (err) {
      setError(err.message);
      console.error(err);
    }
  };

  const addTask = async () => {
    if (!newTaskTitle.trim()) return;
    try {
      const res = await fetch(`${API_BASE_URL}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: newTaskTitle }),
      });
      if (!res.ok) throw new Error("Failed to add task");
      const data = await res.json();
      setTasks([...tasks, data]);
      setNewTaskTitle("");
    } catch (err) {
      setError(err.message);
    }
  };

  const deleteTask = async (id) => {
    try {
      const res = await fetch(`${API_BASE_URL}/tasks/${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to delete task");
      setTasks(tasks.filter((t) => t.id !== id));
      setComments((prev) => {
        const updated = { ...prev };
        delete updated[id];
        return updated;
      });
    } catch (err) {
      setError(err.message);
    }
  };

  const startEditTask = (task) => {
    setEditingTaskId(task.id);
    setEditingTaskTitle(task.title);
  };

  const saveTaskEdit = async (taskId) => {
    if (!editingTaskTitle.trim()) return;
    try {
      const res = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: editingTaskTitle }),
      });
      if (!res.ok) throw new Error("Failed to update task");
      setTasks(
        tasks.map((t) => (t.id === taskId ? { ...t, title: editingTaskTitle } : t))
      );
      setEditingTaskId(null);
    } catch (err) {
      setError(err.message);
    }
  };

  // -------------------- COMMENT CRUD --------------------
  const fetchComments = async (taskId) => {
    try {
      const res = await fetch(`${API_BASE_URL}/tasks/${taskId}/comments`);
      if (!res.ok) throw new Error("Failed to fetch comments");
      const data = await res.json();
      setComments((prev) => ({ ...prev, [taskId]: data }));
    } catch (err) {
      setError(err.message);
    }
  };

  const addComment = async (taskId) => {
    const content = newComment[taskId];
    if (!content?.trim()) return;

    try {
      const res = await fetch(`${API_BASE_URL}/tasks/${taskId}/comments`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content }),
      });
      if (!res.ok) throw new Error("Failed to add comment");
      const data = await res.json();
      setComments((prev) => ({ ...prev, [taskId]: [...(prev[taskId] || []), data] }));
      setNewComment((prev) => ({ ...prev, [taskId]: "" }));
    } catch (err) {
      setError(err.message);
    }
  };

  const startEditComment = (taskId, comment) => {
    setEditingCommentId(comment.id);
    setEditingCommentContent(comment.content);
  };

  const saveCommentEdit = async (taskId, commentId) => {
    if (!editingCommentContent.trim()) return;

    try {
      const res = await fetch(`${API_BASE_URL}/comments/${commentId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: editingCommentContent }),
      });
      if (!res.ok) throw new Error("Failed to update comment");

      setComments((prev) => ({
        ...prev,
        [taskId]: prev[taskId].map((c) =>
          c.id === commentId ? { ...c, content: editingCommentContent } : c
        ),
      }));
      setEditingCommentId(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const deleteComment = async (taskId, commentId) => {
    try {
      const res = await fetch(`${API_BASE_URL}/comments/${commentId}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to delete comment");
      setComments((prev) => ({
        ...prev,
        [taskId]: prev[taskId].filter((c) => c.id !== commentId),
      }));
    } catch (err) {
      setError(err.message);
    }
  };

  // -------------------- RENDER --------------------
  return (
    <div style={{ padding: "20px" }}>
      <h2>🧭 Task Manager</h2>
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {/* Add Task */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="New Task Title"
          value={newTaskTitle}
          onChange={(e) => setNewTaskTitle(e.target.value)}
          style={{ padding: "6px", width: "250px", marginRight: "10px" }}
        />
        <button onClick={addTask} style={{ padding: "6px 10px" }}>
          ➕ Add Task
        </button>
      </div>

      {/* List Tasks */}
      {tasks.map((task) => (
        <div
          key={task.id}
          style={{
            border: "1px solid #ccc",
            borderRadius: "10px",
            padding: "15px",
            marginBottom: "15px",
            background: "#f9f9f9",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            {editingTaskId === task.id ? (
              <>
                <input
                  value={editingTaskTitle}
                  onChange={(e) => setEditingTaskTitle(e.target.value)}
                  style={{ width: "70%" }}
                />
                <button onClick={() => saveTaskEdit(task.id)}>💾 Save</button>
                <button onClick={() => setEditingTaskId(null)}>❌ Cancel</button>
              </>
            ) : (
              <>
                <strong>{task.title}</strong>
                <div>
                  <button onClick={() => startEditTask(task)} style={{ marginRight: "5px" }}>
                    ✏ Edit
                  </button>
                  <button onClick={() => deleteTask(task.id)} style={{ color: "red" }}>
                    🗑 Delete
                  </button>
                </div>
              </>
            )}
          </div>

          {/* Comments */}
          <div style={{ marginTop: "10px", marginLeft: "20px" }}>
            <button
              onClick={() => fetchComments(task.id)}
              style={{ background: "#007bff", color: "white", border: "none", padding: "4px 8px", borderRadius: "6px" }}
            >
              💬 Load Comments
            </button>

            {/* Comment List */}
            {(comments[task.id] || []).map((c) => (
              <div key={c.id} style={{ marginTop: "8px" }}>
                {editingCommentId === c.id ? (
                  <>
                    <input
                      value={editingCommentContent}
                      onChange={(e) => setEditingCommentContent(e.target.value)}
                      style={{ width: "60%", marginRight: "5px" }}
                    />
                    <button onClick={() => saveCommentEdit(task.id, c.id)}>💾 Save</button>
                    <button onClick={() => setEditingCommentId(null)}>❌ Cancel</button>
                  </>
                ) : (
                  <>
                    🗨 {c.content}{" "}
                    <span style={{ fontSize: "0.8em", color: "gray" }}>
                      ({new Date(c.created_at).toLocaleDateString()})
                    </span>
                    <button onClick={() => startEditComment(task.id, c)} style={{ marginLeft: "5px" }}>
                      ✏ Edit
                    </button>
                    <button onClick={() => deleteComment(task.id, c.id)} style={{ marginLeft: "5px", color: "red" }}>
                      🗑 Delete
                    </button>
                  </>
                )}
              </div>
            ))}

            {/* Add New Comment */}
            <div style={{ marginTop: "10px" }}>
              <input
                placeholder="Write a comment..."
                value={newComment[task.id] || ""}
                onChange={(e) => setNewComment((prev) => ({ ...prev, [task.id]: e.target.value }))}
                style={{ padding: "5px", width: "200px", marginRight: "5px" }}
              />
              <button onClick={() => addComment(task.id)} style={{ background: "green", color: "white", border: "none", padding: "4px 8px", borderRadius: "6px" }}>
                ➤ Add
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default TaskManager;
