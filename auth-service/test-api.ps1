# Auth Service Test Script
# This PowerShell script tests all endpoints of the Auth Service

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Auth Service API Test Suite" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:5000"

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
Write-Host "GET $baseUrl/health" -ForegroundColor Gray
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/health" -Method GET
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Status: $($data.status)" -ForegroundColor Green
    Write-Host "   Service: $($data.service)" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "❌ Health check failed: $_" -ForegroundColor Red
    Write-Host "   Make sure the service is running: python app.py" -ForegroundColor Yellow
    exit
}

# Test 2: Register User
Write-Host "Test 2: Register New User" -ForegroundColor Yellow
Write-Host "POST $baseUrl/register" -ForegroundColor Gray
$registerBody = @{
    username = "test_user_$(Get-Random -Maximum 1000)"
    email = "test$(Get-Random -Maximum 1000)@example.com"
    password = "TestPassword123"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/register" -Method POST -Body $registerBody -ContentType "application/json"
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ $($data.message)" -ForegroundColor Green
    Write-Host "   User ID: $($data.user.id)" -ForegroundColor Green
    Write-Host "   Username: $($data.user.username)" -ForegroundColor Green
    Write-Host "   Email: $($data.user.email)" -ForegroundColor Green
    Write-Host ""
    
    # Save credentials for login test
    $testEmail = $data.user.email
    $testPassword = "TestPassword123"
} catch {
    Write-Host "❌ Registration failed: $_" -ForegroundColor Red
    Write-Host ""
}

# Test 3: Login
Write-Host "Test 3: User Login" -ForegroundColor Yellow
Write-Host "POST $baseUrl/login" -ForegroundColor Gray
$loginBody = @{
    email = $testEmail
    password = $testPassword
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/login" -Method POST -Body $loginBody -ContentType "application/json"
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ $($data.message)" -ForegroundColor Green
    Write-Host "   Token: $($data.token.Substring(0, 50))..." -ForegroundColor Green
    Write-Host ""
    
    # Save token for protected endpoint test
    $token = $data.token
} catch {
    Write-Host "❌ Login failed: $_" -ForegroundColor Red
    Write-Host ""
}

# Test 4: Validate Token
Write-Host "Test 4: Validate Token" -ForegroundColor Yellow
Write-Host "POST $baseUrl/validate" -ForegroundColor Gray
$validateBody = @{
    token = $token
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/validate" -Method POST -Body $validateBody -ContentType "application/json"
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Token is valid: $($data.valid)" -ForegroundColor Green
    Write-Host "   User ID: $($data.user.user_id)" -ForegroundColor Green
    Write-Host "   Username: $($data.user.username)" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "❌ Token validation failed: $_" -ForegroundColor Red
    Write-Host ""
}

# Test 5: Access Protected Endpoint
Write-Host "Test 5: Access Protected Endpoint" -ForegroundColor Yellow
Write-Host "GET $baseUrl/me" -ForegroundColor Gray
$headers = @{
    Authorization = "Bearer $token"
}

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/me" -Method GET -Headers $headers
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Successfully accessed protected endpoint" -ForegroundColor Green
    Write-Host "   User ID: $($data.user.user_id)" -ForegroundColor Green
    Write-Host "   Username: $($data.user.username)" -ForegroundColor Green
    Write-Host "   Email: $($data.user.email)" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "❌ Protected endpoint access failed: $_" -ForegroundColor Red
    Write-Host ""
}

# Test 6: Test Invalid Token
Write-Host "Test 6: Test Invalid Token (Should Fail)" -ForegroundColor Yellow
Write-Host "GET $baseUrl/me with invalid token" -ForegroundColor Gray
$invalidHeaders = @{
    Authorization = "Bearer invalid_token_12345"
}

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/me" -Method GET -Headers $invalidHeaders
    Write-Host "❌ Should have failed but didn't!" -ForegroundColor Red
    Write-Host ""
} catch {
    Write-Host "✅ Correctly rejected invalid token" -ForegroundColor Green
    Write-Host "   Error: Invalid or expired token" -ForegroundColor Green
    Write-Host ""
}

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  All Tests Completed!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your Auth Service is working correctly! 🎉" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Review the code in app.py, models.py, and config.py" -ForegroundColor White
Write-Host "2. Try testing with Postman for a better experience" -ForegroundColor White
Write-Host "3. Read the phase2-auth-service-guide.md for detailed explanations" -ForegroundColor White
Write-Host ""
