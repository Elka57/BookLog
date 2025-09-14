import { Typography, Box } from "@mui/material";
import React from "react";


const SendMailPage = () => {

  return (
    <Box sx={{paddingTop: '50px'}}>
      <Typography variant="h6" sx={{textAlign: 'center'}}>
        Проверьте адрес электронной почты, указанный при регистрации, на него выслано письмо с дальнейшими инструкциями 
      </Typography>
    </Box>
    
  )
};

export default SendMailPage;