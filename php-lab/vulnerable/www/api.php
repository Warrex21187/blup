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

// Pour toute action offensive : si le serveur est patché, on bloque !
if (in_array($action, ['ransomware', 'deface', 'steal', 'oom_trigger'])) {
    if (!$isVulnerable) {
        http_response_code(403);
        echo json_encode([
            'success' => false,
            'error' => 'BLOCKED_BY_PATCH',
            'message' => 'Attaque rejetée ! Le correctif CVE-2026-109618 est actif sur PHP ' . $phpVersion,
            'php_version' => $phpVersion
        ]);
        exit;
    }
}

// Déclencheur OOM pour CVE-2026-109618
if ($action === 'oom_trigger') {
    // Vérifier que session.upload_progress est activé
    if (!ini_get('session.upload_progress.enabled')) {
        echo json_encode([
            'success' => false,
            'error' => 'MITIGATION_ACTIVE',
            'message' => 'session.upload_progress.enabled est désactivé - la faille ne peut pas être exploitée'
        ]);
        exit;
    }
    
    // Générer une réponse indiquant que le déclencheur a été envoyé
    // En réalité, l'exploitation nécessite une requête multipart massive
    echo json_encode([
        'success' => true,
        'message' => 'Déclencheur OOM envoyé - vérifiez les logs du serveur pour la corruption mémoire',
        'php_version' => $phpVersion,
        'upload_progress_enabled' => (int)ini_get('session.upload_progress.enabled')
    ]);
    exit;
}

// Application de l'action sur serveur vulnérable
if ($action === 'ransomware') {
    $data = [
        'state' => 'ransomware',
        'title' => 'SYSTÈME CHIFFRÉ — DEMANDE DE RANÇON',
        'ransom_amount' => '50 000 € (2.5 BTC)',
        'updated_at' => date('H:i:s'),
        'php_version' => $phpVersion,
        'cve' => 'CVE-2026-109618',
        'exploit' => 'PHP2Shell - Use-After-Free via OOM dans session.upload_progress'
    ];
    file_put_contents($statusFile, json_encode($data, JSON_PRETTY_PRINT));
    echo json_encode(['success' => true, 'state' => 'ransomware']);
    exit;
}

if ($action === 'deface') {
    $data = [
        'state' => 'deface',
        'title' => 'SITE COMPROMIS PAR PHP2SHELL',
        'updated_at' => date('H:i:s'),
        'php_version' => $phpVersion,
        'cve' => 'CVE-2026-109618'
    ];
    file_put_contents($statusFile, json_encode($data, JSON_PRETTY_PRINT));
    echo json_encode(['success' => true, 'state' => 'deface']);
    exit;
}

if ($action === 'steal') {
    $data = [
        'state' => 'data_leak',
        'title' => 'FUITE DE DONNÉES RH DÉTECTÉE',
        'leaked_records' => 4,
        'updated_at' => date('H:i:s'),
        'php_version' => $phpVersion,
        'cve' => 'CVE-2026-109618',
        'exploit' => 'Exfiltration via corruption mémoire Use-After-Free'
    ];
    file_put_contents($statusFile, json_encode($data, JSON_PRETTY_PRINT));

    // Données exfiltrées
    $stolenData = [
        ['nom' => 'Alice Dupont', 'poste' => 'Directrice RH', 'salaire' => '5 800 €', 'password' => 'Password123!', 'secu' => '1 85 06 75 123 456', 'iban' => 'FR76 3000 4000 0123 4567 8901 234'],
        ['nom' => 'Bob Martin', 'poste' => 'DSI / Tech Lead', 'salaire' => '6 200 €', 'password' => 'Admin2024*Super', 'secu' => '1 82 11 92 654 321', 'iban' => 'FR76 3000 2000 0987 6543 2109 876'],
        ['nom' => 'Claire Bernard', 'poste' => 'Comptable', 'salaire' => '3 100 €', 'password' => 'Azerty2026', 'secu' => '2 89 04 69 789 012', 'iban' => 'FR76 3000 1000 0456 7890 1234 567'],
        ['nom' => 'David Leroy', 'poste' => 'Commercial', 'salaire' => '2 900 €', 'password' => 'Welcome2026!', 'secu' => '1 93 02 31 345 678', 'iban' => 'FR76 3000 5000 0234 5678 9012 345']
    ];

    echo json_encode([
        'success' => true,
        'state' => 'data_leak',
        'stolen_data' => $stolenData,
        'exploit_details' => 'CVE-2026-109618: Use-After-Free via OOM dans Zend Engine (session.upload_progress)'
    ], JSON_PRETTY_PRINT);
    exit;
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
