import { VStack, Input, Button, Box, Heading, Text } from "@chakra-ui/react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { BookUpdate } from "../types/Book";
import {
  FormControl,
  FormLabel,
  FormErrorMessage,
} from "@chakra-ui/form-control";

interface BookDetailsFormProps {
  initialValues: Partial<BookUpdate>;
  onSubmit: (values: Partial<BookUpdate>) => void;
}

const validationSchema = Yup.object().shape({
  title: Yup.string().required("Title is required"),
  original_title: Yup.string(),
  authors_input: Yup.string().required("Authors are required"),
  isbn: Yup.string(),
  isbn13: Yup.string(),
  average_rating: Yup.number()
    .min(0, "Rating must be at least 0")
    .max(5, "Rating must be at most 5"),
  original_publication_year: Yup.number(),
  language_code: Yup.string(),
  image_url: Yup.string().url("Invalid URL format"),
});

const BookDetailsForm: React.FC<BookDetailsFormProps> = ({
  initialValues,
  onSubmit,
}) => {
  return (
    <Box p={4} borderWidth="1px" borderRadius="lg" boxShadow="md">
      <Heading mb={6} textAlign="left" size={"lg"}>
        Edit Book Details
      </Heading>
      <Formik
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={onSubmit}
      >
        <Form>
          <VStack align="stretch">
            <FormControl>
              <FormLabel>Title</FormLabel>
              <Field as={Input} name="title" required />
              <ErrorMessage name="title" component={FormErrorMessage} />
            </FormControl>

            <FormControl>
              <FormLabel>Original Title</FormLabel>
              <Field as={Input} name="original_title" />
              <ErrorMessage
                name="original_title"
                component={FormErrorMessage}
              />
            </FormControl>

            <FormControl>
              <FormLabel>Authors (comma-separated)</FormLabel>
              <Field as={Input} name="authors_input" required />
              <ErrorMessage name="authors_input" component={FormErrorMessage} />
            </FormControl>

            <FormControl>
              <FormLabel>ISBN</FormLabel>
              <Field as={Input} name="isbn" />
              <ErrorMessage name="isbn" component={FormErrorMessage} />
            </FormControl>

            <FormControl>
              <FormLabel>ISBN13</FormLabel>
              <Field as={Input} name="isbn13" />
              <ErrorMessage name="isbn13" component={FormErrorMessage} />
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
              <ErrorMessage
                name="average_rating"
                component={FormErrorMessage}
              />
            </FormControl>

            <FormControl>
              <FormLabel>Publication Year</FormLabel>
              <Field
                as={Input}
                name="original_publication_year"
                type="number"
              />
              <ErrorMessage
                name="original_publication_year"
                component={FormErrorMessage}
              />
            </FormControl>

            <FormControl>
              <FormLabel>Language Code</FormLabel>
              <Field as={Input} name="language_code" />
              <ErrorMessage name="language_code" component={FormErrorMessage} />
            </FormControl>

            <FormControl>
              <FormLabel>Image URL</FormLabel>
              <Field as={Input} name="image_url" />
              <ErrorMessage name="image_url" component={FormErrorMessage} />
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
