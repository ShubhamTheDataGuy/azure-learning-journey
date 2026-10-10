# Day 8: AZ-104 Microsoft Azure Administrator Practice Exam & Milestone Quiz (Days 1–7)

*A comprehensive 24-question scenario-based certification practice exam covering Azure compute, storage, virtual networking, encryption, high availability, and scaling from Days 1 to 7.*

---

## Introduction & Exam Blueprint Alignment

Welcome to the Day 8 milestone review of the Azure Learning Journey. Over the past seven days, we built real-world cloud infrastructure from the ground up: provisioning Linux and Windows compute nodes, managing data disks and snapshots, securing workloads with Azure Key Vault and disk encryption, automating bootstraps with Custom Script Extensions, engineering multi-rack and multi-zone high availability, and mastering both Uniform and Flexible Virtual Machine Scale Sets.

This milestone guide is designed from the perspective of the **AZ-104: Microsoft Azure Administrator** certification exam. In the official AZ-104 exam, questions are heavily scenario-driven: you are presented with business requirements, architectural constraints, network diagrams, and operational roadblocks, and must determine the correct configuration or troubleshooting command.

### AZ-104 Exam Objective Mapping

| Exam Domain | Official Exam Weight | Covered Lab Topics (Days 1–7) | Practice Questions |
| :--- | :--- | :--- | :--- |
| **Manage Azure identities and governance** | 15–20% | Azure RBAC, Key Vault permissions, Key Vault Administrator role (Day 3) | Questions 7, 8 |
| **Implement and manage storage** | 15–20% | Managed Disks, LUNs, Snapshots (Full vs Incremental), SSE with CMK, ADE (Days 2 & 3) | Questions 4, 5, 6, 9 |
| **Deploy and manage Azure compute resources** | 20–25% | Linux/Windows VMs, Custom Script Extensions, Availability Sets, Availability Zones, VMSS Uniform & Flexible (Days 1, 2, 4, 5, 6, 7) | Questions 1, 10, 11, 12, 13, 14, 15, 16, 21, 22, 23, 24 |
| **Configure and manage virtual networking** | 20–25% | VNets, Subnets, Network Security Groups (NSGs), Port priorities, Public IPs (Days 1 & 4) | Questions 1, 2, 3 |
| **Monitor and maintain Azure resources** | 10–15% | Azure Monitor autoscale rules, `Microsoft.Insights`, Metric lookback, Cooldown timers (Day 6) | Questions 17, 18, 19, 20 |

---

## Interactive AZ-104 Practice Exam Simulator

Test your knowledge in real time before reviewing the detailed architectural explanations below. Select your answers and click **Submit Exam & Calculate Score** to evaluate your performance against the official passing threshold of **700 / 1000**.

<div id="quiz-container" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 24px; margin-bottom: 32px; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 20px;">
<div>
<h3 style="margin: 0; color: #0f172a;">AZ-104 Interactive Exam Simulator</h3>
<p style="margin: 4px 0 0 0; color: #64748b; font-size: 14px;">Total Questions: 24 | Passing Score: 700 / 1000 (70%)</p>
</div>
<div id="quiz-badge" style="background: #0284c7; color: #ffffff; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 13px;">
Status: In Progress
</div>
</div>
<form id="az104-quiz-form">
<div id="quiz-questions-render"></div>
<div style="margin-top: 28px; display: flex; gap: 12px; align-items: center;">
<button type="button" id="btn-submit-quiz" onclick="window.gradeQuiz()" style="background: #0284c7; color: #ffffff; border: none; padding: 10px 24px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 14px;">
Submit Exam & Calculate Score
</button>
<button type="button" id="btn-reset-quiz" onclick="window.resetQuiz()" style="background: #e2e8f0; color: #334155; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 14px;">
Reset Exam
</button>
</div>
</form>
<div id="quiz-result-card" style="display: none; margin-top: 24px; padding: 20px; border-radius: 6px; border: 1px solid #cbd5e1;"></div>
</div>

