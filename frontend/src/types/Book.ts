export interface Book {
  id: number;
  title: string;
  original_title: string;
  authors: { name: string }[];
  isbn?: string;
  isbn13?: string;
  average_rating?: number;
  ratings_count?: number;
  original_publication_year?: number;
  image_url?: string;
  small_image_url?: string;
  language_code?: string;
  goodreads_book_id?: string;
  reserved?: boolean;
  // TODO: Add more fields
}
