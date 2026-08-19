# ================================
# Phoenix Cosmogenic Module v13
# ================================

class PhoenixSystem {
    [double]$Curvature = 0.0
    [double]$AngularMomentum = 0.0
    [double]$RadialTensionInner = 0.0
    [double]$RadialTensionOuter = 0.0
    [double]$CoreDensity = 1.0

    [double]$DeltaOmega = 0.0
    [double]$DeltaSigma = 0.0
    [double]$DeltaPhi = 0.0

    [double]$ContractedOmega = 0.0
    [double]$ContractedSigma = 0.0
    [double]$ContractedPhi = 0.0

    [double]$Stage1_CellularPotentialEnergy = 0.0
    [double]$Stage2_MolecularValenceOrder = 0.0
    [double]$Stage3_EnzymaticReactionLoops = 0.0
    [double]$Stage4_LineageSplitFidelity = 0.0
    [double]$Stage5_TissueIntegrationCoherence = 0.0
    [double]$Stage6_OrganismalThresholdMetric = 0.0
    [double]$Stage7_ExoticAdaptationPotential = 0.0
    [double]$Stage8_EvolutionarySingularityMass = 0.0

    [double]$Stage1Threshold = 0.12
    [double]$Stage2Threshold = 0.22
    [double]$Stage3Threshold = 0.34
    [double]$Stage4Threshold = 0.46
    [double]$Stage5Threshold = 0.58
    [double]$Stage6Threshold = 0.70
    [double]$Stage7Threshold = 0.82
    [double]$Stage8Threshold = 0.92

    [double]$MeaningApexIndex = 0.0
    [double]$EntropicNegentropy = 0.0
    [double]$ResonanceHarmony = 0.0

    [int]$ActiveStage = 1
    [string]$ActiveStageName = "Cellular Potential Energy"

    PhoenixSystem() {}
}

function Get-StageNames {
    return @(
        "Cellular Potential Energy",
        "Molecular Valence Order",
        "Enzymatic Reaction Loops",
        "Lineage Split Fidelity",
        "Tissue Integration Coherence",
        "Organismal Threshold Metric",
        "Exotic Adaptation Potential",
        "Evolutionary Singularity Mass"
    )
}

function Get-StageThresholds {
    param([PhoenixSystem]$System)
    return @(
        $System.Stage1Threshold,
        $System.Stage2Threshold,
        $System.Stage3Threshold,
        $System.Stage4Threshold,
        $System.Stage5Threshold,
        $System.Stage6Threshold,
        $System.Stage7Threshold,
        $System.Stage8Threshold
    )
}

function Get-StageEnergies {
    param([PhoenixSystem]$System)
    return @(
        $System.Stage1_CellularPotentialEnergy,
        $System.Stage2_MolecularValenceOrder,
        $System.Stage3_EnzymaticReactionLoops,
        $System.Stage4_LineageSplitFidelity,
        $System.Stage5_TissueIntegrationCoherence,
        $System.Stage6_OrganismalThresholdMetric,
        $System.Stage7_ExoticAdaptationPotential,
        $System.Stage8_EvolutionarySingularityMass
    )
}

function Set-StageEnergies {
    param(
        [PhoenixSystem]$System,
        [double[]]$Energies
    )

    $System.Stage1_CellularPotentialEnergy = $Energies[0]
    $System.Stage2_MolecularValenceOrder = $Energies[1]
    $System.Stage3_EnzymaticReactionLoops = $Energies[2]
    $System.Stage4_LineageSplitFidelity = $Energies[3]
    $System.Stage5_TissueIntegrationCoherence = $Energies[4]
    $System.Stage6_OrganismalThresholdMetric = $Energies[5]
    $System.Stage7_ExoticAdaptationPotential = $Energies[6]
    $System.Stage8_EvolutionarySingularityMass = $Energies[7]
}

function Limit-Unit {
    param([double]$Value)
    return [math]::Max(0.0, [math]::Min(1.0, $Value))
}

function New-PhoenixSystem {
    $sys = [PhoenixSystem]::new()
    $sys.Curvature = 1.0
    $sys.AngularMomentum = 1.0
    $sys.RadialTensionInner = 1.0
    $sys.RadialTensionOuter = 1.0
    $sys.CoreDensity = 1.0
    return $sys
}

function ΔΩ { param([PhoenixSystem]$System) return $System.Curvature * 0.5 }
function ΔΛ { param([PhoenixSystem]$System) return $System.AngularMomentum * 0.1 }
function ΔΣ { param([PhoenixSystem]$System) return $System.RadialTensionInner - $System.RadialTensionOuter }
function ΔΞ { param([PhoenixSystem]$System) return ($System.RadialTensionInner + $System.RadialTensionOuter) * 0.05 }
function ΔΦ { param([PhoenixSystem]$System) return $System.CoreDensity * 0.01 }

