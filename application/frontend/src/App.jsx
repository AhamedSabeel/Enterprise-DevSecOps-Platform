import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "";

function App() {
  const [health, setHealth] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [taskName, setTaskName] = useState("");
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const getHealth = async () => {
    try {
      const response = await axios.get(`${API_URL}/health`);
      setHealth(response.data);
    } catch (error) {
      console.error("Health check failed:", error);
      setHealth({ status: "unavailable" });
    }
  };

  const getTasks = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/tasks`);
      setTasks(response.data);
    } catch (error) {
      console.error("Failed to fetch tasks:", error);
      setMessage("Unable to load tasks from the backend.");
    }
  };

  const loadDashboard = async () => {
    setLoading(true);

    await Promise.all([
      getHealth(),
      getTasks()
    ]);

    setLoading(false);
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const createTask = async (event) => {
    event.preventDefault();

    if (!taskName.trim()) {
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/api/tasks`, {
        name: taskName,
      });

      setMessage(`Task "${response.data.name}" created successfully.`);
      setTaskName("");

      await getTasks();
    } catch (error) {
      console.error("Failed to create task:", error);
      setMessage("Failed to create the background task.");
    }
  };

  if (loading) {
    return (
      <div className="loading">
        Loading Enterprise DevSecOps Platform...
      </div>
    );
  }

  return (
    <main className="dashboard">
      <header className="header">
        <div>
          <h1>Enterprise DevSecOps Platform</h1>
          <p>Multi-Service Cloud Native Operations Dashboard</p>
        </div>

        <button onClick={loadDashboard}>
          Refresh
        </button>
      </header>

      <section className="status-grid">
        <div className="card">
          <h3>Platform Status</h3>
          <p className={`status ${health?.status}`}>
            {health?.status || "Unknown"}
          </p>
        </div>

        <div className="card">
          <h3>Backend API</h3>
          <p>{health?.service || "Unavailable"}</p>
        </div>

        <div className="card">
          <h3>PostgreSQL</h3>
          <p className={`status ${health?.database}`}>
            {health?.database || "Unknown"}
          </p>
        </div>

        <div className="card">
          <h3>Redis</h3>
          <p className={`status ${health?.redis}`}>
            {health?.redis || "Unknown"}
          </p>
        </div>
      </section>

      <section className="task-section">
        <h2>Background Tasks</h2>

        <form onSubmit={createTask} className="task-form">
          <input
            type="text"
            placeholder="Enter task name"
            value={taskName}
            onChange={(event) => setTaskName(event.target.value)}
          />

          <button type="submit">
            Create Task
          </button>
        </form>

        {message && (
          <p className="message">{message}</p>
        )}

        <div className="task-list">
          {tasks.length === 0 ? (
            <p>No tasks created yet.</p>
          ) : (
            tasks.map((task) => (
              <div className="task-card" key={task.id}>
                <div>
                  <strong>{task.name}</strong>
                  <p>Task ID: {task.id}</p>
                </div>

                <span className="task-status">
                  {task.status}
                </span>
              </div>
            ))
          )}
        </div>
      </section>
    </main>
  );
}

export default App;
