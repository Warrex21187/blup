<?php
// Script de traitement des uploads pour déclencher CVE-2026-109618
// Ce script est vulnérable car il utilise PHP 8.4.26 avec session.upload_progress.enabled

// Activer le suivi de progression de session (nécessaire pour la faille)
ini_set('session.upload_progress.enabled', '1');

// Démarrer la session pour activer le suivi
session_start();

// Vérifier si une progression d'upload est en cours
if (isset($_POST['PHP_SESSION_UPLOAD_PROGRESS'])) {
    $upload_id = $_POST['PHP_SESSION_UPLOAD_PROGRESS'];
    
    // À ce stade, si la requête est très volumineuse (> memory_limit),
    // PHP va déclencher une erreur OOM et utiliser longjmp()
    // qui ne nettoie pas correctement les structures de session.upload_progress
    // => Use-After-Free possible !
    
    // Simuler un traitement qui consomme beaucoup de mémoire
    $data = [];
    foreach ($_POST as $key => $value) {
        if ($key !== 'PHP_SESSION_UPLOAD_PROGRESS') {
            // Stockage des données du formulaire
            $data[$key] = $value;
            
            // Consommation mémoire intentionnelle pour déclencher OOM
            // En réalité, c'est la taille de la requête qui déclenche l'OOM
            if (memory_get_usage() > 15 * 1024 * 1024) { // 15Mo
                // On est proche de la limite (16Mo)
                // La prochaine allocation pourrait déclencher l'OOM
            }
        }
    }
    
    // Si on arrive ici, c'est que l'OOM n'a pas été déclenché
    // ou que le worker a survécu (mais avec des pointeurs corrompus)
    echo json_encode([
        'status' => 'upload_processed',
        'upload_id' => $upload_id,
        'memory_peak' => memory_get_peak_usage(),
        'php_version' => phpversion(),
        'vulnerable' => version_compare(phpversion(), '8.4.27', '<')
    ]);
    exit;
}

// Réponse par défaut
echo json_encode([
    'status' => 'waiting_for_upload',
    'php_version' => phpversion(),
    'memory_limit' => ini_get('memory_limit'),
    'upload_progress_enabled' => ini_get('session.upload_progress.enabled')
]);
