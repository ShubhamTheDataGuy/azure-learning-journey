# Install IIS feature
Install-WindowsFeature -name Web-Server -IncludeManagementTools

# Define IIS root
$path = "C:\inetpub\wwwroot"

# Create simple HTML page
$html = @"
<html>
  <head><title>Custom Script Extensions Demo</title></head>
  <body>
    <h1>We now have Internet Information services running on the machine</h1>
  </body>
</html>
"@

# Save file as default.html
Set-Content -Path "$path\default.html" -Value $html -Force