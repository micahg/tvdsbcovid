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


### Building the Docker Image

```
docker build . -t mfg81/tvdsbcovid:0.0.1
docker push mfg81/tvdsbcovid:0.0.1
```

### Getting the Docker Image

```
docker pull mfg81/tvdsbcovid:0.0.1
```

### Running the Container

```
docker run --env-file ./env.list mfg81/tvdsbcovid:0.0.1
```

### Running the Container Daily

Use CRON for linux -- sorry windows. Here is a daily entry

```
0 7 * * 1-5 docker run --env-file ./env.list mfg81/tvdsbcovid:0.0.1
```

The above should be 7am on weekdays.
