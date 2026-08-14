Import-Module "$PSScriptRoot\Engine.psm1" -Force
$s1=New-MagSeed -X -0.35 -Y 0.0 -Strength 1.0
$s2=New-MagSeed -X 0.35 -Y 0.0 -Strength -1.0
$d1=New-MagDipole -X 0.0 -Y 0.45 -MomentX 0.0 -MomentY 0.8
$result=Invoke-MagSimulation -Sources @($s1,$s2,$d1) -StepsX 31 -StepsY 31 -ReadyThreshold 0.04
$result.Recon | Format-List
