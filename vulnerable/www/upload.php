<?php
// PHP2Shell Lab - OOM Trigger for CVE-2026-109618
// This endpoint accepts multipart uploads to trigger OOM condition

header('Content-Type: text/html');

echo "<html><body style='font-family: Arial; margin: 20px;'>";
echo "<h1>PHP2Shell - OOM Trigger</h1>";
echo "<p>This endpoint demonstrates CVE-2026-109618 (Use-After-Free via OOM)</p>";
echo "<p><strong>Warning:</strong> Uploading large files (>16MB) will trigger OOM condition</p>";

// Log the access
file_put_contents('php://stderr', "[" . date('Y-m-d H:i:s') . "] OOM Trigger accessed from " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n", FILE_APPEND);

// Check if this is a POST request with file upload
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    echo "<p><strong>Upload detected!</strong></p>";
    
    // Check content length
    $content_length = $_SERVER['CONTENT_LENGTH'] ?? 0;
    echo "<p>Content-Length: " . number_format($content_length / (1024*1024), 2) . " MB</p>";
    
    // Check if upload progress is enabled
    if (ini_get('session.upload_progress.enabled')) {
        echo "<p style='color: red;'><strong>VULNERABLE:</strong> session.upload_progress.enabled = ON</p>";
        echo "<p style='color: red;'>This server is VULNERABLE to CVE-2026-109618!</p>";
    } else {
        echo "<p style='color: green;'><strong>SAFE:</strong> session.upload_progress.enabled = OFF</p>";
    }
    
    echo "<p>Memory Limit: " . ini_get('memory_limit') . "</p>";
    
    // If content is large enough, it would trigger OOM
    if ($content_length > 16 * 1024 * 1024) {
        echo "<p style='color: red;'><strong>OOM TRIGGERED:</strong> Content exceeds memory limit!</p>";
        echo "<p style='color: red;'>Use-After-Free condition created in Zend Engine</p>";
        
        // Create proof file
        file_put_contents('/var/www/html/proof.php', '<?php echo "OOM Triggered - CVE-2026-109618"; ?>');
        
        echo "<p><a href='/proof.php'>View Proof File</a></p>";
    }
} else {
    echo "<p>Send a POST request with large multipart data to trigger OOM</p>";
}

echo "<p><a href='/'>Back to main page</a></p>";
echo "</body></html>";
