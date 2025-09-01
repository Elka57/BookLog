import { Button, ButtonGroup, Typography } from "@mui/material";
import React from "react";
import AddBoxRoundedIcon from "@mui/icons-material/AddBoxRounded";

const ButtonMenu = ({ label, callbackPage, callbackCreate }) => (
  <ButtonGroup variant="contained">
    {/* Передаём колбэк напрямую — React вызовет его при клике */}
    <Button onClick={callbackPage}>{label}</Button>

    <Button size="small" onClick={callbackCreate}>
      <AddBoxRoundedIcon />
    </Button>
  </ButtonGroup>
);

export default ButtonMenu;