import { Link } from "react-router-dom";
import { setAccessToken } from "../../utils/auth";
import "../../styles/login-page.css";

function Login() {
  const handleFormSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const form = new FormData(event.currentTarget);
    const emailValue = form.get("email");
    if (emailValue === null) {
      console.error("No email value found in Form Data");
    }
    form.delete("email");
    form.append("username", emailValue as string);

    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      body: form,
      credentials: "include",
    });

    if (!response.ok) {
      const errorText = await response.json();
      console.error("Login Failed", response.status, errorText);
      return;
    }

    if (response.ok) {
      const data = await response.json();
      setAccessToken(data.access_token);
    }
  };

  return (
    <form className="login-form" onSubmit={handleFormSubmit}>
      <header className="login-header"> Login</header>

      <div className="input-box">
        {/* <label htmlFor="email">Email</label> */}
        <input
          className="input-field"
          id="email"
          name="email"
          required
          type="email"
          placeholder="name@email.com"
        />
        <br></br>
        {/* <label htmlFor="password">Password</label> */}
        <input
          className="input-field"
          id="password"
          name="password"
          type="password"
          required
          placeholder="password"
        />
        <br></br>
        <div className="input-submit">
          <button className="btn-submit" type="submit">
            Login
          </button>
        </div>
        <p className="auth-footer">
          Don't have an Account ?
          <Link to="/signup" className="signup-link">
            Sign Up
          </Link>
        </p>
      </div>
    </form>
  );
}
export default Login;
