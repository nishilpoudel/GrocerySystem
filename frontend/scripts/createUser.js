document.addEventListener("DOMContentLoaded", function () {
  loadItems();
});

function loadItems() {
  const form = document.getElementById("create-user");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payLoad = Object.fromEntries(new FormData(form).entries());
    console.log("payload", payLoad);

    const response = await fetch("/create-user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payLoad),
    });
    console.log("response", response);

    if (!response.ok) {
      alert("Error Creating User");
      return;
    }

    if (response.ok) {
      const { access_token, token_type } = await response.json();
      localStorage.setItem("ACCESS_TOKEN", access_token);
      localStorage.setItem("TOKEN_TYPE", token_type);
      console.log("token", access_token);
    }

    window.location.href = "/landing";
  });
}
