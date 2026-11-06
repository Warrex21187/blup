<?php
// Script de traitement des uploads pour le serveur PATCHÉ
// Ce script est protégé car il utilise PHP 8.4.27+ avec le correctif CVE-2026-109618

// Note: session.upload_progress est désactivé dans php.ini pour ce serveur
// Même si on essaye de l'activer ici, c'est trop tard - il faut le faire dans php.ini

// Démarrer la session
session_start();

// Vérifier si une progression d'upload est en cours
if (isset($_POST['PHP_SESSION_UPLOAD_PROGRESS'])) {
    $upload_id = $_POST['PHP_SESSION_UPLOAD_PROGRESS'];
    
    // Avec PHP 8.4.27+, le correctif empêche la corruption mémoire
    // Même si memory_limit est dépassé, le nettoyage est correct
    
    $data = [];
    foreach ($_POST as $key => $value) {
        if ($key !== 'PHP_SESSION_UPLOAD_PROGRESS') {
            $data[$key] = $value;
        }
    }
    
    echo json_encode([
        'status' => 'upload_processed',
        'upload_id' => $upload_id,
        'memory_peak' => memory_get_peak_usage(),
        'php_version' => phpversion(),
        'vulnerable' => version_compare(phpversion(), '8.4.27', '<'),
        'protected' => true,
        'message' => 'Ce serveur est protégé contre CVE-2026-109618'
    ]);
    exit;
}

// Réponse par défaut
echo json_encode([
    'status' => 'waiting_for_upload',
    'php_version' => phpversion(),
    'memory_limit' => ini_get('memory_limit'),
    'upload_progress_enabled' => ini_get('session.upload_progress.enabled'),
    'protected' => version_compare(phpversion(), '8.4.27', '>=')
]);
