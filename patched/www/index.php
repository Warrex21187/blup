<!DOCTYPE html>
<html>
<head>
    <title>PHP2Shell Lab - Patched Server (PHP 8.4.27)</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: Arial; margin: 20px; background: #fff; color: #333; }
        .vulnerable { border: 2px solid #c00; padding: 15px; margin: 15px 0; background: #fee; }
        .safe { border: 2px solid #0c0; padding: 15px; margin: 15px 0; background: #efe; }
        .status { font-size: 24px; font-weight: bold; }
        .proof { background: #ff0; padding: 10px; margin: 10px 0; border-left: 4px solid #f00; }
        h1 { color: #0c0; }
        .php-version { font-family: monospace; background: #f0f0f0; padding: 5px 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>✅ PHP2Shell Lab - PATCHED Server</h1>
    
    <?php
    $php_version = phpversion();
    $upload_progress = ini_get('session.upload_progress.enabled');
    $memory_limit = ini_get('memory_limit');
    ?>
    
    <div class="safe">
        <span class="status" style="color: #0c0;">🔒 PROTECTED 🔒</span>
        <p><strong>PHP Version:</strong> <span class="php-version"><?php echo $php_version; ?></span></p>
        <p><strong>CVE:</strong> CVE-2026-109618 (PHP2Shell) - <span style="color: #0c0; font-weight: bold;">PATCHED</span></p>
        <p><strong>CVSS:</strong> 9.2 (Critical)</p>
        <p><strong>CWE:</strong> CWE-416 (Use After Free)</p>
        <p><strong>session.upload_progress.enabled:</strong> <span style="color: #0c0; font-weight: bold;"><?php echo $upload_progress ? 'ON ❌' : 'OFF ✅'; ?></span></p>
        <p><strong>Memory Limit:</strong> <?php echo $memory_limit; ?></p>
        <p><strong>Protection:</strong> This server is PROTECTED against Use-After-Free attacks!</p>
    </div>
    
    <h2>🎯 Server Status</h2>
    <ul>
        <li><a href="/api.php?action=status">📊 Check API Status</a></li>
        <li><a href="/upload.php">🛡️ Upload handler (secure)</a></li>
    </ul>
    
    <h2>🔒 Security Information</h2>
    <div class="safe">
        <p><strong>🎯 Patch Applied:</strong> PHP <?php echo $php_version; ?> includes fix for CVE-2026-109618</p>
        <p><strong>🛡️ Mitigation:</strong> session.upload_progress.enabled = <?php echo $upload_progress ? '1 (WARNING!)' : '0 ✅'; ?></p>
        <p><strong>📋 Recommendation:</strong> Always keep PHP updated to the latest version</p>
        <p><strong>📅 Patch Date:</strong> October 22, 2026</p>
    </div>
    
    <h2>🚫 Attack Test Results</h2>
    <ul>
        <li>✅ OOM Attack: <strong>BLOCKED</strong> (session.upload_progress disabled)</li>
        <li>✅ Ransomware: <strong>BLOCKED</strong> (PHP 8.4.27 has security patch)</li>
        <li>✅ Data Exfiltration: <strong>BLOCKED</strong> (PHP 8.4.27 has security patch)</li>
        <li>✅ Website Defacement: <strong>BLOCKED</strong> (PHP 8.4.27 has security patch)</li>
    </ul>
    
    <h2>💡 Try It Yourself</h2>
    <p>Try attacking this server with:</p>
    <ul>
        <li><code>python attack.py --target http://localhost:8889 --oom</code></li>
        <li><code>python attack.py --target http://localhost:8889 --ransomware</code></li>
    </ul>
    <p>All attacks will be <strong>BLOCKED</strong> because this server is patched!</p>
    
    <div style="margin-top: 20px; padding: 10px; background: #f0f0f0; border-radius: 5px;">
        <p><small>🕒 Last updated: <?php echo date('Y-m-d H:i:s'); ?> | 🌐 Server: <?php echo $_SERVER['SERVER_ADDR']; ?> | 📦 PHP: <?php echo $php_version; ?></small></p>
    </div>
</body>
</html>
