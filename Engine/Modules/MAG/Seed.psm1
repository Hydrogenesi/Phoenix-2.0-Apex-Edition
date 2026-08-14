Set-StrictMode -Version Latest
function New-MagSeed {
  [CmdletBinding()] param([double]$X,[double]$Y,[double]$Strength)
  [pscustomobject]@{ PSTypeName='PNX.MAG.Seed'; X=$X; Y=$Y; Strength=$Strength }
}
Export-ModuleMember -Function New-MagSeed
