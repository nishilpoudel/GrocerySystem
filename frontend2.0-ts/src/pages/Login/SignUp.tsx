// set up navigation
// set up error handling
// use a better way of storing access_tokens

import React, { useState } from "react";
import { setAccessToken } from "../../utils/auth";

function SignUp() {
  const [error, setError] = useState<string | null>(null);
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const formData = new FormData(event.currentTarget);
      const { first_name, last_name, email, hashed_password } =
        Object.fromEntries(formData);
      const payLoad = {
        first_name: first_name,
        last_name: last_name,
        email: email,
        hashed_password: hashed_password,
      };

      const response = await fetch("http://localhost:8000/create-user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payLoad),
      });

      if (!response.ok) {
        const message = await response.text();
        setError(message || "Sign up Failed");
        return;
      }

      if (response.ok) {
        // I want to have access to the json response here

        const data = await response.json();
        setAccessToken(data.access_token);
      }
    } catch (error) {
      console.error("Error", error);
    }
  };

  return (
    <>
      <h1 className="header">Sign Up</h1>
      <form className="login-form" onSubmit={handleSubmit}>
        <label> First Name: </label>
        <input type="text" id="first_name" name="first_name" required />
        <label> Last Name: </label>
        <input type="text" id="last_name" name="last_name" required />

        <label> Email: </label>
        <input type="email" id="email" name="email" required />

        <label> Password: </label>
        <input
          type="password"
          id="hashed_password"
          name="hashed_password"
          required
        />

        <button type="submit">Submit</button>
        <button type="reset">Reset</button>
      </form>
    </>
  );
}

export default SignUp;
