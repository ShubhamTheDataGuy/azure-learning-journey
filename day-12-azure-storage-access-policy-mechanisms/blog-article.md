# Day 12: Azure Storage Access Policy Mechanisms: Stored Access Policies, SAS Revocation, and Immutability Governance

*An in-depth architectural and hands-on guide to mastering Azure Storage access policies: binding Shared Access Signatures to container-level Stored Access Policies (SAP), achieving instant non-destructive token revocation, dissecting cryptographic parameters (the `si` parameter), diagnosing `AuthorizationPermissionMismatch` 403 errors, and evaluating WORM immutable storage.*

---

## Executive Summary and Learning Objectives

In **Day 11**, we examined **Shared Access Signatures (SAS)** as a least-privilege alternative to 512-bit account keys. However, we discovered an inherent operational vulnerability of ad-hoc SAS tokens: because the permissions, start timestamp, and expiration timestamp are cryptographically hashed directly into the signature string (`sig`), **an ad-hoc SAS cannot be modified or revoked in flight**. If an ad-hoc SAS is compromised or needs to be terminated prematurely, the only remediation is rotating the parent Storage Account Key, an aggressive action that abruptly invalidates every other SAS token and service integration reliant on that key.

To solve this lifecycle management challenge, Azure Storage provides **Stored Access Policies (SAP)**. A Stored Access Policy decouples the SAS token parameters from the URL query string by storing the authorization rules server-side directly on the container. By referencing a Stored Access Policy via the Signed Identifier (`si`) parameter, administrators gain the ability to **alter permissions, modify expiration windows, or revoke active SAS tokens instantly without touching storage account keys**.

Furthermore, storage governance encompasses data integrity and compliance through **Immutable Blob Storage** (Write Once, Read Many / WORM), preventing modification or deletion of business-critical data regardless of user privilege level.

In this practical lab, we configure a container-level Stored Access Policy, issue a policy-backed Service SAS, mount the storage container in Microsoft Azure Storage Explorer, and intentionally trigger cryptographic authorization enforcement to observe Azure's runtime permission validation.

### Key Skills Acquired
- Designing and provisioning **Stored Access Policies (SAP)** on Azure Blob containers with granular CRUDL permissions.
- Generating policy-backed **Service SAS** tokens utilizing the Signed Identifier (`si`) query parameter.
- Understanding how Stored Access Policies abstract permissions (`sp`) away from client-visible URIs into server-side storage metadata.
- Mounting policy-scoped blob containers into **Microsoft Azure Storage Explorer** using SAS connection strings.
- Diagnosing and analyzing the runtime error: `RESPONSE 403: AuthorizationPermissionMismatch - This request is not authorized to perform this operation using this permission.`
- Implementing immediate, non-destructive SAS revocation patterns without triggering account key rotation outages.
- Contrasting Stored Access Policies with **Immutable Blob Storage** (Time-based retention and Legal holds) for compliance-driven data retention.

---

## Architectural Comparison: Ad-Hoc SAS vs. Policy-Backed SAS

The core architectural differentiator between an ad-hoc SAS and a policy-backed SAS lies in where the authorization state is stored and verified.

```mermaid
flowchart TD
    subgraph AdHoc["Ad-Hoc SAS (Day 11 Pattern)"]
        A1["Client URI: ?sp=r&st=...&se=...&sig=..."] --> A2["Azure Storage Engine"]
        A2 --> A3["Stateless HMAC Verification"]
        A3 --> A4{"Revocation Possible?"}
        A4 -- No --> A5["Must Rotate Entire Account Key"]
        A5 --> A6["Cascading Outage Across All Services"]
    end

    subgraph PolicyBacked["Policy-Backed SAS (Day 12 Pattern)"]
        B1["Client URI: ?si=READONLY&sig=..."] --> B2["Azure Storage Engine"]
        B2 --> B3["HMAC Verification of 'si' Reference"]
        B3 --> B4["Lookup Server-Side Policy on Container 'data'"]
        B4 --> B5{"Policy Active & Operation Permitted?"}
        B5 -- Yes --> B6["Allow Request (Read / List)"]
        B5 -- No --> B7["Deny: 403 AuthorizationPermissionMismatch"]
        B4 -. Revocation .-> B8["Admin Updates / Deletes Policy Server-Side"]
        B8 --> B9["Instant Token Revocation (Zero Key Rotation)"]
    end
```

