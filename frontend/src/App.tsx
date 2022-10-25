import React from 'react';
import './App.css';
import {Formik, FormikProps, Form, Field, FieldProps, useFormik} from 'formik';


const FormContainer = () => {
  const formik = useFormik({
    initialValues: {
      username: '',
      password: '',
      email: ''
    },
    onSubmit: values => {
      alert(JSON.stringify(values, null, 2));
    }
  });

  return (
    <form onSubmit={formik.handleSubmit} className="form">
      <label htmlFor="email">Email Address</label>
      <input
        id="email"
        name="email"
        type="email"
        onChange={formik.handleChange}
        value={formik.values.email}
      />

      <label htmlFor="username">Username</label>
       <input
         id="username"
         name="username"
         type="username"
         onChange={formik.handleChange}
         value={formik.values.username}
       />

       <label htmlFor="password">Password</label>
       <input
         id="password"
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
      <FormContainer />
    </div>
  );
}

export default App;