<script>
const quizQuestions = [
  {
    id: 1,
    topic: "Day 1: Virtual Networking & NSGs",
    question: "You have an Azure Linux VM running Ubuntu 24.04 with Nginx active on TCP port 80. An NSG associated with the subnet has an inbound rule 'Allow-SSH' with Priority 100 (port 22) and the default rule 'DenyAllInBound' with Priority 65500. Users report they cannot browse to the Nginx landing page. You add a new inbound security rule named 'Allow-HTTP' with Priority 65501 allowing port 80. The issue persists. Why can users still not access the web server?",
    options: [
      "A. The priority number 65501 is higher than 65500, meaning DenyAllInBound is evaluated and matches first.",
      "B. Azure NSGs do not support port 80 on Ubuntu Linux without an Application Gateway.",
      "C. The rule priority must match the port number (priority must be 80).",
      "D. Inbound rules only apply to virtual network internal traffic, not Internet traffic."
    ],
    correct: 0,
    explanation: "NSG rules are processed in priority order from lowest number to highest number. Because 65500 is lower than 65501, the default DenyAllInBound rule is evaluated first and drops the packet before Allow-HTTP is ever reached. Priority must be between 100 and 4096 (e.g., Priority 200)."
  },
  {
    id: 2,
    topic: "Day 1: Compute & SSH Access",
    question: "You need to securely connect to an Azure Linux VM over SSH using password authentication from your management workstation. Which combination of network prerequisites must be satisfied?",
    options: [
      "A. The VM must have an assigned public IP or Bastion, the NSG must allow inbound TCP port 22, and the guest sshd configuration must permit password authentication.",
      "B. The VM must have a dedicated ExpressRoute circuit and port 3389 opened on the network interface.",
      "C. The VM must belong to an Azure Active Directory Domain Services managed domain.",
      "D. Password authentication requires an attached Ultra Disk at LUN 0."
    ],
    correct: 0,
    explanation: "For direct external SSH access using passwords, the VM needs a routable endpoint (Public IP, Bastion, or NAT rule), an NSG allowing inbound traffic on TCP port 22, and the Linux guest OS sshd service configured with PasswordAuthentication yes."
  },
  {
    id: 3,
    topic: "Day 1: Network Security Group Hierarchy",
    question: "An administrator associates NSG-Subnet with Subnet-1 and NSG-NIC with the network interface of VM-1. When an inbound packet arrives from the Internet targeted at VM-1, in what sequence are the network security group rules evaluated?",
    options: [
      "A. NSG-Subnet is evaluated first; if permitted, NSG-NIC is evaluated second. If either denies the traffic, the packet is dropped.",
      "B. NSG-NIC is evaluated first; if permitted, NSG-Subnet is evaluated second.",
      "C. Only the NSG with the lowest rule priority number across both groups is evaluated.",
      "D. Rules from both NSGs are merged into a single priority list and executed simultaneously."
    ],
    correct: 0,
    explanation: "For inbound traffic, Azure evaluates the Subnet NSG first. If traffic is allowed, it is then evaluated by the NIC NSG. If either layer drops the traffic, the packet is denied. For outbound traffic, the reverse occurs: NIC NSG first, then Subnet NSG."
  },
  {
    id: 4,
    topic: "Day 2: Managed Disks & In-Guest Volume Setup",
    question: "You attach a new 128 GiB Premium SSD data disk in the Azure Portal at LUN 0 to an existing Windows Server 2025 virtual machine. You log in via RDP but notice the new volume does not appear in File Explorer. What is the required next step?",
    options: [
      "A. Inside the Windows guest OS, open Disk Management, bring the disk online, initialize it with GPT partition style, and format a volume with NTFS/ReFS.",
      "B. Restart the virtual machine from the Azure Portal to force Azure Resource Manager to format the disk.",
      "C. Change the disk host caching property from None to Read/Write in the Azure Portal.",
      "D. Upgrade the virtual machine compute SKU to an E-series memory-optimized size."
    ],
    correct: 0,
    explanation: "Azure provisions managed data disks as raw, uninitialized block storage devices. The cloud fabric attaches the disk to the virtual SCSI controller, but the guest operating system administrator must bring the disk online, initialize the partition table (GPT/MBR), and format the file system (NTFS/ReFS)."
  },
  {
    id: 5,
    topic: "Day 2: Azure Disk Snapshots & Migration",
    question: "You take a point-in-time Snapshot of a managed data disk attached to VM-A. You need to attach the data captured in this snapshot as a new data disk to VM-B. What is the required procedure?",
    options: [
      "A. You cannot attach a snapshot directly to a VM. You must first create an Azure Managed Disk from the snapshot, then attach that new Managed Disk to VM-B.",
      "B. In VM-B, go to Disks > Attach existing disk and select the snapshot resource directly.",
      "C. Convert the snapshot to an Azure Storage Blob container, download the VHD, and upload it via AzCopy.",
      "D. Restore the snapshot using Azure Backup Recovery Services Vault only."
    ],
    correct: 0,
    explanation: "Azure Snapshots are read-only point-in-time copies. A snapshot cannot be directly mounted or attached to a virtual machine SCSI controller. You must first provision an Azure Managed Disk with the snapshot as its source, and then attach that managed disk to the target VM."
  },
  {
    id: 6,
    topic: "Day 2: Incremental vs Full Snapshots",
    question: "You manage a 1 TB managed data disk where only 25 GB of data changes daily. You need to implement daily snapshots while minimizing storage costs and retaining cross-region copy capability. What should you configure?",
    options: [
      "A. Create Incremental Snapshots, which only store and bill for the differential blocks changed since the previous snapshot.",
      "B. Create Full Snapshots, because incremental snapshots do not support differential block storage.",
      "C. Deallocate the VM before taking a full VHD clone to an archive blob container.",
      "D. Use Disk Export with a SAS URL generated daily."
    ],
    correct: 0,
    explanation: "Incremental snapshots are billed only for the changed delta blocks (25 GB), drastically reducing storage expenditure compared to full snapshots (1 TB each). They also support differential copy across regions for disaster recovery."
  },
  {
    id: 7,
    topic: "Day 3: Azure Key Vault & Managed Identities",
    question: "You create an Azure Key Vault with Azure RBAC authorization enabled and generate an RSA key named 'db-enc-key'. You attempt to create a Disk Encryption Set (DES) referencing this key, but the operation fails with an authorization error. What must you configure?",
    options: [
      "A. Assign the system-assigned managed identity of the Disk Encryption Set the 'Key Vault Crypto Service Encryption User' role on the Key Vault.",
      "B. Change the Key Vault permission model to classic Access Policies and grant your personal user account Owner permissions.",
      "C. Enable public network access from all networks on the Key Vault firewall.",
      "D. Export the private key from the Key Vault and embed it in the ARM deployment template."
    ],
    correct: 0,
    explanation: "When a Disk Encryption Set is provisioned, Azure automatically creates a system-assigned managed identity for it. Under Azure RBAC, that managed identity must be granted the 'Key Vault Crypto Service Encryption User' role (or wrap/unwrap permissions) on the Key Vault to access the key."
  },
  {
    id: 8,
    topic: "Day 3: Server-Side Encryption (SSE) vs Azure Disk Encryption (ADE)",
    question: "An auditor asks you to distinguish between Server-Side Encryption with Customer-Managed Keys (SSE with CMK) and Azure Disk Encryption (ADE). Which statement accurately describes the architectural difference?",
    options: [
      "A. SSE encrypts data at rest at the Azure storage host level using hypervisor CPU cycles; ADE operates inside the guest OS using BitLocker (Windows) or DM-Crypt (Linux).",
      "B. SSE only works on unmanaged disks, whereas ADE is required for all Azure Managed Disks.",
      "C. ADE is managed exclusively by Microsoft platform keys, while SSE requires customer-managed keys.",
      "D. SSE requires a VM extension running inside the guest operating system, while ADE requires no guest agent."
    ],
    correct: 0,
    explanation: "Server-Side Encryption (SSE) encrypts storage data at rest at the Azure physical storage cluster/host level transparently without consuming VM CPU. Azure Disk Encryption (ADE) utilizes a VM extension to enable OS-level BitLocker (Windows) or DM-Crypt (Linux) inside the guest OS."
  },
  {
    id: 9,
    topic: "Day 3: Disk Encryption Sets (DES) Configuration",
    question: "You want to update an existing, attached OS managed disk on a production VM from platform-managed keys (PMK) to customer-managed keys (CMK) using a Disk Encryption Set. What prerequisite action must you perform on the virtual machine?",
    options: [
      "A. You must stop (deallocate) the virtual machine before associating the Disk Encryption Set with the OS disk.",
      "B. You must delete the VM and redeploy it from an unencrypted generalized image.",
      "C. You can update the DES live while the VM is running without any downtime.",
      "D. You must convert the disk from Premium SSD to Standard HDD first."
    ],
    correct: 0,
    explanation: "To change the encryption settings or associate a Disk Encryption Set with an attached OS disk, the virtual machine must be in the Stopped (Deallocated) state. Once deallocated, the disk encryption property can be modified and the VM restarted."
  },
  {
    id: 10,
    topic: "Day 4: Custom Script Extension & Storage Security",
    question: "You use the Custom Script for Linux extension to deploy an application on an Ubuntu VM. The setup script is stored in a private Azure Blob Storage container with no anonymous public access. How does the VM extension authenticate to download the script?",
    options: [
      "A. The storage account access key or SAS URI is provided inside the extension's protectedSettings block, which is encrypted by Azure.",
      "B. The storage container must be converted to Public Read access during deployment.",
      "C. The VM must download the script via an anonymous GitHub mirror.",
      "D. VM extensions cannot access private Azure Blob Storage containers."
    ],
    correct: 0,
    explanation: "Custom Script Extensions accept a protectedSettings configuration block. Credentials placed in protectedSettings (such as storageAccountKey or SAS tokens) are encrypted by Azure Resource Manager and decrypted only inside the guest VM agent."
  },
  {
    id: 11,
    topic: "Day 4: VM Extension Execution Limits",
    question: "You author a Custom Script Extension on a Windows Server VM that runs a complex database restoration task. The extension remains in the 'Transitioning' status and eventually terminates with a failure code after 90 minutes. What is the root cause?",
    options: [
      "A. Azure VM extensions enforce a hard 90-minute maximum execution timeout; scripts exceeding this limit are terminated as failed.",
      "B. Windows Server Datacenter restricts PowerShell scripts to a 15-minute runtime ceiling.",
      "C. The Azure storage account throttled the script download after 30 minutes.",
      "D. The virtual machine ran out of IOPS on the temporary disk (D: drive)."
    ],
    correct: 0,
    explanation: "Azure VM Custom Script Extensions enforce an absolute maximum execution window of 90 minutes. If a script runs longer or prompts for interactive console input that never arrives, the Azure guest agent times out and marks the deployment as failed."
  },
  {
    id: 12,
    topic: "Day 4: Extension Idempotency & Reboots",
    question: "A PowerShell script executed via Custom Script Extension requires a system reboot halfway through its configuration steps. What is the recommended practice for handling reboots in custom extension scripts?",
    options: [
      "A. Design the script to be idempotent, recording completed milestones in a marker file or registry key so that upon reboot resumption it continues without repeating steps.",
      "B. Never reboot inside an extension; reboots immediately corrupt the Azure VM agent.",
      "C. Trigger an immediate hard shutdown using Stop-Computer without returning an exit code.",
      "D. Split the script into 5 separate Custom Script Extensions attached simultaneously."
    ],
    correct: 0,
    explanation: "If a script triggers a reboot, it must be written idempotently. The script should verify what has already completed before executing commands so that subsequent passes exit with code 0 once all tasks are complete."
  },
  {
    id: 13,
    topic: "Day 5: Availability Sets Mechanics",
    question: "You deploy four virtual machines in an Availability Set configured with 2 Fault Domains (FD) and 2 Update Domains (UD). VM-1 is in (FD0, UD0), VM-2 is in (FD1, UD1), VM-3 is in (FD0, UD0), and VM-4 is in (FD1, UD1). If a hardware power supply unit (PSU) fails on the rack hosting Fault Domain 0, which virtual machines remain operational?",
    options: [
      "A. VM-2 and VM-4 remain running, because they are isolated on physical rack hardware in Fault Domain 1.",
      "B. Only VM-1 remains running.",
      "C. All four VMs go offline because they share the same availability set.",
      "D. All four VMs remain running due to automatic hypervisor memory cloning."
    ],
    correct: 0,
    explanation: "Fault Domains define physical hardware rack, power supply, and network switch isolation. If the physical rack hosting Fault Domain 0 experiences a hardware power failure, VMs in Fault Domain 1 (VM-2 and VM-4) are physically isolated and remain fully operational."
  },
  {
    id: 14,
    topic: "Day 5: Availability Zones & SLA Guarantees",
    question: "An enterprise workload requires a Microsoft Azure SLA of at least 99.99% for its virtual machine compute tier in a single region. Which architectural requirement is mandatory?",
    options: [
      "A. Deploy two or more virtual machines across two or more Availability Zones in the region, fronted by a Zone-Redundant Standard Load Balancer.",
      "B. Deploy two virtual machines in an Availability Set with 3 Fault Domains and Premium SSDs.",
      "C. Deploy a single virtual machine with an Ultra Disk and 128 vCPUs.",
      "D. Configure cross-region asynchronous storage replication using GRS."
    ],
    correct: 0,
    explanation: "The Azure 99.99% compute SLA is achieved only when two or more instances are distributed across separate physical Availability Zones within the same region, with traffic distributed via a Zone-Redundant Standard Load Balancer. Availability Sets provide up to 99.95%."
  },
  {
    id: 15,
    topic: "Day 5: Availability Set Migration Constraints",
    question: "You have a standalone production virtual machine named 'vm-core' that was deployed without an Availability Set. Leadership asks you to add 'vm-core' into an existing Availability Set named 'as-prod'. Can you perform this action directly in the Azure Portal?",
    options: [
      "A. No. A virtual machine can only be placed in an Availability Set during initial creation; you must delete the VM (retaining its OS disk) and recreate it inside the Availability Set.",
      "B. Yes. Open the VM Availability blade, select Change Availability Set, and restart the VM.",
      "C. Yes, provided the VM is stopped (deallocated) before moving.",
      "D. No, standalone VMs can never be placed into an Availability Set under any circumstances."
    ],
    correct: 0,
    explanation: "Azure does not support moving an existing virtual machine into an Availability Set after deployment. The standard pattern is to capture/retain the existing OS managed disk, delete the VM resource, and deploy a new VM from that managed disk specifying the target Availability Set."
  },
  {
    id: 16,
    topic: "Day 5: Managed Disks & Fault Domain Alignment",
    question: "Why does Microsoft mandate using Azure Managed Disks (rather than legacy unmanaged storage account VHDs) when deploying VMs in an Availability Set?",
    options: [
      "A. Managed Disks automatically align the storage cluster fault domains with the compute fault domains of the VMs, preventing single storage rack failures from affecting multiple VMs.",
      "B. Unmanaged disks do not support NTFS or ext4 file systems.",
      "C. Managed Disks provide unlimited free storage for up to 3 years.",
      "D. Availability Sets cannot be created without attaching at least 4 data disks."
    ],
    correct: 0,
    explanation: "When Managed Disks are used with an Availability Set, the Azure fabric controller aligns storage cluster fault domains with compute fault domains. With legacy unmanaged disks, multiple VMs might store VHDs in the same storage cluster, creating a single point of failure."
  },
  {
    id: 17,
    topic: "Day 6: VMSS Autoscale Temporal Mechanics",
    question: "You configure an autoscale rule on a Uniform VMSS with baseline count 1: 'If Average Percentage CPU > 70% over 5 minutes, increase count by 1 (Cooldown: 5 minutes)'. If CPU load jumps to 95% at 10:00 AM and remains at 95% until 10:12 AM, what is the instance count at 10:12 AM?",
    options: [
      "A. 3 instances (scales to 2 at 10:05 AM, cooldown suppresses actions until 10:10 AM, then scales to 3 at 10:11-10:12 AM).",
      "B. 1 instance (cooldown prevents any scaling for the first 15 minutes).",
      "C. 7 instances (scales out by 1 instance every single minute load is sustained).",
      "D. 2 instances (autoscale rules can only fire once per calendar day)."
    ],
    correct: 0,
    explanation: "At 10:05 AM (5-minute rolling average > 70%), Azure scales from 1 to 2 instances. A 5-minute cooldown activates from 10:05 to 10:10 AM. At 10:10 AM, cooldown expires. By 10:11-10:12 AM, the sustained 95% CPU load breaches the threshold again, scaling to 3 instances."
  },
  {
    id: 18,
    topic: "Day 6: Missing Resource Provider Registration",
    question: "When configuring a custom metric autoscale setting on a scale set, saving fails with 'MissingSubscriptionRegistration: The subscription is not registered to use namespace microsoft.insights'. Which command resolves this?",
    options: [
      "A. az provider register --namespace Microsoft.Insights",
      "B. az vmss update --name SET0000 --enable-insights",
      "C. az monitor alert create --insights-enable true",
      "D. az feature register --namespace Microsoft.Compute --name Autoscale"
    ],
    correct: 0,
    explanation: "Azure Monitor autoscaling operates under the Microsoft.Insights resource provider. If this namespace is not registered on the subscription, ARM API calls to create or update autoscale settings fail with MissingSubscriptionRegistration. Running az provider register --namespace Microsoft.Insights registers the namespace."
  },
  {
    id: 19,
    topic: "Day 6: Autoscale Asymmetric Rules & Flapping",
    question: "An administrator creates a scale-out rule: 'When CPU > 80%, add 1 VM'. No scale-in rule is created. During the night, CPU drops to 4%. What happens to the scale set instances and cloud billing?",
    options: [
      "A. The scale set remains at its maximum scaled-out instance count indefinitely, continuing to incur compute charges until a scale-in rule is created or manual reduction occurs.",
      "B. Azure automatically terminates all instances once CPU drops below 10%.",
      "C. The scale set deallocates instances automatically at midnight UTC.",
      "D. An error notification is sent and the scale set resets to 0 instances."
    ],
    correct: 0,
    explanation: "Autoscale rules are strictly deterministic. Azure Monitor never assumes an intention to scale in without an explicit scale-in rule. Without a paired scale-in rule (e.g., CPU < 25%), instances remain active at peak capacity, leading to severe unexpected billing."
  },
  {
    id: 20,
    topic: "Day 6: Autoscale Cooldown Purpose",
    question: "What critical failure condition does the autoscale 'Cooldown' period prevent in production environments?",
    options: [
      "A. Flapping (thrashing) and premature over-provisioning caused by evaluating metrics before newly provisioned VMs have fully initialized and absorbed traffic.",
      "B. Operating system kernel crashes caused by high processor clock speeds.",
      "C. Throttling of the Azure Key Vault cryptographic REST APIs.",
      "D. Memory leaks inside the guest systemd init process."
    ],
    correct: 0,
    explanation: "Newly launched instances require time to boot, start web services, and receive load balancer health probe passes. Cooldown enforces a quiet period, preventing the autoscale engine from repeatedly firing additional scale-outs before the new VM can alleviate the load."
  },
  {
    id: 21,
    topic: "Day 7: Flexible Orchestration Mode & Multi-SKU",
    question: "You need to configure a scale set that combines Standard_B2ts_v2, Standard_B2ats_v2, and Standard_B2als_v2 virtual machines in the same tier, automatically deploying the cheapest available size upon scale-out. What orchestration mode and setting must you choose?",
    options: [
      "A. Flexible Orchestration Mode with a Multi-SKU profile and the 'Lowest price' allocation strategy.",
      "B. Uniform Orchestration Mode with an Availability Set attachment.",
      "C. Classic Cloud Services with dynamic VIP swapping.",
      "D. Azure Batch compute pool with dedicated node reservation."
    ],
    correct: 0,
    explanation: "Flexible Orchestration Mode is the only scale set mode that supports selecting up to 5 different VM sizes in a single scale set. Setting the Allocation Strategy to 'Lowest price' enables Azure to dynamically pick the cheapest available SKU when provisioning capacity."
  },
  {
    id: 22,
    topic: "Day 7: Attaching Standalone VMs via Azure CLI",
    question: "You want to deploy a new standalone Linux VM named 'vm-worker02' and immediately associate it as an active member of an existing Flexible scale set named 'set0001'. Which Azure CLI command parameter is used?",
    options: [
      "A. az vm create --resource-group rg --name vm-worker02 --vmss set0001 ...",
      "B. az vmss add-instance --scale-set set0001 --vm vm-worker02",
      "C. az vm join-pool --name vm-worker02 --target set0001",
      "D. az compute attach --vm vm-worker02 --scale-set set0001"
    ],
    correct: 0,
    explanation: "In Azure CLI, the az vm create command provides the --vmss parameter. When targeted at a scale set configured in Flexible orchestration mode, the newly created standalone VM is registered as a member instance of the scale set."
  },
  {
    id: 23,
    topic: "Day 7: Platform Fault Domain Spreading",
    question: "An enterprise wants to migrate from legacy Availability Sets to a modern compute architecture that supports mixed VM sizes, scales up to 1,000 instances, and guarantees physical server rack (Fault Domain) isolation within an Availability Zone. What should you recommend?",
    options: [
      "A. Virtual Machine Scale Sets in Flexible Orchestration Mode with Platform Fault Domain spread configured.",
      "B. Virtual Machine Scale Sets in Uniform Orchestration Mode with spot priority.",
      "C. Proximity Placement Groups with single standalone VMs.",
      "D. Dedicated Host Groups spanning multiple geographical regions."
    ],
    correct: 0,
    explanation: "Flexible VMSS is Microsoft's strategic successor to Availability Sets. It supports spreading standalone VMs across up to 5 platform fault domains within an availability zone, supports mixed VM sizes, and scales up to 1,000 instances."
  },
  {
    id: 24,
    topic: "Day 7: Resource Representation Differences",
    question: "How do virtual machine instances appear in Azure Resource Manager (ARM) when deployed in Flexible mode compared to Uniform mode?",
    options: [
      "A. In Flexible mode, each instance is a first-class, standalone Microsoft.Compute/virtualMachines resource visible directly in the resource group; in Uniform mode, instances are child resources under the scale set URI.",
      "B. In Uniform mode, instances have independent public IPs, while Flexible mode instances cannot have IP addresses.",
      "C. Flexible mode instances do not have OS disks in the resource group.",
      "D. Uniform mode instances are managed via the Azure Kubernetes Service control plane."
    ],
    correct: 0,
    explanation: "In Uniform mode, instances are subordinate child entities (virtualMachineScaleSets/virtualMachines). In Flexible mode, each instance is a full, top-level Microsoft.Compute/virtualMachines resource with its own independent OS disk, NIC, and lifecycle."
  }
];