### Authorization State Comparison Matrix

| Architectural Dimension | Ad-Hoc Shared Access Signature | Policy-Backed Shared Access Signature |
| :--- | :--- | :--- |
| **State Location** | Stateless (entirely encoded within URL query string) | Stateful (authorization rules persisted in container metadata) |
| **Permission Specification** | Parameter `sp` embedded in URL (`sp=r`, `sp=rl`, `sp=rdl`) | Defined in container policy; `sp` omitted from client query string |
| **URL Parameter Binding** | Signed parameters: `sp`, `st`, `se`, `spr`, `sv`, `sr`, `sig` | Signed parameters: `si`, `spr`, `sv`, `sr`, `sig` (`st` and `se` optional) |
| **Permission Mutability** | Completely immutable; modifying query string invalidates `sig` | Fully mutable; administrator can update policy permissions dynamically |
| **Revocation Mechanism** | Account key rotation (destructive to all other SAS tokens) | Modify expiration time or delete policy server-side (instantaneous) |
| **Supported Scope** | Blob, Container, Account, Queue, Table, File Share | Blob Container, File Share, Queue, Table (Not supported for Account SAS) |
| **Capacity Limit** | Unlimited concurrent ad-hoc signatures | Maximum of 5 Stored Access Policies per container/resource |

---

## Technical Specifications and Lab Assets

The configurations implemented during this practical demonstration are detailed below:

| Resource Element | Value / Setting | Technical Significance |
| :--- | :--- | :--- |
| **Storage Account** | `azurestudystorage01` | Azure Storage General Purpose v2 (GPv2) instance |
| **Resource Group** | `azure-study` | Logical resource management grouping |
| **Target Container** | `data` | Blob container storing enterprise document assets |
| **Stored Access Policy ID** | `READONLY` | Unique alphanumeric identifier (`si`) up to 64 characters |
| **Policy Permissions** | Read, List (`rl`) | Grants object downloading and container enumeration only |
| **Signing Key** | Storage Account `Key 1` | 512-bit symmetric secret used to compute HMAC-SHA256 signature |
| **Signed Identifier (`si`)** | `READONLY` | Cryptographic parameter mapping incoming requests to server policy |
| **Protocol Enforcement** | HTTPS only (`spr=https`) | Rejects plain-text unencrypted HTTP requests |
| **Client Application** | Microsoft Azure Storage Explorer | Cross-platform desktop management client |
| **Target Document Object** | `documents/2308.15363v4.pdf` | Sample research document stored in container |
| **Tested Action** | HTTP `DELETE` | Intercepted and blocked by authorization engine |

---

## Step-by-Step Hands-On Implementation

### Phase 1: Navigating to the Target Container and Access Policy Blade

To establish server-side governance, access policies must be authored at the container level. Within the Azure Portal, open the storage account `azurestudystorage01` and access the Containers management blade under **Data storage**.

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/01_navigating_to_blob_container.png" alt="Navigating to Blob Container" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 1: Navigating to the storage account containers blade and selecting the target data container.</p>
</div>

1. In the `azurestudystorage01 | Containers` view, select the container named `data`.
2. Notice the existing configuration: the anonymous access level is set to `Blob`, which was configured during Day 9.
3. Within the container sidebar under **Settings**, select **Access policy**.

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/02_container_access_policy_blade.png" alt="Container Access Policy Blade" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 2: The container Access policy blade presenting Stored access policies and Immutable blob storage.</p>
</div>

