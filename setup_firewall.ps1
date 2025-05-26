# Run this script as administrator
$port = 8000
$ruleName = "Python Manufacturing Web App"

# Remove existing rule if it exists
Remove-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue

# Create new inbound rule
New-NetFirewallRule -DisplayName $ruleName `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort $port `
    -Action Allow `
    -Program "python.exe" `
    -Description "Allow incoming connections for Python Manufacturing Web App"

Write-Host "Firewall rule has been created successfully!"
Write-Host "Other devices on your network should now be able to connect." 