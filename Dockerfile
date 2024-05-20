# Use the official image as a parent image
FROM mcr.microsoft.com/windows/servercore:ltsc2019

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python
RUN powershell -Command `
    Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.8.5/python-3.8.5-amd64.exe -OutFile python-installer.exe; `
    Start-Process python-installer.exe -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait; `
    Remove-Item -Force python-installer.exe

# Install required Python packages
RUN pip install flask pandas watchdog

# Set environment variables for Flask
ENV FLASK_APP=app.py

# Expose port 5000
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]

