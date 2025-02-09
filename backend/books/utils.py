import unicodedata


def clean_isbn(value):
    """Ensure ISBN is stored correctly as a string without scientific notation issues."""
    if not value:
        return None
    value = value.strip()

    if "e" in value.lower():
        return None

    return value


def book_exists(row):
    from books.models import Book
    """Check if a book exists based on title and authors (mandatory), and optionally isbn13 or isbn."""
    isbn13 = clean_isbn(row.get("isbn13", ""))
    isbn = clean_isbn(row.get("isbn", ""))
    title = row.get("title", "").strip()
    authors = row.get("authors", "").strip()

    if not title or not authors:
        return False

    queryset = Book.objects.none()

    if isbn13:
        queryset |= Book.objects.filter(isbn13=isbn13)

    if isbn:
        queryset |= Book.objects.filter(isbn=isbn)

    author_list = [normalize_name(author) for author in authors.split(",")]
    queryset |= Book.objects.filter(title__iexact=title, authors__normalized_name__in=author_list)

    return queryset.exists()


def normalize_name(name):
    """Normalize author names: remove accents, extra spaces, and convert to lowercase."""
    name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode("utf-8")
    name = " ".join(name.lower().split())
    return name.replace(".", "")
