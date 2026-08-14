Set-StrictMode -Version Latest
function Get-MagFieldTensor {
  [CmdletBinding()] param([double]$X,[double]$Y,[object[]]$Sources,[double]$Softening=0.0001)
  $bx=0.0; $by=0.0
  foreach($s in $Sources){
    if($s.PSTypeName -eq 'PNX.MAG.Seed'){
      $dx=$X-$s.X; $dy=$Y-$s.Y; $r2=($dx*$dx)+($dy*$dy)+$Softening
      $inv=$s.Strength/[math]::Pow($r2,1.5); $bx+=$dx*$inv; $by+=$dy*$inv
    } elseif($s.PSTypeName -eq 'PNX.MAG.Dipole'){
      $dx=$X-$s.X; $dy=$Y-$s.Y; $r2=($dx*$dx)+($dy*$dy)+$Softening; $r=[math]::Sqrt($r2)
      $mx=$s.MomentX; $my=$s.MomentY; $mdotr=($mx*$dx)+($my*$dy); $inv5=1.0/[math]::Pow($r,5)
      $bx += (3.0*$dx*$mdotr - $mx*$r2) * $inv5
      $by += (3.0*$dy*$mdotr - $my*$r2) * $inv5
    }
  }
  [pscustomobject]@{PSTypeName='PNX.MAG.Field';X=$X;Y=$Y;Bx=$bx;By=$by;Magnitude=[math]::Sqrt(($bx*$bx)+($by*$by))}
}
Export-ModuleMember -Function Get-MagFieldTensor
