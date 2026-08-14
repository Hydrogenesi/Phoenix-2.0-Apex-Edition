Set-StrictMode -Version Latest
function New-MagDipole {
  [CmdletBinding()] param([double]$X,[double]$Y,[double]$MomentX,[double]$MomentY)
  [pscustomobject]@{ PSTypeName='PNX.MAG.Dipole'; X=$X; Y=$Y; MomentX=$MomentX; MomentY=$MomentY }
}
Export-ModuleMember -Function New-MagDipole
