# tvdsbcovid

Automated COVID screening utility. Don't be an ass - keep your people home if they're not feeling well!

## Build Docker Image

```
docker build -t tvdsb:0.0.1  .
```

## Running Docker Container

### Setting Up TVDSB Accounts

Create an environment file that looks like:

```
USER=A,B,C
PASS=D,E,F
```

Where each comma-delimited entry is a user or pass.


### Running the Container

```
docker run --env-file ./env.list tvdsb:0.0.1
```

### Running the Container Daily

Use CRON for linux -- sorry windows.
