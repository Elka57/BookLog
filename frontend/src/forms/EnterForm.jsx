// src/components/EnterForm.jsx
import React, { useState } from "react";
import { Box, TextField, Button, Typography, Alert } from "@mui/material";
import { useLoginMutation } from "../store/authApiSlice"; // ← вместо useLoginRestAuthMutation
import { useDispatch } from "react-redux";
import { authApi } from "../store/authApiSlice"; // для вызова fetchCurrentUser, если нужно
import { logout as clearAuth } from "../store/authSlice"; // на случай ошибки
import { useNavigate } from "react-router-dom";


const EnterForm = ({ onLoginSuccess, onForgotPassword }) => {
  const dispatch = useDispatch();
  const [form, setForm] = useState({ username: "", password: "" });
  const [login, { isLoading, error }] = useLoginMutation(); // ← новый хук
  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // 1) Сессия ставится под капотом (httpOnly cookie)
      await login(form).unwrap();

      // 2) Если ваш authApi.login.onQueryStarted НЕ диспатчит fetchCurrentUser,
      //    вы можете запустить его здесь:
      dispatch(authApi.endpoints.fetchCurrentUser.initiate());

      // 3) Вызываем коллбэк успешного входа в систему
      onLoginSuccess?.();
      navigate('/', { replace: true });
    } catch (err) {
      console.error("Login failed:", err);

      // В случае критической ошибки можно сбросить стейт
      dispatch(clearAuth());
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        width: 1,
        maxWidth: 360,
        mx: "auto",
        mt: 4,
        display: "flex",
        flexDirection: "column",
        gap: 2,
      }}
    >
      <Typography variant="h5" align="center">
        Вход в систему
      </Typography>

      {error?.data?.detail && (
        <Alert severity="error">{error.data.detail}</Alert>
      )}

      <TextField
        label="Username или Email"
        name="username"
        value={form.username}
        onChange={handleChange}
        required
      />

      <TextField
        label="Пароль"
        name="password"
        type="password"
        value={form.password}
        onChange={handleChange}
        required
      />

      <Box sx={{ display: "flex", justifyContent: "space-between" }}>
        <Button type="submit" variant="contained" disabled={isLoading}>
          {isLoading ? "Входим…" : "Войти"}
        </Button>
        <Button variant="text" onClick={onForgotPassword}>
          Забыли пароль?
        </Button>
      </Box>
    </Box>
  );
};

export default EnterForm;
