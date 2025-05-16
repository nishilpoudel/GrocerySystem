import CreateItemComponent from "../../components/CreateItem";
import { useEffect, useState } from "react";
import { DisplayItem } from "../../types/Item";
import { fetchWithAuth } from "../../api/fetchWithAuth";

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
      {items.length === 0 ? "No items loaded" : JSON.stringify(items, null, 2)}

      <CreateItemComponent />
    </div>
  );
}
