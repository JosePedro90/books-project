import axios from "axios";
import { API_BASE_URL } from "./axios";

interface TokenResponse {
  access: string;
  refresh: string;
}

export const login = async (
  username: string,
  password: string
): Promise<TokenResponse> => {
  const response = await axios.post<TokenResponse>(
    `${API_BASE_URL}/api/token/`,
    { username, password }
  );
  return response.data;
};

export const refreshAccessToken = async (
  refreshToken: string
): Promise<{ access: string }> => {
  const response = await axios.post<{ access: string }>(
    `${API_BASE_URL}/api/token/refresh/`,
    { refresh: refreshToken }
  );
  return response.data;
};
