import { useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useVerifyEmailMutation } from "../../store/authApiSlice";
import { Typography } from "@mui/material";

export default function ConfirmEmailPage() {
  const { key } = useParams();
  const navigate = useNavigate();
  const [verifyEmail, { isLoading, isError, isSuccess, error }] =
    useVerifyEmailMutation();

  useEffect(() => {
    verifyEmail({ key });
  }, [key, verifyEmail]);

  if (isLoading) return <Typography variant="h6">Подтверждаем email…</Typography>;
  if (isError) return <Typography variant="h6">Ошибка: {error?.data?.detail || error.error}</Typography>;
  if (isSuccess) {
    setTimeout(() => navigate("/login"), 1500);
    return <Typography variant="h6">Почта подтверждена! Сейчас перенаправим на вход…</Typography>;
  }
  return null;
}
