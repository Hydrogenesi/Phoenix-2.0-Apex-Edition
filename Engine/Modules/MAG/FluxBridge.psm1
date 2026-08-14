Set-StrictMode -Version Latest
function New-MagGrid {
  [CmdletBinding()] param([double]$MinX,[double]$MaxX,[double]$MinY,[double]$MaxY,[int]$StepsX,[int]$StepsY)
  $grid=New-Object System.Collections.Generic.List[object]
  $dx=($MaxX-$MinX)/[math]::Max(1,($StepsX-1)); $dy=($MaxY-$MinY)/[math]::Max(1,($StepsY-1))
  for($iy=0;$iy -lt $StepsY;$iy++){ for($ix=0;$ix -lt $StepsX;$ix++){
    $grid.Add([pscustomobject]@{X=$MinX+($ix*$dx);Y=$MinY+($iy*$dy)})
  }}
  ,$grid
}
Export-ModuleMember -Function New-MagGrid
