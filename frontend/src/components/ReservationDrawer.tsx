import {
  DrawerBackdrop,
  DrawerBody,
  DrawerCloseTrigger,
  DrawerContent,
  DrawerHeader,
  DrawerRoot,
  DrawerTitle,
} from "./ui/drawer";

import { useState } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { createReservation } from "../api/reservations";
import { toaster } from "./ui/toaster";
import { Button, Input, Text, useDisclosure } from "@chakra-ui/react";
import {
  FormControl,
  FormErrorMessage,
  FormLabel,
} from "@chakra-ui/form-control";
import { Book } from "../types/Book";
import { useQueryClient } from "@tanstack/react-query";

const ReservationDrawer = ({ book }: { book: Book }) => {
  const { open, onOpen, onClose } = useDisclosure();
  const [apiError, setApiError] = useState("");
  const queryClient = useQueryClient();

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
        queryClient.invalidateQueries({ queryKey: ["books"] });
        formik.resetForm();
        onClose();
      } catch (error) {
        setApiError("An error occurred while creating the reservation.");
        console.error("Reservation error:", error);
      } finally {
      }
    },
  });

  return (
    <>
      <Button variant="outline" size="2xs" onClick={onOpen}>
        Make Reservation
      </Button>
      <DrawerRoot open={open} onOpenChange={onOpen}>
        <DrawerBackdrop />
        <DrawerContent>
          <DrawerHeader>
            <DrawerTitle mt={4}>
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
              <Button type="submit" mt={4}>
                Make Reservation
              </Button>
            </form>
          </DrawerBody>

          <DrawerCloseTrigger asChild>
            <Button variant="outline" mr={3} onClick={onClose}>
              Cancel
            </Button>
          </DrawerCloseTrigger>
        </DrawerContent>
      </DrawerRoot>
    </>
  );
};

export default ReservationDrawer;
