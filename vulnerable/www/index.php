<!DOCTYPE html>
<html>
<head>
    <title>PHP2Shell Lab - Vulnerable Server (PHP 8.4.26)</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: Arial; margin: 20px; background: #fff; color: #333; }
        .vulnerable { border: 2px solid #c00; padding: 15px; margin: 15px 0; background: #fee; }
        .safe { border: 2px solid #0c0; padding: 15px; margin: 15px 0; background: #efe; }
        .status { font-size: 24px; font-weight: bold; }
        .proof { background: #ff0; padding: 10px; margin: 10px 0; border-left: 4px solid #f00; }
        h1 { color: #c00; }
        .php-version { font-family: monospace; background: #f0f0f0; padding: 5px 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>⚠️ PHP2Shell Lab - VULNERABLE Server</h1>
    
    <?php
    $php_version = phpversion();
    $upload_progress = ini_get('session.upload_progress.enabled');
    $memory_limit = ini_get('memory_limit');
    ?>
    
    <div class="vulnerable">
        <span class="status" style="color: #c00;">🚨 VULNERABLE 🚨</span>
        <p><strong>PHP Version:</strong> <span class="php-version"><?php echo $php_version; ?></span></p>
        <p><strong>CVE:</strong> CVE-2026-109618 (PHP2Shell)</p>
        <p><strong>CVSS:</strong> 9.2 (Critical)</p>
        <p><strong>CWE:</strong> CWE-416 (Use After Free)</p>
        <p><strong>session.upload_progress.enabled:</strong> <span style="color: #c00; font-weight: bold;"><?php echo $upload_progress ? 'ON ❌' : 'OFF ✅'; ?></span></p>
        <p><strong>Memory Limit:</strong> <?php echo $memory_limit; ?></p>
        <p><strong>Warning:</strong> This server is VULNERABLE to Use-After-Free attacks via OOM!</p>
    </div>
    
    <h2>🎯 Attack Demonstration</h2>
    <ul>
        <li><a href="/api.php?action=status">📊 Check API Status</a></li>
        <li><a href="/upload.php">💥 Trigger OOM (CVE-2026-109618)</a></li>
    </ul>
    
    <h2>📋 Available Attack Commands</h2>
    <ul>
        <li><code>python attack.py --oom</code> - Trigger OOM vulnerability</li>
        <li><code>python attack.py --ransomware</code> - Deploy ransomware</li>
        <li><code>python attack.py --steal</code> - Exfiltrate data</li>
        <li><code>python attack.py --deface</code> - Deface website</li>
        <li><code>python attack.py --restore</code> - Restore server</li>
        <li><code>python attack.py --compare</code> - Compare with patched server</li>
    </ul>
    
    <h2>🔍 Proof Files</h2>
    <?php
    $proof_files = [
        'proof.php' => 'Generic proof of exploitation',
        'proof_ransomware.php' => 'Ransomware attack proof',
        'proof_deface.html' => 'Website defacement proof',
        'proof_data_leak.csv' => 'Data exfiltration proof',
        'DONNEES_RH_EXFILTREES.csv' => 'HR data file'
    ];
    
    $has_proofs = false;
    foreach ($proof_files as $file => $desc) {
        if (file_exists($file)) {
            $has_proofs = true;
            echo "<li class='proof'><a href='$file'>$file</a> - $desc (✅ EXISTS)</li>";
        } else {
            echo "<li>$file - $desc (❌ not yet created)</li>";
        }
    }
    
    if ($has_proofs) {
        echo "<li class='proof' style='margin-top: 10px;'><strong>⚠️ This server has been COMPROMISED!</strong></li>";
    }
    ?>
    
    <div style="margin-top: 20px; padding: 10px; background: #f0f0f0; border-radius: 5px;">
        <p><small>🕒 Last updated: <?php echo date('Y-m-d H:i:s'); ?> | 🌐 Server: <?php echo $_SERVER['SERVER_ADDR']; ?> | 📦 PHP: <?php echo $php_version; ?></small></p>
    </div>
</body>
</html>
