echo "Building Container"
docker build -t lab2_deployed:1.0 -f lab_2/Dockerfile .

echo "Start Container in detached mode"
docker run --rm --name lab_2 -d -p 8000:8000 lab2_deployed:1.0

echo "Wait for the Docker container to start"
sleep 15

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
docker stop lab_2

echo "Deleting docker image"
docker image rm lab2_deployed:1.0
