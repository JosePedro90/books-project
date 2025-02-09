import { VStack, Input, Button, Box, Heading } from "@chakra-ui/react";
import { Formik, Form, Field } from "formik";
import { BookUpdate } from "../types/Book";
import { FormControl, FormLabel } from "@chakra-ui/form-control";

interface BookDetailsFormProps {
  initialValues: Partial<BookUpdate>;
  onSubmit: (values: Partial<BookUpdate>) => void;
}

const BookDetailsForm: React.FC<BookDetailsFormProps> = ({
  initialValues,
  onSubmit,
}) => {
  return (
    <Box p={4} borderWidth="1px" borderRadius="lg" boxShadow="md">
      <Heading mb={6} textAlign="left" size={"lg"}>
        Edit Book Details
      </Heading>
      <Formik initialValues={initialValues} onSubmit={onSubmit}>
        <Form>
          <VStack align="stretch">
            <FormControl>
              <FormLabel>Title</FormLabel>
              <Field as={Input} name="title" required />
            </FormControl>

            <FormControl>
              <FormLabel>Original Title</FormLabel>
              <Field as={Input} name="original_title" />
            </FormControl>

            <FormControl>
              <FormLabel>Authors (comma-separated)</FormLabel>
              <Field as={Input} name="authors_input" required />
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
                step="0.01"
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

            <FormControl>
              <FormLabel>Language Code</FormLabel>
              <Field as={Input} name="language_code" />
            </FormControl>

            <Button
              marginTop={5}
              type="submit"
              colorScheme="blue"
              loadingText="Saving..."
            >
              Save Changes
            </Button>
          </VStack>
        </Form>
      </Formik>
    </Box>
  );
};

export default BookDetailsForm;
