<?php
// PHP2Shell Lab - API Endpoint for CVE-2026-109618 Demo
// Simulates vulnerable PHP 8.4.26 behavior

header('Content-Type: application/json');

// Simulate PHP 8.4.26 version
$php_version = '8.4.26';
$is_vulnerable = true;
$upload_progress_enabled = true;

$action = $_REQUEST['action'] ?? '';

switch ($action) {
    case 'status':
        $response = [
            'php_version' => $php_version,
            'is_vulnerable' => $is_vulnerable,
            'upload_progress_enabled' => $upload_progress_enabled,
            'cve' => 'CVE-2026-109618',
            'cvss' => '9.2',
            'cwe' => 'CWE-416',
            'description' => 'Use-After-Free via OOM in Zend Engine',
            'status' => 'VULNERABLE',
            'message' => 'This server is VULNERABLE to PHP2Shell (CVE-2026-109618)'
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
</body>
</html>
HTML;
        
        file_put_contents('/var/www/html/proof_ransomware.php', $ransomware_content);
        file_put_contents('/var/www/html/index.php', $ransomware_content);
        
        // Create marker file
        file_put_contents('/var/www/html/.h4ck3d', 'PHP2Shell was here - ' . date('Y-m-d H:i:s'));
        
        $response = [
            'success' => true,
            'message' => 'Ransomware deployed successfully',
            'files_encrypted' => 842,
            'ransom_amount' => '50,000 EUR',
            'proof_file' => '/proof_ransomware.php'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'steal':
        // Create fake HR data file
        $csv_data = "ID,Name,SSN,Email,Salary,Department\n";
        for ($i = 1; $i <= 100; $i++) {
            $csv_data .= "$i,Employee $i," . str_pad(rand(100000000, 999999999), 9, '0', STR_PAD_LEFT) . ",employee$i@company.com," . rand(30000, 150000) . ",HR\n";
        }
        
        file_put_contents('/var/www/html/DONNEES_RH_EXFILTREES.csv', $csv_data);
        file_put_contents('/var/www/html/proof_data_leak.csv', $csv_data);
        
        $response = [
            'success' => true,
            'message' => 'Data exfiltration successful',
            'records_stolen' => 12482,
            'file_created' => '/DONNEES_RH_EXFILTREES.csv',
            'data_types' => ['SSN', 'Addresses', 'Salaries', 'Performance Reviews']
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
    </style>
</head>
<body>
    <h1>HACKED BY PHP2Shell</h1>
    <p style="font-size: 24px;">This website has been compromised via CVE-2026-109618</p>
    <p style="font-size: 18px;">Use-After-Free vulnerability in PHP Zend Engine</p>
</body>
</html>
HTML;
        
        file_put_contents('/var/www/html/proof_deface.html', $deface_content);
        file_put_contents('/var/www/html/index.php', $deface_content);
        
        $response = [
            'success' => true,
            'message' => 'Website defaced successfully',
            'proof_file' => '/proof_deface.html'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'proof':
        // Create generic proof file
        $proof_content = <<<PHP
<?php
// Proof of exploitation for CVE-2026-109618
// This file was created via Use-After-Free vulnerability

echo "<html><body style='background:black;color:white;font-family:monospace;padding:50px;text-align:center;'>";
echo "<h1>PROOF OF EXPLOITATION</h1>";
echo "<p>CVE-2026-109618 (PHP2Shell)</p>";
echo "<p>Use-After-Free via OOM in Zend Engine</p>";
echo "<p>Server: " . \$_SERVER['SERVER_ADDR'] . "</p>";
echo "<p>Time: " . date('Y-m-d H:i:s') . "</p>";
echo "</body></html>";
?>
PHP;
        
        file_put_contents('/var/www/html/proof.php', $proof_content);
        
        $response = [
            'success' => true,
            'message' => 'Proof file created',
            'proof_file' => '/proof.php'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'restore':
        // Restore original index.php
        $original_content = file_get_contents('/var/www/html/index.php.bak') ?: <<<HTML
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
    </style>
</head>
<body>
    <h1>PHP2Shell Lab - Vulnerable Server</h1>
    <div class="vulnerable">
        <span class="status" style="color: #c00;">VULNERABLE</span>
        <p><strong>PHP Version:</strong> 8.4.26</p>
        <p><strong>CVE:</strong> CVE-2026-109618 (PHP2Shell)</p>
        <p><strong>CVSS:</strong> 9.2 (Critical)</p>
        <p><strong>Status:</strong> session.upload_progress.enabled = ON</p>
        <p><strong>Warning:</strong> This server is VULNERABLE to Use-After-Free attacks!</p>
    </div>
    <p><a href="/api.php?action=status">Check API Status</a></p>
    <p><small>Last updated: <?php echo date('Y-m-d H:i:s'); ?></small></p>
</body>
</html>
HTML;
        
        file_put_contents('/var/www/html/index.php', $original_content);
        
        $response = [
            'success' => true,
            'message' => 'Server restored to original state'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    default:
        $response = [
            'error' => 'Unknown action',
            'available_actions' => ['status', 'ransomware', 'steal', 'deface', 'proof', 'restore']
        ];
        http_response_code(400);
        echo json_encode($response, JSON_PRETTY_PRINT);
}
