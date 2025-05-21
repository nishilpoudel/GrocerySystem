import React from "react";
import "../../styles/item-card.css";

type DisplayItemCardProps = {
  name: string;
  price: number;
  description: string;
  is_organic: boolean;
};

export default function DisplayItemCard({
  name,
  price,
  description,
  is_organic,
}: DisplayItemCardProps) {
  return (
    <div className="container">
      <div className="card">
        <h3> {name}</h3>
        <p> {description}</p>
        <p> {price}</p>
        {is_organic && <p> Organic</p>}
      </div>
    </div>
  );
}