The Access policy blade contains two distinct governance sections:
- **Stored access policies**: Used to control, group, and revoke Shared Access Signatures without altering storage account keys.
- **Immutable blob storage**: Used to enforce Write Once, Read Many (WORM) data preservation policies for compliance and legal retention.

---

### Phase 2: Defining and Saving a Stored Access Policy

Click **+ Add policy** under the **Stored access policies** section. A modal configuration flyout appears.

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/03_add_stored_access_policy_dialog.png" alt="Add Stored Access Policy Dialog" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 3: Configuring the policy identifier READONLY within the Add policy flyout.</p>
</div>

1. **Identifier**: Enter `READONLY`. The identifier can be up to 64 characters long and must be unique within the container.
2. **Permissions**: Click the Permissions dropdown. Azure Storage containers support granular flags: `Read`, `Add`, `Create`, `Write`, `Delete`, and `List`.

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/04_configuring_policy_permissions_read_list.png" alt="Configuring Policy Permissions Read and List" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 4: Selecting granular permissions Read and List from the policy configuration dropdown.</p>
</div>

3. Select `Read` and `List` (`rl`).
   - `Read` permits reading blob content, block lists, and blob properties.
   - `List` permits enumerating blobs and directories within the container namespace (required for Storage Explorer tree navigation).
4. **Start time** and **Expiry time**: In this configuration, we leave the temporal fields blank at the policy level to demonstrate binding expiration at SAS generation time, or they can be enforced directly by the policy.
5. Click **OK**.

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/05_stored_access_policy_added_save_required.png" alt="Stored Access Policy Added Save Required" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 5: Policy staged in the portal table showing rl permissions and notification prompt to save changes.</p>
</div>

> [!IMPORTANT]
> Adding a policy in the portal table stages the change in browser memory only. The policy is not written to the Azure Storage container until you click the top **Save** button. Failing to click Save leaves the container without server-side policy metadata.

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/06_saved_container_stored_access_policy.png" alt="Saved Container Stored Access Policy" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 6: Committing the Stored Access Policy to Azure Storage by clicking Save.</p>
</div>

Click **Save**. Azure executes a `Set Container ACL` REST operation against `https://azurestudystorage01.blob.core.windows.net/data?restype=container&comp=acl` to commit the XML access policy structure into container metadata.

---

### Phase 3: Generating a Policy-Backed Shared Access Signature

Now that the policy is persisted on the container, we generate a SAS token that delegates its authorization to this policy.

1. In the container sidebar, navigate to **Shared access tokens**.
2. Notice the default state: **Stored access policy** is set to `None`, and the **Permissions** dropdown allows manual selection.

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/07_shared_access_tokens_blade_default.png" alt="Shared Access Tokens Blade Default" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 7: The Shared access tokens blade before linking to a stored access policy.</p>
</div>

3. Expand the **Stored access policy** dropdown and select `READONLY`.

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/08_associating_sas_with_stored_policy.png" alt="Associating SAS with Stored Policy" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 8: Selecting the READONLY stored access policy from the configuration dropdown.</p>
</div>

Notice what occurs the moment `READONLY` is selected:
- The **Permissions** field automatically disables and displays `2 selected` (grayed out). The portal prevents setting ad-hoc permissions because permissions are inherited dynamically from the server-side policy.
- Configure Start and Expiry timestamps (Start: `10/19/2026 7:52:08 PM`, Expiry: `10/20/2026 4:07:08 AM`).
- Ensure **Allowed protocols** is set to `HTTPS only`.
- Click **Generate SAS token and URL**.

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/09_policy_backed_sas_token_and_url_generated.png" alt="Policy Backed SAS Token and URL Generated" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 9: Generated SAS token and URL displaying the si=READONLY parameter and absence of client permissions.</p>
</div>

#### Detailed Cryptographic URL Analysis

Examine the generated Blob SAS URL:

```text
https://azurestudystorage01.blob.core.windows.net/data?st=2026-10-19T14:22:08Z&se=2026-10-19T22:37:08Z&si=READONLY&spr=https&sv=2026-02-06&sr=c&sig=eQZ7q4GkaYp6rFKzwwj962tgI93fG%2F75pvwRzUi6frY%3D
```

