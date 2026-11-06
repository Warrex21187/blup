<?php
// PHP2Shell Lab - API Endpoint for CVE-2026-109618 Demo
// REAL PHP 8.4.27 - PATCHED

header('Content-Type: application/json');

// Get REAL PHP version
$php_version = phpversion();
$is_vulnerable = false;
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
            'status' => 'PROTECTED',
            'description' => 'Use-After-Free via OOM in Zend Engine - PATCHED in this version',
            'message' => 'This server is PROTECTED against PHP2Shell (CVE-2026-109618)',
            'publication_date' => '2026-10-21',
            'patch_date' => '2026-10-22',
            'protection' => 'session.upload_progress.enabled = 0',
            'server_addr' => $_SERVER['SERVER_ADDR'] ?? 'unknown',
            'server_software' => $_SERVER['SERVER_SOFTWARE'] ?? 'unknown'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'ransomware':
    case 'steal':
    case 'deface':
    case 'proof':
        // All attacks are blocked on patched server
        http_response_code(403);
        
        // Log the blocked attack
        error_log("[PHP2Shell] Attack BLOCKED on PHP {$php_version} - session.upload_progress.enabled = " . ($upload_progress_enabled ? '1' : '0'));
        
        $response = [
            'error' => 'Attack blocked',
            'message' => 'This server has the security patch applied (PHP ' . $php_version . ')',
            'php_version' => $php_version,
            'protection' => 'session.upload_progress.enabled = ' . ($upload_progress_enabled ? '1 (WARNING: should be 0!)' : '0'),
            'recommendation' => 'Always keep PHP updated to the latest version',
            'fixed_cve' => 'CVE-2026-109618',
            'cve_status' => 'PATCHED'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'restore':
        $response = [
            'success' => true,
            'message' => 'Server is already in protected state',
            'php_version' => $php_version,
            'is_vulnerable' => $is_vulnerable
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'oom':
        $response = [
            'success' => false,
            'message' => 'OOM attack BLOCKED - session.upload_progress is disabled',
            'php_version' => $php_version,
            'upload_progress_enabled' => $upload_progress_enabled,
            'protection' => 'session.upload_progress.enabled = 0 prevents CVE-2026-109618'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    default:
        $response = [
            'error' => 'Unknown action',
            'available_actions' => ['status'],
            'note' => 'Attack actions are blocked on this patched server',
            'php_version' => $php_version,
            'is_vulnerable' => $is_vulnerable
        ];
        http_response_code(400);
        echo json_encode($response, JSON_PRETTY_PRINT);
}
