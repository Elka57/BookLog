// src/components/AuthorizationBar.jsx
import React from "react";
import {
  Box,
  Typography,
  Button,
  Chip,
  Avatar,
  IconButton,
} from "@mui/material";
import { useDispatch } from "react-redux";
import {
  useFetchCurrentUserQuery,
  useLogoutMutation,
} from "../store/authApiSlice";
import { logout as clearAuth } from "../store/authSlice";
import ExitToAppRoundedIcon from "@mui/icons-material/ExitToAppRounded";
import { authApi } from "../store/authApiSlice";

const AuthorizationBar = ({ callbackPage }) => {
  const dispatch = useDispatch();

  // всегда пытаемся загрузить профиль
  const { data: user, isLoading } = useFetchCurrentUserQuery();

  const [logoutApi, { isLoading: isLoggingOut }] = useLogoutMutation();

  if (isLoading) {
    return <Typography>Загрузка...</Typography>;
  }

  // если нет пользователя — показываем кнопку входа
  if (!user) {
    return (
      <Button variant="text" onClick={() => callbackPage(0)}>
        Вход/Регистрация
      </Button>
    );
  }

  // при наличии пользователя — отображаем имя и кнопку выхода
  const handleLogout = async () => {
    try {
      await logoutApi().unwrap();
    } catch {
      // даже при ошибке логаута чистим стейт
    } finally {
      dispatch(authApi.util.resetApiState());
      dispatch(clearAuth());
    }
  };

  return (
    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
      <Chip
        avatar={<Avatar src={user.logo ?? undefined} />}
        label={user.name || user.username}
        variant="outlined"
        onClick={() => callbackPage(1)}
      />
      <IconButton
        aria-label="exit"
        onClick={handleLogout}
        disabled={isLoggingOut}
      >
        <ExitToAppRoundedIcon />
      </IconButton>
    </Box>
  );
};

export default AuthorizationBar;
