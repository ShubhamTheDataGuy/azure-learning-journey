# Azure Learning Journey

Daily hands-on tutorials and blogs documenting practical cloud engineering with Microsoft Azure.

## Articles & Labs
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
