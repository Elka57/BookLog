import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 минут кэша
      cacheTime: 1000 * 60 * 30, // 30 минут хранения
      refetchOnWindowFocus: false, // не дергать при фокусе окна
    },
  },
});
