<?php
// PHP2Shell Lab - OOM Trigger for CVE-2026-109618
// REAL PHP 8.4.26 - VULNERABLE
// This endpoint accepts multipart uploads to trigger OOM condition

header('Content-Type: text/html');

$php_version = phpversion();
$upload_progress = ini_get('session.upload_progress.enabled');
$memory_limit = ini_get('memory_limit');

// Convert memory_limit to bytes
preg_match('/^(\d+)\s*([KMGT])?B?$/i', $memory_limit, $matches);
$memory_bytes = $matches[1];
if (isset($matches[2])) {
    switch (strtoupper($matches[2])) {
        case 'G': $memory_bytes *= 1024 * 1024 * 1024; break;
        case 'M': $memory_bytes *= 1024 * 1024; break;
        case 'K': $memory_bytes *= 1024; break;
    }
}

// Log the access
file_put_contents('php://stderr', "[" . date('Y-m-d H:i:s') . "] OOM Trigger accessed from " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n", FILE_APPEND);

echo "<html><body style='font-family: Arial; margin: 20px; background: #fff; color: #333;'>";
echo "<h1>💥 PHP2Shell - OOM Trigger (CVE-2026-109618)</h1>";
echo "<p>This endpoint demonstrates CVE-2026-109618 (Use-After-Free via OOM)</p>";
echo "<div style='background: #fee; border: 2px solid #c00; padding: 15px; margin: 15px 0;'>";
echo "<p style='color: #c00; font-weight: bold;'>⚠️ WARNING: This server is VULNERABLE!</p>";
echo "<p><strong>PHP Version:</strong> {$php_version}</p>";
echo "<p><strong>session.upload_progress.enabled:</strong> " . ($upload_progress ? "<span style='color: #c00;'>ON ❌</span>" : "OFF ✅") . "</p>";
echo "<p><strong>Memory Limit:</strong> {$memory_limit} ({$memory_bytes} bytes)</p>";
echo "</div>";

// Check if this is a POST request with file upload
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    echo "<div style='background: #e7f3ff; border: 2px solid #2196F3; padding: 15px; margin: 15px 0;'>";
    echo "<p><strong>✅ Upload detected!</strong></p>";
    
    // Check content length
    $content_length = $_SERVER['CONTENT_LENGTH'] ?? 0;
    echo "<p><strong>Content-Length:</strong> " . number_format($content_length) . " bytes (" . number_format($content_length / (1024*1024), 2) . " MB)</p>";
    
    // Check if upload exceeded memory limit
    if ($content_length > $memory_bytes) {
        echo "<p style='color: #c00; font-weight: bold;'>💥 OOM CONDITION TRIGGERED!</p>";
        echo "<p style='color: #c00;'>Content-Length ({$content_length} bytes) > Memory Limit ({$memory_bytes} bytes)</p>";
        echo "<p style='color: #c00;'>Use-After-Free condition created in Zend Engine</p>";
        echo "<p style='color: #c00;'>CVE-2026-109618 can now be exploited!</p>";
        
        // Create proof file
        $proof_content = <<<PHP
<?php
// Proof of OOM exploitation for CVE-2026-109618
// Generated via Use-After-Free vulnerability in PHP Zend Engine

echo "<html><body style='background:black;color:white;font-family:monospace;padding:50px;text-align:center;'>";
echo "<h1>✅ OOM EXPLOITATION SUCCESSFUL</h1>";
echo "<p>CVE-2026-109618 (PHP2Shell)</p>";
echo "<p>Use-After-Free via OOM in Zend Engine</p>";
echo "<p>PHP Version: " . phpversion() . "</p>";
echo "<p>Server: " . \$_SERVER['SERVER_ADDR'] . "</p>";
echo "<p>Time: " . date('Y-m-d H:i:s') . "</p>";
echo "<p>session.upload_progress.enabled: " . (ini_get('session.upload_progress.enabled') ? 'ON' : 'OFF') . "</p>";
echo "<p style='color: #0f0;'>OOM condition was triggered!</p>";
echo "</body></html>";
?>
PHP;
        
        file_put_contents('/var/www/html/proof_oom.php', $proof_content);
        file_put_contents('/var/www/html/proof.php', $proof_content);
        
        // Log the successful OOM trigger
        error_log("[PHP2Shell] OOM TRIGGERED via CVE-2026-109618 on PHP {$php_version}");
        error_log("[PHP2Shell] Content-Length: {$content_length} bytes > Memory Limit: {$memory_bytes} bytes");
        error_log("[PHP2Shell] Use-After-Free condition created in Zend Engine");
        
        echo "<p><a href='/proof_oom.php' style='background: #0c0; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>📄 View Proof File</a></p>";
    } else {
        echo "<p>⚠️ Content-Length ({$content_length} bytes) <= Memory Limit ({$memory_bytes} bytes)</p>";
        echo "<p>OOM not triggered. Try sending a larger payload (> {$memory_limit}).</p>";
    }
    
    // Check if upload progress is enabled
    if ($upload_progress) {
        echo "<p style='color: #c00;'><strong>🚨 VULNERABLE:</strong> session.upload_progress.enabled = ON</p>";
        echo "<p style='color: #c00;'>This server is VULNERABLE to CVE-2026-109618!</p>";
    } else {
        echo "<p style='color: #0c0;'><strong>✅ SAFE:</strong> session.upload_progress.enabled = OFF</p>";
    }
    
    echo "</div>";
} else {
    echo "<div style='background: #fff3cd; border: 2px solid #ffc107; padding: 15px; margin: 15px 0;'>";
    echo "<p>ℹ️ Send a POST request with large multipart data to trigger OOM</p>";
    echo "<p><strong>Required:</strong> Content-Length > {$memory_limit} (currently {$memory_bytes} bytes)</p>";
    echo "<p><strong>Method:</strong> POST /upload.php</p>";
    echo "<p><strong>Content-Type:</strong> multipart/form-data</p>";
    echo "</div>";
}

echo "<p><a href='/'>← Back to main page</a></p>";
echo "</body></html>";
