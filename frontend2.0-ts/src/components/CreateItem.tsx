import React from "react";
import { CreateItem } from "../types/Item";
import { fetchWithAuth } from "../api/fetchWithAuth";

export default function CreateItemComponent(): any {
  const handleFormSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const formData = event.currentTarget;
    const form = new FormData(formData);

    const response = await fetchWithAuth("http://localhost:8000/create", {
      method: "POST",
      headers: { "Content-type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        name: form.get("name"),
        price: parseFloat(form.get("price") as string),
        description: form.get("description"),
        is_organic: form.get("is_organic") === "yes",
      } as CreateItem),
    });
    if (!response.ok) {
      const errText = await response.json();
      console.error("Error", errText);
    }
  };

  return (
    <div className="body">
      <dialog className="dialog" open>
        <form onSubmit={handleFormSubmit}>
          <label htmlFor="name">
            {" "}
            Name
            <input
              className="form-input"
              id="name"
              name="name"
              type="text"
              required
              placeholder="apple"
            />
          </label>
          <label htmlFor="price">
            Price
            <input
              className="form-input"
              id="price"
              name="price"
              type="number"
              step={0.1}
              required
              placeholder="$$$"
            />{" "}
          </label>
          <label htmlFor="description">
            Description
            <input
              className="form-input"
              id="description"
              name="description"
              type="text"
              placeholder="Red Apple"
            />{" "}
          </label>
          <label htmlFor="is_organic">
            {" "}
            Organic
            <select className="form-select" name="is_organic">
              {" "}
              <option value="yes"> Yes </option> <option value="no"> No</option>
            </select>
          </label>
          <button className="form-button" type="submit">
            {" "}
            Create!{" "}
          </button>
        </form>
      </dialog>
    </div>
  );
}
