// src/components/ChangePicture.jsx
import React, { useState, useEffect } from "react";
import { Box, IconButton } from "@mui/material";
import BackspaceRoundedIcon from "@mui/icons-material/BackspaceRounded";
import ImageUpload from "../uploads/ImageUpload";

const ChangePicture = ({
  // URL превью из сервера (initial)
  urlPicture,
  // CSS-стили для <img>
  imgStyle,
  // подпись для загрузчика
  label,
  // props от Controller: value = { file, previewUrl } или null
  value,
  onChange,
  onBlur,
  required = false,
  ...rest
}) => {
  const [hasPreview, setHasPreview] = useState(Boolean(urlPicture || value));

  // синхронизируем превью, если form сбрасывается или приходит новый url
  useEffect(() => {
    setHasPreview(Boolean(urlPicture || value));
  }, [urlPicture, value]);

  const handleFileChange = (fileObj) => {
    onChange(fileObj);
    setHasPreview(Boolean(fileObj));
  };

  const handleReset = () => {
    onChange(null);
    onBlur?.();
    setHasPreview(false);
  };

  // Определяем, откуда брать картинку: из form State (новая) или из server URL
  const previewSrc = value?.previewUrl || urlPicture || "";

  return (
    <Box mt={2}>
      {hasPreview ? (
        <Box
          position="relative"
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <img src={previewSrc} alt="Превью" style={imgStyle} />
          <IconButton
            size="small"
            onClick={handleReset}
            sx={{ position: "absolute", top: 0, right: 0 }}
          >
            <BackspaceRoundedIcon fontSize="small" />
          </IconButton>
        </Box>
      ) : (
        <ImageUpload
          fullWidth
          label={label}
          value={value}
          onChange={handleFileChange}
          onBlur={onBlur}
          required={required}
          {...rest}
        />
      )}
    </Box>
  );
};

export default ChangePicture;
