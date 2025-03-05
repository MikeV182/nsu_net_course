## How to launch?

``` sh
# initialize the PostgreSQL container
docker run --name postgres-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=nsunetdb \
  -p 22222:5432 \
  -v $(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql \
  -d postgres:latest


# build an image for my app and run a container
docker build -t fastapi-app .
docker run --name fastapi-app --link postgres-db:db -p 11111:11111 -d fastapi-app


# to see all running containers
docker ps
# to stop a container
docker stop <id-of-container>  
# to remove a container
docker rm <id-of-container>
```