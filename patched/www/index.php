<!DOCTYPE html>
<html>
<head>
    <title>PHP2Shell Lab - Patched Server (PHP 8.4.27)</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: Arial; margin: 20px; background: #fff; color: #333; }
        .vulnerable { border: 2px solid #c00; padding: 10px; margin: 10px 0; }
        .safe { border: 2px solid #0c0; padding: 10px; margin: 10px 0; }
        .status { font-size: 24px; font-weight: bold; }
    </style>
</head>
<body>
    <h1>PHP2Shell Lab - Patched Server</h1>
    <div class="safe">
        <span class="status" style="color: #0c0;">PROTECTED</span>
        <p><strong>PHP Version:</strong> 8.4.27</p>
        <p><strong>CVE:</strong> CVE-2026-109618 (PHP2Shell) - PATCHED</p>
        <p><strong>CVSS:</strong> 9.2 (Critical)</p>
        <p><strong>CWE:</strong> CWE-416 (Use After Free)</p>
        <p><strong>Status:</strong> session.upload_progress.enabled = OFF</p>
        <p><strong>Memory Limit:</strong> 16M</p>
        <p><strong>Protection:</strong> This server is PROTECTED against Use-After-Free attacks!</p>
    </div>
    
    <h2>Server Status</h2>
    <ul>
        <li><a href="/api.php?action=status">Check API Status</a></li>
        <li><a href="/upload.php">Upload handler (secure)</a></li>
    </ul>
    
    <h2>Security Information</h2>
    <div class="safe">
        <p><strong>Patch Applied:</strong> PHP 8.4.27 includes fix for CVE-2026-109618</p>
        <p><strong>Mitigation:</strong> session.upload_progress.enabled = 0</p>
        <p><strong>Recommendation:</strong> Always keep PHP updated to the latest version</p>
    </div>
    
    <p><small>Last updated: <?php echo date('Y-m-d H:i:s'); ?></small></p>
    <p><small>Server: <?php echo $_SERVER['SERVER_ADDR']; ?></small></p>
</body>
</html>
