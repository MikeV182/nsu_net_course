## How to launch?

``` sh
docker run --name postgres-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=nsunetdb \
  -p 22222:5432 \
  -v $(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql \
  -d postgres:latest


docker build -t fastapi-app .
docker run --name fastapi-app --link postgres-db:db -p 11111:11111 -d fastapi-app


service nginx stop


docker build -t nginx-app -f nginx-Dockerfile .
docker run --name nginx-container --link fastapi-app:fastapi-app -p 80:80 -d nginx-app


docker ps # to see all running containers
docker stop <id-of-container>  
docker rm <id-of-container>

# Local address
ifconfig
# Узнать внешний адресс своей машины
curl ifconfig.me
```