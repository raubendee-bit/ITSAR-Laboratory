# If you get an execution policy error, run this first:
# Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser -Force

Write-Host "Starting all microservices..." -ForegroundColor Cyan
Write-Host ""

Start-Job -Name "StudentService"    -ScriptBlock { param($r) Set-Location "$r\services\student-service";    python app.py } -ArgumentList $PSScriptRoot
Start-Job -Name "CourseService"     -ScriptBlock { param($r) Set-Location "$r\services\course-service";     python app.py } -ArgumentList $PSScriptRoot
Start-Job -Name "EnrollmentService" -ScriptBlock { param($r) Set-Location "$r\services\enrollment-service"; python app.py } -ArgumentList $PSScriptRoot
Start-Job -Name "Frontend"          -ScriptBlock { param($r) Set-Location "$r\frontend";                    python -m http.server 5500 } -ArgumentList $PSScriptRoot

Start-Sleep -Seconds 2

Write-Host "All services started!" -ForegroundColor Green
Write-Host ""
Write-Host "  Frontend           -> http://localhost:5500" -ForegroundColor Magenta
Write-Host "  Student Service    -> http://localhost:8001" -ForegroundColor Blue
Write-Host "  Course Service     -> http://localhost:8002" -ForegroundColor Yellow
Write-Host "  Enrollment Service -> http://localhost:8003" -ForegroundColor Green
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Gray
Write-Host "  Get-Job                  -> check status of all services" -ForegroundColor Gray
Write-Host "  Receive-Job -Name <name> -> view logs of a service"       -ForegroundColor Gray
Write-Host "  Get-Job | Stop-Job       -> stop all services"            -ForegroundColor Gray
Write-Host "  Get-Job | Remove-Job     -> clean up all jobs"            -ForegroundColor Gray
