<?php
// API de contrôle de l'état du lab pour la démo CVE-2026-109618 (PHP2Shell)
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

$statusFile = __DIR__ . '/status.json';

// Déterminer si le serveur est vulnérable à CVE-2026-109618
// Versions vulnérables : PHP 5.x-8.1 (EOL), 8.2 < 8.2.35, 8.3 < 8.3.36, 8.4 < 8.4.27
$phpVersion = phpversion();
$isVulnerable = version_compare($phpVersion, '8.4.27', '<');

$action = $_GET['action'] ?? $_POST['action'] ?? 'status';

if ($action === 'status') {
    if (file_exists($statusFile)) {
        echo file_get_contents($statusFile);
    } else {
        echo json_encode([
            'state' => 'normal',
            'updated_at' => date('H:i:s'),
            'php_version' => $phpVersion,
            'is_vulnerable' => $isVulnerable,
            'sapi' => php_sapi_name(),
            'upload_progress_enabled' => (int)ini_get('session.upload_progress.enabled')
        ]);
    }
    exit;
}

// Pour toute action offensive : si le serveur est patché, on bloque SYSTÉMATIQUEMENT !
if (in_array($action, ['ransomware', 'deface', 'steal', 'oom_trigger'])) {
    if (!$isVulnerable) {
        http_response_code(403);
        echo json_encode([
            'success' => false,
            'error' => 'BLOCKED_BY_PATCH',
            'message' => 'Attaque rejetée ! Le correctif CVE-2026-109618 est actif sur PHP ' . $phpVersion,
            'php_version' => $phpVersion,
            'patch_date' => '21 octobre 2026'
        ]);
        exit;
    }
}

if ($action === 'restore') {
    $data = [
        'state' => 'normal',
        'updated_at' => date('H:i:s'),
        'php_version' => $phpVersion
    ];
    file_put_contents($statusFile, json_encode($data, JSON_PRETTY_PRINT));
    echo json_encode(['success' => true, 'state' => 'normal']);
    exit;
}

echo json_encode(['error' => 'Action inconnue']);
