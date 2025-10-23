// client/src/App.jsx
import React from "react";
import "./App.css"; 
import TaskManager from "./components/TaskManager"; // ✅ Keep only this

function App() {
  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Full-Stack Assessment Solution</h1>
      <p>Frontend running on port 5173 ⚛️ | Backend running on port 5000 🐍</p>
      <hr />

      {/* Task + Comment CRUD */}
      <section>
        <h2>Task & Comment Manager</h2>
        <TaskManager />
      </section>
    </div>
  );
}

export default App;
