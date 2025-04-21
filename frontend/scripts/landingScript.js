document.addEventListener("DOMContentLoaded", function () {
  loadItems();
});

async function loadItems() {
  try {
    const response = await fetch("/items");
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
        <div class = "quantity-details">
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
    <div class = "exp-date-details"
        <h4> ${item.image_url} </h4>
        </div>`;

    row.appendChild(image_url);

    tableBody.appendChild(row);
  });
}
