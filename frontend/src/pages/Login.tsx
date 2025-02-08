import { useState } from "react";
import {
  Box,
  Button,
  Input,
  VStack,
  Heading,
  Center,
  Text,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/auth";
import useAuth from "../hooks/useAuth";
import {
  FormControl,
  FormLabel,
  FormErrorMessage,
} from "@chakra-ui/form-control";
import { useFormik } from "formik";
import * as Yup from "yup";

const Login = () => {
  const navigate = useNavigate();
  const { saveTokens } = useAuth();
  const [apiError, setApiError] = useState("");

  const validationSchema = Yup.object().shape({
    username: Yup.string().required("Username is required"),
    password: Yup.string().required("Password is required"),
  });

  const formik = useFormik({
    initialValues: {
      username: "",
      password: "",
    },
    validationSchema,
    onSubmit: async (values) => {
      setApiError("");
      try {
        const { access, refresh } = await login(
          values.username,
          values.password
        );
        saveTokens(access, refresh);
        navigate("/admin");
      } catch (error) {
        setApiError("Invalid credentials");
      }
    },
  });

  return (
    <Center h="75vh">
      <Box p={8} bg="white" borderRadius="lg" boxShadow="md">
        <Heading as="h2" size="lg" mb={6} textAlign="center">
          Book Records Login
        </Heading>

        <form onSubmit={formik.handleSubmit}>
          <VStack spaceY={4}>
            <FormControl
              isRequired
              isInvalid={formik.touched.username && !!formik.errors.username}
            >
              <FormLabel htmlFor="username">Username</FormLabel>
              <Input
                w="sm"
                id="username"
                name="username"
                value={formik.values.username}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
              />
              <FormErrorMessage>{formik.errors.username}</FormErrorMessage>
            </FormControl>

            <FormControl
              isRequired
              isInvalid={formik.touched.password && !!formik.errors.password}
            >
              <FormLabel htmlFor="password">Password</FormLabel>
              <Input
                w="sm"
                id="password"
                name="password"
                type="password"
                value={formik.values.password}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
              />
              <FormErrorMessage>{formik.errors.password}</FormErrorMessage>
            </FormControl>

            {apiError && (
              <Text color="red.500" mt={2}>
                {apiError}
              </Text>
            )}

            <Button type="submit" width="full" colorScheme="blue">
              Sign In
            </Button>
          </VStack>
        </form>
      </Box>
    </Center>
  );
};

export default Login;
