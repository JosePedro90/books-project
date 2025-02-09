import { useState } from "react";
import {
  Box,
  Button,
  Heading,
  Text,
  Alert,
  VStack,
  Center,
  Flex,
} from "@chakra-ui/react";
import { useDropzone } from "react-dropzone";
import axios from "../api/axios";
import { toaster } from "../components/ui/toaster";
import { CloseButton } from "../components/ui/close-button";
import { useNavigate } from "react-router-dom";

const FileUploadPage = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "text/csv": [".csv"],
    },
    multiple: false,
    onDrop: (acceptedFiles) => {
      setSelectedFile(acceptedFiles[0]);
    },
  });

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setIsLoading(true);

      const response = await axios.post("/api/upload-csv/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const { task_id } = response.data;

      toaster.create({
        title: "Upload Successful",
        description: `File uploaded. Report will be emailed to you. Task ID: ${task_id}`,
        type: "success",
        duration: 5000,
      });
    } catch (error) {
      toaster.create({
        title: "Upload Failed",
        description: "Error uploading file",
        type: "error",
        duration: 5000,
      });
    } finally {
      setIsLoading(false);
      setSelectedFile(null);
    }
  };

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
        <Heading textAlign="center">Upload Book Data</Heading>
      </Flex>

      <VStack>
        <Box
          {...getRootProps()}
          p={8}
          border="2px dashed"
          borderColor={isDragActive ? "blue.300" : "gray.200"}
          borderRadius="md"
          width="100%"
          textAlign="center"
          cursor="pointer"
          _hover={{ borderColor: "blue.200" }}
        >
          <input {...getInputProps()} />
          <Center height="100px">
            {isDragActive ? (
              <Text fontSize="lg" color="blue.500">
                Drop the CSV file here
              </Text>
            ) : (
              <Text fontSize="lg" color="gray.500">
                Drag & drop a CSV file here, or click to select
              </Text>
            )}
          </Center>
        </Box>

        {selectedFile && (
          <Box width="100%">
            <Text fontSize="md" mb={2}>
              Selected file: {selectedFile.name} (
              {Math.round(selectedFile.size / 1024)}KB)
            </Text>

            <Button
              colorScheme="blue"
              width="100%"
              onClick={handleUpload}
              disabled={isLoading}
              loadingText="Uploading..."
            >
              Upload File
            </Button>
          </Box>
        )}

        <Alert.Root status="info" borderRadius="md">
          <Alert.Indicator />
          CSV must follow the required format.
        </Alert.Root>
      </VStack>
    </Box>
  );
};

export default FileUploadPage;
