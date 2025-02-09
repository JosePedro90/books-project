import { useParams, useNavigate } from "react-router-dom";
import { Box, Flex, Heading, Spinner, Text } from "@chakra-ui/react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Book } from "../types/Book";
import { getBook, updateBook } from "../api/books";
import { toaster } from "../components/ui/toaster";

import BookDetailsForm from "../components/BookDetailsForm";
import BookReservations from "../components/BookReservations";
import { CloseButton } from "../components/ui/close-button";

const BookDetailsPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const {
    data: book,
    isLoading,
    isError,
    refetch,
  } = useQuery<Book>({
    queryKey: ["book", id],
    queryFn: () => getBook(Number(id)),
    enabled: !!id,
    retry: false,
  });

  const mutation = useMutation({
    mutationFn: (values: Partial<Book>) => updateBook(Number(id), values),
    onSuccess: (updatedBook: Book) => {
      queryClient.setQueryData(["book", id], updatedBook);
      queryClient.invalidateQueries({ queryKey: ["books"] });
      toaster.create({
        description: "Book updated successfully",
        duration: 2000,
        type: "success",
      });
    },
    onError: (error) => {
      console.error("Update error:", error);
      toaster.create({
        title: "Error",
        description: "Failed to update book",
        type: "error",
        duration: 3000,
      });
      refetch();
    },
  });

  const handleSubmit = async (values: Partial<Book>) => {
    mutation.mutate(values);
  };

  if (isLoading) {
    return (
      <Box p={4} textAlign="center">
        <Spinner />
        <Text mt={2}>Loading book details...</Text>
      </Box>
    );
  }

  if (isError || !book) {
    return (
      <Box p={4} textAlign="center">
        <Text>Book not found</Text>
      </Box>
    );
  }

  return (
    <Box p={4} maxW="800px" mx="auto">
      <Flex align="center" justifyContent="center" mb={4} position="relative">
        <CloseButton
          aria-label="Close"
          size="xs"
          onClick={() => navigate("/books")}
          position="absolute"
          left={1}
        />
        <Heading textAlign="center">Admin Page</Heading>
      </Flex>
      <Box mb={4}>
        <BookDetailsForm
          initialValues={{
            title: book.title,
            original_title: book.original_title,
            authors_input: book.authors.map((a) => a.name).join(", ") || "",
            isbn: book.isbn,
            isbn13: book.isbn13,
            average_rating: book.average_rating,
            original_publication_year: book.original_publication_year,
            language_code: book.language_code,
            image_url: book.image_url,
          }}
          onSubmit={handleSubmit}
        />
      </Box>
      <BookReservations bookId={book.id} />
    </Box>
  );
};

export default BookDetailsPage;
