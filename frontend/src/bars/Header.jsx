import { Typography, Box } from "@mui/material";
import React from "react";
import ButtonMenu from "../buttons/ButtonMenu";
import AuthorizationBar from "./AuthorizationBar";


const Header = ({ page, onChangePage, create }) => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
      }}
    >
      <Box>
        <ButtonMenu
          label="Дневники"
          callbackPage={() => onChangePage(2)} // передаём нужный индекс
          callbackCreate={() => create(2)}
        />
        <ButtonMenu
          label="Цитаты"
          callbackPage={() => onChangePage(3)} // передаём нужный индекс
          callbackCreate={() => create(3)}
        />
        <ButtonMenu
          label="Книги"
          callbackPage={() => onChangePage(4)}
          callbackCreate={() => create(4)}
        />
        <ButtonMenu
          label="Авторы"
          callbackPage={() => onChangePage(5)}
          callbackCreate={() => create(5)}
        />
        <ButtonMenu
          label="Жанры"
          callbackPage={() => onChangePage(6)}
          callbackCreate={() => create(6)}
        />
      </Box>
      <AuthorizationBar callbackPage={onChangePage} />
    </Box>
  );
};

export default Header;

