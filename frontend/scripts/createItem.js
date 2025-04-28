document.addEventListener("DOMContentLoaded", function () {
  loadItems();
});

function loadItems() {
  const form = document.getElementById("item-form");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("ACCESS_TOKEN");
    if (!token) {
      alert("You must login in first");
      return window.location.href("/login.html");
    }

    const payload = Object.fromEntries(new FormData(form).entries());
    payload.price = parseFloat(payload.price);
    payload.is_organic = payload.is_organic === "yes";

    const res = await fetch("/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      alert("Item Created");
      return (window.location.href = "/landing");
    } else {
      const err = await res.json();
      alert("Error: " + (err.detail || JSON.stringify(err)));
    }
  });
}
