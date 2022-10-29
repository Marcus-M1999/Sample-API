#pkill -f "port-forward"
echo "starting minikube"
minikube start --kubernetes-version=v1.23.8
eval $(minikube docker-env)

echo "Building Container"
docker build -t lab3_deployed:1.0 -f lab_3/Dockerfile .

echo "Start Container in detached mode"
docker run --rm --name lab_3 -d -p 8000:8000 lab3_deployed:1.0

echo "Wait for the Docker container to start"
sleep 15

echo "Creating Namespace"
Kubectl apply -f lab_3/infra/namespace.yaml

echo "Loading configuration (will sleep for 20 seconds)"
Kubectl apply -f lab_3/infra/deployment-redis.yaml -n w255
Kubectl apply -f lab_3/infra/service-redis.yaml -n w255
Kubectl apply -f lab_3/infra/deployment-pythonapi.yaml -n w255
Kubectl apply -f lab_3/infra/service-prediction.yaml -n w255
sleep 20

echo "conducting health check"
finished=false
pid=0

#write script for redis, if it runs locally then put in init

while ! $finished; do
  kubectl port-forward service-pythonapi-service 8000:8000 -n w255 &
  pid=$!
  health_status=$(curl -s -o /dev/null -w "%{http_code}" -X GET "http://localhost:8000/health")
  if [ $health_status = 200 ]; then
    finished=true
    echo "health check sucessful"
  else
    echo "No response, waiting for 15 seconds then checking again"
    sleep 15
  fi
done

echo "testing '/hello' endpoint with ?name=Marcus"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=Marcus"

echo "testing '/' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/"

echo "testing '/docs' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/docs"

echo "testing '/predict' endpoint"
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322.0
                               , "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}'

echo "testing '/health' endpoint"
curl -X 'GET' \
  'http://localhost:8000/health' \
  -H 'accept: application/json'


echo "killing container"
docker stop lab_3

echo "Deleting docker image"
docker image rm lab3_deployed:1.0

echo "Killing K8s cluster"
kubectl delete all -n w255
kubectl delete ns w255
minikube delete
