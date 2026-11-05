<?php
$phpVersion = phpversion();
$isVulnerable = version_compare($phpVersion, '8.4.27', '<');
$statusFile = __DIR__ . '/status.json';
$status = [
    'state' => 'normal',
    'title' => '',
    'ransom_amount' => ''
];
if (file_exists($statusFile)) {
    $content = json_decode(file_get_contents($statusFile), true);
    if ($content) $status = array_merge($status, $content);
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acme Corp — Portail d'Entreprise (Sécurisé)</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', -apple-system, sans-serif; }
        
        body.state-normal {
            background: #f4f6f9;
            color: #2c3e50;
            transition: all 0.5s ease;
        }
        .header-normal {
            background: linear-gradient(135deg, #0d47a1, #1976d2);
            color: white;
            padding: 18px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .header-normal h1 { font-size: 1.4rem; display: flex; align-items: center; gap: 10px; }
        .badge-normal {
            background: rgba(255,255,255,0.2);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        .container { max-width: 1050px; margin: 30px auto; padding: 0 20px; }
        .card {
            background: white;
            border-radius: 12px;
            padding: 26px;
            margin-bottom: 22px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border: 1px solid #e8ecef;
        }
        .card h2 { color: #1565c0; font-size: 1.25rem; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
        .grid-info { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 16px; }
        .item-info { background: #f8fafc; padding: 14px; border-radius: 8px; border-left: 4px solid #1976d2; }
        .item-info span { font-size: 0.75rem; text-transform: uppercase; color: #64748b; font-weight: 600; display: block; }
        .item-info strong { font-size: 1.05rem; color: #1e293b; margin-top: 4px; display: block; }
        .emp-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        .emp-table th { background: #f1f5f9; text-align: left; padding: 12px; font-size: 0.85rem; color: #475569; }
        .emp-table td { padding: 12px; border-top: 1px solid #e2e8f0; font-size: 0.9rem; }
        .tag-safe { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; }
        .tag-vuln { background: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; }
        
        .protected-banner {
            background: #dcfce7;
            border-left: 5px solid #16a34a;
            color: #166534;
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 12px rgba(22, 163, 54, 0.15);
        }
        
        .attack-blocked {
            background: #dcfce7;
            border: 3px solid #16a34a;
            border-radius: 16px;
            padding: 40px;
            max-width: 800px;
            margin: 40px auto;
            text-align: center;
            box-shadow: 0 0 40px rgba(22, 163, 54, 0.3);
        }
        .attack-blocked h2 {
            color: #166534;
            font-size: 2rem;
            margin-bottom: 20px;
        }
        .attack-blocked p {
            font-size: 1.1rem;
            color: #166534;
            line-height: 1.6;
        }

        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }
        @keyframes red-glow { 0% { background: #0d0000; } 100% { background: #220000; } }
        @keyframes pulse-border { 0% { transform: scale(1); } 50% { transform: scale(1.01); } 100% { transform: scale(1); } }
    </style>
</head>

<body class="state-<?php echo htmlspecialchars($status['state']); ?>">

    <!-- ================= SCÈNE 1 : ÉTAT NORMAL ================= -->
    <?php if ($status['state'] === 'normal'): ?>
        
        <header class="header-normal">
            <h1>🏢 Acme Technologies <span>— Portail Collaborateur</span></h1>
            <div style="display: flex; gap: 12px; align-items: center;">
                <span class="badge-normal">🌐 RÉSEAU INTERNE</span>
                <?php if ($isVulnerable): ?>
                    <span class="tag-vuln">⚠️ VULNÉRABLE (PHP <?php echo $phpVersion; ?>)</span>
                <?php else: ?>
                    <span class="tag-safe">🔒 SÉCURISÉ (PHP <?php echo $phpVersion; ?>)</span>
                <?php endif; ?>
            </div>
        </header>

        <div class="container">
            
            <div class="protected-banner">
                <div>
                    <strong style="font-size: 1.1rem; display: block;">🛡️ SERVEUR PROTÉGÉ CONTRE CVE-2026-109618</strong>
                    <span>Ce serveur exécute PHP <?php echo $phpVersion; ?> avec le correctif officiel du 21 octobre 2026.</span>
                </div>
                <span style="background: #166534; color: white; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 0.85rem;">✓ CORRIGÉ</span>
            </div>

            <div class="card">
                <h2>📊 Diagnostic du Système</h2>
                <div class="grid-info">
                    <div class="item-info">
                        <span>Version PHP</span>
                        <strong><?php echo $phpVersion; ?></strong>
                    </div>
                    <div class="item-info">
                        <span>Mode d'exécution</span>
                        <strong>Apache mod_php</strong>
                    </div>
                    <div class="item-info">
                        <span>Serveur Web</span>
                        <strong>Apache / <?php echo apache_get_version(); ?></strong>
                    </div>
                    <div class="item-info">
                        <span>Upload Progress</span>
                        <?php if (ini_get('session.upload_progress.enabled')): ?>
                            <strong style="color: #dc2626;">Actif (⚠️ Vecteur potentiel)</strong>
                        <?php else: ?>
                            <strong style="color: #16a34a;">Désactivé (Mitigé ✓)</strong>
                        <?php endif; ?>
                    </div>
                    <div class="item-info">
                        <span>Memory Limit</span>
                        <strong><?php echo ini_get('memory_limit'); ?></strong>
                    </div>
                    <div class="item-info">
                        <span>Statut Sécurité</span>
                        <?php if ($isVulnerable): ?>
                            <strong style="color: #dc2626;">Version NON corrigée</strong>
                        <?php else: ?>
                            <strong style="color: #16a34a;">Patch Appliqué ✓</strong>
                        <?php endif; ?>
                    </div>
                </div>

                <div style="margin-top: 20px; padding: 16px; background: #dcfce7; border-radius: 8px; border-left: 4px solid #16a34a; font-size: 0.9rem; line-height: 1.6;">
                    <strong>✅ PROTECTION ACTIVE :</strong><br>
                    ✅ Mise à jour vers PHP <?php echo $phpVersion; ?> (corrigé le 21/10/2026)<br>
                    ✅ <code>session.upload_progress.enabled = 0</code> (mitigation supplémentaire)<br>
                    ✅ Correction du Use-After-Free dans Zend Engine<br>
                    ✅ Toutes les attaques CVE-2026-109618 sont <strong>bloquées</strong>
                </div>
            </div>

            <div class="card">
                <h2>👥 Annuaire & Données RH de l'Entreprise</h2>
                <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 14px;">
                    Données confidentielles internes réservées aux salariés d'Acme Technologies.
                    <strong style="color: #16a34a;">Ce serveur est protégé contre les exfiltrations.</strong>
                </p>
                <table class="emp-table">
                    <thead>
                        <tr>
                            <th>Nom & Prénom</th>
                            <th>Département</th>
                            <th>Email Professionnel</th>
                            <th>Accès Système</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Alice Dupont</strong></td>
                            <td>Ressources Humaines</td>
                            <td>alice.dupont@acme.corp</td>
                            <td><span class="tag-safe">Niveau RH</span></td>
                        </tr>
                        <tr>
                            <td><strong>Bob Martin</strong></td>
                            <td>Direction Informatique (DSI)</td>
                            <td>bob.martin@acme.corp</td>
                            <td><span class="tag-safe">Admin Root</span></td>
                        </tr>
                        <tr>
                            <td><strong>Claire Bernard</strong></td>
                            <td>Comptabilité & Paie</td>
                            <td>claire.bernard@acme.corp</td>
                            <td><span class="tag-safe">Accès Bancaire</span></td>
                        </tr>
                        <tr>
                            <td><strong>David Leroy</strong></td>
                            <td>Ventes & Partenariats</td>
                            <td>david.leroy@acme.corp</td>
                            <td><span class="tag-safe">Commercial</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="card">
                <h2>📅 Actualités & Notes de Service</h2>
                <div style="background: #dcfce7; padding: 14px; border-radius: 8px; border-left: 4px solid #16a34a; font-size: 0.9rem; line-height: 1.6;">
                    <strong>✅ Rappel :</strong> Ce serveur est à jour et protégé contre CVE-2026-109618. Toutes les tentatives d'exploitation sont automatiquement bloquées.
                </div>
            </div>

        </div>

    <!-- ================= SCÈNE 2 : ATTAQUE BLOQUÉE ================= -->
    <?php elseif ($status['state'] === 'ransomware' || $status['state'] === 'deface' || $status['state'] === 'data_leak'): ?>

        <div class="attack-blocked">
            <h2>✅ ATTAQUE BLOQUÉE !</h2>
            <p>
                <strong>Tentative d'exploitation de CVE-2026-109618 détectée et neutralisée.</strong><br><br>
                Ce serveur exécute PHP <?php echo $phpVersion; ?> avec le correctif officiel.<br>
                Le Use-After-Free dans Zend Engine a été corrigé le 21 octobre 2026.<br><br>
                <strong>Résultat :</strong> L'attaquant ne peut pas compromettre ce système.
            </p>
        </div>
        
        <div class="container" style="margin-top: 20px;">
            <div class="card">
                <h2>📊 Diagnostic du Système</h2>
                <div class="grid-info">
                    <div class="item-info">
                        <span>Version PHP</span>
                        <strong><?php echo $phpVersion; ?></strong>
                    </div>
                    <div class="item-info">
                        <span>Statut Sécurité</span>
                        <strong style="color: #16a34a;">✅ PROTÉGÉ CONTRE CVE-2026-109618</strong>
                    </div>
                    <div class="item-info">
                        <span>Upload Progress</span>
                        <strong style="color: #16a34a;">Désactivé</strong>
                    </div>
                </div>
            </div>
        </div>

    <?php endif; ?>

    <!-- Synchronisation en temps réel -->
    <script>
        let currentState = "<?php echo $status['state']; ?>";
        setInterval(async () => {
            try {
                const res = await fetch('api.php?action=status&t=' + Date.now());
                const data = await res.json();
                if (data.state && data.state !== currentState) {
                    window.location.reload();
                }
            } catch (e) {}
        }, 1200);
    </script>
</body>
</html>
