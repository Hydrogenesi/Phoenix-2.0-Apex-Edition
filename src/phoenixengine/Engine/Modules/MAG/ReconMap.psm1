Set-StrictMode -Version Latest
function New-MagReconMap {
  [CmdletBinding()] param([object[]]$FieldSamples,[double]$ReadyThreshold=0.05)
  $max=($FieldSamples|Measure-Object Magnitude -Maximum).Maximum
  $avg=($FieldSamples|Measure-Object Magnitude -Average).Average
  if($null -eq $max){$max=0.0}; if($null -eq $avg){$avg=0.0}
  $status=if($max -ge $ReadyThreshold){'ready'}else{'foul'}
  $score=if($ReadyThreshold -le 0){100}else{[math]::Min(100,[int](($max/$ReadyThreshold)*100))}
  [pscustomobject]@{PSTypeName='PNX.MAG.Recon';Status=$status;Score=$score;MaxMagnitude=$max;AverageMagnitude=$avg;Threshold=$ReadyThreshold}
}
Export-ModuleMember -Function New-MagReconMap