function renderQuiz() {
  const container = document.getElementById("quiz-questions-render");
  if (!container) return;
  if (container.children.length > 0) return;
  let html = "";
  quizQuestions.forEach((q, idx) => {
    html += `
      <div id="q-card-${q.id}" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 18px; margin-bottom: 18px;">
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px;">
          <span style="font-size: 12px; font-weight: 700; color: #0284c7; text-transform: uppercase;">Question ${q.id} of 24 &bull; ${q.topic}</span>
          <span id="q-status-${q.id}" style="font-size: 12px; font-weight: 600; color: #94a3b8;">Unanswered</span>
        </div>
        <p style="font-weight: 600; color: #1e293b; margin: 0 0 14px 0; font-size: 15px; line-height: 1.5;">${q.question}</p>
        <div style="display: flex; flex-direction: column; gap: 8px;">
    `;
    q.options.forEach((opt, optIdx) => {
      html += `
        <label style="display: flex; align-items: flex-start; gap: 10px; cursor: pointer; padding: 8px 12px; border-radius: 4px; border: 1px solid #e2e8f0; background: #f8fafc; font-size: 14px; color: #334155;">
          <input type="radio" name="q_${q.id}" value="${optIdx}" onchange="window.markAnswered(${q.id})" style="margin-top: 3px;">
          <span>${opt}</span>
        </label>
      `;
    });
    html += `
        </div>
        <div id="q-feedback-${q.id}" style="display: none; margin-top: 12px; padding: 10px 14px; border-radius: 4px; font-size: 13px; line-height: 1.4;"></div>
      </div>
    `;
  });
  container.innerHTML = html;
}

