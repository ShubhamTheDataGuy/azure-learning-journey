# Azure Learning Journey

Daily hands-on tutorials and blogs documenting practical cloud engineering with Microsoft Azure.

## Articles & Labs
- **[Day 5: Azure High Availability – Availability Sets vs Availability Zones](./day-05-azure-availability-zones-and-sets/blog-article.md)**
  - Physical infrastructure failure modes and the Azure resiliency hierarchy
  - SLA mathematics: 99.9% vs 99.95% vs 99.99% availability tiers
  - Availability Sets deep dive: Fault Domains (racks/PDU/switch isolation) and Update Domains (host maintenance isolation)
  - Managed Disks storage cluster alignment with compute fault domains
  - Availability Zones deep dive: physically separated datacenters, independent power/cooling, and sub-2ms fiber mesh
  - Zonal vs Zone-Redundant vs Regional resource classification
  - Subscription logical-to-physical zone mapping mechanics
  - Standard Load Balancer integration with zone-redundant frontends and health probes
  - Production Azure CLI automation scripts and Bicep infrastructure-as-code blueprints
  - Comprehensive 12-dimension comparison matrix and 1-year quick revision cheat sheet
- **[Day 4: Azure Custom Script Extensions – Windows (IIS) & Linux (NGINX)](./day-04-azure-custom-script-extension/blog-article.md)**
  - Azure Storage Account provisioning (`storageshubham01`) with private blob container (`scripts`)
  - Authoring cross-platform automation scripts: PowerShell for IIS (`setup-iis.ps1`) and Bash for NGINX (`setup-nginx.sh`)
  - Windows Server 2025 (`webvm01`) deployment with Custom Script Extension in the VM Advanced wizard
  - Ubuntu Linux 24.04 (`webvm02`) deployment with Custom Script for Linux extension and explicit shell command invocation
  - Network Security Group (NSG) configuration for inbound HTTP (Port 80) traffic
  - Resolving IIS default document precedence vs custom `default.html`
  - Zero-touch public endpoint verification for both IIS and NGINX servers without RDP or SSH access
- **[Day 3: Azure VM Encryption – SSE with CMK & BitLocker ADE](./day-03-azure-vm-encryption/blog-article.md)**
  - Azure Key Vault deployment with Azure RBAC permission model
  - Resolving Key Vault data plane authorization errors (`Key Vault Administrator` role assignment)
  - Hardware-backed RSA 2048-bit cryptographic key generation
  - Disk Encryption Set (DES) creation and Server-Side Encryption (SSE) with Customer-Managed Keys (CMK)
  - Key Vault Access configuration for volume encryption (`Azure Disk Encryption for volume encryption`)
  - Enabling Azure Disk Encryption on Windows Server 2025 OS disks via VM Extension
  - In-guest BitLocker encryption verification with `manage-bde -status` (XTS-AES 256 and BEK volume)
- **[Day 2: Azure Windows VM, Data Disks, Snapshots & Migration](./day-02-azure-windows-vm-data-disks-snapshots-migration/blog-article.md)**
  - Windows Server 2025 Datacenter provisioning & RDP access (port 3389)
  - Resolving regional compute SKU availability (`NotAvailableForSubscription`)
  - Attaching 4 GiB Premium SSD data disks at LUN 0
  - In-guest GPT initialization, NTFS formatting, and drive assignment in Server Manager
  - Point-in-time Azure Disk Snapshot creation
  - Snapshot to Managed Disk restoration workflow
  - Cross-VM disk attachment and in-guest data integrity verification
- **[Day 1: Deploying a Linux Virtual Machine & Setting Up Nginx](./day-01-azure-linux-vm/blog-article.md)**
  - Azure Portal VM provisioning (Ubuntu 24.04 LTS)
  - SSH configuration and remote connection
  - Nginx installation & systemd status
  - Network Security Group (NSG) troubleshooting: Port 80 HTTP rules
  - Verification & teardown
