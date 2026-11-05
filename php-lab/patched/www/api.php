<?php
// API de contrôle de l'état du lab pour la démo
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

$statusFile = __DIR__ . '/status.json';

// Déterminer si le serveur est vulnérable ou patché (version PHP < 8.3.8)
$phpVersion = phpversion();
$isVulnerable = version_compare($phpVersion, '8.3.8', '<');

$action = $_GET['action'] ?? $_POST['action'] ?? 'status';

if ($action === 'status') {
    if (file_exists($statusFile)) {
        echo file_get_contents($statusFile);
    } else {
        echo json_encode([
            'state' => 'normal',
            'updated_at' => date('H:i:s'),
            'php_version' => $phpVersion,
            'is_vulnerable' => $isVulnerable
        ]);
    }
    exit;
}

// Pour toute action offensive : si le serveur est patché, on bloque systématiquement !
if (in_array($action, ['ransomware', 'deface', 'steal'])) {
    if (!$isVulnerable) {
        http_response_code(403);
        echo json_encode([
            'success' => false,
            'error' => 'BLOCKED_BY_PATCH',
            'message' => 'Attaque rejetée ! Le correctif CVE-2024-4577 est actif sur PHP ' . $phpVersion,
            'php_version' => $phpVersion
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