function markAnswered(qId) {
  const statusEl = document.getElementById(`q-status-${qId}`);
  if (statusEl) {
    statusEl.innerText = "Answered";
    statusEl.style.color = "#0284c7";
  }
}

function gradeQuiz() {
  let score = 0;
  let correctCount = 0;
  let answeredCount = 0;

  quizQuestions.forEach(q => {
    const selected = document.querySelector(`input[name="q_${q.id}"]:checked`);
    const card = document.getElementById(`q-card-${q.id}`);
    const feedback = document.getElementById(`q-feedback-${q.id}`);
    const statusEl = document.getElementById(`q-status-${q.id}`);

    if (selected) {
      answeredCount++;
      const userAns = parseInt(selected.value, 10);
      feedback.style.display = "block";

      if (userAns === q.correct) {
        correctCount++;
        statusEl.innerText = "Correct";
        statusEl.style.color = "#16a34a";
        card.style.border = "1px solid #86efac";
        card.style.background = "#f0fdf4";
        feedback.style.background = "#dcfce7";
        feedback.style.color = "#166534";
        feedback.innerHTML = `<strong>Correct:</strong> ${q.explanation}`;
      } else {
        statusEl.innerText = "Incorrect";
        statusEl.style.color = "#dc2626";
        card.style.border = "1px solid #fca5a5";
        card.style.background = "#fef2f2";
        feedback.style.background = "#fee2e2";
        feedback.style.color = "#991b1b";
        feedback.innerHTML = `<strong>Incorrect.</strong> Correct answer is <strong>${q.options[q.correct].substring(0, 2)}</strong>.<br>${q.explanation}`;
      }
    } else {
      feedback.style.display = "block";
      statusEl.innerText = "Skipped";
      statusEl.style.color = "#d97706";
      card.style.border = "1px solid #fde68a";
      feedback.style.background = "#fef3c7";
      feedback.style.color = "#92400e";
      feedback.innerHTML = `<strong>Skipped.</strong> Correct answer is <strong>${q.options[q.correct].substring(0, 2)}</strong>.<br>${q.explanation}`;
    }
  });

  const scaledScore = Math.round((correctCount / quizQuestions.length) * 1000);
  const passed = scaledScore >= 700;
  const resultCard = document.getElementById("quiz-result-card");
  const badge = document.getElementById("quiz-badge");

  resultCard.style.display = "block";
  if (passed) {
    badge.innerText = "Passed";
    badge.style.background = "#16a34a";
    resultCard.style.background = "#f0fdf4";
    resultCard.style.borderColor = "#86efac";
    resultCard.innerHTML = `
      <h4 style="margin: 0 0 8px 0; color: #166534; font-size: 18px;">Congratulations! You Passed the Practice Exam</h4>
      <p style="margin: 0 0 6px 0; color: #15803d; font-size: 15px;">
        <strong>Scaled Score: ${scaledScore} / 1000</strong> (Passing: 700 / 1000)
      </p>
      <p style="margin: 0; color: #166534; font-size: 14px;">
        Questions Correct: <strong>${correctCount} of 24</strong> (${Math.round((correctCount/24)*100)}%). You have mastered Days 1 through 7 cloud concepts and demonstrate high readiness for the AZ-104 compute and storage exam objectives.
      </p>
    `;
  } else {
    badge.innerText = "Needs Review";
    badge.style.background = "#dc2626";
    resultCard.style.background = "#fef2f2";
    resultCard.style.borderColor = "#fca5a5";
    resultCard.innerHTML = `
      <h4 style="margin: 0 0 8px 0; color: #991b1b; font-size: 18px;">Exam Completed - Passing Score Not Reached</h4>
      <p style="margin: 0 0 6px 0; color: #b91c1c; font-size: 15px;">
        <strong>Scaled Score: ${scaledScore} / 1000</strong> (Passing: 700 / 1000)
      </p>
      <p style="margin: 0; color: #991b1b; font-size: 14px;">
        Questions Correct: <strong>${correctCount} of 24</strong> (${Math.round((correctCount/24)*100)}%). Review the detailed answer explanations and lab deep dives below, then retry the simulator.
      </p>
    `;
  }
}

function resetQuiz() {
  document.getElementById("az104-quiz-form").reset();
  const badge = document.getElementById("quiz-badge");
  const resultCard = document.getElementById("quiz-result-card");
  badge.innerText = "Status: In Progress";
  badge.style.background = "#0284c7";
  resultCard.style.display = "none";

  quizQuestions.forEach(q => {
    const card = document.getElementById(`q-card-${q.id}`);
    const feedback = document.getElementById(`q-feedback-${q.id}`);
    const statusEl = document.getElementById(`q-status-${q.id}`);
    if (card) {
      card.style.background = "#ffffff";
      card.style.borderColor = "#e2e8f0";
    }
    if (feedback) feedback.style.display = "none";
    if (statusEl) {
      statusEl.innerText = "Unanswered";
      statusEl.style.color = "#94a3b8";
    }
  });
}

window.quizQuestions = quizQuestions;
window.renderQuiz = renderQuiz;
window.markAnswered = markAnswered;
window.gradeQuiz = gradeQuiz;
window.resetQuiz = resetQuiz;

if (document.getElementById("quiz-questions-render")) {
  renderQuiz();
}
</script>

---

## Complete Question Bank with In-Depth Architectural Analysis

Below is the complete 24-question repository with collapsible `<details>` answer blocks, distractor breakdowns, real-world exam traps, and links to our hands-on lab articles.

---

### Domain 1: Virtual Networking, Linux Compute & Network Security Groups

#### Question 1
You have an Azure Linux VM running Ubuntu 24.04 with Nginx active on TCP port 80. An NSG associated with the subnet has an inbound rule `Allow-SSH` with Priority 100 (port 22) and the default rule `DenyAllInBound` with Priority 65500. Users report they cannot browse to the Nginx landing page. You add a new inbound security rule named `Allow-HTTP` with Priority 65501 allowing port 80. The issue persists. Why can users still not access the web server?

