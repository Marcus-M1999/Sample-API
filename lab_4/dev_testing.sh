echo "starting minikube"
minikube start --kubernetes-version=v1.23.8
eval $(minikube docker-env)
kubectl config use-context minikube

echo "Building Container"
docker build -t lab4_deployed:1.0 -f lab_4/Dockerfile .

echo "Start Container in detached mode"
docker run -d --name lab4 -p 8000:8000 lab4_deployed:1.0

echo "Wait for the Docker container to start"
sleep 15

echo "Creating Namespace"
Kubectl apply -f lab_4/infra/namespace.yaml

echo "setting Namespace & prefix variables"
NAMESPACE=w255
PREFIX=w255

kubectl kustomize .k8s/overlays/dev
kubectl apply -k .k8s/overlays/dev
sleep 30

echo "checking logs"
kubectl --namespace $NAMESPACE logs deployment.apps/lab4

echo "Deleting all services & pods"
kubectl delete services lab4 --namespace=$PREFIX
kubectl delete services redis --namespace=$PREFIX
kubectl delete --all pods --namespace=$PREFIX

echo "testing '/predict' endpoint"
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "MedInc": [10.0, 10.0],
  "HouseAge": [10.0, 10.0],
  "AveRooms": [10.0, 10.0],
  "AveBedrms": [10.0, 10.0],
  "Population": [10.0, 10.0],
  "AveOccup": [10.0, 10.0],
  "Latitude": [10.0, 10.0],
  "Longitude": [10.0, 10.0]
}'


echo "deleting deployments, services, namespace & minikube"
kubectl delete all --all -n w255
kubectl delete ns w255
minikube delete
#minikube stop
