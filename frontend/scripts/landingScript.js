document.addEventListener("DOMContentLoaded", function () {
  loadItems();
});

async function loadItems() {
  try {
    const token = localStorage.getItem("ACCESS_TOKEN");
    if (!token) {
      console.error("No access token—user is not logged in");
      return;
    }

    const response = await fetch("/items", {
      method: "GET",
      headers: {
        AUTHORIZATION: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      console.error("Fetch error", response.status, await response.text());
      return;
    }
    const items = await response.json();

    const updatedItems = items.map((item) => {
      const updatedOrganic = item.is_organic !== false ? "Yes" : "No";
      const updatedName =
        item.name.charAt(0).toUpperCase() + item.name.slice(1);

      return {
        ...item,
        name: updatedName,
        is_organic: updatedOrganic,
      };
    });

    displayItems(updatedItems);
  } catch (error) {
    console.error("Error fetching items", error);
  }
}

function displayItems(items) {
  const tableBody = document.getElementById("items-table-body");
  tableBody.innerHTML = "";

  items.forEach((item) => {
    const row = document.createElement("tr");

    const name = document.createElement("td");
    name.innerHTML = `
        <div class = "name-details">
            <h4>${item.name} </h4>
        </div>`;
    row.appendChild(name);

    const price = document.createElement("td");
    price.innerHTML = `
        <div class = "price-details">
            <h4>$${item.price} </h4>     
        </div>`;
    row.appendChild(price);

    const description = document.createElement("td");
    description.innerHTML = `
        <div class = "description-details">
            <h4> ${item.description} </h4>
        </div>`;
    row.appendChild(description);

    const organic = document.createElement("td");
    organic.innerHTML = `
    <div class = "organic-details">
        <h4> ${item.is_organic} </h4>
        </div>`;
    row.appendChild(organic);

    const image_url = document.createElement("td");
    image_url.innerHTML = `
    <div class = "image_url-details"
        <h4> ${item.image_url} </h4>
        </div>`;

    row.appendChild(image_url);

    tableBody.appendChild(row);
  });
}
