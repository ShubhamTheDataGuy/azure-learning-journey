import subprocess
from pathlib import Path
import shutil

REPO_ROOT = Path(r"C:\Users\Shubham\Desktop\Azure-Learning-Journey")
DAY2_DIR = REPO_ROOT / "day-02-azure-windows-vm-data-disks-snapshots-migration"
CURATED_DIR = DAY2_DIR / "screenshots" / "curated"
BRAIN_DIR = Path(r"C:\Users\Shubham\.gemini\antigravity\brain\3f36748e-db4f-4b5b-aff2-ab97385431c2")

CURATED_DIR.mkdir(parents=True, exist_ok=True)

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
  body {
    background: #080D1A;
    color: #F8FAFC;
    width: 2400px;
    height: 1350px;
    padding: 35px 50px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    position: relative;
  }

  /* Header */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 2px solid #1E293B;
    padding-bottom: 18px;
    z-index: 10;
  }
  .title-area h1 {
    font-size: 38px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
  }
  .title-area .sub {
    font-size: 18px;
    color: #94A3B8;
    display: flex;
    gap: 25px;
  }
  .title-area .sub span {
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }
  .badge-tag {
    background: #1E293B;
    color: #38BDF8;
    padding: 4px 12px;
    border-radius: 6px;
    font-family: monospace;
    font-size: 16px;
    border: 1px solid #334155;
  }

  /* Legend */
  .legend {
    display: flex;
    gap: 24px;
    background: #0F172A;
    padding: 12px 24px;
    border-radius: 10px;
    border: 1px solid #1E293B;
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 16px;
    font-weight: 600;
  }
  .line-sample {
    width: 30px;
    height: 4px;
    border-radius: 2px;
  }
  .line-attach { background: #38BDF8; box-shadow: 0 0 10px #38BDF8; }
  .line-snap { background: #C084FC; box-shadow: 0 0 10px #C084FC; }
  .line-restore { background: #34D399; box-shadow: 0 0 10px #34D399; }
  .line-target { background: #818CF8; box-shadow: 0 0 10px #818CF8; }

  /* Azure Cloud Container */
  .azure-cloud {
    background: #060A14;
    border: 3px solid #0284C7;
    border-radius: 24px;
    padding: 35px 35px;
    position: relative;
    box-shadow: 0 0 60px rgba(2, 132, 199, 0.15);
    height: 1100px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .cloud-badge {
    position: absolute;
    top: -20px;
    left: 45px;
    background: #0284C7;
    color: #FFFFFF;
    font-size: 17px;
    font-weight: 800;
    padding: 7px 22px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
  }
  .rg-badge {
    position: absolute;
    top: -18px;
    left: 440px;
    background: #1E293B;
    color: #CBD5E1;
    font-size: 15px;
    font-weight: 600;
    padding: 6px 18px;
    border-radius: 16px;
    border: 1px solid #334155;
  }

  /* 4-Stage Grid */
  .stages-grid {
    display: grid;
    grid-template-columns: 530px 480px 480px 530px;
    gap: 65px;
    height: 980px;
    position: relative;
    z-index: 10;
    align-items: stretch;
  }

  /* Column styling */
  .stage-col {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
  }

  /* Banner */
  .stage-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 18px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 14px;
  }
  .banner-vm1 { background: #0C4A6E; color: #7DD3FC; border: 1px solid #0284C7; }
  .banner-snap { background: #581C87; color: #E9D5FF; border: 1px solid #9333EA; }
  .banner-disk { background: #064E3B; color: #A7F3D0; border: 1px solid #059669; }
  .banner-vm2 { background: #312E81; color: #C7D2FE; border: 1px solid #4F46E5; }

  /* VM Card */
  .vm-box {
    background: #0B1324;
    border: 2px solid #0284C7;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 10px 35px rgba(2, 132, 199, 0.15);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex-grow: 1;
  }
  .vm-box.target {
    border-color: #6366F1;
    box-shadow: 0 10px 35px rgba(99, 102, 241, 0.18);
  }

  .vm-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }
  .vm-title {
    font-size: 24px;
    font-weight: 800;
    color: #F8FAFC;
  }
  .vm-box.target .vm-title { color: #C7D2FE; }

  .sku-badge {
    background: #030712;
    color: #38BDF8;
    padding: 4px 12px;
    border-radius: 6px;
    font-family: monospace;
    font-size: 15px;
    border: 1px solid #1E293B;
  }
  .vm-box.target .sku-badge { color: #A5B4FC; }

  .spec-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-bottom: 14px;
  }
  .spec-item {
    background: #030712;
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid #1F2937;
  }
  .spec-label { font-size: 11px; color: #64748B; text-transform: uppercase; font-weight: 700; margin-bottom: 2px; }
  .spec-val { font-size: 14px; font-weight: 700; color: #E2E8F0; }

  /* Disk Inside VM Card */
  .disk-subcard {
    background: #0F172A;
    border: 2px solid #38BDF8;
    border-radius: 14px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .disk-subcard.os-disk {
    border-color: #334155;
    background: #070B14;
    padding: 12px 16px;
    margin-bottom: 12px;
  }
  .disk-subcard.migrated {
    border-color: #10B981;
    background: #061A14;
  }

  .disk-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .disk-title {
    font-size: 18px;
    font-weight: 700;
    color: #38BDF8;
    font-family: monospace;
  }
  .disk-subcard.migrated .disk-title { color: #34D399; }

  .lun-badge {
    background: #0284C7;
    color: #FFFFFF;
    font-size: 12px;
    font-weight: 800;
    padding: 3px 10px;
    border-radius: 12px;
  }
  .disk-subcard.migrated .lun-badge { background: #059669; }

  /* In-Guest Data Box */
  .data-payload-box {
    background: #030712;
    border: 1px solid #1E293B;
    border-left: 5px solid #F59E0B;
    border-radius: 8px;
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .data-payload-box.verified {
    border-left-color: #10B981;
    background: #022018;
  }
  .payload-title {
    font-size: 13px;
    font-weight: 700;
    color: #FBBF24;
    display: flex;
    justify-content: space-between;
  }
  .data-payload-box.verified .payload-title { color: #34D399; }
  .payload-content {
    font-family: monospace;
    font-size: 13px;
    color: #F8FAFC;
    background: #080D1A;
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid #1E293B;
  }

  /* Snapshot Card */
  .snapshot-card {
    background: #110B24;
    border: 2px solid #A855F7;
    border-radius: 20px;
    padding: 26px;
    box-shadow: 0 10px 35px rgba(168, 85, 247, 0.18);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex-grow: 1;
    position: relative;
  }
  .snap-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .snap-title {
    font-size: 22px;
    font-weight: 800;
    color: #C084FC;
  }
  .snap-pill {
    background: #6B21A8;
    color: #FAF5FF;
    font-size: 12px;
    font-weight: 800;
    padding: 4px 12px;
    border-radius: 12px;
  }
  .snap-detail {
    background: #030712;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #2E1065;
    font-family: monospace;
    font-size: 14px;
    color: #E9D5FF;
    line-height: 1.8;
  }
  .gotcha-box {
    background: #1F1300;
    border: 1px solid #78350F;
    border-left: 5px solid #F59E0B;
    border-radius: 10px;
    padding: 16px;
    font-size: 14px;
    color: #FDE68A;
    line-height: 1.5;
  }

  /* Restored Managed Disk Card */
  .managed-disk-card {
    background: #061A14;
    border: 2px solid #10B981;
    border-radius: 20px;
    padding: 26px;
    box-shadow: 0 10px 35px rgba(16, 185, 129, 0.18);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex-grow: 1;
    position: relative;
  }
  .mdisk-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .mdisk-title {
    font-size: 22px;
    font-weight: 800;
    color: #34D399;
  }
  .mdisk-pill {
    background: #065F46;
    color: #ECFDF5;
    font-size: 12px;
    font-weight: 800;
    padding: 4px 12px;
    border-radius: 12px;
  }
  .mdisk-detail {
    background: #030712;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #064E3B;
    font-family: monospace;
    font-size: 14px;
    color: #A7F3D0;
    line-height: 1.8;
  }
  .ready-box {
    background: #022C22;
    border: 1px solid #047857;
    border-radius: 10px;
    padding: 16px;
    font-size: 14px;
    color: #6EE7B7;
    line-height: 1.5;
  }

  /* SVG Flow Layer */
  #svg-flow {
    position: absolute;
    top: 0;
    left: 0;
    width: 2400px;
    height: 1350px;
    pointer-events: none;
    z-index: 25;
  }
  .flow-label {
    fill: #CBD5E1;
    font-size: 13px;
    font-weight: 700;
    font-family: monospace;
  }
  .label-bg {
    fill: #0F172A;
    stroke: #334155;
    stroke-width: 1px;
    rx: 6px;
  }
</style>
</head>
<body>

  <!-- Header -->
  <div class="header">
    <div class="title-area">
      <h1>Microsoft Azure Managed Disk Lifecycle & Cross-VM Migration</h1>
      <div class="sub">
        <span>Region: <b class="badge-tag">Japan West</b></span>
        <span>Resource Group: <b class="badge-tag">azure-study-1</b></span>
        <span>Workload: <b class="badge-tag">Windows Server 2025 Datacenter + Data Disks & Snapshots</b></span>
      </div>
    </div>
    <div class="legend">
      <div class="legend-item"><div class="line-sample line-attach"></div> Data Disk Attach & I/O</div>
      <div class="legend-item"><div class="line-sample line-snap"></div> Snapshot Point-in-Time Copy</div>
      <div class="legend-item"><div class="line-sample line-restore"></div> Managed Disk Creation</div>
      <div class="legend-item"><div class="line-sample line-target"></div> Target VM Attachment & Mount</div>
    </div>
  </div>

  <!-- Azure Cloud Boundary -->
  <div class="azure-cloud">
    <div class="cloud-badge">Microsoft Azure Boundary</div>
    <div class="rg-badge">Resource Group: azure-study-1</div>

    <div class="stages-grid">

      <!-- Step 1: Source VM (webvm02) -->
      <div class="stage-col">
        <div class="stage-banner banner-vm1">
          <span>Phase 1: Source Virtual Machine</span>
          <span>webvm02</span>
        </div>

        <div class="vm-box">
          <div>
            <div class="vm-header-row">
              <div class="vm-title">Virtual Machine: webvm02</div>
              <div class="sku-badge">Standard_B2als_v2</div>
            </div>

            <div class="spec-grid">
              <div class="spec-item">
                <div class="spec-label">Operating System</div>
                <div class="spec-val">Windows Server 2025 (x64)</div>
              </div>
              <div class="spec-item">
                <div class="spec-label">Compute SKU</div>
                <div class="spec-val">2 vCPUs | 4 GiB RAM</div>
              </div>
              <div class="spec-item">
                <div class="spec-label">Public IP / RDP</div>
                <div class="spec-val">20.210.157.100 (Port 3389)</div>
              </div>
              <div class="spec-item">
                <div class="spec-label">Virtual Network</div>
                <div class="spec-val">vnetjapanwestTemplate</div>
              </div>
            </div>

            <!-- OS Disk -->
            <div class="disk-subcard os-disk">
              <div class="disk-header">
                <span style="font-size: 14px; font-weight: 700; color: #94A3B8;">OS Disk: webvm02_OsDisk_1</span>
                <span style="font-size: 12px; color: #64748B;">127 GiB (C:)</span>
              </div>
            </div>
          </div>

          <!-- Source Data Disk -->
          <div id="card-datadisk1" class="disk-subcard">
            <div class="disk-header">
              <span class="disk-title">datadisk-webvm02-1</span>
              <span class="lun-badge">LUN 0</span>
            </div>
            <div style="font-size: 13px; color: #94A3B8; font-family: monospace;">
              Size: 4 GiB | Premium SSD LRS | Cache: Read-only
            </div>

            <!-- Payload in Disk 1 -->
            <div class="data-payload-box">
              <div class="payload-title">
                <span>In-Guest Mount: Drive E:\ (NTFS, GPT)</span>
                <span>4.00 GB</span>
              </div>
              <div style="font-size: 12px; color: #94A3B8;">Created Test File: <code>E:\data.txt</code></div>
              <div class="payload-content">"my name is shubham and i love cloud computing."</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 2: Azure Snapshot -->
      <div class="stage-col">
        <div class="stage-banner banner-snap">
          <span>Phase 2: Point-In-Time Backup</span>
          <span>Snapshot</span>
        </div>

        <div id="card-snapshot" class="snapshot-card">
          <div>
            <div class="snap-header">
              <span class="snap-title">Disk Snapshot</span>
              <span class="snap-pill">Read-Only</span>
            </div>

            <div style="font-size: 18px; font-weight: 800; color: #E9D5FF; font-family: monospace; margin: 12px 0 16px 0;">
              webvm02-datadisk-1-snapshot-1
            </div>

            <div class="snap-detail">
              <b>Source Disk:</b> datadisk-webvm02-1<br>
              <b>Snapshot Type:</b> Full Snapshot<br>
              <b>Storage Tier:</b> Standard HDD (ZRS)<br>
              <b>State:</b> Point-in-Time Frozen State<br>
              <b>Data Payload:</b> Exact sector bit-copy of 4 GiB
            </div>
          </div>

          <div class="gotcha-box">
            <b>Architectural Rule:</b><br>
            Azure Snapshots cannot be attached directly to a Virtual Machine. You must create an independent <b>Managed Disk</b> from the snapshot before attachment.
          </div>
        </div>
      </div>

      <!-- Step 3: Restored Managed Disk -->
      <div class="stage-col">
        <div class="stage-banner banner-disk">
          <span>Phase 3: Restored Disk</span>
          <span>Managed Disk</span>
        </div>

        <div id="card-restored-disk" class="managed-disk-card">
          <div>
            <div class="mdisk-header">
              <span class="mdisk-title">Managed Disk</span>
              <span class="mdisk-pill">Ready to Attach</span>
            </div>

            <div style="font-size: 18px; font-weight: 800; color: #A7F3D0; font-family: monospace; margin: 12px 0 16px 0;">
              attached-disk-1
            </div>

            <div class="mdisk-detail">
              <b>Source Snapshot:</b> webvm02-...-snapshot-1<br>
              <b>Disk Type:</b> Data Disk (OS: None)<br>
              <b>Storage Tier:</b> Premium SSD LRS<br>
              <b>Size:</b> 4 GiB (P1 - 120 IOPS / 25 MB/s)<br>
              <b>Region:</b> Japan West (same as VMs)
            </div>
          </div>

          <div class="ready-box">
            <b>Independent Azure Resource:</b><br>
            Can be attached to any compatible VM in Japan West with complete filesystem and NTFS partition preservation.
          </div>
        </div>
      </div>

      <!-- Step 4: Destination VM (webvm03) -->
      <div class="stage-col">
        <div class="stage-banner banner-vm2">
          <span>Phase 4: Target VM & Verification</span>
          <span>webvm03</span>
        </div>

        <div class="vm-box target">
          <div>
            <div class="vm-header-row">
              <div class="vm-title">Virtual Machine: webvm03</div>
              <div class="sku-badge">Standard_B2als_v2</div>
            </div>

            <div class="spec-grid">
              <div class="spec-item">
                <div class="spec-label">Operating System</div>
                <div class="spec-val">Windows Server 2025 (x64)</div>
              </div>
              <div class="spec-item">
                <div class="spec-label">Compute SKU</div>
                <div class="spec-val">2 vCPUs | 4 GiB RAM</div>
              </div>
              <div class="spec-item">
                <div class="spec-label">Public Inbound</div>
                <div class="spec-val">RDP (Port 3389 Allowed)</div>
              </div>
              <div class="spec-item">
                <div class="spec-label">Resource Group</div>
                <div class="spec-val">azure-study-1</div>
              </div>
            </div>

            <!-- OS Disk -->
            <div class="disk-subcard os-disk">
              <div class="disk-header">
                <span style="font-size: 14px; font-weight: 700; color: #94A3B8;">OS Disk: webvm03_OsDisk_1</span>
                <span style="font-size: 12px; color: #64748B;">127 GiB (C:)</span>
              </div>
            </div>
          </div>

          <!-- Migrated Data Disk -->
          <div id="card-targetdisk" class="disk-subcard migrated">
            <div class="disk-header">
              <span class="disk-title">attached-disk-1</span>
              <span class="lun-badge">LUN 0</span>
            </div>
            <div style="font-size: 13px; color: #A7F3D0; font-family: monospace;">
              Size: 4 GiB | Premium SSD LRS | Cache: Read Only
            </div>

            <!-- Payload Verified in Disk 2 -->
            <div class="data-payload-box verified">
              <div class="payload-title">
                <span>Auto-Mounted In-Guest: Drive D:\ (NTFS)</span>
                <span>3.98 GB</span>
              </div>
              <div style="font-size: 12px; color: #A7F3D0;">Verified File Content via Notepad:</div>
              <div class="payload-content">"my name is shubham and i love cloud computing."</div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- SVG Flow Connections -->
  <svg id="svg-flow">
    <defs>
      <marker id="arrow-snap" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto">
        <path d="M 0 0 L 8 4 L 0 8 Z" fill="#C084FC" />
      </marker>
      <marker id="arrow-restore" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto">
        <path d="M 0 0 L 8 4 L 0 8 Z" fill="#34D399" />
      </marker>
      <marker id="arrow-target" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto">
        <path d="M 0 0 L 8 4 L 0 8 Z" fill="#818CF8" />
      </marker>
    </defs>
  </svg>

  <script>
    window.addEventListener('DOMContentLoaded', () => {
      const svg = document.getElementById('svg-flow');

      function drawPath(fromElem, toElem, color, markerId, dash=false, labelText=null, offsetY=0) {
        const rA = fromElem.getBoundingClientRect();
        const rB = toElem.getBoundingClientRect();
        const x1 = rA.right;
        const y1 = rA.top + rA.height / 2 + offsetY;
        const x2 = rB.left;
        const y2 = rB.top + rB.height / 2 + offsetY;

        const dx = (x2 - x1) * 0.5;
        const d = `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;

        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', d);
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke', color);
        path.setAttribute('stroke-width', '4');
        if (dash) path.setAttribute('stroke-dasharray', '8 6');
        if (markerId) path.setAttribute('marker-end', `url(#${markerId})`);
        path.style.filter = `drop-shadow(0 0 8px ${color})`;
        svg.appendChild(path);

        if (labelText) {
          const midX = (x1 + x2) / 2;
          const midY = (y1 + y2) / 2 - 18;

          const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
          const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
          const w = 150;
          rect.setAttribute('x', midX - w / 2);
          rect.setAttribute('y', midY - 14);
          rect.setAttribute('width', w);
          rect.setAttribute('height', 26);
          rect.setAttribute('class', 'label-bg');

          const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          text.setAttribute('x', midX);
          text.setAttribute('y', midY + 4);
          text.setAttribute('text-anchor', 'middle');
          text.setAttribute('class', 'flow-label');
          text.textContent = labelText;

          g.appendChild(rect);
          g.appendChild(text);
          svg.appendChild(g);
        }
      }

      const cardDataDisk1 = document.getElementById('card-datadisk1');
      const cardSnapshot = document.getElementById('card-snapshot');
      const cardRestoredDisk = document.getElementById('card-restored-disk');
      const cardTargetDisk = document.getElementById('card-targetdisk');

      // 1. Data Disk 1 -> Snapshot
      drawPath(cardDataDisk1, cardSnapshot, '#C084FC', 'arrow-snap', false, '1. Create Snapshot', -30);

      // 2. Snapshot -> Managed Disk
      drawPath(cardSnapshot, cardRestoredDisk, '#34D399', 'arrow-restore', false, '2. Create Managed Disk', 0);

      // 3. Managed Disk -> Target VM
      drawPath(cardRestoredDisk, cardTargetDisk, '#818CF8', 'arrow-target', false, '3. Attach to VM', 30);
    });
  </script>

</body>
</html>
"""

html_path = BRAIN_DIR / "scratch" / "day02_diagram.html"
html_path.write_text(html_content, encoding="utf-8")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
output_png = CURATED_DIR / "00_azure_disk_lifecycle_architecture.png"
brain_png = BRAIN_DIR / "day02_architecture_diagram.png"

cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--force-device-scale-factor=1",
    "--window-size=2400,1350",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=1000",
    f"--screenshot={str(output_png)}",
    str(html_path)
]

print("Rendering Day 2 high-res diagram with Chrome...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("Chrome exit code:", res.returncode)

shutil.copy(output_png, brain_png)
print(f"Saved diagram to {output_png} and {brain_png}")
