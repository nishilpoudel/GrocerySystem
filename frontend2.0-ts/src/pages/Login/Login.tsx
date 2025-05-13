import { setAccessToken } from "../../utils/auth";

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
      console.log("AccessToken", data.access_token);

      console.log("Login Successful");
    }
  };

  return (
    <form className="login-form" onSubmit={handleFormSubmit}>
      <label>Email</label>
      <input
        id="email"
        name="email"
        required
        type="email"
        placeholder="name@email.com"
      />
      <label>Password</label>
      <input id="password" name="password" type="password" required />
      <button type="submit">Login</button>
    </form>
  );
}
export default Login;
