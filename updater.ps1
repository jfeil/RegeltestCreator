$app = Get-Process -Id $Args[1] -ErrorAction SilentlyContinue
Write-Output "Waiting 10 seconds to close the application..."
Start-Sleep -Seconds 10
# get Program process
Write-Output "Checking if it is closed..."
if ($app)
{
    # try gracefully first
    $app.CloseMainWindow()
    # kill after five seconds
    Start-Sleep -Seconds 5
    if (!$app.HasExited)
    {
        Write-Output "Force closing the programm..."
        $app | Stop-Process -Force
    }
}
Remove-Variable app
Write-Output "Deleting the old executable..."
Remove-Item $Args[0]
Write-Output "Moving the new executable..."
Move-Item $Args[2] $Args[0]
Write-Output "Done! Starting the closed app!"
$Args[0]