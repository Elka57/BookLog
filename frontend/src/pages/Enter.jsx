import { Typography, Box, ToggleButtonGroup, ToggleButton } from "@mui/material";
import React, { useState } from "react";
import EnterForm from "../forms/EnterForm";
import RegisterForm from "../forms/RegisterForm";

const Enter = ({ onLoginSuccess, onForgotPassword, onRegisterSuccess }) => {
  const [currentForm, setCurrentForm] = useState(0);

  const forms = {
    0: (
      <EnterForm
        onLoginSuccess={onLoginSuccess}
        onForgotPassword={onForgotPassword}
      />
    ),
    1: <RegisterForm 
        onRegisterSuccess={onRegisterSuccess}
      />,
  };

  return (
    <Box>
      <Typography>Страница входа/регистрации</Typography>
      <ToggleButtonGroup
        exclusive
        value={currentForm}
        onChange={(event, newValue) => {
          if (newValue === null) return;
          setCurrentForm(newValue);
        }}
      >
        <ToggleButton value={0}>
          <Typography variant="button">Вход</Typography>
        </ToggleButton>
        <ToggleButton value={1}>
          <Typography variant="button">Регистрация</Typography>
        </ToggleButton>
      </ToggleButtonGroup>
      <Box>{forms[currentForm] || null}</Box>
    </Box>
  );
};

export default Enter;