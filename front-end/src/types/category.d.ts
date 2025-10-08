type CategoryFilter = {
  filtername: string;
  type: "string" | "number";
};

type Category = {
  id: number;
  title: string;
  filters?: {
    type: "object";
    properties: {
      [key: string]: {
        type: "string" | "number";
      };
    };
  };
};

export type { Category, CategoryFilter };
