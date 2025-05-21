import CreateItemComponent from "../../components/Item/CreateItem";
import { useEffect, useState } from "react";
import { DisplayItem } from "../../types/Item";
import { fetchWithAuth } from "../../api/fetchWithAuth";
import DisplayItemCard from "../../components/Item/DisplayItemCard";
import "../../styles/landing-page.css";

// useEffect is not finished, need to have error handling
// needs to update on create item change
// need to add more state
//

export default function LandingPage() {
  const [items, setItems] = useState<DisplayItem[]>([]);

  useEffect(() => {
    async function loadItems() {
      try {
        const response = await fetchWithAuth(
          "http://localhost:8000/user-items"
        );

        if (!response.ok) {
          const message = await response.json();
          console.error("Error with fetch with auth response", message);
        }

        const data = (await response.json()) as DisplayItem[];
        setItems(data);
      } catch (e: any) {
        console.error("Error", e.message);
      } finally {
        // something
      }
    }
    loadItems();
  }, []);

  return (
    <div>
      <div className="create-button">
        <CreateItemComponent />
      </div>
      <div>
        {items.map((item) => (
          <DisplayItemCard
            key={item.id}
            name={item.name}
            price={item.price}
            description={item.description}
            is_organic={item.is_organic}
          />
        ))}
      </div>
    </div>
  );
}
