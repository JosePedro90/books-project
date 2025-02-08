import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Box, Heading, Button, VStack, Input, Text } from "@chakra-ui/react";
import { Formik, Form, Field } from "formik";
import { Book } from "../types/Book";
import { updateBook } from "../api/books";
import api from "../api/axios";
import ProtectedRoute from "../components/ProtectedRoute";
import { FormControl, FormLabel } from "@chakra-ui/form-control";

const BookDetailsPage = () => {
  const { id } = useParams<{ id: string }>();
  const [book, setBook] = useState<Book | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  console.log("aqui", id);

  useEffect(() => {
    const fetchBookDetails = async () => {
      try {
        const response = await api.get<Book>(`/api/books/${id}/`);
        setBook(response.data);
      } catch (error) {
        console.error("Error fetching book details:", error);
        // toast({
        //   title: "Error",
        //   description: "Failed to fetch book details",
        //   status: "error",
        //   duration: 3000,
        //   isClosable: true,
        // });
      } finally {
        setIsLoading(false);
      }
    };

    fetchBookDetails();
  }, [id]);

  const handleSubmit = async (values: Partial<Book>) => {
    try {
      if (!id) return;

      const updatedBook = await updateBook(Number(id), values);
      setBook(updatedBook);
      // toast({
      //   title: "Success",
      //   description: "Book updated successfully",
      //   status: "success",
      //   duration: 2000,
      //   isClosable: true,
      // });
      navigate("/books");
    } catch (error) {
      console.error("Error updating book:", error);
      // toast({
      //   title: "Error",
      //   description: "Failed to update book",
      //   status: "error",
      //   duration: 3000,
      //   isClosable: true,
      // });
    }
  };

  if (isLoading) {
    return <Box p={4}>Loading book details...</Box>;
  }

  if (!book) {
    return <Box p={4}>Book not found</Box>;
  }

  return (
    <ProtectedRoute>
      <Box p={4} maxW="800px" mx="auto">
        <Heading mb={6}>Edit Book Details</Heading>

        <Formik
          initialValues={{
            title: book.title,
            authors: book.authors.map((a) => a.name).join(", "),
            isbn: book.isbn,
            isbn13: book.isbn13,
            average_rating: book.average_rating,
            original_publication_year: book.original_publication_year,
          }}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting }) => (
            <Form>
              <VStack spacing={4} align="stretch">
                <FormControl>
                  <FormLabel>Title</FormLabel>
                  <Field as={Input} name="title" required />
                </FormControl>

                <FormControl>
                  <FormLabel>Authors (comma-separated)</FormLabel>
                  <Field as={Input} name="authors" required />
                </FormControl>

                <FormControl>
                  <FormLabel>ISBN</FormLabel>
                  <Field as={Input} name="isbn" />
                </FormControl>

                <FormControl>
                  <FormLabel>ISBN13</FormLabel>
                  <Field as={Input} name="isbn13" />
                </FormControl>

                <FormControl>
                  <FormLabel>Average Rating</FormLabel>
                  <Field
                    as={Input}
                    name="average_rating"
                    type="number"
                    min="0"
                    max="5"
                    step="0.1"
                  />
                </FormControl>

                <FormControl>
                  <FormLabel>Publication Year</FormLabel>
                  <Field
                    as={Input}
                    name="original_publication_year"
                    type="number"
                  />
                </FormControl>

                <Button
                  type="submit"
                  colorScheme="blue"
                  isLoading={isSubmitting}
                  loadingText="Saving..."
                >
                  Save Changes
                </Button>
              </VStack>
            </Form>
          )}
        </Formik>
      </Box>
    </ProtectedRoute>
  );
};

export default BookDetailsPage;
