import type { ApiError, ApiResponse } from "./api";

export type {
  ApiError,
  ApiResponse,
};

export type UserRole = "admin";

export type User = {
  id: string;
  email: string;
  role: UserRole;
};

export type LoginRequest = {
  email: string;
  password: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
  user: User;
};

export type ApiResult<T> = ApiResponse<T>;
