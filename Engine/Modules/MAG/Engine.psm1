Set-StrictMode -Version Latest
Import-Module "$PSScriptRoot\Seed.psm1" -Force
Import-Module "$PSScriptRoot\Dipole.psm1" -Force
Import-Module "$PSScriptRoot\FieldTensor.psm1" -Force
Import-Module "$PSScriptRoot\FluxBridge.psm1" -Force
Import-Module "$PSScriptRoot\ReconMap.psm1" -Force
function Invoke-MagSimulation {
  [CmdletBinding()] param([object[]]$Sources,[double]$MinX=-1,[double]$MaxX=1,[double]$MinY=-1,[double]$MaxY=1,[int]$StepsX=21,[int]$StepsY=21,[double]$ReadyThreshold=0.05)
  $grid=New-MagGrid -MinX $MinX -MaxX $MaxX -MinY $MinY -MaxY $MaxY -StepsX $StepsX -StepsY $StepsY
  $samples=New-Object System.Collections.Generic.List[object]
  foreach($p in $grid){ $samples.Add((Get-MagFieldTensor -X $p.X -Y $p.Y -Sources $Sources)) }
  $recon=New-MagReconMap -FieldSamples $samples -ReadyThreshold $ReadyThreshold
  [pscustomobject]@{PSTypeName='PNX.MAG.Result';Sources=$Sources;Samples=$samples;Recon=$recon}
}
Export-ModuleMember -Function Invoke-MagSimulation
