<?php
// PHP2Shell Lab - Secure Upload Handler for Patched Server
// REAL PHP 8.4.27 - PATCHED
// This endpoint blocks exploitation attempts

header('Content-Type: text/html');

$php_version = phpversion();
$upload_progress = ini_get('session.upload_progress.enabled');
$memory_limit = ini_get('memory_limit');

echo "<html><body style='font-family: Arial; margin: 20px; background: #fff; color: #333;'>";
echo "<h1>🛡️ PHP2Shell - Secure Upload Handler (PATCHED)</h1>";
echo "<p>This server is PATCHED against CVE-2026-109618</p>";
echo "<div style='background: #efe; border: 2px solid #0c0; padding: 15px; margin: 15px 0;'>";
echo "<p style='color: #0c0; font-weight: bold;'>✅ PROTECTED: PHP {$php_version}</p>";
echo "<p><strong>session.upload_progress.enabled:</strong> " . ($upload_progress ? "<span style='color: #c00;'>ON ❌</span>" : "<span style='color: #0c0;'>OFF ✅</span>") . "</p>";
echo "<p><strong>Memory Limit:</strong> {$memory_limit}</p>";
echo "<p><strong>Protection:</strong> CVE-2026-109618 is PATCHED in this version</p>";
echo "</div>";

// Log the access
file_put_contents('php://stderr', "[" . date('Y-m-d H:i:s') . "] Secure upload accessed from " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n", FILE_APPEND);

// Check if this is a POST request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    echo "<div style='background: #e8f5e9; border: 2px solid #4CAF50; padding: 15px; margin: 15px 0;'>";
    echo "<p><strong>⚠️ Upload attempt detected!</strong></p>";
    
    $content_length = $_SERVER['CONTENT_LENGTH'] ?? 0;
    echo "<p><strong>Content-Length:</strong> " . number_format($content_length) . " bytes (" . number_format($content_length / (1024*1024), 2) . " MB)</p>";
    
    // Check if upload progress is disabled (patched)
    if (!$upload_progress) {
        echo "<p style='color: #0c0; font-weight: bold;'>✅ ATTACK BLOCKED!</p>";
        echo "<p style='color: #0c0;'>session.upload_progress.enabled = OFF</p>";
        echo "<p style='color: #0c0;'>This server is PROTECTED against CVE-2026-109618!</p>";
        echo "<p style='color: #0c0;'>Even with large payloads, the vulnerability cannot be exploited.</p>";
        
        // Log the blocked attempt
        error_log("[PHP2Shell] ATTACK BLOCKED on PHP {$php_version} - session.upload_progress.enabled = 0");
        
        // Return 403 Forbidden
        http_response_code(403);
    } else {
        echo "<p style='color: #c00; font-weight: bold;'>⚠️ WARNING: session.upload_progress is enabled!</p>";
        echo "<p style='color: #c00;'>This configuration is not recommended for PHP {$php_version}</p>";
        echo "<p>Even though this is a patched version, session.upload_progress should be disabled for maximum security.</p>";
    }
    
    echo "</div>";
} else {
    echo "<div style='background: #e3f2fd; border: 2px solid #2196F3; padding: 15px; margin: 15px 0;'>";
    echo "<p>ℹ️ This server is secure. Upload attempts will be blocked.</p>";
    echo "<p><strong>PHP Version:</strong> {$php_version} (PATCHED)</p>";
    echo "<p><strong>Protection:</strong> CVE-2026-109618 is fixed in this version</p>";
    echo "</div>";
}

echo "<p><a href='/'>← Back to main page</a></p>";
echo "</body></html>";
