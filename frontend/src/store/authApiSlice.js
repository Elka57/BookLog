// src/store/authApiSlice.js

import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { setCredentials, setUser, logout } from "./authSlice";

// 1) Базовый запрос, подставляем Access Token
const baseQuery = fetchBaseQuery({
  baseUrl: "/api/",
  prepareHeaders: (headers, { getState }) => {
    const token = getState().auth.accessToken;
    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }
    return headers;
  },
  credentials: "include", // если используете куки для csrf
});

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: async (args, api, extraOptions) => {
    // 2) Оборачиваем базовый запрос, чтобы автоматически рефрешить токен при 401
    let result = await baseQuery(args, api, extraOptions);

    if (result.error?.status === 401) {
      const refreshToken = api.getState().auth.refreshToken;
      if (refreshToken) {
        // запрос на обновление Access Token
        const refreshResult = await baseQuery(
          {
            url: "auth/token/refresh/",
            method: "POST",
            body: { refresh: refreshToken },
          },
          api,
          extraOptions
        );

        if (refreshResult.data?.access) {
          // сохраним новый токен
          api.dispatch(
            setCredentials({
              accessToken: refreshResult.data.access,
              refreshToken,
            })
          );
          // повторим исходный запрос
          result = await baseQuery(args, api, extraOptions);
        } else {
          // если рефреш не сработал — выходим
          api.dispatch(logout());
        }
      }
    }

    return result;
  },
  tagTypes: ["User"],
  endpoints: (build) => ({
    // LOGIN
    login: build.mutation({
      query: (credentials) => ({
        url: "auth/login/",
        method: "POST",
        body: credentials, // { username/email, password }
      }),
      async onQueryStarted(arg, { dispatch, queryFulfilled }) {
        try {
          // 1. ждём ответа с токенами
          const { data } = await queryFulfilled;
          const { access, refresh } = data;

          // 2. сохраняем токены в Redux
          dispatch(
            setCredentials({
              accessToken: access,
              refreshToken: refresh,
            })
          );

          // 3. сразу запрашиваем профиль и кладём его в стейт
          const { data: user } = await dispatch(
            authApi.endpoints.fetchCurrentUser.initiate()
          ).unwrap();
          dispatch(setUser(user));
        } catch {
          // ignore
        }
      },
    }),

    // LOGOUT
    logout: build.mutation({
      query: (refreshToken) => ({
        url: "auth/logout/",
        method: "POST",
        body: { refresh_token: refreshToken },
      }),
      async onQueryStarted(arg, { dispatch, queryFulfilled }) {
        try {
          await queryFulfilled;
        } catch {
          // даже если сервер вернёт ошибку, очищаем стейт
        } finally {
          dispatch(logout());
        }
      },
    }),

    // REGISTER → после рега логинимся автоматически
    register: build.mutation({
      query: (formData) => ({
        url: "auth/register/",
        method: "POST",
        body: formData, // FormData с полями email*, username*, password1*, password2*
      }),
      async onQueryStarted(formData, { dispatch, queryFulfilled }) {
        try {
          await queryFulfilled;
          const username = formData.get("username");
          const password = formData.get("password1");

          // инициируем login, чтобы получить токены и профиль
          await dispatch(
            authApi.endpoints.login.initiate({ username, password })
          ).unwrap();
        } catch {
          // если регистрация или логин упали — игнорируем
        }
      },
    }),

    // VERIFY EMAIL
    verifyEmail: build.mutation({
      query: (data) => ({
        url: "auth/register/verify-email/",
        method: "POST",
        body: data, // { key }
      }),
    }),

    // FETCH CURRENT USER
    fetchCurrentUser: build.query({
      query: () => "users/user/current/",
      providesTags: (result) =>
        result ? [{ type: "User", id: result.id }] : [],
    }),

    // UPDATE CURRENT USER
    updateCurrentUser: build.mutation({
      query: (patch) => ({
        url: "users/user/current/",
        method: "PATCH",
        body: patch,
      }),
      invalidatesTags: (result) =>
        result ? [{ type: "User", id: result.id }] : [],
    }),

    // PROFILE DELETION
    requestProfileDeletion: build.mutation({
      query: () => ({
        url: "profile-delete/request/",
        method: "POST",
      }),
    }),
    confirmProfileDeletion: build.mutation({
      query: (data) => ({
        url: "profile-delete/confirm/",
        method: "POST",
        body: data, // { key }
      }),
      async onQueryStarted(arg, { dispatch, queryFulfilled }) {
        try {
          await queryFulfilled;
        } catch {}
        dispatch(logout());
      },
    }),
  }),
});

export const {
  useLoginMutation,
  useLogoutMutation,
  useRegisterMutation,
  useVerifyEmailMutation,
  useFetchCurrentUserQuery,
  useUpdateCurrentUserMutation,
  useRequestProfileDeletionMutation,
  useConfirmProfileDeletionMutation,
} = authApi;
