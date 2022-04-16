# ip_locator
Basic web service that gets the Latitude and Longitude of a provided IP address.

# How to Use:

## To Use docker-compose, do:

```
git clone https://github.com/CrosleyZack/ip_locator.git
cd ip_locator
docker-compose up
```

Then access in your browser at 127.0.0.1:5000

## To Docker build, do:

```
git clone https://github.com/CrosleyZack/ip_locator.git
cd ip_locator
docker build -t iplocator -f Dockerfile .
docker run -p 5000:5000 -dit iplocator
```

Then access in your browser at 127.0.0.1:5000