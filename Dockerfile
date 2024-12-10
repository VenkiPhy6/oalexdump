# Use the official PostgreSQL image as the base
FROM postgres:latest

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Create a directory for Python scripts
WORKDIR /usr/src

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=oalexer
ENV POSTGRES_PASSWORD=alexandria
ENV POSTGRES_DB=openalex

# Expose PostgreSQL port
EXPOSE 5432

# Command to start PostgreSQL
CMD ["docker-entrypoint.sh", "postgres"]