Let us dissect the parameters:
- `st=2026-10-19T14:22:08Z`: Signed start timestamp in UTC.
- `se=2026-10-19T22:37:08Z`: Signed expiration timestamp in UTC.
- `si=READONLY`: **Signed Identifier**. References the Stored Access Policy named `READONLY` stored on container `data`.
- `spr=https`: Enforces TLS encryption for transport.
- `sv=2026-02-06`: Azure Storage REST API protocol version.
- `sr=c`: Signed resource type, confirming container-level scope.
- `sig=eQZ7q4GkaYp6rFKzwwj9...`: HMAC-SHA256 signature calculated over the canonical string containing `si`.

> [!NOTE]
> Contrast this with Day 11's ad-hoc SAS: the query string **completely omits the `sp` (signed permissions) parameter**. The client has no explicit permission flags embedded in its URI. When a request arrives, Azure Storage queries the container ACL table for policy `READONLY` and loads permissions `rl` into memory.

Copy the generated **Blob SAS URL**.

---

### Phase 4: Attaching the Policy-Backed SAS in Azure Storage Explorer

1. Launch **Microsoft Azure Storage Explorer**.
2. Click the plug icon (**Attach to a resource**) on the vertical toolbar.
3. Select **Blob container or directory**.

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/10_storage_explorer_select_sas_connection.png" alt="Storage Explorer Select SAS Connection" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 10: Selecting Shared access signature URL (SAS) as the connection method in Storage Explorer.</p>
</div>

4. In the **Select Connection Method** wizard, choose **Shared access signature URL (SAS)** and click **Next**.
5. In the **Enter Connection Info** step:
   - **Display name**: Enter `data-1`.
   - **Blob container or directory SAS URL**: Paste the copied policy-backed SAS URL.

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/11_storage_explorer_enter_policy_sas_url.png" alt="Storage Explorer Enter Policy SAS URL" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 11: Supplying connection parameters with the policy-backed SAS URL referencing si=READONLY.</p>
</div>

6. Click **Next**, review the connection summary, and click **Connect**.
7. The container appears in the left hierarchy under `Emulator & Attached > Storage Accounts > (Attached Containers) > Blob Containers > data-1 (SAS)`.
8. Expand `data-1 (SAS)` and enter the virtual folder `documents`. The blob `2308.15363v4.pdf` appears in the object list.

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/12_storage_explorer_browsing_container_documents.png" alt="Storage Explorer Browsing Container Documents" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 12: Successfully enumerating container blobs using the Read and List permissions granted by the policy.</p>
</div>

Because the Stored Access Policy includes the `List` (`l`) permission, Storage Explorer enumerates the container contents without raising the missing list permission error encountered in Day 11.

---

### Phase 5: Testing Authorization Enforcement (Triggering the 403 Gotcha)

Now, we test write/delete boundaries. The Stored Access Policy grants `rl` (Read and List). What happens when a client holding this token attempts to delete a blob?

1. Select the blob `2308.15363v4.pdf`.
2. Click **Delete** in the top action toolbar.
3. Storage Explorer displays a confirmation dialog: *"Are you sure you want to delete '2308.15363v4.pdf'? If soft delete is disabled, deleted blobs will be permanently deleted."*

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/13_initiating_blob_deletion_dialog.png" alt="Initiating Blob Deletion Dialog" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 13: Storage Explorer prompting confirmation before sending an unprivileged HTTP DELETE request.</p>
</div>

4. Click **Yes**.
5. Storage Explorer initiates an HTTP `DELETE` request via AzCopy to:
   `https://azurestudystorage01.blob.core.windows.net/data/documents%2F2308.15363v4.pdf?...`
6. The operation fails immediately. The Activities pane registers a red failure badge with comprehensive REST diagnostics.

