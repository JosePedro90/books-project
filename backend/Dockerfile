FROM python:3.11-slim-buster

WORKDIR /app

# Install system dependencies (including postgresql-client)
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY bin/start.sh /app/bin/start.sh
RUN chmod +x /app/bin/start.sh

EXPOSE 8000

# Run the start script from the /app/bin directory
CMD ["/app/bin/start.sh"]