function Invoke-Contraction {
    param(
        [double]$x,
        [double]$Scale = 10.0
    )
    if ($Scale -eq 0) { return $x }
    $ratio = [math]::Abs($x / $Scale)
    return $x / (1 + $ratio)
}

function Update-PhoenixConvergenceMetrics {
    param([PhoenixSystem]$System)

    $energies = Get-StageEnergies -System $System
    $total = ($energies | Measure-Object -Sum).Sum

    $weights = 1..8
    $weighted = 0.0
    for ($i = 0; $i -lt 8; $i++) {
        $weighted += $energies[$i] * $weights[$i]
    }
    $System.MeaningApexIndex = Limit-Unit ($weighted / ($weights | Measure-Object -Sum).Sum)

    if ($total -le 0) {
        $System.EntropicNegentropy = 0.0
    }
    else {
        $entropy = 0.0
        foreach ($e in $energies) {
            if ($e -gt 0) {
                $p = $e / $total
                $entropy -= $p * [math]::Log($p)
            }
        }
        $maxEntropy = [math]::Log(8)
        $System.EntropicNegentropy = Limit-Unit (1.0 - ($entropy / $maxEntropy))
    }

    $adjacent = @()
    for ($i = 0; $i -lt 7; $i++) {
        $a = $energies[$i]
        $b = $energies[$i + 1]
        $adjacent += 1.0 - [math]::Abs($a - $b)
    }
    $System.ResonanceHarmony = Limit-Unit (($adjacent | Measure-Object -Average).Average)
}

function Update-PhoenixStageEnergies {
    param(
        [PhoenixSystem]$System,
        [double]$Omega,
        [double]$Lambda,
        [double]$Sigma,
        [double]$Xi,
        [double]$Phi
    )

    $energies = Get-StageEnergies -System $System
    $thresholds = Get-StageThresholds -System $System

    $baseDrive = Limit-Unit (([math]::Abs($Omega) * 0.22) + ([math]::Abs($Lambda) * 0.30) + ([math]::Abs($Sigma) * 0.16) + ([math]::Abs($Xi) * 0.14) + ([math]::Abs($Phi) * 6.0))

    $updated = @()
    for ($i = 0; $i -lt 8; $i++) {
        $current = $energies[$i]
        $feedForward = if ($i -eq 0) { $baseDrive } else { $updated[$i - 1] * 0.52 }

        $gate = 1.0
        if ($i -gt 0 -and $updated[$i - 1] -lt $thresholds[$i - 1]) {
            $gate = 0.55
        }

        $retained = $current * 0.88
        $delta = ($feedForward * 0.42 * $gate) + ($baseDrive * 0.08)
        $updated += (Limit-Unit ($retained + $delta))
    }

    Set-StageEnergies -System $System -Energies $updated

    $active = 1
    for ($i = 0; $i -lt 8; $i++) {
        if ($updated[$i] -ge $thresholds[$i]) {
            $active = $i + 1
        }
        else {
            break
        }
    }

    $System.ActiveStage = $active
    $System.ActiveStageName = (Get-StageNames)[$active - 1]

    Update-PhoenixConvergenceMetrics -System $System
}

function Get-ProgressBar {
    param([double]$Value)

    $clamped = Limit-Unit $Value
    $filled = [int][math]::Round($clamped * 10)
    $empty = 10 - $filled
    return ("█" * $filled) + ("░" * $empty)
}

function Invoke-OperatorHUDv13 {
    param(
        [PhoenixSystem]$System,
        [int]$Iteration,
        [int]$TotalIterations
    )

    Write-Host "===== PHOENIX OPERATOR HUD v13 ====="
    Write-Host "Iteration $Iteration / $TotalIterations"
    Write-Host "Active Stage: $($System.ActiveStage) ($($System.ActiveStageName))"
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host "Stage Energies:"

    $labels = Get-StageNames
    $energies = Get-StageEnergies -System $System

    for ($i = 0; $i -lt 8; $i++) {
        $energy = $energies[$i]
        $bar = Get-ProgressBar -Value $energy
        $percent = [math]::Round($energy * 100, 1)
        $marker = if (($i + 1) -eq $System.ActiveStage) { " ← ACTIVE" } else { "" }
        Write-Host ("  {0}. {1,-26} {2} {3,5}%{4}" -f ($i + 1), $labels[$i], $bar, $percent, $marker)
    }

    $status = if ($System.MeaningApexIndex -ge 0.95) { "Terminal unity reached" }
              elseif ($System.MeaningApexIndex -ge 0.70) { "Approaching singularity" }
              else { "Emergence in progress" }

    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host "Convergence Metrics:"
    Write-Host ("  Meaning Apex Index:    {0:N3} ({1:N1}% singularity attained)" -f $System.MeaningApexIndex, ($System.MeaningApexIndex * 100))
    Write-Host ("  Entropic Negentropy:   {0:N3}" -f $System.EntropicNegentropy)
    Write-Host ("  Resonance Harmony:     {0:N3}" -f $System.ResonanceHarmony)
    Write-Host "  Convergence Status:    $status"
    Write-Host "======================================"
}

