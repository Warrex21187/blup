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
            'upload_progress_enabled' => (int)ini_get('session.upload_progress.enabled'),
            'memory_limit' => ini_get('memory_limit')
        ]);
    }
    exit;
}

// Pour toute action offensive : si le serveur est patché, on bloque !
if (in_array($action, ['ransomware', 'deface', 'steal', 'oom_trigger', 'execute', 'create_proof'])) {
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
    echo json_encode([
        'success' => true,
        'message' => 'Déclencheur OOM envoyé - vérifiez les logs du serveur pour la corruption mémoire',
        'php_version' => $phpVersion,
        'upload_progress_enabled' => (int)ini_get('session.upload_progress.enabled'),
        'vulnerable' => true,
        'exploit' => 'CVE-2026-109618 - Use-After-Free via OOM dans Zend Engine'
    ]);
    exit;
}

// Exécution de commande (simulation pour démo)
if ($action === 'execute') {
    $command = $_POST['command'] ?? '';
    
    // Sécurité : ne pas exécuter de vraies commandes dangereuses en démo
    // Mais simuler le résultat
    $safe_commands = ['id', 'whoami', 'uname -a', 'date', 'php -v'];
    
    if (in_array($command, $safe_commands)) {
        $output = shell_exec($command . ' 2>&1');
        echo json_encode([
            'success' => true,
            'command' => $command,
            'output' => trim($output),
            'message' => 'Commande exécutée (simulation pour démo pédagogique)'
        ]);
    } else {
        echo json_encode([
            'success' => true,
            'command' => $command,
            'output' => '[SIMULATION] Commande serait exécutée sur un système vulnérable',
            'message' => 'Démonstration pédagogique - aucune commande réelle exécutée'
        ]);
    }
    exit;
}

// Création d'une preuve d'exploitation
if ($action === 'create_proof') {
    $content = $_POST['content'] ?? '';
    $proof_file = __DIR__ . '/proof.php';
    
    if (!empty($content)) {
        file_put_contents($proof_file, $content);
        echo json_encode([
            'success' => true,
            'file' => 'proof.php',
            'message' => 'Preuve d'exploitation créée',
            'url' => '/proof.php'
        ]);
    } else {
        // Contenu par défaut
        $default_content = '<?php echo "PHP2Shell Exploit - CVE-2026-109618 - SUCCESS"; ?>';
        file_put_contents($proof_file, $default_content);
        echo json_encode([
            'success' => true,
            'file' => 'proof.php',
            'message' => 'Preuve d'exploitation créée avec contenu par défaut',
            'url' => '/proof.php'
        ]);
    }
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
        'exploit' => 'PHP2Shell - Use-After-Free via OOM dans Zend Engine (session.upload_progress)'
    ];
    file_put_contents($statusFile, json_encode($data, JSON_PRETTY_PRINT));
    
    // Créer un fichier de preuve
    $proof_content = '<?php echo "<h1>SYSTÈME COMPROMIS PAR PHP2SHELL (CVE-2026-109618)</h1>"; ?>';
    file_put_contents(__DIR__ . '/proof_ransomware.php', $proof_content);
    
    echo json_encode(['success' => true, 'state' => 'ransomware', 'proof_file' => 'proof_ransomware.php']);
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
    
    // Créer un fichier de preuve
    $proof_content = '<?php echo "<h1>HACKED BY PHP2SHELL - CVE-2026-109618</h1>"; ?>';
    file_put_contents(__DIR__ . '/proof_deface.php', $proof_content);
    
    echo json_encode(['success' => true, 'state' => 'deface', 'proof_file' => 'proof_deface.php']);
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

    // Créer un fichier de preuve avec les données exfiltrées
    $proof_content = '<?php\n';
    $proof_content .= 'echo "<h1>DONNÉES EXFILTRÉES - CVE-2026-109618</h1>";\n';
    $proof_content .= 'echo "<pre>";\n';
    $proof_content .= 'echo file_get_contents("DONNEES_RH_EXFILTREES.csv");\n';
    $proof_content .= 'echo "</pre>";\n';
    $proof_content .= '?>';
    file_put_contents(__DIR__ . '/proof_steal.php', $proof_content);

    // Données exfiltrées
    $stolenData = [
        ['nom' => 'Alice Dupont', 'poste' => 'Directrice RH', 'salaire' => '5 800 €', 'password' => 'Password123!', 'secu' => '1 85 06 75 123 456', 'iban' => 'FR76 3000 4000 0123 4567 8901 234'],
        ['nom' => 'Bob Martin', 'poste' => 'DSI / Tech Lead', 'salaire' => '6 200 €', 'password' => 'Admin2024*Super', 'secu' => '1 82 11 92 654 321', 'iban' => 'FR76 3000 2000 0987 6543 2109 876'],
        ['nom' => 'Claire Bernard', 'poste' => 'Comptable', 'salaire' => '3 100 €', 'password' => 'Azerty2026', 'secu' => '2 89 04 69 789 012', 'iban' => 'FR76 3000 1000 0456 7890 1234 567'],
        ['nom' => 'David Leroy', 'poste' => 'Commercial', 'salaire' => '2 900 €', 'password' => 'Welcome2026!', 'secu' => '1 93 02 31 345 678', 'iban' => 'FR76 3000 5000 0234 5678 9012 345']
    ];

    // Créer le fichier CSV
    $csv_file = __DIR__ . '/DONNEES_RH_EXFILTREES.csv';
    $fp = fopen($csv_file, 'w');
    fputcsv($fp, ['Nom', 'Poste', 'Salaire Net', 'Mot de passe', 'N° Securité Sociale', 'IBAN'], ';');
    foreach ($stolenData as $emp) {
        fputcsv($fp, $emp, ';');
    }
    fclose($fp);

    echo json_encode([
        'success' => true,
        'state' => 'data_leak',
        'stolen_data' => $stolenData,
        'csv_file' => 'DONNEES_RH_EXFILTREES.csv',
        'proof_file' => 'proof_steal.php',
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
    
    // Supprimer les fichiers de preuve
    $proof_files = ['proof.php', 'proof_ransomware.php', 'proof_deface.php', 'proof_steal.php'];
    foreach ($proof_files as $file) {
        if (file_exists(__DIR__ . '/' . $file)) {
            unlink(__DIR__ . '/' . $file);
        }
    }
    
    echo json_encode(['success' => true, 'state' => 'normal', 'message' => 'Site restauré']);
    exit;
}

echo json_encode(['error' => 'Action inconnue']);
