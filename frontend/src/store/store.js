// src/store/index.js
import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./authSlice";
import { authApi } from "./authApiSlice";
import { journalApi } from "./journalApiSlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    [authApi.reducerPath]: authApi.reducer,
    [journalApi.reducerPath]: journalApi.reducer,
  },
  middleware: (getDefault) =>
    getDefault().concat(authApi.middleware).concat(journalApi.middleware),
});
