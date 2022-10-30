import React from 'react'
import axios from 'axios'
import {useFormik, Field, Form, Formik} from 'formik';
import * as Yup from 'yup';

// TODO: Alert user the criteria to fulfill for a valid username and password with yup.

const LoginSchema = Yup.object().shape({
    username: Yup.string()
        .min(2, 'Too Short!')
        .max(50, 'Too Long!')
        .required('Required'),
    password: Yup.string()
        .min(8, 'Too Short!')
        .max(50, 'Too Long!')
        .required('Required'),
});

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
      validationSchema: LoginSchema,
      onSubmit: (values: LogInProps) => {
        onSubmit(values);
      }
    });
  
    return (
        <div className="form formBorder">
            <h2>Log In</h2>
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
        </div>
    );
  }

export default LogInContainer