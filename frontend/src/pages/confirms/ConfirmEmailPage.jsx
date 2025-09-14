import { useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useConfirmEmailMutation } from "../../store/authApiSlice";
import { Typography } from "@mui/material";

export default function ConfirmEmailPage() {
  const { key } = useParams();
  const navigate = useNavigate();
  const [confirmEmail, { isLoading, isSuccess, isError }] = useConfirmEmailMutation();

  useEffect(() => {
    if (key) confirmEmail({ key });
  }, [key, confirmEmail]);

  if (isLoading) return <Typography variant="h6">Подтверждаем email…</Typography>;
  if (isError) return <Typography variant="h6">Ошибка: {isError?.data?.detail || isError.error}</Typography>;
  if (isSuccess) {
    setTimeout(() => navigate("/*"), 1500);
    return <Typography variant="h6">Почта подтверждена! Вы будете перенаправлены на главную страницу.</Typography>;
  }
  return null;
}
