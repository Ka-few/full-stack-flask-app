import React, { useState, useEffect } from "react";

function Course() {
  const [courses, setCourses] = useState([]);
  const [formData, setFormData] = useState({ name: "", description: "", credits: "" });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/courses")
      .then((res) => res.json())
      .then((data) => setCourses(data))
      .catch((err) => console.error("Fetch error:", err));
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Submitting form", { editingId, formData });
    // ensure credits is a number
    const payload = { ...formData, credits: Number(formData.credits) };

    if (editingId) {
      // Update existing
      fetch(`http://127.0.0.1:5555/courses/${editingId}`, {
        method: "PUT",           // try PATCH first; see notes if backend doesn't accept PATCH
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then((res) => {
          if (!res.ok) throw new Error("Update failed");
          return res.json();
        })
        .then((updatedCourse) => {
          setCourses((prev) => prev.map((c) => (c.id === updatedCourse.id ? updatedCourse : c)));
          setFormData({ name: "", description: "", credits: "" });
          setEditingId(null);;
        })
        .catch((err) => console.error("Error updating course:", err));
    } else {
      // Create new
      fetch("http://127.0.0.1:5555/courses", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then((res) => res.json())
        .then((newCourse) => {
          setCourses((prev) => [...prev, newCourse]);
          setFormData({ name: "", description: "", credits: "" });
        })
        .catch((err) => console.error("Error adding course:", err));
    }
  };

  const handleEdit = (course) => {
    setEditingId(course.id);
    setFormData({
      name: course.name ?? "",
      description: course.description ?? "",
      credits: course.credits == null ? "" : String(course.credits),
    });
    // focus the first field so user sees the form is active
    const el = document.getElementById("course-name");
    if (el) el.focus();
  };

  const handleCancel = () => {
    setEditingId(null);
    setFormData({ name: "", description: "", credits: "" });
  };

  const handleDelete = (id) => {
    if (!window.confirm("Delete this course?")) return;
    fetch(`http://127.0.0.1:5555/courses/${id}`, { method: "DELETE" })
      .then((res) => {
        if (!res.ok) throw new Error("Delete failed");
        setCourses((prev) => prev.filter((c) => c.id !== id));
      })
      .catch((err) => console.error("Error deleting course:", err));
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="course-form" aria-label="course-form">
        <input
          id="course-name"
          name="name"
          placeholder="Course Name"
          value={formData.name}
          onChange={handleChange}
        />
        <input
          name="description"
          placeholder="Course Description"
          value={formData.description}
          onChange={handleChange}
        />
        <input
          name="credits"
          type="number"
          placeholder="Credits"
          value={formData.credits}
          onChange={handleChange}
          min="0"
        />
        <button type="submit" className="primary">
          {editingId ? "Update Course" : "Add Course"}
        </button>
        {editingId && (
          <button type="button" className="muted" onClick={handleCancel}>
            Cancel
          </button>
        )}
      </form>

      <div className="course-list">
        {courses.map((course) => (
          <div className="course-card" key={course.id}>
            <div className="course-info">
              <div className="course-title">
                <strong>{course.name}</strong> <span className="credits">({course.credits} credits)</span>
              </div>
              <div className="course-desc">{course.description}</div>
            </div>

            <div className="course-actions">
              <button className="edit" onClick={() => handleEdit(course)}>
                Edit
              </button>
              <button className="delete" onClick={() => handleDelete(course.id)}>
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Course;
