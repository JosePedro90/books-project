from django.core.mail import send_mail


def send_ingestion_report(books_processed, books_inserted, books_skipped, errors, filename, admin_email):
    """Send an email report after book ingestion to the admin email from the request."""
    subject = "📚 Book Ingestion Report"
    message = (
        f"File: {filename}\n"
        f"Total Books Processed: {books_processed}\n"
        f"Books Inserted: {books_inserted}\n"
        f"Books Skipped (Duplicated): {books_skipped}\n"
        f"Errors: {len(errors)}\n"
    )

    if errors:
        message += "\nError Details:\n" + "\n".join(errors[:5])  # Limit to first 5 errors

    # Send the email to the admin from the request
    send_mail(
        subject,
        message,
        "no-reply@books-jpm.com",  # Mock sender email
        [admin_email],  # Dynamic recipient from request
        fail_silently=False,
    )
