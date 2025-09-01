import React, { useRef, useState, useEffect } from "react";
import {
  Box,
  Button,
  Typography,
  IconButton,
  CircularProgress,
} from "@mui/material";
import DeleteRoundedIcon from "@mui/icons-material/DeleteRounded";

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 МБ

const ImageUpload = ({
  label,
  value,
  onChange,
  required = false,
  ...props
}) => {
  // Состояния для ошибки, превью и индикатора загрузки
  const [error, setError] = useState("");
  const [previewUrl, setPreviewUrl] = useState(value ? value.previewUrl : null);
  const [uploading, setUploading] = useState(false);

  // Ссылка на input, который скрыт
  const inputRef = useRef();

  // Обработчик выбора файла
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Валидация типа файла (должно быть изображение)
    if (!file.type.startsWith("image/")) {
      setError("Выберите изображение.");
      return;
    }
    // Валидация размера файла
    if (file.size > MAX_FILE_SIZE) {
      setError("Размер файла не должен превышать 5 МБ.");
      return;
    }

    setError("");
    setUploading(true);
    // Создаем временную ссылку для предпросмотра
    const preview = URL.createObjectURL(file);
    setPreviewUrl(preview);
    // Имитация загрузки (реальную логику можно добавить позже)
    onChange && onChange({ file, previewUrl: preview });
    setUploading(false);
  };

  // Обработчик удаления изображения
  const handleDelete = () => {
    setPreviewUrl(null);
    onChange && onChange(null);
  };

  // При размонтировании освобождаем объектную ссылку
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  return (
    <Box>
      {/* Скрытый input для выбора файла */}
      <input
        accept="image/*"
        type="file"
        hidden
        ref={inputRef}
        onChange={handleFileChange}
      />

      {/* Если превью отсутствует, отображаем кнопку загрузки */}
      {!previewUrl && (
        <Button
          variant="contained"
          color="primary"
          fullWidth
          type="button"
          onClick={() => inputRef.current?.click()}
        >
          {uploading ? <CircularProgress size={20} /> : "Загрузить изображение"}
        </Button>
      )}

      {/* Если превью загружено, выводим текст label вместо кнопки */}
      {previewUrl && (
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            padding: "10px",
            border: "1px solid #8d9095",
            borderRadius: "4px",
          }}
        >
          <Typography
            variant="body2"
            sx={{ mt: 1, marginTop: 0, color: "rgba(0, 0, 0, 0.87)" }}
            onClick={() => inputRef.current?.click()}
            style={{ cursor: "pointer" }}
          >
            {label}
          </Typography>
          <Box
            mt={2}
            position="relative"
            display="inline-block"
            sx={{ marginTop: 0 }}
          >
            <img
              src={previewUrl}
              alt="Превью"
              style={{
                width: "150px",
                height: "100px",
                borderRadius: 20,
                objectFit: "cover",
              }}
            />
            <IconButton
              size="small"
              onClick={handleDelete}
              sx={{
                position: "absolute",
                top: 0,
                right: 0,
                color: "white",
              }}
            >
              <DeleteRoundedIcon fontSize="small" />
            </IconButton>
          </Box>
        </Box>
      )}

      {error && (
        <Typography variant="caption" color="error" sx={{ mt: 1 }}>
          {error}
        </Typography>
      )}
    </Box>
  );
};

export default ImageUpload;
