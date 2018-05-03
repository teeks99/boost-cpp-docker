
FROM microsoft/windowsservercore:1709

RUN @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

# wait for vs_installer.exe, vs_installerservice.exe
# or vs_installershell.exe because choco doesn't
RUN powershell -NoProfile -InputFormat None -Command \
    choco install python -y --params "/InstallDir:C:\tools\python3"; \
    choco install python2 -y --params "/InstallDir:C:\tools\python2"; \
    choco install visualcpp-build-tools \
        --version 15.0.26228.20170424 -y; \
    Write-Host 'Waiting for Visual C++ Build Tools to finish'; \
    Wait-Process -Name vs_installer

CMD powershell -ExecutionPolicy Bypass
