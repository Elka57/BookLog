// src/store/apiSlice.js

import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const journalApi = createApi({
  reducerPath: "journalApi",
  baseQuery: fetchBaseQuery({ baseUrl: "/api/" }),
  tagTypes: ["Author", "Genre", "Book", "BookLog", "Quote", "Like", "Share"],
  endpoints: (build) => ({
    //
    // Authors
    //
    fetchAuthors: build.query({
      query: (params) => ({ url: "authors/", params }),
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "Author", id })),
              { type: "Author", id: "LIST" },
            ]
          : [{ type: "Author", id: "LIST" }],
    }),
    fetchAuthorById: build.query({
      query: (id) => `authors/${id}/`,
      providesTags: (result, error, id) => [{ type: "Author", id }],
    }),
    createAuthor: build.mutation({
      query: (data) => ({ url: "authors/", method: "POST", body: data }),
      invalidatesTags: [{ type: "Author", id: "LIST" }],
    }),
    updateAuthor: build.mutation({
      query: ({ id, ...data }) => ({
        url: `authors/${id}/`,
        method: "PUT",
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "Author", id }],
    }),
    patchAuthor: build.mutation({
      query: ({ id, ...data }) => ({
        url: `authors/${id}/`,
        method: "PATCH",
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "Author", id }],
    }),
    deleteAuthor: build.mutation({
      query: (id) => ({ url: `authors/${id}/`, method: "DELETE" }),
      invalidatesTags: [{ type: "Author", id: "LIST" }],
    }),
    approveAuthor: build.mutation({
      query: (id) => ({
        url: `authors/${id}/approve/`,
        method: "POST",
      }),
      invalidatesTags: (result, error, id) => [{ type: "Author", id }],
    }),
    rejectAuthor: build.mutation({
      query: (id) => ({
        url: `authors/${id}/reject/`,
        method: "POST",
      }),
      invalidatesTags: (result, error, id) => [{ type: "Author", id }],
    }),

    //
    // Genres
    //
    fetchGenres: build.query({
      query: (params) => ({ url: "genres/", params }),
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "Genre", id })),
              { type: "Genre", id: "LIST" },
            ]
          : [{ type: "Genre", id: "LIST" }],
    }),
    fetchGenreById: build.query({
      query: (id) => `genres/${id}/`,
      providesTags: (result, error, id) => [{ type: "Genre", id }],
    }),
    createGenre: build.mutation({
      query: (data) => ({ url: "genres/", method: "POST", body: data }),
      invalidatesTags: [{ type: "Genre", id: "LIST" }],
    }),
    updateGenre: build.mutation({
      query: ({ id, ...data }) => ({
        url: `genres/${id}/`,
        method: "PUT",
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "Genre", id }],
    }),
    patchGenre: build.mutation({
      query: ({ id, ...data }) => ({
        url: `genres/${id}/`,
        method: "PATCH",
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "Genre", id }],
    }),
    deleteGenre: build.mutation({
      query: (id) => ({ url: `genres/${id}/`, method: "DELETE" }),
      invalidatesTags: [{ type: "Genre", id: "LIST" }],
    }),

    //
    // Books
    //
    fetchBooks: build.query({
      query: (params) => ({ url: "books/", params }),
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "Book", id })),
              { type: "Book", id: "LIST" },
            ]
          : [{ type: "Book", id: "LIST" }],
    }),
    fetchBookById: build.query({
      query: (id) => `books/${id}/`,
      providesTags: (result, error, id) => [{ type: "Book", id }],
    }),
    createBook: build.mutation({
      query: (data) => ({ url: "books/", method: "POST", body: data }),
      invalidatesTags: [{ type: "Book", id: "LIST" }],
    }),
    updateBook: build.mutation({
      query: ({ id, ...data }) => ({
        url: `books/${id}/`,
        method: "PUT",
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "Book", id }],
    }),
    patchBook: build.mutation({
      query: ({ id, ...data }) => ({
        url: `books/${id}/`,
        method: "PATCH",
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "Book", id }],
    }),
    deleteBook: build.mutation({
      query: (id) => ({ url: `books/${id}/`, method: "DELETE" }),
      invalidatesTags: [{ type: "Book", id: "LIST" }],
    }),
    approveBook: build.mutation({
      query: (id) => ({ url: `books/${id}/approve/`, method: "POST" }),
      invalidatesTags: (result, error, id) => [{ type: "Book", id }],
    }),
    rejectBook: build.mutation({
      query: (id) => ({ url: `books/${id}/reject/`, method: "POST" }),
      invalidatesTags: (result, error, id) => [{ type: "Book", id }],
    }),

    //
    // BookLogs
    //
    fetchBookLogs: build.query({
      query: (params) => ({ url: "booklogs/", params }),
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "BookLog", id })),
              { type: "BookLog", id: "LIST" },
            ]
          : [{ type: "BookLog", id: "LIST" }],
    }),
    fetchBookLogById: build.query({
      query: (id) => `booklogs/${id}/`,
      providesTags: (result, error, id) => [{ type: "BookLog", id }],
    }),
    createBookLog: build.mutation({
      query: (data) => ({ url: "booklogs/", method: "POST", body: data }),
      invalidatesTags: [{ type: "BookLog", id: "LIST" }],
    }),
    updateBookLog: build.mutation({
      query: ({ id, ...data }) => ({
        url: `booklogs/${id}/`,
        method: "PUT",
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "BookLog", id }],
    }),
    patchBookLog: build.mutation({
      query: ({ id, ...data }) => ({
        url: `booklogs/${id}/`,
        method: "PATCH",
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "BookLog", id }],
    }),
    deleteBookLog: build.mutation({
      query: (id) => ({ url: `booklogs/${id}/`, method: "DELETE" }),
      invalidatesTags: [{ type: "BookLog", id: "LIST" }],
    }),

    //
    // Quotes
    //
    fetchQuotes: build.query({
      query: (params) => ({ url: "quotes/", params }),
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "Quote", id })),
              { type: "Quote", id: "LIST" },
            ]
          : [{ type: "Quote", id: "LIST" }],
    }),
    fetchQuoteById: build.query({
      query: (id) => `quotes/${id}/`,
      providesTags: (result, error, id) => [{ type: "Quote", id }],
    }),
    createQuote: build.mutation({
      query: (data) => ({ url: "quotes/", method: "POST", body: data }),
      invalidatesTags: [{ type: "Quote", id: "LIST" }],
    }),
    updateQuote: build.mutation({
      query: ({ id, ...data }) => ({
        url: `quotes/${id}/`,
        method: "PUT",
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "Quote", id }],
    }),
    patchQuote: build.mutation({
      query: ({ id, ...data }) => ({
        url: `quotes/${id}/`,
        method: "PATCH",
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "Quote", id }],
    }),
    deleteQuote: build.mutation({
      query: (id) => ({ url: `quotes/${id}/`, method: "DELETE" }),
      invalidatesTags: [{ type: "Quote", id: "LIST" }],
    }),

    //
    // Likes
    //
    fetchLikes: build.query({
      query: (params) => ({ url: "likes/", params }),
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "Like", id })),
              { type: "Like", id: "LIST" },
            ]
          : [{ type: "Like", id: "LIST" }],
    }),
    fetchLikeById: build.query({
      query: (id) => `likes/${id}/`,
      providesTags: (result, error, id) => [{ type: "Like", id }],
    }),
    createLike: build.mutation({
      query: (data) => ({ url: "likes/", method: "POST", body: data }),
      invalidatesTags: (result, error, data) => [{ type: "Like", id: "LIST" }],
    }),
    deleteLike: build.mutation({
      query: (id) => ({ url: `likes/${id}/`, method: "DELETE" }),
      invalidatesTags: [{ type: "Like", id: "LIST" }],
    }),

    //
    // Shares
    //
    fetchShares: build.query({
      query: (params) => ({ url: "shares/", params }),
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "Share", id })),
              { type: "Share", id: "LIST" },
            ]
          : [{ type: "Share", id: "LIST" }],
    }),
    fetchShareById: build.query({
      query: (id) => `shares/${id}/`,
      providesTags: (result, error, id) => [{ type: "Share", id }],
    }),
    createShare: build.mutation({
      query: (data) => ({ url: "shares/", method: "POST", body: data }),
      invalidatesTags: (result, error, data) => [{ type: "Share", id: "LIST" }],
    }),
    deleteShare: build.mutation({
      query: (id) => ({ url: `shares/${id}/`, method: "DELETE" }),
      invalidatesTags: [{ type: "Share", id: "LIST" }],
    }),
  }),
});