- **A.** The priority number 65501 is higher than 65500, meaning `DenyAllInBound` is evaluated and matches first.
- **B.** Azure NSGs do not support port 80 on Ubuntu Linux without an Application Gateway.
- **C.** The rule priority must match the port number (priority must be 80).
- **D.** Inbound rules only apply to virtual network internal traffic, not Internet traffic.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Azure Network Security Group (NSG) rules are evaluated strictly in **priority order from lowest number to highest number**. When a packet arrives, the Azure virtual filtering engine iterates through the rule list. As soon as a rule matches the 5-tuple (source IP, source port, destination IP, destination port, protocol), that action is applied immediately and processing terminates.
- Priority `100` (`Allow-SSH`): Matches only port 22. Port 80 packets pass through.
- Priority `65500` (`DenyAllInBound`): Default Azure platform rule matching `*` traffic and denying it.
- Priority `65501` (`Allow-HTTP`): Because 65501 is greater than 65500, `DenyAllInBound` evaluates first and drops the packet. The rule at 65501 is never reached.
- To resolve this, `Allow-HTTP` must be assigned a priority between `100` and `4096` (e.g., Priority `200`).

**Distractor Breakdown:**
- *Option B is incorrect:* Azure NSGs natively filter Layer 4 TCP/UDP traffic regardless of guest OS or load balancers.
- *Option C is incorrect:* Rule priority is an arbitrary integer between 100 and 4096; it does not correspond to port numbers.
- *Option D is incorrect:* Inbound rules filter all ingress packets regardless of origin.

> [!IMPORTANT]
> **AZ-104 Exam Trap:** Remember that default Azure NSG rules (`AllowVNetInBound` at 65000, `AllowAzureLoadBalancerInBound` at 65001, `DenyAllInBound` at 65500) cannot be deleted. You can only override them by defining custom rules with a priority lower than 65000.

*Related Lab Reference:* [Day 1: Azure Linux VM & Nginx Setup](/day-01-azure-linux-vm/blog-article.md)
</details>

---

#### Question 2
You need to securely connect to an Azure Linux VM over SSH using password authentication from your management workstation. Which combination of network prerequisites must be satisfied?

- **A.** The VM must have an assigned public IP or Bastion, the NSG must allow inbound TCP port 22, and the guest sshd configuration must permit password authentication.
- **B.** The VM must have a dedicated ExpressRoute circuit and port 3389 opened on the network interface.
- **C.** The VM must belong to an Azure Active Directory Domain Services managed domain.
- **D.** Password authentication requires an attached Ultra Disk at LUN 0.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Direct remote administrative connectivity to an Azure Linux virtual machine requires three synchronized layers:
1. **Network Routing:** The VM must have a routable public IP address, or connectivity through Azure Bastion or Load Balancer Inbound NAT rules.
2. **Network Security Group:** An inbound security rule allowing TCP port 22 from your workstation IP (or `Any`).
3. **Guest OS Service:** The OpenSSH daemon (`sshd`) must be running and configured with `PasswordAuthentication yes` in `/etc/ssh/sshd_config`.

**Distractor Breakdown:**
- *Option B is incorrect:* Port 3389 is for Windows Remote Desktop Protocol (RDP), not Linux SSH. ExpressRoute is an enterprise hybrid interconnect, not a prerequisite for basic VM access.
- *Option C is incorrect:* Linux VMs do not require Azure AD DS for standard local user authentication.
- *Option D is incorrect:* Disk SKU has zero relationship with SSH authentication.

*Related Lab Reference:* [Day 1: Azure Linux VM & Nginx Setup](/day-01-azure-linux-vm/blog-article.md)
</details>

---

#### Question 3
An administrator associates `NSG-Subnet` with `Subnet-1` and `NSG-NIC` with the network interface of `VM-1`. When an inbound packet arrives from the Internet targeted at `VM-1`, in what sequence are the network security group rules evaluated?

- **A.** `NSG-Subnet` is evaluated first; if permitted, `NSG-NIC` is evaluated second. If either denies the traffic, the packet is dropped.
- **B.** `NSG-NIC` is evaluated first; if permitted, `NSG-Subnet` is evaluated second.
- **C.** Only the NSG with the lowest rule priority number across both groups is evaluated.
- **D.** Rules from both NSGs are merged into a single priority list and executed simultaneously.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Azure enforces a strict bidirectional dual-perimeter evaluation flow:
- **Inbound Traffic:** Packets arriving at a subnet are evaluated against the **Subnet NSG first**. If allowed by the subnet rules, the packet proceeds to the **NIC NSG second**. If either NSG denies the packet, it is dropped.
- **Outbound Traffic:** The flow is reversed. Packets leaving a VM are evaluated by the **NIC NSG first**, and if permitted, evaluated by the **Subnet NSG second**.

```
Inbound:   Internet ===> [Subnet NSG] ===> [NIC NSG] ===> VM Application
Outbound:  VM Application ===> [NIC NSG] ===> [Subnet NSG] ===> Internet
```

> [!TIP]
> **AZ-104 Exam Tip:** For defense-in-depth, configure broad perimeter rules (e.g., blocking known malicious subnets) on the Subnet NSG, and workload-specific rules (e.g., allowing port 80 to web servers only) on the NIC NSG.

*Related Lab Reference:* [Day 1: Azure Linux VM & Nginx Setup](/day-01-azure-linux-vm/blog-article.md)
</details>

---

### Domain 2: Azure Storage, Managed Disks, Snapshots & Migration

#### Question 4
You attach a new 128 GiB Premium SSD data disk in the Azure Portal at LUN 0 to an existing Windows Server 2025 virtual machine. You log in via RDP but notice the new volume does not appear in File Explorer. What is the required next step?

- **A.** Inside the Windows guest OS, open Disk Management, bring the disk online, initialize it with GPT partition style, and format a volume with NTFS/ReFS.
- **B.** Restart the virtual machine from the Azure Portal to force Azure Resource Manager to format the disk.
- **C.** Change the disk host caching property from None to Read/Write in the Azure Portal.
- **D.** Upgrade the virtual machine compute SKU to an E-series memory-optimized size.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
When you attach a managed disk in Azure, the platform connects a virtual SCSI block storage device to the VM. Azure does not format or modify the internal byte structures of the disk. Inside the Windows operating system:
1. The new disk appears as `Offline` and `Not Initialized`.
2. The administrator must bring the disk `Online`.
3. The disk must be initialized with a partition table: **GUID Partition Table (GPT)** is recommended for all modern disks (required for volumes > 2 TB).
4. A new Simple Volume must be created and formatted with a filesystem (**NTFS** or **ReFS**) and assigned a drive letter (e.g., `F:`).

*Related Lab Reference:* [Day 2: Azure Windows VM, Data Disks, Snapshots & Migration](/day-02-azure-windows-vm-data-disks-snapshots-migration/blog-article.md)
</details>

---

#### Question 5
You take a point-in-time Snapshot of a managed data disk attached to `VM-A`. You need to attach the data captured in this snapshot as a new data disk to `VM-B`. What is the required procedure?

- **A.** You cannot attach a snapshot directly to a VM. You must first create an Azure Managed Disk from the snapshot, then attach that new Managed Disk to `VM-B`.
- **B.** In `VM-B`, go to Disks > Attach existing disk and select the snapshot resource directly.
- **C.** Convert the snapshot to an Azure Storage Blob container, download the VHD, and upload it via AzCopy.
- **D.** Restore the snapshot using Azure Backup Recovery Services Vault only.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
In Microsoft Azure, an **Azure Disk Snapshot** is an independent, read-only, point-in-time copy of a managed disk stored as an unmanaged VHD blob.
- Snapshots are storage artifacts; they **cannot be mounted or attached directly** to a virtual machine SCSI controller.
- To use snapshot data on any virtual machine, you must execute a two-step promotion workflow:
  1. Provision a new **Azure Managed Disk** specifying the Snapshot as its `Source`.
  2. Attach the newly created Managed Disk to the target virtual machine (`VM-B`) under the Disks blade.

```
[Snapshot: snap-data-01] ===(Create Managed Disk)===> [Managed Disk: disk-restored-01] ===(Attach)===> [VM-B]
```

*Related Lab Reference:* [Day 2: Azure Windows VM, Data Disks, Snapshots & Migration](/day-02-azure-windows-vm-data-disks-snapshots-migration/blog-article.md)
</details>

---

#### Question 6
You manage a 1 TB managed data disk where only 25 GB of data changes daily. You need to implement daily snapshots while minimizing storage costs and retaining cross-region copy capability. What should you configure?

- **A.** Create Incremental Snapshots, which only store and bill for the differential blocks changed since the previous snapshot.
- **B.** Create Full Snapshots, because incremental snapshots do not support differential block storage.
- **C.** Deallocate the VM before taking a full VHD clone to an archive blob container.
- **D.** Use Disk Export with a SAS URL generated daily.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Azure supports two snapshot types:
- **Full Snapshots:** Capture a complete copy of the entire disk (1 TB). Every daily snapshot consumes and bills for the entire 1 TB, creating massive unnecessary storage costs.
- **Incremental Snapshots:** The baseline snapshot captures the used blocks; subsequent snapshots capture **only the differential blocks (delta)** modified since the last snapshot. If only 25 GB changes, only 25 GB is written and billed.
- Incremental snapshots are stored on Standard HDD storage regardless of the parent disk tier (Premium or Ultra), drastically reducing cost, and natively support copying across Azure regions for disaster recovery.