<div style="text-align: center; margin: 1.5rem 0;">
<img src="./screenshots/curated/14_delete_rejected_authorization_permission_mismatch.png" alt="Delete Rejected Authorization Permission Mismatch" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
<p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">Figure 14: Azure Storage REST engine rejecting the operation with HTTP 403 AuthorizationPermissionMismatch.</p>
</div>

#### Anatomy of the Failure Response

Review the exact error log output captured in the Activities panel:

```text
Deletion of '2308.15363v4.pdf' from 'data/documents/' failed: 
0 completed, error: Authentication Failed. 
The SAS is not correct or expired or does not have the correct permission DELETE
https://azurestudystorage01.blob.core.windows.net/data/documents%2F2308.15363v4.pdf

RESPONSE 403: 403 This request is not authorized to perform this operation using this permission.
ERROR CODE: AuthorizationPermissionMismatch
--------------------------------------------------------------------------------
<?xml version="1.0" encoding="utf-8"?>
<Error>
  <Code>AuthorizationPermissionMismatch</Code>
  <Message>This request is not authorized to perform this operation using this permission.
RequestId:3e89a54e-d01e-0012-4217-74892c000000
Time:2026-10-19T14:44:59.2081534Z</Message>
</Error>
```

#### Diagnostic Evaluation
1. **HTTP Status 403**: The signature and authentication succeeded (the HMAC signature matches), but the request was forbidden due to authorization constraints.
2. **Error Code `AuthorizationPermissionMismatch`**: Azure Storage compared the required operation privilege (`Delete` / `d`) against the server-side permissions bound to `si=READONLY` (`Read, List` / `rl`). Because `d` was absent from the policy ACL, the request was rejected at the fabric edge.

---

## The Power of Stored Access Policies: Instant Revocation and Permission Elevation

To appreciate why Stored Access Policies are vital in enterprise architecture, consider how this scenario would be resolved in production:

### Scenario A: Elevation of Privilege Without Reissuing Tokens
If the client legitimately requires deletion capabilities:
1. In the Azure Portal, open container `data > Access policy`.
2. Edit policy `READONLY` and add `Delete` (`rld`).
3. Click **Save**.
4. **Result**: The client in Storage Explorer retries the delete operation **using the exact same SAS URL**, and it succeeds immediately! No new SAS tokens need to be generated or distributed.

### Scenario B: Instant Revocation in Response to Security Incident
If a SAS token using `si=READONLY` is leaked or compromised:
1. Open container `data > Access policy`.
2. Click the ellipsis (`...`) next to `READONLY` and select **Delete**, or modify the policy identifier to `READONLY_V2`.
3. Click **Save**.
4. **Result**: Within seconds, any client attempting to make a call with `si=READONLY` receives an HTTP 403 `AuthenticationFailed` (Policy not found).
5. **Impact**: Zero downtime for other applications; no account keys were rotated.

```mermaid
sequenceDiagram
    autonumber
    participant Client as Client Application
    participant Storage as Azure Storage Engine
    participant Admin as Security Administrator

    Note over Client,Storage: Client holds SAS with si=READONLY
    Client->>Storage: GET /data/documents/file.pdf?si=READONLY
    Storage->>Storage: Lookup Policy 'READONLY' -> Permits 'r'
    Storage-->>Client: 200 OK (File Stream)

    Note over Admin,Storage: Administrator revokes policy server-side
    Admin->>Storage: DELETE Container Policy 'READONLY'
    Storage-->>Admin: 204 No Content (Policy Removed)

    Note over Client,Storage: Client attempts access after revocation
    Client->>Storage: GET /data/documents/file.pdf?si=READONLY
    Storage->>Storage: Lookup Policy 'READONLY' -> NOT FOUND
    Storage-->>Client: 403 Forbidden (AuthenticationFailed)
```

---

## Immutable Blob Storage: WORM Compliance Architecture

During Phase 1, we observed the **Immutable blob storage** section directly beneath Stored access policies on the container blade.

Immutable blob storage enforces **Write Once, Read Many (WORM)** state on data. Once written, blobs cannot be modified or deleted by anyone, including the Global Administrator, Subscription Owner, or Azure Support, for the specified duration.

