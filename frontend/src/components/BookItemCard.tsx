import {
  Flex,
  Box,
  Image,
  Stack,
  Link,
  TagRoot,
  TagLabel,
  Text,
  Badge,
} from "@chakra-ui/react";
import { Book } from "../types/Book";
import Rating from "./Rating";
import { formatPublicationYear } from "../utils/formatting";
import ReservationModal from "./ReservationModal";

interface BookItemCardProps {
  book: Book;
}

const BookItemCard: React.FC<BookItemCardProps> = ({ book }) => {
  const imageUrl = book.image_url || book.small_image_url;

  return (
    <Flex p={4} w="full" alignItems="center" justifyContent="center">
      <Box
        w="350px"
        h="450px"
        borderWidth="1px"
        rounded="lg"
        shadow="lg"
        position="relative"
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
      >
        <Link href={`/books/${book.id}`}>
          <Image
            src={imageUrl}
            alt={`Picture of ${book.title}`}
            roundedTop="lg"
            objectFit="contain"
            h="auto"
            w="auto"
            maxH="200px"
            display="block"
            mx="auto"
          />
        </Link>

        <Box p="6" textAlign="center">
          <Box fontSize="2xl" fontWeight="semibold" lineHeight="tight">
            {book.original_title ?? book.title}
          </Box>

          <Text fontSize="sm" color="gray.500" mt={2}>
            {book.authors && book.authors.length > 0
              ? book.authors.map((author) => author.name).join(", ")
              : "No authors listed"}{" "}
          </Text>

          <Flex justifyContent="center" alignContent="center" mt={2}>
            <Rating
              rating={book.average_rating}
              numReviews={book.ratings_count}
            />
          </Flex>
          <Stack direction="row" spaceX={1} mt={2} justify="center">
            {book.original_publication_year && (
              <TagRoot>
                <TagLabel>
                  {formatPublicationYear(book.original_publication_year)}
                </TagLabel>
              </TagRoot>
            )}
            {book.language_code && (
              <TagRoot>
                <TagLabel>{book.language_code.toUpperCase()}</TagLabel>
              </TagRoot>
            )}
            {book.goodreads_book_id && (
              <Link
                href={`https://www.goodreads.com/book/show/${book.goodreads_book_id}`}
              >
                <TagRoot>
                  <TagLabel>Goodreads</TagLabel>
                </TagRoot>
              </Link>
            )}
          </Stack>

          <Stack direction="row" spaceX={1} mt={2} justify="center">
            <Badge
              backgroundColor={book.reserved ? "red.100" : "green.100"}
              mt={2}
            >
              {book.reserved ? "Reserved" : "Available"}
            </Badge>
            {!book.reserved && <ReservationModal book={book} />}
          </Stack>
        </Box>
      </Box>
    </Flex>
  );
};

export default BookItemCard;
