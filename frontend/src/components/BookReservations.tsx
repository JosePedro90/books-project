import { useState } from "react";
import {
  Box,
  Heading,
  Spinner,
  Text,
  Button,
  Stack,
  Card,
  HStack,
  Separator,
  Badge,
} from "@chakra-ui/react";
import { Reservation } from "../types/Reservation";
import {
  getReservationsByBookId,
  updateReservation,
} from "../api/reservations";
import { toaster } from "../components/ui/toaster";
import Select from "./ui/select";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

interface BookReservationsProps {
  bookId: number;
}

const BookReservations: React.FC<BookReservationsProps> = ({ bookId }) => {
  const queryClient = useQueryClient();
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editingStatus, setEditingStatus] = useState<string>("");

  const {
    data: reservations = [],
    isLoading,
    isError,
  } = useQuery<Reservation[]>({
    queryKey: ["reservations", bookId],
    queryFn: () =>
      getReservationsByBookId(bookId).then((res) => res.results || res),
  });

  const mutation = useMutation({
    mutationFn: ({ id, status }: { id: number; status: string }) =>
      updateReservation(id, { status }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["reservations", bookId] });
      toaster.create({
        description: "Reservation updated",
        type: "success",
        duration: 2000,
      });
      setEditingId(null);
    },
    onError: () => {
      toaster.create({
        title: "Error",
        description: "Failed to update reservation.",
        type: "error",
        duration: 3000,
      });
    },
  });

  const handleStatusChange = (value: string) => {
    setEditingStatus(value);
  };

  const handleSave = (id: number) => {
    mutation.mutate({ id, status: editingStatus });
  };

  if (isLoading) {
    return (
      <Box p={4} textAlign="center">
        <Spinner />
        <Text mt={2}>Loading...</Text>
      </Box>
    );
  }

  if (isError) {
    return (
      <Box p={4} textAlign="center">
        <Text>Error loading reservations</Text>
      </Box>
    );
  }

  const reservationOptions = [
    { label: "Reserved", value: "reserved" },
    { label: "Canceled", value: "canceled" },
    { label: "Returned", value: "returned" },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case "reserved":
        return "green.100";
      case "canceled":
        return "red.100";
      case "returned":
        return "blue.100";
      default:
        return "gray";
    }
  };
  return (
    <Box p={4} borderWidth="1px" borderRadius="lg" boxShadow="md">
      <Heading mb={6} textAlign="left" size={"lg"}>
        Edit Book Reservations
      </Heading>
      {!reservations.length ? (
        <Box p={4} textAlign="center">
          No reservations found.
        </Box>
      ) : (
        <Stack>
          {reservations.map((r) => (
            <Card.Root key={r.id}>
              <Card.Body>
                <Stack>
                  <HStack>
                    <Text fontWeight="bold">{r.name}</Text>
                    <Text overflow="hidden" textOverflow="ellipsis">
                      {r.email}
                    </Text>
                  </HStack>
                  <HStack>
                    <Box>
                      {editingId === r.id ? (
                        <Select
                          options={reservationOptions}
                          onChange={handleStatusChange}
                          size="sm"
                          value={editingStatus}
                        />
                      ) : (
                        <Badge backgroundColor={getStatusColor(r.status)}>
                          {r.status}
                        </Badge>
                      )}
                    </Box>
                    <Box>
                      {editingId === r.id ? (
                        <Button
                          size="xs"
                          onClick={() => handleSave(r.id)}
                          disabled={
                            mutation.isPending &&
                            mutation.variables?.id === r.id
                          }
                        >
                          Save
                        </Button>
                      ) : (
                        <Button
                          size="xs"
                          onClick={() => {
                            setEditingId(r.id);
                            setEditingStatus(r.status);
                          }}
                          disabled={editingId !== null && editingId !== r.id}
                        >
                          Edit
                        </Button>
                      )}
                    </Box>
                  </HStack>
                  <HStack justifyContent="space-between">
                    <Text fontSize="xs">
                      Reserved At: {new Date(r.reserved_at).toLocaleString()}
                    </Text>
                    <Text fontSize="xs">
                      Returned At:{" "}
                      {r.returned_at
                        ? new Date(r.returned_at).toLocaleString()
                        : "Not returned"}
                    </Text>
                  </HStack>
                </Stack>
              </Card.Body>
              {reservations.indexOf(r) !== reservations.length - 1 && (
                <Separator />
              )}
            </Card.Root>
          ))}
        </Stack>
      )}
    </Box>
  );
};

export default BookReservations;
