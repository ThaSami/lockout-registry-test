``` docker build -t lockoutapi .```
``` docker run -p 8080:4999 --env API_PORT=4999 --env BRANCH_NAME=main lockoutreg ```

## Installing requiremenets
``` make install ```

## For testing
``` make test ```

## Lint with 
``` make lint ```

## Run with 
``` make start-api ```