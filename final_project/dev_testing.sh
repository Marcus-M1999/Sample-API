echo "starting minikube"
minikube start --kubernetes-version=v1.23.8
eval $(minikube docker-env)
kubectl config use-context minikube

echo "Building Container"
docker build -t project:1.0 -f mlapi/Dockerfile .

echo "Start Container in detached mode"
docker run -d --name project -p 8000:8000 project:1.0

echo "Wait for the Docker container to start"
sleep 15

echo "Creating Namespace"
Kubectl apply -f infra/namespace.yaml

echo "setting Namespace & prefix variables"
NAMESPACE=w255
PREFIX=w255

kubectl kustomize .k8s/overlays/dev
kubectl apply -k .k8s/overlays/dev
sleep 30

echo "checking logs"
kubectl --namespace $NAMESPACE logs deployment.apps/project

echo "Deleting all services & pods"
#kubectl delete services lab4 --namespace=$PREFIX
#kubectl delete services redis --namespace=$PREFIX
#kubectl delete --all pods --namespace=$PREFIX

echo "testing '/predict' endpoint"
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"text": ["I hate you.", "I love you."]}'


echo "deleting deployments, services, namespace & minikube"
kubectl delete all --all -n w255
kubectl delete ns w255
minikube delete
#minikube stop
