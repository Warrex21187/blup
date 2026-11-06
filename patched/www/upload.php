<?php
// PHP2Shell Lab - Secure Upload Handler for Patched Server
// This endpoint blocks exploitation attempts

header('Content-Type: text/html');

echo "<html><body style='font-family: Arial; margin: 20px;'>";
echo "<h1>PHP2Shell - Secure Upload Handler</h1>";
echo "<p>This server is PATCHED against CVE-2026-109618</p>";

// Log the access
file_put_contents('php://stderr', "[" . date('Y-m-d H:i:s') . "] Secure upload accessed from " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n", FILE_APPEND);

// Check if this is a POST request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    echo "<p><strong>Upload attempt detected!</strong></p>";
    
    // Check if upload progress is disabled (patched)
    if (!ini_get('session.upload_progress.enabled')) {
        echo "<p style='color: green;'><strong>PROTECTED:</strong> session.upload_progress.enabled = OFF</p>";
        echo "<p style='color: green;'>This server is PROTECTED against CVE-2026-109618!</p>";
        echo "<p style='color: green;'>Attack BLOCKED!</p>";
        
        // Log the blocked attempt
        file_put_contents('php://stderr', "[" . date('Y-m-d H:i:s') . "] ATTACK BLOCKED from " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n", FILE_APPEND);
        
        // Return 403 Forbidden
        http_response_code(403);
    } else {
        echo "<p style='color: red;'><strong>WARNING:</strong> session.upload_progress is enabled!</p>";
    }
} else {
    echo "<p>This server is secure. Upload attempts will be blocked.</p>";
}

echo "<p><a href='/'>Back to main page</a></p>";
echo "</body></html>";