*Related Lab Reference:* [Day 2: Azure Windows VM, Data Disks, Snapshots & Migration](/day-02-azure-windows-vm-data-disks-snapshots-migration/blog-article.md)
</details>

---

### Domain 3: Azure Identity, Governance & Virtual Machine Encryption

#### Question 7
You create an Azure Key Vault with Azure RBAC authorization enabled and generate an RSA key named `db-enc-key`. You attempt to create a Disk Encryption Set (DES) referencing this key, but the operation fails with an authorization error. What must you configure?

- **A.** Assign the system-assigned managed identity of the Disk Encryption Set the `Key Vault Crypto Service Encryption User` role on the Key Vault.
- **B.** Change the Key Vault permission model to classic Access Policies and grant your personal user account Owner permissions.
- **C.** Enable public network access from all networks on the Key Vault firewall.
- **D.** Export the private key from the Key Vault and embed it in the ARM deployment template.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
A **Disk Encryption Set (DES)** acts as an identity bridge between Azure Managed Disks and Azure Key Vault:
1. When you create a DES, Azure automatically provisions a **system-assigned managed identity** for that DES resource.
2. Under the modern Azure RBAC permission model, that managed identity possesses zero data plane rights by default.
3. To allow the DES to wrap and unwrap data encryption keys, the cloud administrator must navigate to Key Vault > Access control (IAM) > Add role assignment, select `Key Vault Crypto Service Encryption User`, and assign it to the DES managed identity principal.

> [!WARNING]
> **AZ-104 Exam Trap:** The classic Azure `Owner` or `Contributor` role grants control-plane management over the Key Vault resource itself, but **does not grant data-plane access** to cryptographic keys or secrets. Always use dedicated data-plane roles like `Key Vault Administrator` or `Key Vault Crypto Service Encryption User`.

*Related Lab Reference:* [Day 3: Azure VM Encryption](/day-03-azure-vm-encryption/blog-article.md)
</details>

---

#### Question 8
An enterprise security policy mandates that all Windows Server virtual machines must be encrypted at the guest OS level using BitLocker, with encryption keys backed by Azure Key Vault. Which encryption solution and VM extension must be implemented?

- **A.** Azure Disk Encryption (ADE) using the `AzureDiskEncryption` VM extension, which leverages BitLocker on Windows or DM-Crypt on Linux and stores Key Encryption Keys (KEK) in Azure Key Vault.
- **B.** Server-Side Encryption (SSE) with Platform-Managed Keys (PMK).
- **C.** Azure Storage Service Encryption with double encryption at rest.
- **D.** BitLocker To Go configured on an attached USB flash drive.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Azure provides two primary disk encryption architectures:
1. **Server-Side Encryption (SSE):** Transparent encryption performed at the physical storage host tier. It requires no agent inside the VM and can use platform-managed (PMK) or customer-managed keys (CMK via DES).
2. **Azure Disk Encryption (ADE):** Guest operating system volume encryption. It deploys the `AzureDiskEncryption` VM extension into Windows (BitLocker) or Linux (DM-Crypt). BitLocker encrypts the volume, and the BitLocker Encryption Key (BEK) is wrapped by a Key Encryption Key (KEK) and stored securely in Azure Key Vault.

*Related Lab Reference:* [Day 3: Azure VM Encryption](/day-03-azure-vm-encryption/blog-article.md)
</details>

---

#### Question 9
You want to update an existing, attached OS managed disk on a production VM from platform-managed keys (PMK) to customer-managed keys (CMK) using a Disk Encryption Set. What prerequisite action must you perform on the virtual machine?

- **A.** You must stop (deallocate) the virtual machine before associating the Disk Encryption Set with the OS disk.
- **B.** You must delete the VM and redeploy it from an unencrypted generalized image.
- **C.** You can update the DES live while the VM is running without any downtime.
- **D.** You must convert the disk from Premium SSD to Standard HDD first.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
While data disks can occasionally be modified when detached, changing the encryption parameters or associating a Disk Encryption Set with an **active OS disk** requires releasing the hypervisor lock. The virtual machine must be placed in the **Stopped (Deallocated)** state. Once deallocated, you update the disk's encryption settings in the Azure Portal or via CLI (`az disk update --encryption-type ... --disk-encryption-set ...`), and restart the VM.

*Related Lab Reference:* [Day 3: Azure VM Encryption](/day-03-azure-vm-encryption/blog-article.md)
</details>

---

### Domain 4: Custom Script Extensions & Virtual Machine Bootstrapping

#### Question 10
You use the Custom Script for Linux extension to deploy an application on an Ubuntu VM. The setup script is stored in a private Azure Blob Storage container with no anonymous public access. How does the VM extension authenticate to download the script?

- **A.** The storage account access key or SAS URI is provided inside the extension's `protectedSettings` block, which is encrypted by Azure.
- **B.** The storage container must be converted to Public Read access during deployment.
- **C.** The VM must download the script via an anonymous GitHub mirror.
- **D.** VM extensions cannot access private Azure Blob Storage containers.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Azure VM Extensions utilize two configuration schemas:
- `settings` (Public Settings): Stored in plaintext in the ARM template and readable by anyone with read access to the VM resource.
- `protectedSettings`: Encrypted with a platform certificate by Azure Resource Manager. The payload can only be decrypted inside the guest VM by the Azure VM Agent.
- Passing the storage account access key or SAS token inside `protectedSettings` allows the extension to download scripts from private blob containers securely without compromising enterprise credential posture.

*Related Lab Reference:* [Day 4: Azure Custom Script Extensions – Windows & Linux](/day-04-azure-custom-script-extension/blog-article.md)
</details>

---

#### Question 11
You author a Custom Script Extension on a Windows Server VM that runs a complex database restoration task. The extension remains in the 'Transitioning' status and eventually terminates with a failure code after 90 minutes. What is the root cause?

- **A.** Azure VM extensions enforce a hard 90-minute maximum execution timeout; scripts exceeding this limit are terminated as failed.
- **B.** Windows Server Datacenter restricts PowerShell scripts to a 15-minute runtime ceiling.
- **C.** The Azure storage account throttled the script download after 30 minutes.
- **D.** The virtual machine ran out of IOPS on the temporary disk (D: drive).

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
The Azure Virtual Machine Guest Agent enforces a strict **90-minute execution timeout** on the Custom Script Extension. If a script:
- Performs operations exceeding 90 minutes,
- Hangs waiting for interactive standard input (`Read-Host` or interactive confirmation), or
- Becomes deadlocked by background child processes,
The agent terminates the task and reports provisioning failure. Long-running tasks must be initiated as background scheduled tasks or executed through Azure Automation or Azure Image Builder.

*Related Lab Reference:* [Day 4: Azure Custom Script Extensions – Windows & Linux](/day-04-azure-custom-script-extension/blog-article.md)
</details>

---

#### Question 12
A PowerShell script executed via Custom Script Extension requires a system reboot halfway through its configuration steps. What is the recommended practice for handling reboots in custom extension scripts?

- **A.** Design the script to be idempotent, recording completed milestones in a marker file or registry key so that upon reboot resumption it continues without repeating steps.
- **B.** Never reboot inside an extension; reboots immediately corrupt the Azure VM agent.
- **C.** Trigger an immediate hard shutdown using Stop-Computer without returning an exit code.
- **D.** Split the script into 5 separate Custom Script Extensions attached simultaneously.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
When a script triggers an operating system reboot, the guest agent is temporarily halted. Upon system startup, the extension handler restarts the script to ensure completion.
- To prevent infinite loops or partial re-installations, scripts must be **idempotent**.
- Check whether the feature or file already exists (e.g., checking `Test-Path C:\installed.lock` or checking `(Get-WindowsFeature Web-Server).Installed`). If completed, exit cleanly with return code `0`.

*Related Lab Reference:* [Day 4: Azure Custom Script Extensions – Windows & Linux](/day-04-azure-custom-script-extension/blog-article.md)
</details>

---

### Domain 5: Virtual Machine High Availability – Availability Sets & Availability Zones

#### Question 13
You deploy four virtual machines in an Availability Set configured with 2 Fault Domains (FD) and 2 Update Domains (UD). VM-1 is in (FD0, UD0), VM-2 is in (FD1, UD1), VM-3 is in (FD0, UD0), and VM-4 is in (FD1, UD1). If a hardware power supply unit (PSU) fails on the rack hosting Fault Domain 0, which virtual machines remain operational?

