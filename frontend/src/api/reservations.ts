import { Reservation } from "../types/Reservation";
import api from "./axios";

export const createReservation = async (
  data: Reservation
): Promise<Reservation> => {
  try {
    const response = await api.post(`/api/reservations/`, data);
    return response.data;
  } catch (error) {
    console.error("Error updating book:", error);
    throw error; // Re-throw the error to be handled by the caller
  }
};
