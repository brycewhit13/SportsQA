FROM python:3.9

# Create working directory
WORKDIR /app

# Copy requirements.txt file
COPY requirements.txt ./requirements.txt

# Install dependencies
RUN pip3 install -r requirements.txt

# Download NLTK punkt and stopwords
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords

# Expose port
EXPOSE 8080

# Copy all files for app
COPY . /app

#Run app
CMD ["gunicorn", "app:app", "-b", ":8080", "--timeout", "300"]