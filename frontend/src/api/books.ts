import { Book } from "../types/Book";
import api from "./axios";
import { useInfiniteQuery } from "@tanstack/react-query";

export const useInfiniteBooks = (
  search: string,
  ordering: string,
  reservationStatus: string
) => {
  const {
    data,
    isLoading,
    error,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    initialPageParam: 1,
    queryKey: ["books", search, ordering, reservationStatus],
    queryFn: async ({ pageParam = 1 }) => {
      try {
        const response = await api.get("/api/books/", {
          params: {
            page: pageParam,
            search,
            ordering,
            reserved:
              reservationStatus === "all"
                ? undefined
                : reservationStatus === "reserved",
          },
        });
        return response.data;
      } catch (error) {
        console.error("Error fetching books:", error);
        return { results: [], count: 0 };
      }
    },
    getNextPageParam: (lastPage) => {
      if (lastPage.next) {
        const url = new URL(lastPage.next);
        const nextPage = url.searchParams.get("page");
        return nextPage ? parseInt(nextPage, 10) : undefined;
      }
      return undefined;
    },
  });

  const books = data?.pages.flatMap((page) => page.results) || [];

  return {
    data: books,
    isLoading,
    error,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  };
};

export const updateBook = async (
  id: number,
  data: Partial<Book>
): Promise<Book> => {
  try {
    const response = await api.put(`/api/books/${id}/`, data);
    return response.data;
  } catch (error) {
    console.error("Error updating book:", error);
    throw error; // Re-throw the error to be handled by the caller
  }
};

export const getBook = async (id: number): Promise<Book> => {
  try {
    const response = await api.get(`/api/books/${id}/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching book:", error);
    throw error;
  }
};
