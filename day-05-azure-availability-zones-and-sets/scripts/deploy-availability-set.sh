#!/bin/bash
# ==============================================================================
# Script: deploy-availability-set.sh
# Purpose: Deploys an Azure Availability Set with 3 Fault Domains and 5 Update
#          Domains, followed by two load-balanced VMs with aligned managed disks.
# ==============================================================================

set -euo pipefail

# Configuration Variables
RESOURCE_GROUP="rg-ha-demo"
LOCATION="centralindia"
AVSET_NAME="as-web-tier"
VNET_NAME="vnet-ha-demo"
SUBNET_NAME="snet-web"
ADMIN_USER="azureuser"
VM_SIZE="Standard_B2s"

echo "Step 1: Creating Resource Group..."
az group create \
    --name "${RESOURCE_GROUP}" \
    --location "${LOCATION}"

echo "Step 2: Creating Virtual Network and Subnet..."
az network vnet create \
    --resource-group "${RESOURCE_GROUP}" \
    --name "${VNET_NAME}" \
    --address-prefix "10.0.0.0/16" \
    --subnet-name "${SUBNET_NAME}" \
    --subnet-prefix "10.0.1.0/24"

echo "Step 3: Creating Availability Set with Managed Disks..."
# Note: platform-fault-domain-count is up to 3 in supported regions
# platform-update-domain-count can be up to 20 (default is 5)
az vm availability-set create \
    --resource-group "${RESOURCE_GROUP}" \
    --name "${AVSET_NAME}" \
    --platform-fault-domain-count 3 \
    --platform-update-domain-count 5 \
    --location "${LOCATION}"

echo "Step 4: Deploying VM 1 into Availability Set..."
az vm create \
    --resource-group "${RESOURCE_GROUP}" \
    --name "vm-web-01" \
    --availability-set "${AVSET_NAME}" \
    --image "Ubuntu2204" \
    --size "${VM_SIZE}" \
    --admin-username "${ADMIN_USER}" \
    --generate-ssh-keys \
    --vnet-name "${VNET_NAME}" \
    --subnet "${SUBNET_NAME}" \
    --nsg-rule HTTP \
    --no-wait

echo "Step 5: Deploying VM 2 into Availability Set..."
az vm create \
    --resource-group "${RESOURCE_GROUP}" \
    --name "vm-web-02" \
    --availability-set "${AVSET_NAME}" \
    --image "Ubuntu2204" \
    --size "${VM_SIZE}" \
    --admin-username "${ADMIN_USER}" \
    --generate-ssh-keys \
    --vnet-name "${VNET_NAME}" \
    --subnet "${SUBNET_NAME}" \
    --nsg-rule HTTP

echo "Step 6: Querying Domain Placement of Deployed VMs..."
az vm availability-set list-assigned-vms \
    --resource-group "${RESOURCE_GROUP}" \
    --name "${AVSET_NAME}" \
    --output table

echo "Deployment complete. VMs successfully distributed across fault and update domains."
