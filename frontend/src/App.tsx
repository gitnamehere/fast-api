import React from 'react';
import './App.css';
import {Formik, FormikProps, Form, Field, FieldProps, useFormik} from 'formik';
import axios from 'axios';

const FormContainer = () => {
  const onSubmit = (values: any) => {
    console.log(values);
    axios.post('http://localhost:8000/api/users/submit', values)
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const formik = useFormik({
    initialValues: {
      username: '',
      password: '',
      email: ''
    },
    validateOnBlur: true,
    onSubmit: values => {
      onSubmit(values);
    }
  });

  return (
    <form onSubmit={formik.handleSubmit} className="form">
      <input
        id="email"
        placeholder='E-Mail'
        name="email"
        type="email"
        onChange={formik.handleChange}
        value={formik.values.email}
      />
      <input
        id="username"
        placeholder="Username"
        name="username"
        type="username"
        onChange={formik.handleChange}
        value={formik.values.username}
      />
      <input
        id="password"
        placeholder='Password'
        name="password"
        type="password"
        onChange={formik.handleChange}
        value={formik.values.password}
      />
      <button type="submit">Submit</button>
    </form>
  );
}

function App() {
  return (
    <div className="App">
      <h1>Extremely minimalistic form for the purposes of learning, development, testing.</h1>
      <h2>Sign Up</h2>
      <FormContainer />
    </div>
  );
}

export default App;
