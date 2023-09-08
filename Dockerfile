FROM python:3.11

# Set the environment variable for the port
ENV PORT 8080

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    wget \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libu2f-udev \
    libvulkan1 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils

# Download and install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Set the environment variables and working directory
ENV APP_HOME /APP_HOME
WORKDIR $APP_HOME
COPY . .

# Start your application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app
