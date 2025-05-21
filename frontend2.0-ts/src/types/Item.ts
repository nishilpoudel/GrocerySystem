export type CreateItem = {
  name: string;
  description: string;
  price: number;
  is_organic: boolean;
};

export type DisplayItem = {
  id: number;
  name: string;
  price: number;
  description: string;
  is_organic: boolean;
};
