param(
  [string]$Root = "C:\Users\Infin\Projects\Phoenix-2.0-Apex-Edition"
)

$Mag = Join-Path $Root "Engine\Modules\MAG"

Start-Process notepad.exe (Join-Path $Root "RED_ROBIN_A_PROMPT.txt")
Start-Process notepad.exe (Join-Path $Root "RED_ROBIN_B_PROMPT.txt")
Start-Process notepad.exe (Join-Path $Root "RED_ROBIN_C_PROMPT.txt")
Start-Process notepad.exe (Join-Path $Root "RED_ROBIN_D_PROMPT.txt")
Start-Process notepad.exe (Join-Path $Root "RED_ROBIN_RUN_ORDER.txt")
Start-Process notepad.exe (Join-Path $Root "GET_SHIT_DONE.RED_ROBIN.PNX.txt")
Start-Process explorer.exe $Mag
