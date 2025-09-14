// src/components/RegisterForm.jsx

import React from "react";
import { useForm, Controller } from "react-hook-form";
import {
  Box,
  TextField,
  Button,
  Typography,
  MenuItem,
  Alert,
} from "@mui/material";
import ChangePicture from "../fields/ChangePicture";
import { useRegisterMutation } from "../store/authApiSlice";

const userTypeOptions = [
  { value: 0, label: "Блогер - ведущий дневник" },
  { value: 1, label: "Читатель" },
];

const RegisterForm = ({ onRegisterSuccess }) => {
  const {
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm({
    defaultValues: {
      username: "",
      email: "",
      name: "",
      password1: "",
      password2: "",
      user_type: 1,
      logo: null,
    },
  });

  const [register, { isLoading, error }] = useRegisterMutation();

  const onSubmit = async (values) => {
    const formData = new FormData();
    formData.append("username", values.username);
    formData.append("email", values.email);
    formData.append("name", values.name);
    formData.append("password1", values.password1);
    formData.append("password2", values.password2);
    formData.append("user_type", values.user_type);
    if (values.logo?.file) {
      formData.append("logo", values.logo.file);
    }

    try {
      await register(formData).unwrap();
      reset();
      onRegisterSuccess?.();
    } catch (e) {
      console.error("Registration failed", e);
    }
  };

  // Вывод ошибок полей из dj-rest-auth
  const renderFieldErrors = (field) => {
    const fieldErrors = error?.data?.[field];
    if (Array.isArray(fieldErrors)) {
      return fieldErrors.map((msg, i) => (
        <Alert key={i} severity="error">
          {msg}
        </Alert>
      ));
    }
    return null;
  };

  // Общие ошибки (non_field_errors)
  const generalErrors = error?.data?.non_field_errors;

  return (
    <Box
      component="form"
      onSubmit={handleSubmit(onSubmit)}
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
        Регистрация
      </Typography>

      {Array.isArray(generalErrors) &&
        generalErrors.map((msg, i) => (
          <Alert key={i} severity="error">
            {msg}
          </Alert>
        ))}

      {/* Логин */}
      <Controller
        name="username"
        control={control}
        rules={{ required: "Обязательное поле" }}
        render={({ field }) => (
          <TextField
            {...field}
            label="Логин"
            error={!!errors.username}
            helperText={errors.username?.message}
            required
          />
        )}
      />
      {renderFieldErrors("username")}

      {/* Email */}
      <Controller
        name="email"
        control={control}
        rules={{ required: "Обязательное поле" }}
        render={({ field }) => (
          <TextField
            {...field}
            label="E-mail"
            type="email"
            error={!!errors.email}
            helperText={errors.email?.message}
            required
          />
        )}
      />
      {renderFieldErrors("email")}

      {/* Имя */}
      <Controller
        name="name"
        control={control}
        render={({ field }) => <TextField {...field} label="Имя" />}
      />
      {renderFieldErrors("name")}

      {/* Пароль */}
      <Controller
        name="password1"
        control={control}
        rules={{ required: "Обязательное поле" }}
        render={({ field }) => (
          <TextField
            {...field}
            label="Пароль"
            type="password"
            error={!!errors.password1}
            helperText={errors.password1?.message}
            required
          />
        )}
      />
      {renderFieldErrors("password1")}

      {/* Подтверждение пароля */}
      <Controller
        name="password2"
        control={control}
        rules={{ required: "Обязательное поле" }}
        render={({ field }) => (
          <TextField
            {...field}
            label="Подтвердите пароль"
            type="password"
            error={!!errors.password2}
            helperText={errors.password2?.message}
            required
          />
        )}
      />
      {renderFieldErrors("password2")}

      {/* Выбор типа пользователя */}
      <Controller
        name="user_type"
        control={control}
        render={({ field }) => (
          <TextField {...field} select label="Выберите тип">
            {userTypeOptions.map((opt) => (
              <MenuItem key={opt.value} value={opt.value}>
                {opt.label}
              </MenuItem>
            ))}
          </TextField>
        )}
      />
      {renderFieldErrors("user_type")}

      {/* Загрузка лого */}
      <Controller
        name="logo"
        control={control}
        render={({ field }) => (
          <ChangePicture
            label="Логотип профиля"
            value={field.value}
            onChange={field.onChange}
            onBlur={field.onBlur}
            imgStyle={{ width: 100, height: 100, objectFit: "cover" }}
          />
        )}
      />
      {renderFieldErrors("logo")}

      <Button type="submit" variant="contained" disabled={isLoading}>
        {isLoading ? "Регистрируем…" : "Зарегистрироваться"}
      </Button>
    </Box>
  );
};

export default RegisterForm;
