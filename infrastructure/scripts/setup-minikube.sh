#!/bin/bash
set -e

echo "🏝️ Setting up Minikube for Oasis..."

# 1. Start Minikube
echo "Starting Minikube cluster (4 CPUs, 8GB RAM)..."
minikube start --cpus=4 --memory=8192 --driver=docker

# 2. Enable Addons
echo "Enabling necessary addons..."
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard

# 3. Build Docker images inside Minikube's Docker daemon
echo "Configuring Docker environment..."
eval $(minikube docker-env)

echo "Building Docker images (this may take a while)..."
cd ../../
docker compose build

# 4. Apply Kubernetes Manifests via Helm
echo "Deploying Oasis via Helm..."
kubectl create namespace oasis || true
helm upgrade --install oasis ./infrastructure/helm/oasis-chart -n oasis --create-namespace

echo "✅ Setup complete! Oasis is running on local Kubernetes."
echo "Access the Minikube IP below:"
minikube ip
