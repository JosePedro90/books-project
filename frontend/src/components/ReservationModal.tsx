import {
  DrawerBackdrop,
  DrawerBody,
  DrawerCloseTrigger,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerRoot,
  DrawerTitle,
  DrawerTrigger,
} from "./ui/drawer";

import { useState } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { createReservation } from "../api/reservations"; // Import your API function
import { toaster } from "./ui/toaster";
import { Button, Input, Text } from "@chakra-ui/react";
import {
  FormControl,
  FormErrorMessage,
  FormLabel,
} from "@chakra-ui/form-control";
import { Book } from "../types/Book";

const ReservationModal = ({ book }: { book: Book }) => {
  const [apiError, setApiError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validationSchema = Yup.object().shape({
    name: Yup.string().required("Name is required"),
    email: Yup.string()
      .email("Invalid email format")
      .required("Email is required"),
  });

  const formik = useFormik({
    initialValues: {
      name: "",
      email: "",
    },
    validationSchema,
    onSubmit: async (values) => {
      setIsSubmitting(true);
      setApiError("");
      try {
        await createReservation({
          name: values.name,
          email: values.email,
          book: book.id,
        });
        toaster.create({
          title: "Reservation Created",
          description: "Your reservation has been successfully created.",
          duration: 5000,
          type: "success",
        });

        formik.resetForm();
      } catch (error) {
        setApiError("An error occurred while creating the reservation.");
        console.error("Reservation error:", error);
      } finally {
        setIsSubmitting(false);
      }
    },
  });

  return (
    <DrawerRoot>
      <DrawerBackdrop />
      <DrawerTrigger asChild>
        <Button variant="outline" size="xs">
          Make Reservation
        </Button>
      </DrawerTrigger>
      <DrawerContent>
        <DrawerHeader>
          <DrawerTitle>
            Make Reservation for {book.original_title ?? book.title}
          </DrawerTitle>
        </DrawerHeader>
        <DrawerBody>
          <form onSubmit={formik.handleSubmit}>
            <FormControl
              isRequired
              isInvalid={!!(formik.touched.name && formik.errors.name)}
            >
              <FormLabel htmlFor="name">Name</FormLabel>
              <Input
                id="name"
                name="name"
                value={formik.values.name}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
              />
              <FormErrorMessage>{formik.errors.name}</FormErrorMessage>
            </FormControl>

            <FormControl
              isRequired
              isInvalid={!!(formik.touched.email && formik.errors.email)}
              mt={4}
            >
              <FormLabel htmlFor="email">Email</FormLabel>
              <Input
                id="email"
                name="email"
                type="email"
                value={formik.values.email}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
              />
              <FormErrorMessage>{formik.errors.email}</FormErrorMessage>
            </FormControl>

            {apiError && (
              <Text color="red.500" mt={2}>
                {apiError}
              </Text>
            )}
            <Button
              type="submit"
              mt={4}
              colorScheme="blue"
              loading={isSubmitting}
            >
              Make Reservation
            </Button>
          </form>
        </DrawerBody>
        <DrawerFooter>
          <DrawerCloseTrigger asChild>
            <Button variant="outline" mr={3}>
              Cancel
            </Button>
          </DrawerCloseTrigger>
        </DrawerFooter>
        <DrawerCloseTrigger />
      </DrawerContent>
    </DrawerRoot>
  );
};

export default ReservationModal;
