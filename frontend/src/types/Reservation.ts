export interface Reservation {
  id: number;
  name: string;
  email: string;
  book: { id: number; title: string };
  status: string;
  reserved_at: string;
  returned_at: string | null;
  updated_at: string;
}

export interface CreateReservation {
  name: string;
  email: string;
  book: number;
}

export interface CreateReservationResponse {
  message: string;
}