```mermaid
flowchart LR
    subgraph Immutability["Immutable Blob Storage Types"]
        direction TB
        TB["Time-Based Retention Policy"]
        LH["Legal Hold Policy"]
    end

    subgraph TBModes["Retention Policy Modes"]
        U["Unlocked (Audit & Testing)"]
        L["Locked (SEC 17a-4 / FINRA Compliance)"]
    end

    TB --> TBModes
    U -->|"Can extend or delete"| App1["Staged Compliance Data"]
    L -->|"Irreversible; cannot shorten or delete"| App2["Regulatory Archive Records"]
    LH -->|"Retained until explicitly cleared"| App3["Litigation & Subpoena Evidence"]
```

### 1. Time-Based Retention Policies
- **Unlocked State**: The policy is active and protects data from modification or deletion, but administrators retain the ability to extend, shorten, or delete the retention policy. Ideal for validation and proof-of-concept testing.
- **Locked State**: Once locked, the policy becomes **strictly irreversible**. The retention interval can only be extended; it can never be shortened or removed. Complies with strict financial regulations:
  - **SEC Rule 17a-4(f)**
  - **FINRA Rule 4511(c)**
  - **CFTC Rule 1.31(b)-(c)**

### 2. Legal Holds
- Applies a non-expiring hold on container data tagged with one or more case identifiers (e.g., `Litigation-2026-Case01`).
- While a legal hold is active, blobs can be created and read, but **cannot be modified or deleted**.
- Unlike locked retention policies, legal holds can be cleared at any time by users possessing the `Microsoft.Storage/storageAccounts/blobServices/containers/clearLegalHold/action` RBAC permission.

### Architectural Matrix: Stored Access Policies vs. Immutable Storage

| Feature | Stored Access Policy (SAP) | Time-Based Retention (WORM) | Legal Hold |
| :--- | :--- | :--- | :--- |
| **Primary Purpose** | Delegated authentication management and SAS lifecycle control | Regulatory compliance and tamper-proof archival | Legal discovery, audit holds, and active litigation preservation |
| **Enforcement Scope** | Specific SAS tokens signed with `si` | All blobs in container (current and future) | All blobs in container |
| **Can Delete Blobs?** | Yes, if policy includes `Delete` (`d`) | No, completely blocked until retention expires | No, completely blocked while hold exists |
| **Can Overwrite Blobs?**| Yes, if policy includes `Write` (`w`) | No, blocked (append-only mode can be enabled) | No, blocked (append-only mode can be enabled) |
| **Can Account Owner Bypass?** | Yes (Owner can modify/delete SAP) | **No** (if policy is Locked, even Subscription Owner cannot delete) | No (must explicitly clear the legal hold tag) |

---

## Production Automation: Azure CLI Reference Guide

In automated enterprise environments, access policies and immutability controls are provisioned via infrastructure-as-code or scripted pipelines.

### 1. Managing Stored Access Policies via Azure CLI

#### Create a Stored Access Policy
```bash
az storage container policy create \
  --account-name azurestudystorage01 \
  --container-name data \
  --name READONLY \
  --permissions rl \
  --auth-mode key
```

#### Generate a Policy-Backed SAS Token
```bash
az storage container generate-sas \
  --account-name azurestudystorage01 \
  --name data \
  --policy-name READONLY \
  --https-only \
  --output tsv \
  --auth-mode key
```

#### Update Policy Permissions (Elevate to Delete Without Changing SAS)
```bash
az storage container policy update \
  --account-name azurestudystorage01 \
  --container-name data \
  --name READONLY \
  --permissions rld \
  --auth-mode key
```

#### List All Active Policies on Container
```bash
az storage container policy list \
  --account-name azurestudystorage01 \
  --container-name data \
  --output table \
  --auth-mode key
```

#### Revoke a Stored Access Policy (Instant SAS Invalidation)
```bash
az storage container policy delete \
  --account-name azurestudystorage01 \
  --container-name data \
  --name READONLY \
  --auth-mode key
```

