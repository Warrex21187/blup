<!DOCTYPE html>
<html>
<head>
    <title>PHP2Shell Lab - Vulnerable Server (PHP 8.4.26)</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: Arial; margin: 20px; background: #fff; color: #333; }
        .vulnerable { border: 2px solid #c00; padding: 10px; margin: 10px 0; }
        .safe { border: 2px solid #0c0; padding: 10px; margin: 10px 0; }
        .status { font-size: 24px; font-weight: bold; }
        .proof { background: #ff0; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>PHP2Shell Lab - Vulnerable Server</h1>
    <div class="vulnerable">
        <span class="status" style="color: #c00;">VULNERABLE</span>
        <p><strong>PHP Version:</strong> 8.4.26</p>
        <p><strong>CVE:</strong> CVE-2026-109618 (PHP2Shell)</p>
        <p><strong>CVSS:</strong> 9.2 (Critical)</p>
        <p><strong>CWE:</strong> CWE-416 (Use After Free)</p>
        <p><strong>Status:</strong> session.upload_progress.enabled = ON</p>
        <p><strong>Memory Limit:</strong> 16M</p>
        <p><strong>Warning:</strong> This server is VULNERABLE to Use-After-Free attacks via OOM!</p>
    </div>
    
    <h2>Attack Demonstration</h2>
    <ul>
        <li><a href="/api.php?action=status">Check API Status</a></li>
        <li><a href="/upload.php">Trigger OOM (CVE-2026-109618)</a></li>
    </ul>
    
    <h2>Proof Files</h2>
    <?php
    $proof_files = [
        'proof.php' => 'Generic proof of exploitation',
        'proof_ransomware.php' => 'Ransomware attack proof',
        'proof_deface.html' => 'Website defacement proof',
        'proof_data_leak.csv' => 'Data exfiltration proof',
        'DONNEES_RH_EXFILTREES.csv' => 'HR data file'
    ];
    
    foreach ($proof_files as $file => $desc) {
        if (file_exists($file)) {
            echo "<li class='proof'><a href='$file'>$file</a> - $desc (EXISTS)</li>";
        } else {
            echo "<li>$file - $desc (not yet created)</li>";
        }
    }
    ?>
    
    <p><small>Last updated: <?php echo date('Y-m-d H:i:s'); ?></small></p>
    <p><small>Server: <?php echo $_SERVER['SERVER_ADDR']; ?></small></p>
</body>
</html>
