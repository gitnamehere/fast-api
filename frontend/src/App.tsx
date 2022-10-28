import React from 'react';
import './App.css';
import {Formik, FormikProps, Form, Field, FieldProps, useFormik} from 'formik';
import axios from 'axios';

// TODO: Add Yup validation

const FormContainer = () => {
  const onSubmit = (values: any) => {
    axios.post('http://localhost:8000/api/users/submit', values)
      .then((response) => {
        console.log(response);
        alert("Form submitted!");
      })
      .catch((error) => {
        console.log(error);
        alert("Failed to submit form.");
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

interface LogInProps {
  username: string;
  password: string;
}

const LogInContainer = () => {

  const onSubmit = (values: LogInProps) => {
    axios.post('http://localhost:8000/api/token', values, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}, withCredentials: true})
      .then((response) => {
        console.log(response);
        alert("Logged in!\n(DEV) Access Token:\n" + response.data.access_token);
      })
      .catch((error) => {
        if (error.response) {
          if (error.response.status === 401) {
            alert("Invalid username or password.");
          } else {
            alert("Failed to submit form.");
          }
        } else {
          console.log(error);
          alert("Failed to submit form.");
        }
    });
  };

  const formik = useFormik({
    initialValues: {
      username: '',
      password: '',
    },
    validateOnBlur: true,
    onSubmit: (values: LogInProps) => {
      onSubmit(values);
    }
  });

  return (
    <form onSubmit={formik.handleSubmit} className="form">
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

function devStuff() {
  return (
    <div>
      <h1>not so secret development stuff</h1>
      <button><a href="http://localhost:8000/docs">FastAPI Docs</a></button>
      <button><a href="http://localhost:8000/api/users/all">All Users in Database</a></button>
    </div>
  )
}

function App() {
  return (
    <div className="App">
      <h1>Almost extremely minimalistic form for the purposes of learning, development, and testing.</h1>
      <h2>Sign Up</h2>
      <FormContainer />
      <h2>Log In</h2>
      <LogInContainer />
      {devStuff()}
    </div>
  );
}

export default App;
