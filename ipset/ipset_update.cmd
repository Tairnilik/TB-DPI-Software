:: credits to zapret-discord-youtube/service.bat/ipset-update
@echo off

set "listFile=%~dp0ipset.txt"
set "url=https://raw.githubusercontent.com/V3nilla/IPSets-For-Bypass-in-Russia/refs/heads/main/ipset-all.txt"

echo Updating ipset-all...

if exist "%SystemRoot%\System32\curl.exe" (
    curl --version | find "libcurl/7"
    if !errorlevel!==0 (
        curl --ssl-no-revoke -L -o "%listFile%" "%url%"
    ) else (
        curl --ssl-revoke-best-effort -L -o "%listFile%" "%url%"
    )
) else (
    powershell -NoProfile -Command ^
        "$url = '%url%';" ^
        "$out = '%listFile%';" ^
        "$dir = Split-Path -Parent $out;" ^
        "if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null };" ^
        "$res = Invoke-WebRequest -Uri $url -TimeoutSec 10 -UseBasicParsing;" ^
        "if ($res.StatusCode -eq 200) { $res.Content | Out-File -FilePath $out -Encoding UTF8 } else { exit 1 }"
)

echo Finished

pause