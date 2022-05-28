# super-system-v

A simple product recommedation app. The user will upload their sales data and the platform would generate product recommendations pairs.

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

## Design

- NodeJS/express is used for backend which returns a private URL that can be saved by the client to view the results whenever.
  - ![](https://i.imgur.com/91myxta.png)
- For frontend, pure HTML/CSS + a little bootstrap
- lastly python for performing the ML task & managing the mongodb database.

![](https://i.imgur.com/Q4NHyhw.png)

[Figma designs](https://www.figma.com/file/I1rh8tC7ybbGxfz7EqStMX/ML-project-Analytics-platform?node-id=812%3A9257)
