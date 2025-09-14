import { Box, Container, Typography } from "@mui/material"
import Header from "./bars/Header";
import { useEffect, useState } from "react";
import Enter from "./pages/Enter";
import Office from "./pages/Office";
import BookLogs from "./pages/BookLogs";
import Quoters from "./pages/Quoters";
import Books from "./pages/Books";
import Authors from "./pages/Authors";
import Genres from "./pages/Genres";
import { useLocation } from "react-router-dom";
import { useFetchCurrentUserQuery } from "./store/authApiSlice";
import SendMailPage from "./pages/confirms/SendMailPage";

const App = ({page=3}) => {
    const location = useLocation();
    const [currentPage, setCurrentPage] = useState(page);

    useEffect(() => {
      if (location.state?.page != null) {
        setCurrentPage(location.state.page);
      }
    }, [location.state]);


    useFetchCurrentUserQuery();

    const pages = {
      0: <Enter 
          onLoginSuccess={() => setCurrentPage(3)}      // после логина → страница цитат
          onForgotPassword={() => setCurrentPage(2)}    // TODO: Сделать страницу забыл пароль
          onRegisterSuccess={() => setCurrentPage(7)}  // TODO: Сделать страницу что вам направлено письмо и проверьте почту
      />,
      1: <Office />,
      2: <BookLogs />,
      3: <Quoters />,
      4: <Books />,
      5: <Authors />,
      6: <Genres />,
      7: <SendMailPage />,
    };

    const handleChangePage = (newVal) => {
      if (newVal !== null) {
        setCurrentPage(newVal);
      }
    };

    const handleCreate = (newVal) => {
      console.log("Хотим создать:", newVal);
    };

    return (
      <Container>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "flex-start",
          }}
        >
          <Header
            page={currentPage}
            onChangePage={handleChangePage}
            create={handleCreate}
          />

          <Box>{pages[currentPage]}</Box>
        </Box>
      </Container>
    );

};

export default App;