FROM apify/actor-python:3.12

# Copy repository files into the actor workspace
COPY . ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Execute main actor entrypoint
CMD ["python3", "main.py"]
