# Start Local Web Server
# Run this script to serve your web UI

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Web Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
}
elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
}
elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
}

if ($pythonCmd) {
    Write-Host "✅ Python found!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Starting web server on http://localhost:8000" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🌐 Open your browser and go to:" -ForegroundColor Cyan
    Write-Host "   http://localhost:8000" -ForegroundColor White
    Write-Host ""
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
    Write-Host ""
    
    # Start Python HTTP server
    & $pythonCmd -m http.server 8000
}
else {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Use Live Server extension in VS Code" -ForegroundColor Yellow
    Write-Host "Or install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
}