function Invoke-PhoenixIgnitionLoop {
    param(
        [Parameter(Mandatory)]
        [PhoenixSystem]$System,
        [int]$Iterations = 20,
        [string]$OutputPath = "./phoenix_simulation_output.json",
        [switch]$RenderHUD
    )

    $records = @()

    for ($i = 1; $i -le $Iterations; $i++) {
        $Omega = ΔΩ -System $System
        $Lambda = ΔΛ -System $System
        $Sigma = ΔΣ -System $System
        $Xi = ΔΞ -System $System
        $Phi = ΔΦ -System $System

        $System.Curvature += 0.01 * $Omega
        $System.AngularMomentum += 0.01 * $Lambda
        $System.RadialTensionInner += 0.01 * ($Sigma + ($System.ResonanceHarmony * 0.05))
        $System.RadialTensionOuter += 0.01 * ($Xi + ((1 - $System.ResonanceHarmony) * 0.05))
        $System.CoreDensity += 0.01 * $Phi

        $System.DeltaOmega = $Omega
        $System.DeltaSigma = $Sigma
        $System.DeltaPhi = $Phi

        $System.ContractedOmega = Invoke-Contraction -x $Omega -Scale 10
        $System.ContractedSigma = Invoke-Contraction -x $Sigma -Scale 10
        $System.ContractedPhi = Invoke-Contraction -x $Phi -Scale 10

        Update-PhoenixStageEnergies -System $System -Omega $Omega -Lambda $Lambda -Sigma $Sigma -Xi $Xi -Phi $Phi

        $record = [ordered]@{
            iteration = $i
            active_stage = $System.ActiveStage
            active_stage_name = $System.ActiveStageName
            deltas = [ordered]@{
                omega = $System.DeltaOmega
                sigma = $System.DeltaSigma
                phi = $System.DeltaPhi
            }
            contracted = [ordered]@{
                omega = $System.ContractedOmega
                sigma = $System.ContractedSigma
                phi = $System.ContractedPhi
            }
            stage_energies = Get-StageEnergies -System $System
            stage_thresholds = Get-StageThresholds -System $System
            meaning_apex_index = $System.MeaningApexIndex
            entropic_negentropy = $System.EntropicNegentropy
            resonance_harmony = $System.ResonanceHarmony
        }
        $records += $record

        if ($RenderHUD) {
            Invoke-OperatorHUDv13 -System $System -Iteration $i -TotalIterations $Iterations
        }
    }

    if ($OutputPath) {
        @{ iterations = $records } | ConvertTo-Json -Depth 6 | Out-File -FilePath $OutputPath -Encoding UTF8
    }

    return [pscustomobject]@{
        System = $System
        Iterations = $records
        OutputPath = $OutputPath
    }
}

function Test-PhoenixSystem {
    param([PhoenixSystem]$System)

    $errors = @()

    $coreValues = @(
        @{ Name = "Curvature"; Value = $System.Curvature },
        @{ Name = "AngularMomentum"; Value = $System.AngularMomentum },
        @{ Name = "RadialTensionInner"; Value = $System.RadialTensionInner },
        @{ Name = "RadialTensionOuter"; Value = $System.RadialTensionOuter },
        @{ Name = "CoreDensity"; Value = $System.CoreDensity }
    )
    foreach ($entry in $coreValues) {
        if ([double]::IsNaN($entry.Value) -or [double]::IsInfinity($entry.Value)) {
            $errors += "$($entry.Name) must be finite"
        }
    }

    $energies = Get-StageEnergies -System $System
    foreach ($energy in $energies) {
        if ($energy -lt 0 -or $energy -gt 1) {
            $errors += "Stage energies must remain in [0,1]"
            break
        }
    }

    if ($System.ActiveStage -lt 1 -or $System.ActiveStage -gt 8) {
        $errors += "Active stage must be between 1 and 8"
    }

    if ($errors.Count -gt 0) {
        Write-Host "PhoenixSystem INVALID:"
        $errors | ForEach-Object { Write-Host " - $_" }
        return $false
    }

    Write-Host "PhoenixSystem VALID."
    return $true
}
