@echo off
echo Iniciando MongoDB con Docker...
docker-compose up -d mongodb

echo Verificando que MongoDB esté corriendo...
timeout /t 5

echo Iniciando el microservicio MessageAdmin...
cd src
python main.py 