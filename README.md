# super-system-v

super sexy ml project

## Run using docker

1. Build the image
    - this step is required only once
    - re-build the image only when changes are made in source code
    - this step may take 10/15 minutes for the very first time

```bash
sudo docker build -t my-super-system .
```

2. Run the container using docker compose

```bash
sudo docker-compose up
```

3. Stop the container

```bash
sudo docker-compose down
```
