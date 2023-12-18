@echo off

set PUSH=%1
set IMAGE=pyrin-rest-server
set TAG=latest

docker build -t %IMAGE%:%TAG% -f docker\Dockerfile .
@REM docker build --pull -t %IMAGE%:%tag% -f docker\Dockerfile .
@REM docker tag %IMAGE%:%tag% %IMAGE%:latest
@REM echo Tagged %IMAGE%:latest

if "%PUSH%" == "push" (
    docker push %IMAGE%:latest
)

endlocal
