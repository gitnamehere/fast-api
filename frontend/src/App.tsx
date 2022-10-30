import React from 'react';
import './App.css';
import {Formik, FormikProps, Form, Field, FieldProps, useFormik} from 'formik';
import SignupContainer from './components/Signup/Signup';
import LogInContainer from './components/Login/Login';

// TODO: Store access token to be used in other requests

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
      <h1>Forms for the purposes of learning, development, and testing.</h1>
      <SignupContainer />
      <LogInContainer />
      {devStuff()}
    </div>
  );
}

export default App;
