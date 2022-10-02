echo "Building Container"
docker build -t lab1_deployed:1.0 -f lab1/Dockerfile .

echo "Start Container in detached mode"
docker run --rm --name lab_1 -d -p 8000:8000 lab1_deployed:1.0

echo "Wait for the Docker container to start"
sleep 5

echo "testing '/hello' endpoint with ?name=Marcus"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=Marcus"

echo "testing '/' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/"

echo "testing '/docs' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/docs"

echo "killing container"
docker stop lab_1

echo "Deleting docker image"
docker image rm lab1_deployed:1.0