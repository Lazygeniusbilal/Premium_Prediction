# Step 1: Use an official Python image as base image
FROM python:3.9-slim

# Step 2: Set up working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file into the container
COPY requirements.txt /app/

# Step 4: Install dependencies and upgrade pip
RUN apt-get update && apt-get install -y libgomp1 && apt-get clean
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 5: Copy the rest of the application into the container
COPY . /app/

# Step 6: Expose the port FastAPI app will run on
EXPOSE 8000

# Step 7: Command to run FastAPI app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
