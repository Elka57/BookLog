import { Typography, Box } from "@mui/material";
import React from "react";
import { useFetchCurrentUserQuery } from "../store/authApiSlice";
import EmailConfirmed from "../bars/EmailConfirmed";


const Office = () => {
  const { data: user, isLoading } = useFetchCurrentUserQuery();

  if (isLoading) {
      return <Typography>Загрузка...</Typography>;
  };

  if (!user) {
    return <Typography>Авторизуйтесь для просмотра личного кабинета</Typography>
  };

  return (
    <Box>
      <EmailConfirmed user={user} />
    </Box>
  );
};

export default Office;