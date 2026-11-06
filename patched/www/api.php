<?php
// PHP2Shell Lab - API Endpoint for CVE-2026-109618 Demo
// Simulates patched PHP 8.4.27 behavior

header('Content-Type: application/json');

// Simulate PHP 8.4.27 version
$php_version = '8.4.27';
$is_vulnerable = false;
$upload_progress_enabled = false;

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
            'description' => 'Use-After-Free via OOM in Zend Engine - PATCHED',
            'status' => 'PROTECTED',
            'message' => 'This server is PROTECTED against PHP2Shell (CVE-2026-109618)'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'ransomware':
    case 'steal':
    case 'deface':
    case 'proof':
        // All attacks are blocked on patched server
        http_response_code(403);
        $response = [
            'error' => 'Attack blocked',
            'message' => 'This server has the security patch applied',
            'php_version' => $php_version,
            'protection' => 'session.upload_progress.enabled = 0',
            'recommendation' => 'Always keep PHP updated to the latest version'
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    case 'restore':
        $response = [
            'success' => true,
            'message' => 'Server is already in protected state',
            'php_version' => $php_version
        ];
        echo json_encode($response, JSON_PRETTY_PRINT);
        break;

    default:
        $response = [
            'error' => 'Unknown action',
            'available_actions' => ['status'],
            'note' => 'Attack actions are blocked on this patched server'
        ];
        http_response_code(400);
        echo json_encode($response, JSON_PRETTY_PRINT);
}
