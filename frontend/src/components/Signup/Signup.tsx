import React from 'react'
import axios from 'axios'
import {useFormik} from 'formik';
import * as Yup from 'yup';

// TODO: Alert user the criteria to fulfill for a valid username and password with yup.

const SignupSchema = Yup.object().shape({
    username: Yup.string()
        .min(2, 'Too Short!')
        .max(50, 'Too Long!')
        .required('Required'),
    password: Yup.string()
        .min(8, 'Too Short!')
        .max(50, 'Too Long!')
        .required('Required'),
    email: Yup.string().email('Invalid email').required('Required'),
});

interface SignupProps {
    username: string;
    password: string;
    email: string;
  }

const SignupContainer = () => {
    const onSubmit = (values: SignupProps) => {
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
      validationSchema: SignupSchema,
      onSubmit: (values: SignupProps) => {    
        onSubmit(values);
      }
    });
  
    return (
        <div className="form formBorder">
            <h2>Sign Up</h2>
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
        </div>
    );
  }

  export default SignupContainer; 