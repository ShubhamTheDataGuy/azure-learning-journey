<#
.SYNOPSIS
    Audits the High Availability placement of all Azure Virtual Machines in a subscription.
.DESCRIPTION
    Inspects whether VMs are configured in Availability Zones, Availability Sets, or standalone,
    and reports their Fault Domain, Update Domain, and Zone distribution.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$ResourceGroupName
)

$query = if ($ResourceGroupName) {
    Get-AzVM -ResourceGroupName $ResourceGroupName -Status
} else {
    Get-AzVM -Status
}

$results = foreach ($vm in $query) {
    $zone = if ($vm.Zones -and $vm.Zones.Count -gt 0) { $vm.Zones -join ", " } else { "None (Regional)" }
    $avSet = if ($vm.AvailabilitySetReference) {
        $vm.AvailabilitySetReference.Id.Split("/")[-1]
    } else {
        "None"
    }

    $fd = if ($vm.PlatformFaultDomain -ne $null) { $vm.PlatformFaultDomain } else { "N/A" }
    $ud = if ($vm.PlatformUpdateDomain -ne $null) { $vm.PlatformUpdateDomain } else { "N/A" }

    [PSCustomObject]@{
        VMName            = $vm.Name
        ResourceGroup     = $vm.ResourceGroupName
        Location          = $vm.Location
        PowerState        = $vm.PowerState
        AvailabilityZone  = $zone
        AvailabilitySet   = $avSet
        FaultDomain       = $fd
        UpdateDomain      = $ud
    }
}

$results | Format-Table -AutoSize
