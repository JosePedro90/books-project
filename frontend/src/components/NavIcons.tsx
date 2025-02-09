import {
  Flex,
  IconButton,
  MenuContent,
  MenuItem,
  MenuRoot,
  MenuTrigger,
} from "@chakra-ui/react";
import { BsUpload, BsPersonCircle } from "react-icons/bs";
import { Link } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import { Tooltip } from "./ui/tooltip";

const NavIcons = () => {
  const { accessToken, logout } = useAuth();

  return (
    <Flex gap="3" align="center">
      {accessToken ? (
        <>
          <Tooltip content="Upload CSV">
            <IconButton
              aria-label="Upload books"
              as={Link}
              to="/upload"
              colorScheme="blue"
              variant="ghost"
            >
              <BsUpload />
            </IconButton>
          </Tooltip>

          <MenuRoot>
            <Tooltip content="Account">
              <MenuTrigger asChild>
                <IconButton aria-label="Account" variant="ghost">
                  <BsPersonCircle size="24px" />
                </IconButton>
              </MenuTrigger>
            </Tooltip>
            <MenuContent>
              <MenuItem value="logout" onClick={logout}>
                Logout
              </MenuItem>
            </MenuContent>
          </MenuRoot>
        </>
      ) : (
        <Tooltip content="Login">
          <IconButton
            aria-label="Login"
            as={Link}
            to="/login"
            colorScheme="blue"
            variant="ghost"
          >
            <BsPersonCircle size="24px" />
          </IconButton>
        </Tooltip>
      )}
    </Flex>
  );
};

export default NavIcons;
