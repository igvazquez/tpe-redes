# Use a slim Python 3.9 base image
FROM python:3.9-slim-buster

# Create a non-root user for the container
RUN groupadd -g 999 python \
    && useradd -r -u 999 -g python python \
    && mkdir -p /usr/app \
    && python -m venv /usr/app/.venv \
    && chown -R python:python /usr/app

ENV PATH="/usr/app/.venv/bin:$PATH"
ENV PIP_NO_CACHE_DIR=off

# Set the working directory for the container
WORKDIR /app

# Copy the Python code and requirements file to the container
COPY --chown=python:python main.py /app/main.py
COPY --chown=python:python requirements.txt /app/requirements.txt

# Install Requirements
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Set the ownership and permissions of the app folder to the non-root user
RUN chown -R python:python /app && chmod -R 755 /app

# Switch to the non-root user
USER python

# Expose port 8000 for the Flask app
EXPOSE 8000

# Start the Flask app
CMD ["python", "main.py"]
