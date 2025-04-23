document.addEventListener("DOMContentLoaded", function () {
  loadItems();
});

function loadItems() {
  const form = document.getElementById("login-form");
  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // this prevents the default from happening ( in this case this is the form being submitted)

    const data = new FormData(form);

    const response = await fetch("/login", {
      method: "POST",
      body: data,
    });

    if (!response.ok) {
      alert("Login Failed");
      return;
    }

    const { access_token, token_type } = await response.json();
    localStorage.setItem("ACCESS_TOKEN", access_token);
    localStorage.setItem("TOKEN_TYPE", token_type);

    window.location.href = "/landing";
  });
}

// document.addEventListener("DOMContentLoaded", function () {
//   loadItems();
// });

// function loadItems() {
//   const form = document.getElementById("login-form");
//   form.addEventListener("submit", async (e) => {
//     e.preventDefault(); // prevents the default action(in this case, cancels the submission until all the data loads)

//     const data = new FormData(form);

//     const response = await fetch("/login", {
//       method: "POST",
//       body: data,
//     });

//     if (!response.ok) {
//       alert("Login Failed");
//       return;
//     }

//     const { access_token, token_type } = await response.json();
//     // store the values in local storage
//     localStorage.setItem("ACCESS_TOKEN", access_token);
//     localStorage.setItem("TOKEN_TYPE", token_type);

//     window.location("/create-item.html");
//   });
// }
