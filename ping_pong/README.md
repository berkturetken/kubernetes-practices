# Ping-pong

## How to run the application locally?
- Start the PostgreSQL server in a Docker container and run it in the background (-d flag), and set up a database: `docker run --name local-postgres -e POSTGRES_DB=ping_pong_db -e POSTGRES_USER=ping_pong_user -e POSTGRES_PASSWORD=ping_pong_pass -p 5432:5432 -d postgres:16.9`
- You can see that Postgres is running in the background: `docker ps`
- Run the application in a virtual environemnt to create a table:
    - Go to the ping_pong application folder
    - Run `source venv/bin/activate` to activate the virtual environment.
    - Run `python3 main.py --local` to run it locally.
- Visit http://localhost:9100/pings to see the number of pings and http://localhost:9100/pingpong to increase the number of pings.

## How to run the application in a Kubernetes cluster?
- Run `docker build -t <docker-username>/ping_pong:latest .` to build a docker image if there is a change in the source code.
- Run `docker push <docker-username>/ping_pong:latest` to push the docker image to Docker Hub.
- Run `k apply -f todo_app/todo_backend/manifests/deployment.yaml`. Check whether other manifests need to be changed. For example, if you need to change anything regarding the pod responsible for Postgres, you need to update the `statefulset.yaml` file.
- Check the logs if necessary: `k logs -f <pod_name>`
- Visit http://localhost:8081/pings to see the number of pings and http://localhost:8081/pingpong to increase the number of pings.