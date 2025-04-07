import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = 'http://localhost:8000'; // Adjust if needed

function App() {
  const [applications, setApplications] = useState([]);
  const [newApplication, setNewApplication] = useState({
    company_name: '',
    job_title: '',
    application_date: '',
  });

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    //IMPORTANT: Replace with a valid JWT token.  This is a placeholder
    const token = 'test'; // Replace with the actual token
    try {
      const response = await fetch(`${API_URL}/applications/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setApplications(data);
    } catch (error) {
      console.error('Error fetching applications:', error);
      alert('Failed to load applications. Check console.');
    }
  };

  const handleInputChange = (e) => {
    setNewApplication({ ...newApplication, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
     //IMPORTANT: Replace with a valid JWT token.  This is a placeholder
    const token = 'test'; // Replace with the actual token
    try {
      const response = await fetch(`${API_URL}/applications/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(newApplication),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      fetchApplications(); // Refresh the list after submission
      setNewApplication({ company_name: '', job_title: '', application_date: '' }); // Clear form
    } catch (error) {
      console.error('Error creating application:', error);
      alert('Failed to create application. Check console.');
    }
  };

  return (
    <div className="App">
      <h1>Job Application Tracker</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="company_name"
          placeholder="Company Name"
          value={newApplication.company_name}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="job_title"
          placeholder="Job Title"
          value={newApplication.job_title}
          onChange={handleInputChange}
        />
        <input
          type="date"
          name="application_date"
          placeholder="Application Date"
          value={newApplication.application_date}
          onChange={handleInputChange}
        />
        <button type="submit">Add Application</button>
      </form>
      <h2>Applications</h2>
      <ul>
        {applications.map((app) => (
          <li key={app.id}>
            {app.company_name} - {app.job_title} ({app.application_date})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;