import React, { useState } from "react";
import { useResendEmailMutation } from "../store/authApiSlice";
import {
  Alert,
  CircularProgress,
  Button,
  Snackbar,
  Box,
} from "@mui/material";
import EmailRoundedIcon from "@mui/icons-material/EmailRounded";

const EmailConfirmed = ({ user }) => {
  // локальное состояние для поля email и ошибки в нём
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success",
  });

  const [resendEmail, { isLoading, isError }] = useResendEmailMutation();

  const handleResendEmail = async () => {
    try {
      // передаём объект { email } в мутацию
      await resendEmail({ 'email': user.email }).unwrap();
      setSnackbar({
        open: true,
        message: "Ссылка для подтверждения отправлена на вашу почту.",
        severity: "success",
      });
    } catch {
      setSnackbar({
        open: true,
        message:
          "Ошибка при отправке. Проверьте адрес электронной почты в настройках.",
        severity: "error",
      });
    }
  };

  return (
    <>
      {!user.email_confirmed && (
        <Alert
          severity="warning"
          sx={{ fontSize: "1rem", fontWeight: "bold", mb: 2 }}
        >
          <Box display="flex" flexDirection="column" gap={1}>
            Электронная почта не подтверждена!
            <Button
              variant="text"
              onClick={handleResendEmail}
              color="warning"
              startIcon={
                isLoading ? (
                  <CircularProgress size={20} color="inherit" />
                ) : (
                  <EmailRoundedIcon />
                )
              }
              disabled={isLoading || isError || !user.email}
            >
              {isLoading ? "Отправляем..." : "Отправить повторно"}
            </Button>
          </Box>
        </Alert>
      )}

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() =>
          setSnackbar((prev) => ({
            ...prev,
            open: false,
          }))
        }
      >
        <Alert
          onClose={() =>
            setSnackbar((prev) => ({
              ...prev,
              open: false,
            }))
          }
          severity={snackbar.severity}
          sx={{ width: "100%" }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </>
  );
};

export default EmailConfirmed;
