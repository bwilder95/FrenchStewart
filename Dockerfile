# Base Image	
FROM python:3.8.2
 
 # Port
ENV PORT 5000

# Get necessary system packages
RUN apt-get update \
  && apt-get install --no-install-recommends --yes \
     build-essential \
     python3 \
     python3-pip \
     python3-dev \
  && rm -rf /var/lib/apt/lists/*
 
# Get necessary python libraries
COPY requirements.txt .
RUN pip3 install --compile --no-cache-dir -r requirements.txt
 
# Copy over code
COPY app.py app.py
COPY app.py models
 
# Create an unprivileged user
RUN useradd --system --user-group --shell /sbin/nologin services
 
# Switch to the unprivileged user
USER services
 
# Run image as a container
CMD ["python", "app.py"]
