import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Provider } from "react-redux";
import { QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { queryClient } from "./queryClient";
import App from "./App";
import { store } from "./store/store.js";
import ConfirmEmailPage from "./pages/confirms/ConfirmEmailPage";
import { AuthProvider } from "./context/AuthContext";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <Provider store={store}>
        <AuthProvider>
          <BrowserRouter>
            <Routes>
              {/* 1) страница подтверждения */}
              <Route path="/confirm-email/:key" element={<ConfirmEmailPage />} />

              {/* 2) страница входа */}
              <Route path="/login" element={<App page={0} />} />

              {/* 2) основной SPA */}
              <Route path="/*" element={<App />} />
            </Routes>
          </BrowserRouter>
        </AuthProvider>
      </Provider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </StrictMode>
);
