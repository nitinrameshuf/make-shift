# Function to close any running 7-Zip processes
function Close-7ZipProcesses {
    $processes = Get-Process -Name "7zFM", "7zG", "7z", "7zFM64", "7zG64" -ErrorAction SilentlyContinue
    if ($processes) {
        Write-Output "Closing running 7-Zip processes..."
        $processes | Stop-Process -Force
    } else {
        Write-Output "No running 7-Zip processes found."
    }
}
