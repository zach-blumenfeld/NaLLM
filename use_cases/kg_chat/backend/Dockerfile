# Use base shared Python image
FROM python:3.11

ENV PYTHONUNBUFFERED=1


# Relevant folder
ARG FOLDER=/use_cases/kg_chat/backend

# Create a folder
RUN mkdir -p $FOLDER

# Install packages
COPY ./use_cases/shared/requirements.txt $FOLDER/requirements.txt
RUN pip install -r $FOLDER/requirements.txt

# Copy the project files into the container
COPY .$FOLDER/src $FOLDER/src

# Copy the shared files into the container
COPY ./use_cases/shared /use_cases/shared

# Expose any necessary ports
EXPOSE 7860

# Set the working directory
WORKDIR $FOLDER/src

# Start the application
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "7860", "--reload", "--reload-dir", "/use_cases", "main:app"]