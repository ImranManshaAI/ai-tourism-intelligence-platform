export type Destination = {
  id: string;
  name: string;
  description: string;
  images: string[];
  opening_hours: string | null;
  ticket_price: string | null;
  facilities: string[];
  travel_tips: string[];
  latitude: number | null;
  longitude: number | null;
  embedding_id: string | null;
};

export type DestinationListResponse = {
  items: Destination[];
  page: number;
  page_size: number;
  total: number;
};

export type CreateDestinationRequest = {
  name: string;
  description: string;
  images: string[];
  opening_hours?: string | null;
  ticket_price?: string | null;
  facilities: string[];
  travel_tips: string[];
  latitude?: number | null;
  longitude?: number | null;
};

export type UpdateDestinationRequest = Partial<CreateDestinationRequest>;