- **A.** VM-2 and VM-4 remain running, because they are isolated on physical rack hardware in Fault Domain 1.
- **B.** Only VM-1 remains running.
- **C.** All four VMs go offline because they share the same availability set.
- **D.** All four VMs remain running due to automatic hypervisor memory cloning.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
- **Fault Domains (FDs):** Define physical hardware isolation (server rack, power distribution unit [PDU], top-of-rack network switch).
- **Update Domains (UDs):** Define planned maintenance sequencing groups.
- VMs residing on `Fault Domain 0` (VM-1 and VM-3) share the physical power and switching of Rack 0. When Rack 0 suffers a physical power outage, both VM-1 and VM-3 lose power.
- VMs residing on `Fault Domain 1` (VM-2 and VM-4) reside on a physically separate server rack with distinct power feeds and network switches, remaining 100% operational.

*Related Lab Reference:* [Day 5: Azure Availability Zones & Availability Sets](/day-05-azure-availability-zones-and-sets/blog-article.md)
</details>

---

#### Question 14
An enterprise workload requires a Microsoft Azure SLA of at least 99.99% for its virtual machine compute tier in a single region. Which architectural requirement is mandatory?

- **A.** Deploy two or more virtual machines across two or more Availability Zones in the region, fronted by a Zone-Redundant Standard Load Balancer.
- **B.** Deploy two virtual machines in an Availability Set with 3 Fault Domains and Premium SSDs.
- **C.** Deploy a single virtual machine with an Ultra Disk and 128 vCPUs.
- **D.** Configure cross-region asynchronous storage replication using GRS.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Azure Compute SLA Hierarchy:
- **Single VM (Premium SSD / Ultra Disk):** 99.9% SLA (~8.76 hours downtime/year).
- **Availability Set (2+ VMs across FDs/UDs):** 99.95% SLA (~4.38 hours downtime/year).
- **Availability Zones (2+ VMs across 2+ Zones):** **99.99% SLA (~52.6 minutes downtime/year)**.
- Availability Zones isolate workloads across physically separate datacenter buildings with independent power, cooling, and fiber networks. Fronting them with a Zone-Redundant Standard Load Balancer is required to route around unavailable zones.

*Related Lab Reference:* [Day 5: Azure Availability Zones & Availability Sets](/day-05-azure-availability-zones-and-sets/blog-article.md)
</details>

---

#### Question 15
You have a standalone production virtual machine named `vm-core` that was deployed without an Availability Set. Leadership asks you to add `vm-core` into an existing Availability Set named `as-prod`. Can you perform this action directly in the Azure Portal?

- **A.** No. A virtual machine can only be placed in an Availability Set during initial creation; you must delete the VM (retaining its OS disk) and recreate it inside the Availability Set.
- **B.** Yes. Open the VM Availability blade, select Change Availability Set, and restart the VM.
- **C.** Yes, provided the VM is stopped (deallocated) before moving.
- **D.** No, standalone VMs can never be placed into an Availability Set under any circumstances.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Assigning a virtual machine to an Availability Set is an **immutable creation-time parameter**. The Azure fabric controller places the VM on specific physical hardware clusters during allocation.
- Once created as a standalone VM, it cannot be moved into an Availability Set via the Portal or CLI.
- The standard migration procedure:
  1. Stop (deallocate) `vm-core`.
  2. Delete the VM resource while **preserving the OS and data managed disks**.
  3. Deploy a new VM from the existing OS managed disk, specifying `-AvailabilitySetName "as-prod"`.

*Related Lab Reference:* [Day 5: Azure Availability Zones & Availability Sets](/day-05-azure-availability-zones-and-sets/blog-article.md)
</details>

---

#### Question 16
Why does Microsoft mandate using Azure Managed Disks (rather than legacy unmanaged storage account VHDs) when deploying VMs in an Availability Set?

- **A.** Managed Disks automatically align the storage cluster fault domains with the compute fault domains of the VMs, preventing single storage rack failures from affecting multiple VMs.
- **B.** Unmanaged disks do not support NTFS or ext4 file systems.
- **C.** Managed Disks provide unlimited free storage for up to 3 years.
- **D.** Availability Sets cannot be created without attaching at least 4 data disks.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
With legacy unmanaged disks, multiple VMs in different compute fault domains might store their page blobs in the same storage account or storage cluster. A storage cluster outage could crash all VMs simultaneously, destroying the fault tolerance benefit.
- Managed Disks resolve this through **storage fault domain alignment**: Azure ensures that the storage hardware hosting the managed disk of VM-1 (FD0) is physically isolated from the storage hardware hosting the disk of VM-2 (FD1).

*Related Lab Reference:* [Day 5: Azure Availability Zones & Availability Sets](/day-05-azure-availability-zones-and-sets/blog-article.md)
</details>

---

### Domain 6: VM Scale Sets – Uniform Mode & Autoscaling

#### Question 17
You configure an autoscale rule on a Uniform VMSS with baseline count 1: "If Average Percentage CPU > 70% over 5 minutes, increase count by 1 (Cooldown: 5 minutes)". If CPU load jumps to 95% at 10:00 AM and remains at 95% until 10:12 AM, what is the instance count at 10:12 AM?

- **A.** 3 instances (scales to 2 at 10:05 AM, cooldown suppresses actions until 10:10 AM, then scales to 3 at 10:11-10:12 AM).
- **B.** 1 instance (cooldown prevents any scaling for the first 15 minutes).
- **C.** 7 instances (scales out by 1 instance every single minute load is sustained).
- **D.** 2 instances (autoscale rules can only fire once per calendar day).

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Step-by-step temporal execution breakdown:
1. **10:00 AM to 10:05 AM (Lookback Window):** CPU utilization averages 95% over the 5-minute duration. The > 70% condition is breached. Azure triggers a **scale-out (+1 instance)**, increasing capacity to **2 instances**.
2. **10:05 AM to 10:10 AM (Cooldown Period):** The 5-minute cooldown timer is active. Azure Monitor ignores any metric breaches during this window to allow VM-2 to boot and take traffic.
3. **10:10 AM:** Cooldown expires. The autoscale daemon resumes evaluation.
4. **10:11 AM to 10:12 AM:** The 5-minute lookback average CPU is still well above 70%. Azure triggers a second scale-out (+1 instance), bringing total capacity to **3 instances**.

*Related Lab Reference:* [Day 6: Azure VM Scale Sets and Autoscaling](/day-06-azure-vm-scale-sets-and-autoscaling/blog-article.md)
</details>

---

#### Question 18
When configuring a custom metric autoscale setting on a scale set, saving fails with `MissingSubscriptionRegistration: The subscription is not registered to use namespace microsoft.insights`. Which command resolves this?

- **A.** `az provider register --namespace Microsoft.Insights`
- **B.** `az vmss update --name SET0000 --enable-insights`
- **C.** `az monitor alert create --insights-enable true`
- **D.** `az feature register --namespace Microsoft.Compute --name Autoscale`

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Azure Monitor and autoscale settings are governed by the `Microsoft.Insights` resource provider.
- If a subscription has never used Azure Monitor autoscale or diagnostic settings before, the resource provider may be in the `NotRegistered` state.
- Attempting to invoke ARM APIs for `Microsoft.Insights/autoscalesettings` throws HTTP 409 `MissingSubscriptionRegistration`.
- Running `az provider register --namespace Microsoft.Insights` registers the provider, allowing autoscale settings to be saved cleanly.

*Related Lab Reference:* [Day 6: Azure VM Scale Sets and Autoscaling](/day-06-azure-vm-scale-sets-and-autoscaling/blog-article.md)
</details>

---

#### Question 19
An administrator creates a scale-out rule: "When CPU > 80%, add 1 VM". No scale-in rule is created. During the night, CPU drops to 4%. What happens to the scale set instances and cloud billing?

- **A.** The scale set remains at its maximum scaled-out instance count indefinitely, continuing to incur compute charges until a scale-in rule is created or manual reduction occurs.
- **B.** Azure automatically terminates all instances once CPU drops below 10%.
- **C.** The scale set deallocates instances automatically at midnight UTC.
- **D.** An error notification is sent and the scale set resets to 0 instances.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Autoscale rules are strictly **declarative and asymmetric**:
- Azure never assumes scale-in intentions. If an engineer configures scale-out on CPU > 80% without a complementary scale-in rule (e.g., CPU < 25%), the instances will scale out during demand spikes and remain running at maximum capacity forever.
- Always pair scale-out rules with scale-in rules with an adequate hysteresis buffer (margin) between thresholds.

*Related Lab Reference:* [Day 6: Azure VM Scale Sets and Autoscaling](/day-06-azure-vm-scale-sets-and-autoscaling/blog-article.md)
</details>

---

#### Question 20
What critical failure condition does the autoscale 'Cooldown' period prevent in production environments?

