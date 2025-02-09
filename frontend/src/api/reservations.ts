import { PaginatedResponse } from "../types/Api";
import {
  CreateReservation,
  CreateReservationResponse,
  Reservation,
} from "../types/Reservation";
import api from "./axios";

export const createReservation = async (
  data: CreateReservation
): Promise<CreateReservationResponse> => {
  try {
    const response = await api.post(`/api/reservations/`, data);
    return response.data;
  } catch (error) {
    console.error("Error updating book:", error);
    throw error;
  }
};

export const getReservations = async (): Promise<
  PaginatedResponse<Reservation>
> => {
  try {
    const response = await api.get(`/api/reservations/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching reservations:", error);
    throw error;
  }
};

export const updateReservation = async (
  id: number,
  data: Partial<
    Omit<Reservation, "id" | "reserved_at" | "returned_at" | "updated_at">
  >
): Promise<Reservation> => {
  try {
    const response = await api.patch(`/api/reservations/${id}/`, data);
    return response.data;
  } catch (error) {
    console.error("Error updating reservation:", error);
    throw error;
  }
};

export const deleteReservation = async (id: number): Promise<void> => {
  try {
    await api.delete(`/api/reservations/${id}/`);
  } catch (error) {
    console.error("Error deleting reservation:", error);
    throw error;
  }
};

export const getReservationsByBookId = async (
  bookId: number
): Promise<PaginatedResponse<Reservation>> => {
  try {
    const response = await api.get(`/api/reservations/?book=${bookId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching reservations by book ID:", error);
    throw error;
  }
};
