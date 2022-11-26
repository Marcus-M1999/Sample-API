echo "starting minikube"
minikube start --kubernetes-version=v1.23.8

echo"Logging into Azure"
az login --tenant berkeleydatasciw255.onmicrosoft.com
az account set --subscription="6baae99a-4d64-4071-bfac-c363e71984c3"
az aks get-credentials --name w255-aks --resource-group w255 --overwrite-existing
kubectl config use-context 255-aks
az acr login --name w255mids

NAMESPACE=marcusmanos

TAG='date + "%m%d%H%M%S"'
echo "TAG" $TAG
sed "s/\[TAG\]/$TAG/g" .k8s/overlays/prod/patch-deployment-lab4_copy.yaml > .k8s/overlays/prod/patch-deployment-lab4.yaml

#ACR
IMAGE_PREFIX=marcusmanos
echo "IMAGE_PREFIX: " $IMAGE_PREFIX

IMAGE_NAME=lab4
ACR_DOMAIN=w255mids.azurecr.io
IMAGE_FQDN="${ACR_DOMAIN}/${IMAGE_PREFIX}/${IMAGE_NAME}:${TAG}"
echo "IMAGE_NAME: " $IMAGE_NAME
echo "ACR_DOMAIN: " $ACR_DOMAIN
echo "IMAGE_FQDN: " $IMAGE_FQDN

echo "building & running docker container"
echo "Building Container"
docker build -t lab4_deployed:1.0 -f lab_4/Dockerfile .
echo "Start Container in detached mode"
docker run --rm --name lab_4 -d -p 8000:8000 lab4_deployed:1.0


docker tag ${IMAGE_NAME} ${IMAGE_FQDN}
docker push ${IMAGE_FQDN}
docker pull ${IMAGE_FQDN}

echo "Generate & apply kustomize files"
kubectl kustomize .k8s/overlays/prod
kubectl apply -k .k8s/overlays/prod


kubectl get pods --namespace=$NAMESPACE
kubectl get services --namespace=$NAMESPACE

echo "testing '/predict' endpoint"
curl -X 'POST' \
  'http://marcusmanos.mids255.com/predict' \
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