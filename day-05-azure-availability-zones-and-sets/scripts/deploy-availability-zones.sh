#!/bin/bash
# ==============================================================================
# Script: deploy-availability-zones.sh
# Purpose: Deploys an Azure Multi-Zone High Availability Architecture:
#          - Zone-Redundant Standard Public IP
#          - Standard Load Balancer with Zone-Redundant Frontend
#          - 3 Virtual Machines distributed across Zone 1, Zone 2, and Zone 3
# ==============================================================================

set -euo pipefail

# Configuration Variables
RESOURCE_GROUP="rg-az-demo"
LOCATION="centralindia"
VNET_NAME="vnet-az-demo"
SUBNET_NAME="snet-web"
LB_NAME="slb-web-tier"
PIP_NAME="pip-slb-web"
ADMIN_USER="azureuser"
VM_SIZE="Standard_B2als_v2"

echo "Step 1: Creating Resource Group..."
az group create \
    --name "${RESOURCE_GROUP}" \
    --location "${LOCATION}"

echo "Step 2: Creating Virtual Network and Subnet..."
az network vnet create \
    --resource-group "${RESOURCE_GROUP}" \
    --name "${VNET_NAME}" \
    --address-prefix "10.10.0.0/16" \
    --subnet-name "${SUBNET_NAME}" \
    --subnet-prefix "10.10.1.0/24"

echo "Step 3: Creating Zone-Redundant Standard Public IP..."
az network public-ip create \
    --resource-group "${RESOURCE_GROUP}" \
    --name "${PIP_NAME}" \
    --sku Standard \
    --tier Regional \
    --zone 1 2 3 \
    --allocation-method Static

echo "Step 4: Creating Standard Load Balancer with Zone-Redundant Frontend..."
az network lb create \
    --resource-group "${RESOURCE_GROUP}" \
    --name "${LB_NAME}" \
    --sku Standard \
    --public-ip-address "${PIP_NAME}" \
    --frontend-ip-name "fe-ip-config" \
    --backend-pool-name "be-pool-web"

echo "Step 5: Configuring Load Balancer Health Probe and Rule (Port 80)..."
az network lb probe create \
    --resource-group "${RESOURCE_GROUP}" \
    --lb-name "${LB_NAME}" \
    --name "probe-http-80" \
    --protocol Http \
    --port 80 \
    --path "/"

az network lb rule create \
    --resource-group "${RESOURCE_GROUP}" \
    --lb-name "${LB_NAME}" \
    --name "rule-http-80" \
    --protocol Tcp \
    --frontend-port 80 \
    --backend-port 80 \
    --frontend-ip-name "fe-ip-config" \
    --backend-pool-name "be-pool-web" \
    --probe-name "probe-http-80"

echo "Step 6: Deploying Virtual Machines Across Availability Zones 1, 2, and 3..."
for ZONE in 1 2 3; do
    VM_NAME="vm-zonal-0${ZONE}"
    NIC_NAME="nic-${VM_NAME}"

    echo "Deploying Network Interface for ${VM_NAME}..."
    az network nic create \
        --resource-group "${RESOURCE_GROUP}" \
        --name "${NIC_NAME}" \
        --vnet-name "${VNET_NAME}" \
        --subnet "${SUBNET_NAME}" \
        --lb-name "${LB_NAME}" \
        --lb-address-pools "be-pool-web"

    echo "Deploying ${VM_NAME} pinned to Zone ${ZONE}..."
    az vm create \
        --resource-group "${RESOURCE_GROUP}" \
        --name "${VM_NAME}" \
        --zone "${ZONE}" \
        --nics "${NIC_NAME}" \
        --image "Ubuntu2204" \
        --size "${VM_SIZE}" \
        --admin-username "${ADMIN_USER}" \
        --generate-ssh-keys \
        --no-wait
done

echo "Multi-zone deployment initiated. All three instances are distributed across physical availability zones."
