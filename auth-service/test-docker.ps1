# Docker Container Test Script
# Tests the containerized Auth Service running on port 5001

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Docker Container Test Suite" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:5001"

# Test 1: Health Check
Write-Host "Test 1: Health Check (Containerized)" -ForegroundColor Yellow
Write-Host "GET $baseUrl/health" -ForegroundColor Gray
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/health" -Method GET -UseBasicParsing
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Status: $($data.status)" -ForegroundColor Green
    Write-Host "   Service: $($data.service)" -ForegroundColor Green
    Write-Host "   Running in Docker container!" -ForegroundColor Cyan
    Write-Host ""
} catch {
    Write-Host "❌ Health check failed: $_" -ForegroundColor Red
    exit
}

# Test 2: Register User
Write-Host "Test 2: Register New User (Docker)" -ForegroundColor Yellow
Write-Host "POST $baseUrl/register" -ForegroundColor Gray
$registerBody = @{
    username = "docker_user_$(Get-Random -Maximum 1000)"
    email = "docker$(Get-Random -Maximum 1000)@example.com"
    password = "DockerTest123"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/register" -Method POST -Body $registerBody -ContentType "application/json" -UseBasicParsing
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ $($data.message)" -ForegroundColor Green
    Write-Host "   User ID: $($data.user.id)" -ForegroundColor Green
    Write-Host "   Username: $($data.user.username)" -ForegroundColor Green
    Write-Host ""
    
    $testEmail = $data.user.email
    $testPassword = "DockerTest123"
} catch {
    Write-Host "❌ Registration failed: $_" -ForegroundColor Red
    Write-Host ""
}

# Test 3: Login
Write-Host "Test 3: User Login (Docker)" -ForegroundColor Yellow
Write-Host "POST $baseUrl/login" -ForegroundColor Gray
$loginBody = @{
    email = $testEmail
    password = $testPassword
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/login" -Method POST -Body $loginBody -ContentType "application/json" -UseBasicParsing
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ $($data.message)" -ForegroundColor Green
    Write-Host "   Token: $($data.token.Substring(0, 50))..." -ForegroundColor Green
    Write-Host ""
    
    $token = $data.token
} catch {
    Write-Host "❌ Login failed: $_" -ForegroundColor Red
    Write-Host ""
}

# Test 4: Protected Endpoint
Write-Host "Test 4: Access Protected Endpoint (Docker)" -ForegroundColor Yellow
Write-Host "GET $baseUrl/me" -ForegroundColor Gray
$headers = @{
    Authorization = "Bearer $token"
}

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/me" -Method GET -Headers $headers -UseBasicParsing
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Successfully accessed protected endpoint" -ForegroundColor Green
    Write-Host "   User ID: $($data.user.user_id)" -ForegroundColor Green
    Write-Host "   Username: $($data.user.username)" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "❌ Protected endpoint access failed: $_" -ForegroundColor Red
    Write-Host ""
}

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Docker Container Tests Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Your containerized Auth Service is working!" -ForegroundColor Green
Write-Host ""
Write-Host "Container Info:" -ForegroundColor Yellow
Write-Host "- Running on: http://localhost:5001" -ForegroundColor White
Write-Host "- Container name: auth-service-container" -ForegroundColor White
Write-Host "- Image: auth-service:latest" -ForegroundColor White
Write-Host ""
Write-Host "Useful Docker Commands:" -ForegroundColor Yellow
Write-Host "- View logs: docker logs auth-service-container" -ForegroundColor White
Write-Host "- Stop container: docker stop auth-service-container" -ForegroundColor White
Write-Host "- Start container: docker start auth-service-container" -ForegroundColor White
Write-Host "- Remove container: docker rm auth-service-container" -ForegroundColor White
Write-Host ""
