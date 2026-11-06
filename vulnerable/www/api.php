<?php
// PHP2Shell Lab - API Endpoint for CVE-2026-109618 Demo
// REAL PHP 8.4.26 - VULNERABLE

header('Content-Type: application/json');

// Get REAL PHP version
$php_version = phpversion();
$is_vulnerable = true;
$upload_progress_enabled = (ini_get('session.upload_progress.enabled') === '1' || ini_get('session.upload_progress.enabled') === true);

$action = $_REQUEST['action'] ?? '';

switch ($action) {
    case 'status':
        $response = [
            'php_version' => $php_version,
            'is_vulnerable' => $is_vulnerable,
            'upload_progress_enabled' => $upload_progress_enabled,
            'memory_limit' => ini_get('memory_limit'),
            'cve' => 'CVE-2026-109618',
            'cvss' => 9.2,
            'cwe' => 'CWE-416',
            'status' => 'VULNERABLE',
            'description' => 'Use-After-Free via OOM in Zend Engine (session.upload_progress)',
            'message' => 'This server is VULNERABLE to PHP2Shell (CVE-2026-109618)',
            'publication_date' => '2026-10-21',
            'fixed_in' => 'PHP 8.4.27',
            'server_addr' => $_SERVER['SERVER_ADDR'] ?? 'unknown',
            'server_software' => $_SERVER['SERVER_SOFTWARE'] ?? 'unknown'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'ransomware':
        // Create ransomware proof file
        $ransomware_content = <<<HTML
<!DOCTYPE html>
<html>
<head>
    <title>HACKED - PHP2Shell</title>
    <style>
        body { background: #000; color: #f00; font-family: Arial; text-align: center; padding: 50px; }
        h1 { font-size: 48px; }
        .ransom { background: #111; padding: 20px; margin: 20px auto; max-width: 600px; border: 2px solid #f00; }
    </style>
</head>
<body>
    <h1>*** HACKED BY PHP2Shell ***</h1>
    <div class="ransom">
        <h2>YOUR FILES ARE ENCRYPTED</h2>
        <p>842 company files have been encrypted (HR, Finance, Contracts)</p>
        <p><strong>Ransom: 50,000 EUR</strong></p>
        <p>Send Bitcoin to: 1PHP2ShellXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX</p>
        <p>You have 72 hours before data is permanently destroyed</p>
    </div>
    <p style="font-size: 12px; color: #666;">
        Exploited via CVE-2026-109618 (Use-After-Free in PHP {$php_version})
    </p>
</body>
</html>
HTML;
        
        // Backup original index
        if (!file_exists('/var/www/html/index.php.bak')) {
            copy('/var/www/html/index.php', '/var/www/html/index.php.bak');
        }
        
        file_put_contents('/var/www/html/proof_ransomware.php', $ransomware_content);
        file_put_contents('/var/www/html/index.php', $ransomware_content);
        
        // Create marker file
        file_put_contents('/var/www/html/.h4ck3d', 'PHP2Shell was here - ' . date('Y-m-d H:i:s') . "\nPHP Version: {$php_version}\n");
        
        // Log the attack
        error_log("[PHP2Shell] Ransomware deployed via CVE-2026-109618 on PHP {$php_version}");
        
        $response = [
            'success' => true,
            'message' => 'Ransomware deployed successfully via CVE-2026-109618',
            'php_version' => $php_version,
            'files_encrypted' => 842,
            'ransom_amount' => '50,000 EUR',
            'proof_file' => '/proof_ransomware.php',
            'exploit' => 'CVE-2026-109618 (Use-After-Free via OOM)'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'steal':
        // Create fake HR data file - simulating data exfiltration
        $csv_data = "ID,Name,SSN,Email,Salary,Department\n";
        for ($i = 1; $i <= 100; $i++) {
            $ssn = str_pad(rand(100000000, 999999999), 9, '0', STR_PAD_LEFT);
            $csv_data .= "$i,Employee $i,$ssn,employee$i@company.com," . rand(30000, 150000) . ",HR\n";
        }
        
        file_put_contents('/var/www/html/DONNEES_RH_EXFILTREES.csv', $csv_data);
        file_put_contents('/var/www/html/proof_data_leak.csv', $csv_data);
        
        // Log the attack
        error_log("[PHP2Shell] Data exfiltration via CVE-2026-109618 on PHP {$php_version}");
        
        $response = [
            'success' => true,
            'message' => 'Data exfiltration successful via CVE-2026-109618',
            'php_version' => $php_version,
            'records_stolen' => 12482,
            'file_created' => '/DONNEES_RH_EXFILTREES.csv',
            'data_types' => ['SSN', 'Addresses', 'Salaries', 'Performance Reviews'],
            'exploit' => 'CVE-2026-109618 (Use-After-Free via OOM)'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'deface':
        // Create defacement page
        $deface_content = <<<HTML
<!DOCTYPE html>
<html>
<head>
    <title>HACKED - PHP2Shell</title>
    <style>
        body { background: #000; color: #0f0; font-family: Courier; text-align: center; padding: 50px; }
        h1 { font-size: 64px; text-shadow: 0 0 10px #0f0; }
        .details { background: #111; padding: 20px; margin: 20px auto; max-width: 800px; border: 2px solid #0f0; }
    </style>
</head>
<body>
    <h1>HACKED BY PHP2Shell</h1>
    <div class="details">
        <p style="font-size: 24px;">This website has been compromised via CVE-2026-109618</p>
        <p style="font-size: 18px;">Use-After-Free vulnerability in PHP Zend Engine</p>
        <p style="font-size: 16px;">PHP Version: {$php_version}</p>
        <p style="font-size: 16px;">session.upload_progress.enabled: " . ($upload_progress_enabled ? 'ON (VULNERABLE)' : 'OFF') . "</p>
    </div>
</body>
</html>
HTML;
        
        file_put_contents('/var/www/html/proof_deface.html', $deface_content);
        file_put_contents('/var/www/html/index.php', $deface_content);
        
        // Log the attack
        error_log("[PHP2Shell] Website defaced via CVE-2026-109618 on PHP {$php_version}");
        
        $response = [
            'success' => true,
            'message' => 'Website defaced successfully via CVE-2026-109618',
            'php_version' => $php_version,
            'proof_file' => '/proof_deface.html',
            'exploit' => 'CVE-2026-109618 (Use-After-Free via OOM)'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'proof':
        // Create generic proof file
        $proof_content = <<<PHP
<?php
// Proof of exploitation for CVE-2026-109618
// This file was created via Use-After-Free vulnerability in PHP Zend Engine
// Exploit: Use-After-Free via OOM (Out-of-Memory) in session.upload_progress

echo "<html><body style='background:black;color:white;font-family:monospace;padding:50px;text-align:center;'>";
echo "<h1>PROOF OF EXPLOITATION</h1>";
echo "<p>CVE-2026-109618 (PHP2Shell)</p>";
echo "<p>Use-After-Free via OOM in Zend Engine</p>";
echo "<p>PHP Version: " . phpversion() . "</p>";
echo "<p>Server: " . \$_SERVER['SERVER_ADDR'] . "</p>";
echo "<p>Time: " . date('Y-m-d H:i:s') . "</p>";
echo "<p>session.upload_progress.enabled: " . (ini_get('session.upload_progress.enabled') ? 'ON' : 'OFF') . "</p>";
echo "</body></html>";
?>
PHP;
        
        file_put_contents('/var/www/html/proof.php', $proof_content);
        
        // Log the attack
        error_log("[PHP2Shell] Proof file created via CVE-2026-109618 on PHP {$php_version}");
        
        $response = [
            'success' => true,
            'message' => 'Proof file created via CVE-2026-109618',
            'php_version' => $php_version,
            'proof_file' => '/proof.php',
            'exploit' => 'CVE-2026-109618 (Use-After-Free via OOM)'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'restore':
        // Restore original index.php
        if (file_exists('/var/www/html/index.php.bak')) {
            copy('/var/www/html/index.php.bak', '/var/www/html/index.php');
            unlink('/var/www/html/index.php.bak');
        }
        
        // Remove proof files
        $proof_files = ['proof.php', 'proof_ransomware.php', 'proof_deface.html', 'proof_data_leak.csv', 'DONNEES_RH_EXFILTREES.csv', '.h4ck3d'];
        foreach ($proof_files as $file) {
            if (file_exists("/var/www/html/{$file}")) {
                unlink("/var/www/html/{$file}");
            }
        }
        
        // Log the restore
        error_log("[PHP2Shell] Server restored to original state");
        
        $response = [
            'success' => true,
            'message' => 'Server restored to original state',
            'php_version' => $php_version
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'oom':
        // Simulate OOM trigger - this would be triggered by upload.php
        $response = [
            'success' => true,
            'message' => 'OOM condition can be triggered via multipart upload to /upload.php',
            'php_version' => $php_version,
            'memory_limit' => ini_get('memory_limit'),
            'upload_progress_enabled' => $upload_progress_enabled,
            'instructions' => 'Send POST request with Content-Length > 16MB to /upload.php to trigger OOM',
            'exploit' => 'CVE-2026-109618 (Use-After-Free via OOM in session.upload_progress)'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    default:
        $response = [
            'error' => 'Unknown action',
            'available_actions' => ['status', 'ransomware', 'steal', 'deface', 'proof', 'restore', 'oom'],
            'php_version' => $php_version,
            'is_vulnerable' => $is_vulnerable
        ];
        http_response_code(400);
        echo json_encode($response, JSON_PRETTY_PRINT);
}
