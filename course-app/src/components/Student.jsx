import React, { useState } from "react";

function Student() {
  const [student, setStudent] = useState({
    name: "",
    email: ""
  });

  const handleChange = (e) => {
    setStudent({ ...student, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("New Student:", student);
  };

  return (
    <div>
      <h2>Add Student</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Student Name"
          value={student.name}
          onChange={handleChange}
        />
        <input
          type="email"
          name="email"
          placeholder="Student Email"
          value={student.email}
          onChange={handleChange}
        />
        <button type="submit">Add Student</button>
      </form>
    </div>
  );
}

export default Student;
