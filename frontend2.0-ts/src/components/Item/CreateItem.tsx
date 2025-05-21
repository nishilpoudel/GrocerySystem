import React, { useState, useRef } from "react";
import { CreateItem } from "../../types/Item";
import { fetchWithAuth } from "../../api/fetchWithAuth";
import "../../styles/item-create.css";
import { JSX } from "react/jsx-runtime";

export default function CreateItemComponent(): JSX.Element {
  const [isOrganic, setIsOrganic] = useState(false);
  const dialogRef = useRef<HTMLDialogElement>(null);

  const handleOpenDialog = () => {
    if (dialogRef.current) {
      dialogRef.current.showModal();
    }
  };

  const handleCloseDialog = () => {
    if (dialogRef.current) {
      dialogRef.current.close();
    }
  };

  const handleFormSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const formData = event.currentTarget;
    const form = new FormData(formData);

    try {
      const response = await fetchWithAuth("http://localhost:8000/create", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          name: form.get("name"),
          price: parseFloat(form.get("price") as string),
          description: form.get("description"),
          is_organic: isOrganic,
        } as CreateItem),
      });
      if (!response.ok) {
        const errText = await response.json();
        console.error("Error", errText);
      } else {
        alert("Congratulations, Item has been created");
        handleCloseDialog();
      }
    } catch (e: any) {
      console.error("Error", e);
    }
  };

  return (
    <div className="body">
      <button onClick={handleOpenDialog}> New Item</button>
      <dialog ref={dialogRef} className="dialog">
        <form onSubmit={handleFormSubmit} method="dialog">
          <p className="form-close " onClick={handleCloseDialog}>
            X{" "}
          </p>
          <h2 className="form-header">Add your item</h2>
          <div className="item-name">
            {" "}
            <input
              className="form-input"
              id="name"
              name="name"
              type="text"
              required
              placeholder="Name"
            />
          </div>
          <div className="form-price">
            <input
              className="form-input"
              id="price"
              name="price"
              type="number"
              step={0.01}
              required
              placeholder="$$$"
            />{" "}
          </div>
          <div className="form-description">
            <input
              className="form-input"
              id="description"
              name="description"
              type="text"
              placeholder="Description"
            />{" "}
          </div>
          <div className="form-organic">
            <label className="switch">
              <input
                type="checkbox"
                name="is_organic"
                checked={isOrganic}
                onChange={(e) => setIsOrganic(e.target.checked)}
              />
              <span className="slider" />
            </label>
            <span className="organic-label">Organic</span>
          </div>
          <button className="form-button" type="submit">
            Create!
          </button>
        </form>
      </dialog>
    </div>
  );
}
