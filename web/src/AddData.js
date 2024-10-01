import React, { useState } from 'react';

const AddData = () => {
  const [formData, setFormData] = useState({ name: '', age: '' });
  const [submittedName, setSubmittedName] = useState(null); // State to store submitted email

  const handleChange = (e) => {
    const { name, value } = e.target;
    // Convert age to an integer if the field is 'age'
    const updatedValue = name === 'age' ? parseInt(value, 10) : value;

    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/add_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData), // Convert form data to JSON
      });

      const result = await response.json();
      console.log(result); // Handle the response from the backend

      // Set the submitted email to state
      setSubmittedName(result.data.name);
    } catch (error) {
      console.error('Error:', error); // Handle any errors
    }
  };

  return (
    <div>
      <h1>Add Data</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Age:
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>

      {/* Conditionally render the submitted email */}
      {submittedName && (
        <div>
          <h2>Submitted Name:</h2>
          <p>{submittedName}</p>
        </div>
      )}
    </div>
  );
};

export default AddData;
