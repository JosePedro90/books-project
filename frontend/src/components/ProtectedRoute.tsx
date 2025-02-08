import { Navigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import { Center, Spinner } from "@chakra-ui/react";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const { accessToken, isLoading } = useAuth();

  if (isLoading) {
    return (
      <Center mt={4}>
        <Spinner />
      </Center>
    );
  }

  return accessToken ? <>{children}</> : <Navigate to="/login" />;
};

export default ProtectedRoute;