- **A.** Flapping (thrashing) and premature over-provisioning caused by evaluating metrics before newly provisioned VMs have fully initialized and absorbed traffic.
- **B.** Operating system kernel crashes caused by high processor clock speeds.
- **C.** Throttling of the Azure Key Vault cryptographic REST APIs.
- **D.** Memory leaks inside the guest systemd init process.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Provisioning a new VM instance takes 2 to 5 minutes (allocating hardware, booting OS, initializing services, passing health probes).
- If there were no cooldown, Azure Monitor would sample CPU utilization 60 seconds after the scale-out action. Because the new VM is not yet serving traffic, average CPU would still be high, triggering another unnecessary scale-out.
- The **cooldown timer** enforces a stabilization buffer, preventing runaway fleet expansion and eliminating destructive **flapping (ping-pong scaling)**.

*Related Lab Reference:* [Day 6: Azure VM Scale Sets and Autoscaling](/day-06-azure-vm-scale-sets-and-autoscaling/blog-article.md)
</details>

---

### Domain 7: Flexible VM Scale Sets & Advanced Fleet Management

#### Question 21
You need to configure a scale set that combines `Standard_B2ts_v2`, `Standard_B2ats_v2`, and `Standard_B2als_v2` virtual machines in the same tier, automatically deploying the cheapest available size upon scale-out. What orchestration mode and setting must you choose?

- **A.** Flexible Orchestration Mode with a Multi-SKU profile and the 'Lowest price' allocation strategy.
- **B.** Uniform Orchestration Mode with an Availability Set attachment.
- **C.** Classic Cloud Services with dynamic VIP swapping.
- **D.** Azure Batch compute pool with dedicated node reservation.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
- **Uniform Mode:** Demands 100% identical VM sizes and identical operating system images.
- **Flexible Mode:** Introduces multi-SKU profiles, enabling you to select up to **5 different VM sizes** in a single scale set.
- By selecting the **Lowest price** allocation strategy, Azure evaluates current pricing across your chosen SKUs and launches the most cost-effective size that has capacity in that availability zone.

*Related Lab Reference:* [Day 7: Azure Flexible VM Scale Sets](/day-07-azure-flexible-vm-scale-sets/blog-article.md)
</details>

---

#### Question 22
You want to deploy a new standalone Linux VM named `vm-worker02` and immediately associate it as an active member of an existing Flexible scale set named `set0001`. Which Azure CLI command parameter is used?

- **A.** `az vm create --resource-group rg --name vm-worker02 --vmss set0001 ...`
- **B.** `az vmss add-instance --scale-set set0001 --vm vm-worker02`
- **C.** `az vm join-pool --name vm-worker02 --target set0001`
- **D.** `az compute attach --vm vm-worker02 --scale-set set0001`

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
In Azure CLI, the standard command `az vm create` accepts the parameter `--vmss <ScaleSetNameOrId>`.
- When targeting a scale set configured in Flexible mode, Azure provisions `vm-worker02` as a standalone top-level `Microsoft.Compute/virtualMachines` resource while registering its membership inside `set0001`.
- You can optionally specify `--platform-fault-domain 1` to control rack distribution.

*Related Lab Reference:* [Day 7: Azure Flexible VM Scale Sets](/day-07-azure-flexible-vm-scale-sets/blog-article.md)
</details>

---

#### Question 23
An enterprise wants to migrate from legacy Availability Sets to a modern compute architecture that supports mixed VM sizes, scales up to 1,000 instances, and guarantees physical server rack (Fault Domain) isolation within an Availability Zone. What should you recommend?

- **A.** Virtual Machine Scale Sets in Flexible Orchestration Mode with Platform Fault Domain spread configured.
- **B.** Virtual Machine Scale Sets in Uniform Orchestration Mode with spot priority.
- **C.** Proximity Placement Groups with single standalone VMs.
- **D.** Dedicated Host Groups spanning multiple geographical regions.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Microsoft officially designates **Flexible VM Scale Sets as the modern successor to Availability Sets**.
- Availability Sets are limited to 200 VMs, do not support mixing Spot and On-Demand instances, and cannot autoscale.
- Flexible VMSS provides platform fault domain spread (FD 0 to 4), supports up to 1,000 instances, allows mixed VM sizes, and qualifies for the 99.95% single-zone high-availability SLA.

*Related Lab Reference:* [Day 7: Azure Flexible VM Scale Sets](/day-07-azure-flexible-vm-scale-sets/blog-article.md)
</details>

---

#### Question 24
How do virtual machine instances appear in Azure Resource Manager (ARM) when deployed in Flexible mode compared to Uniform mode?

- **A.** In Flexible mode, each instance is a first-class, standalone `Microsoft.Compute/virtualMachines` resource visible directly in the resource group; in Uniform mode, instances are child resources under the scale set URI.
- **B.** In Uniform mode, instances have independent public IPs, while Flexible mode instances cannot have IP addresses.
- **C.** Flexible mode instances do not have OS disks in the resource group.
- **D.** Uniform mode instances are managed via the Azure Kubernetes Service control plane.

<details>
<summary><strong>View Answer & Detailed Architectural Analysis</strong></summary>

**Correct Answer:** **A**

**Architectural Analysis:**
Resource URI Comparison:
- **Uniform Instance URI:** `/subscriptions/.../resourceGroups/rg/providers/Microsoft.Compute/virtualMachineScaleSets/SET0000/virtualMachines/0`
  *(Child resource under the VMSS parent; does not appear as a standalone VM in the All Resources view)*
- **Flexible Instance URI:** `/subscriptions/.../resourceGroups/rg/providers/Microsoft.Compute/virtualMachines/set0001_3c0c7e6d`
  *(Top-level standalone resource; appears directly in the resource group alongside its dedicated OS disk and NIC)*

*Related Lab Reference:* [Day 7: Azure Flexible VM Scale Sets](/day-07-azure-flexible-vm-scale-sets/blog-article.md)
</details>

---

## High-Yield 1-Year Revision Cheat Sheet

| Topic / Concept | Critical Key Fact for AZ-104 | Common Exam Trap / Distractor |
| :--- | :--- | :--- |
| **NSG Priority Ordering** | Evaluated lowest number (100) to highest (4096). Match terminates evaluation. | Higher priority number does NOT mean higher importance. 100 beats 200. |
| **Inbound vs Outbound NSGs** | Inbound: Subnet NSG first, then NIC NSG. Outbound: NIC NSG first, then Subnet NSG. | If Subnet NSG drops traffic, NIC NSG is never evaluated. |
| **New Data Disks** | Raw block storage attached to SCSI. Must be brought online and formatted in OS. | Reboots do not format disks. In-guest disk management is required. |
| **Snapshots to VMs** | Snapshots cannot be mounted directly. Must create a Managed Disk from snapshot first. | Attaching a snapshot directly to a VM SCSI controller is invalid. |
| **Incremental Snapshots** | Billed only for modified delta blocks. Stored on Standard HDD. Cross-region copyable. | Full snapshots bill for entire disk capacity every time. |
| **Key Vault RBAC** | Azure Owner/Contributor has control-plane rights only; data plane requires `Key Vault Administrator`. | Subscription Owner cannot read keys without explicit data-plane role. |
| **SSE vs ADE** | SSE = Storage host level (no agent, hypervisor). ADE = In-guest BitLocker/DM-Crypt extension. | ADE requires Azure Key Vault; SSE with PMK requires no Key Vault. |
| **Custom Script Extensions** | Hard 90-minute maximum timeout. Runs as LocalSystem/root. Pass keys in `protectedSettings`. | Scripts with interactive prompts (`Read-Host`) will hang and timeout. |
| **Fault vs Update Domains** | FD = Physical hardware/rack/power isolation. UD = Scheduled rolling reboot groups. | Host maintenance updates one UD at a time, never simultaneously. |
| **HA SLAs** | Single VM = 99.9%. Availability Set = 99.95%. Availability Zones = 99.99%. | Availability Zones require 2+ VMs across 2+ zones fronted by Standard LB. |
| **AS Modification** | VMs can only join an Availability Set during creation. Cannot move existing VM. | You must delete the VM (keep disks) and recreate from managed disk. |
| **Autoscale Registration** | Scale sets fail to save autoscale settings without `Microsoft.Insights` registered. | Run `az provider register --namespace Microsoft.Insights`. |
| **Autoscale Cooldown** | Enforces quiet period post-scale action to prevent flapping and over-provisioning. | Without cooldown, metric sampling causes runaway instance creation. |
| **Uniform vs Flexible VMSS** | Uniform = child instances, identical SKU. Flexible = standalone VMs, up to 5 mixed SKUs. | Orchestration mode is immutable after scale set creation. |
| **Adding VMs to Flexible VMSS** | Use `az vm create --vmss <Name>` or select Scale Set under Availability options in Portal. | Standalone VMs must be in the same VNet and Availability Zone. |

---

*Authored by ShubhamTheDataGuy `<shubhamnagpal789@gmail.com>`*
