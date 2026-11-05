<?php
/**
 * ══════════════════════════════════════════════════════════════════════
 *  LAB PHP2SHELL — API d'état du portail "Acme Corp"
 *  CVE-2026-109618 & CVE-2026-109619 (RCE du moteur PHP,
 *  corrigées le 21/10/2026)
 * ══════════════════════════════════════════════════════════════════════
 *
 *  Rôle pédagogique :
 *   - action 'status'   : état du portail + version PHP + verrou
 *   - actions offensives (ransomware / deface / steal) : SIMULATION
 *     d'impact post-RCE. Elles sont refusées (HTTP 403) si le conteneur
 *     exécute une version PHP corrigée. CE VERROU EST RÉEL : il se base
 *     sur la version PHP qui tourne (branches corrigées : 8.2.35 /
 *     8.3.36 / 8.4.27 / 8.5.12).
 *   - action 'restore' : remet le portail à l'état normal.
 *
 *  L'état est stocké dans /tmp (un fichier PAR conteneur) : le serveur
 *  vulnérable et le serveur patché partagent le même code applicatif
 *  mais vivent leur vie indépendamment.
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

/**
 * VRAI si la version PHP n'a PAS le correctif du 21/10/2026 :
 *   8.2.x < 8.2.35 | 8.3.x < 8.3.36 | 8.4.x < 8.4.27 | 8.5.x < 8.5.12
 * PHP 8.1 et antérieurs (EOL) : aucune version corrigée => vulnérable.
 */
function php_est_vulnerable(string $v): bool
{
    if (version_compare($v, '8.2.0', '<')) return true; // 5.x, 7.x, 8.0, 8.1
    if (version_compare($v, '8.3.0', '<')) return version_compare($v, '8.2.35', '<');
    if (version_compare($v, '8.4.0', '<')) return version_compare($v, '8.3.36', '<');
    if (version_compare($v, '8.5.0', '<')) return version_compare($v, '8.4.27', '<');
    return version_compare($v, '8.5.12', '<');
}

$statusFile   = sys_get_temp_dir() . '/lab_status.json';
$phpVersion   = phpversion();
$isVulnerable = php_est_vulnerable($phpVersion);

$defaults = [
    'state'         => 'normal',
    'title'         => '',
    'ransom_amount' => '',
    'updated_at'    => date('H:i:s'),
];

$status = $defaults;
if (is_file($statusFile)) {
    $saved = json_decode((string) file_get_contents($statusFile), true);
    if (is_array($saved)) {
        $status = array_merge($defaults, $saved);
    }
}

$action = $_GET['action'] ?? $_POST['action'] ?? 'status';

/* ─── ÉTAT DU PORTAIL ──────────────────────────────────────────────── */
if ($action === 'status') {
    echo json_encode([
        'state'         => $status['state'],
        'title'         => $status['title'],
        'ransom_amount' => $status['ransom_amount'],
        'updated_at'    => $status['updated_at'],
        'php_version'   => $phpVersion,
        'is_vulnerable' => $isVulnerable,
        'sapi'          => php_sapi_name(), // "apache2handler" = mod_php
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

/* ─── VERROU : un serveur patché rejette toute action offensive ────── */
if (in_array($action, ['ransomware', 'deface', 'steal'], true) && !$isVulnerable) {
    http_response_code(403);
    echo json_encode([
        'success'     => false,
        'error'       => 'BLOCKED_BY_PATCH',
        'message'     => 'Attaque rejetée : PHP ' . $phpVersion
                       . ' embarque le correctif CVE-2026-109618/109619 (publication du 21/10/2026).',
        'php_version' => $phpVersion,
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

/* ─── ACTIONS OFFENSIVES (simulation d'impact post-RCE) ───────────── */
if ($action === 'ransomware') {
    $data = [
        'state'         => 'ransomware',
        'title'         => 'SYSTÈME CHIFFRÉ — DEMANDE DE RANÇON',
        'ransom_amount' => '50 000 € (2.5 BTC)',
        'updated_at'    => date('H:i:s'),
    ];
    file_put_contents($statusFile, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    echo json_encode([
        'success' => true,
        'state'   => 'ransomware',
        'message' => 'RCE obtenue sur PHP ' . $phpVersion . ' (moteur non corrigé) — rançongiciel déployé.',
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

if ($action === 'deface') {
    $data = [
        'state'      => 'deface',
        'title'      => 'SITE COMPROMIS PAR EXÉCUTION DE CODE',
        'updated_at' => date('H:i:s'),
    ];
    file_put_contents($statusFile, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    echo json_encode([
        'success' => true,
        'state'   => 'deface',
        'message' => 'Contrôle total obtenu — page d\'accueil écrasée.',
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

if ($action === 'steal') {
    $data = [
        'state'          => 'data_leak',
        'title'          => 'FUITE DE DONNÉES RH DÉTECTÉE',
        'leaked_records' => 4,
        'updated_at'     => date('H:i:s'),
    ];
    file_put_contents($statusFile, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

    // Données RH fictives "exfiltrées" (simulation)
    $stolenData = [
        ['nom' => 'Alice Dupont', 'poste' => 'Directrice RH', 'salaire' => '5 800 €', 'password' => 'Password123!', 'secu' => '1 85 06 75 123 456', 'iban' => 'FR76 3000 4000 0123 4567 8901 234'],
        ['nom' => 'Bob Martin', 'poste' => 'DSI / Tech Lead', 'salaire' => '6 200 €', 'password' => 'Admin2024*Super', 'secu' => '1 82 11 92 654 321', 'iban' => 'FR76 3000 2000 0987 6543 2109 876'],
        ['nom' => 'Claire Bernard', 'poste' => 'Comptable', 'salaire' => '3 100 €', 'password' => 'Azerty2026', 'secu' => '2 89 04 69 789 012', 'iban' => 'FR76 3000 1000 0456 7890 1234 567'],
        ['nom' => 'David Leroy', 'poste' => 'Commercial', 'salaire' => '2 900 €', 'password' => 'Welcome2026!', 'secu' => '1 93 02 31 345 678', 'iban' => 'FR76 3000 5000 0234 5678 9012 345'],
    ];

    echo json_encode([
        'success'     => true,
        'state'       => 'data_leak',
        'stolen_data' => $stolenData,
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

/* ─── RESTAURATION ─────────────────────────────────────────────────── */
if ($action === 'restore') {
    $data = [
        'state'      => 'normal',
        'updated_at' => date('H:i:s'),
    ];
    file_put_contents($statusFile, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    echo json_encode([
        'success' => true,
        'state'   => 'normal',
        'message' => 'Portail restauré dans son état initial.',
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

http_response_code(400);
echo json_encode(['error' => 'Action inconnue'], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);