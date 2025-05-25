@echo off
set image=caesaraimusicstreamrecommendation
set latest=latest

:: Test application
docker build -t palondomus/%image%:%latest% .
docker run -it -p 8084:8084 palondomus/%image%:%latest%