---

### 2. Configuring Immutable Blob Storage via Azure CLI

#### Create an Unlocked Time-Based Retention Policy (e.g., 365 Days)
```bash
az storage container immutability-policy create \
  --account-name azurestudystorage01 \
  --container-name data \
  --period 365 \
  --resource-group azure-study
```

#### Lock the Retention Policy (Caution: Irreversible Action)
```bash
az storage container immutability-policy lock \
  --account-name azurestudystorage01 \
  --container-name data \
  --resource-group azure-study
```

#### Apply a Legal Hold Tag
```bash
az storage container legal-hold set \
  --account-name azurestudystorage01 \
  --container-name data \
  --tags "SEC-Audit-2026" "InternalInvestigation-Q4" \
  --resource-group azure-study
```

#### Clear a Legal Hold Tag
```bash
az storage container legal-hold clear \
  --account-name azurestudystorage01 \
  --container-name data \
  --tags "InternalInvestigation-Q4" \
  --resource-group azure-study
```

---

## Enterprise Governance and Security Best Practices

1. **Mandate Stored Access Policies for Long-Lived Service SAS Tokens**: Never issue ad-hoc Service SAS tokens with lifetimes exceeding a few hours. If an integration requires multi-month or annual delegated access, bind the token to a Stored Access Policy so you retain revocation authority.
2. **Respect the 5-Policy Container Limit**: Azure Blob Storage restricts containers to a maximum of 5 Stored Access Policies simultaneously. If your architecture requires more than 5 distinct delegated roles, consider using Microsoft Entra ID RBAC with User Delegation SAS, which supports unlimited ephemeral tokens.
3. **Always Enforce HTTPS (`spr=https`)**: Prevent man-in-the-middle credential interception by mandating TLS transport security for all SAS requests.
4. **Restrict Ingress IP Addresses (`sip`)**: Where possible, specify allowed client IP CIDR ranges in the SAS generation parameters to prevent unauthorized usage if the SAS URI is inadvertently exposed.
5. **Separate Ingestion and Archival Containers for Immutability**: Because locked immutability policies cannot be reversed, keep operational data in standard containers and use Azure Blob Lifecycle Management policies to transition documents into locked WORM compliance containers upon completion.
6. **Audit Access Policy Modifications in Azure Monitor**: Enable Diagnostic Settings on storage accounts to stream `StorageWrite` and `StorageDelete` logs into Log Analytics workspaces, generating automated alerts whenever container ACLs or immutability policies are altered.

---

## Verification Checklist

| Checkpoint | Requirement | Verification Status |
| :--- | :--- | :--- |
| **1. Policy Definition** | Created Stored Access Policy `READONLY` with permissions `rl` | Verified in Azure Portal table |
| **2. Policy Persistence** | Saved container configuration using the portal Save action | Verified via container ACL persistence |
| **3. SAS Generation** | Generated Service SAS referencing `si=READONLY` | Verified absence of `sp` parameter in query string |
| **4. Storage Explorer Mount** | Mounted container `data-1 (SAS)` via SAS URL | Successfully attached and enumerated virtual folders |
| **5. Traversal Validation** | Navigated into `documents` and selected PDF | Read and List permissions validated |
| **6. Enforcement Validation** | Executed HTTP DELETE on `2308.15363v4.pdf` | Intercepted with 403 `AuthorizationPermissionMismatch` |
| **7. Immutability Readiness** | Evaluated WORM Time-based retention vs Legal Holds | Architecture and CLI commands cataloged |

---

## Conclusion

In **Day 12**, we closed the critical security loop introduced in Day 11. While Shared Access Signatures provide least-privilege delegation, Stored Access Policies furnish the indispensable administrative controls required to manage, adjust, and revoke those delegated signatures in production without business disruption. Combined with Immutable Blob Storage, Azure Storage provides a robust, defense-in-depth framework meeting the highest enterprise security and compliance standards.
