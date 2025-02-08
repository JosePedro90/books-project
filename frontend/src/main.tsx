import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient } from "@tanstack/react-query";

import App from "./App";
import { ChakraProvider, defaultSystem } from "@chakra-ui/react";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "./components/ui/toaster";
const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ChakraProvider value={defaultSystem}>
        <Toaster />
        <App />
      </ChakraProvider>
    </QueryClientProvider>
  </React.StrictMode>
);
