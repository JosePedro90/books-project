import { useState, useEffect } from "react";
import {
  Grid,
  GridItem,
  Text,
  Flex,
  Center,
  Spinner,
  Box,
  Heading,
  Button,
  Stack,
  Input,
} from "@chakra-ui/react";

import { useInfiniteBooks } from "../api/books";
import BookItemCard from "../components/BookItemCard";
import Select from "../components/ui/select";
import debounce from "lodash/debounce";
import { BsArrowDown, BsArrowUp } from "react-icons/bs";

const BookList = () => {
  const [search, setSearch] = useState("");
  const [ordering, setOrdering] = useState("");
  const [isAscending, setIsAscending] = useState(true);
  const [debouncedSearch, setDebouncedSearch] = useState("");

  // Debounce the search input
  useEffect(() => {
    const debounceFn = debounce(() => {
      setDebouncedSearch(search);
    }, 200);

    debounceFn();

    return () => debounceFn.cancel();
  }, [search]);

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(event.target.value);
  };

  const handleOrderingChange = (value: string) => {
    const newOrdering = isAscending ? value : `-${value}`;
    setOrdering(newOrdering);
  };

  const toggleSortDirection = () => {
    setIsAscending((prev) => !prev);
    setOrdering((prev) => (prev.startsWith("-") ? prev.slice(1) : `-${prev}`));
  };

  const {
    data: books,
    isLoading,
    error,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteBooks(debouncedSearch, ordering);

  if (error) {
    return (
      <Center h="100vh">
        <Text color="red.500">Error: {error?.message}</Text>
      </Center>
    );
  }

  const orderingOptions = [
    { label: "Title", value: "title" },
    { label: "Average Rating", value: "average_rating" },
    { label: "Ratings Count", value: "ratings_count" },
    { label: "Publication Year", value: "original_publication_year" },
  ];

  return (
    <Box p={4}>
      <Heading as="h2" size="lg" mb={4} textAlign="center">
        Book Records
      </Heading>
      <Stack direction="row" mb={4}>
        <Input
          type="text"
          placeholder="Search books..."
          value={search}
          onChange={handleSearchChange}
          size="md"
        />
        <Select
          options={orderingOptions}
          placeholder="Sort By"
          onChange={handleOrderingChange}
          size="md"
        />
        <Button variant="outline" onClick={toggleSortDirection}>
          {isAscending ? <BsArrowUp /> : <BsArrowDown />}
        </Button>
      </Stack>

      {isLoading ? (
        <Center h="100vh">
          <Spinner size="lg" />
        </Center>
      ) : (
        <>
          <Grid
            templateColumns={{
              sm: "1fr",
              md: "repeat(2, 1fr)",
              lg: "repeat(3, 1fr)",
              xl: "repeat(4, 1fr)",
            }}
            gap={4}
          >
            {books.map((book) => (
              <GridItem key={book.id}>
                <BookItemCard book={book} />
              </GridItem>
            ))}
          </Grid>

          {hasNextPage && (
            <Flex mt={4} justify="center">
              <Button onClick={fetchNextPage} disabled={isFetchingNextPage}>
                Load More
              </Button>
            </Flex>
          )}
          {isFetchingNextPage && (
            <Center mt={4}>
              <Spinner />
            </Center>
          )}
        </>
      )}
    </Box>
  );
};

export default BookList;
