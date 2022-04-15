FROM python:3
# Upgrade pip. Probably not necessary, but good practice.
RUN python -m pip install --upgrade pip
# Install the required libraries.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Expose the appropriate port.
EXPOSE 5000
# Copy files into the docker image.
COPY . .
# Execute the flask file.
WORKDIR /code
CMD ['python', 'ip_locator.py']