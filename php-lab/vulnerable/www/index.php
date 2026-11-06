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
    <title>Acme Corp — Portail d'Entreprise</title>
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
        
        .leak-alert {
            background: #fffbeb;
            border-left: 5px solid #f59e0b;
            color: #92400e;
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
            animation: pulse-border 2s infinite;
        }

        .ransom-box {
            max-width: 900px;
            margin: 40px auto;
            background: #1c0202;
            border: 3px solid #ff1111;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 0 40px rgba(255, 0, 0, 0.6);
            text-align: center;
        }
        .ransom-siren {
            font-size: 3.5rem;
            animation: blink 0.8s infinite;
            margin-bottom: 10px;
        }
        .ransom-title {
            font-size: 2.2rem;
            color: #ff3333;
            font-weight: 900;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 12px;
            text-shadow: 0 0 10px rgba(255, 50, 50, 0.8);
        }
        .ransom-subtitle {
            font-size: 1.15rem;
            color: #ffcccc;
            margin-bottom: 25px;
            line-height: 1.5;
        }
        .countdown-container {
            background: #2b0000;
            border: 2px dashed #ff4444;
            padding: 20px;
            border-radius: 12px;
            margin: 25px 0;
            display: inline-block;
            min-width: 320px;
        }
        .countdown-label { font-size: 0.9rem; text-transform: uppercase; color: #ff9999; letter-spacing: 1px; }
        .countdown-timer { font-size: 2.8rem; font-family: monospace; font-weight: bold; color: #ff2222; margin-top: 6px; }
        .ransom-details {
            background: #150000;
            padding: 20px;
            border-radius: 10px;
            text-align: left;
            margin: 25px 0;
            border: 1px solid #440000;
            font-size: 0.95rem;
            color: #eee;
            line-height: 1.6;
        }
        .ransom-list { list-style: none; margin-top: 10px; }
        .ransom-list li { padding: 4px 0; color: #ff8888; font-family: monospace; }
        .ransom-action {
            background: #ff1111;
            color: white;
            padding: 16px 36px;
            font-size: 1.1rem;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-transform: uppercase;
            box-shadow: 0 0 20px rgba(255,0,0,0.5);
            display: inline-block;
            text-decoration: none;
        }
        .ransom-footer-note {
            margin-top: 25px;
            font-size: 0.85rem;
            color: #888;
            border-top: 1px solid #330000;
            padding-top: 15px;
        }

        .deface-box {
            max-width: 850px;
            margin: 50px auto;
            border: 2px solid #00ff66;
            padding: 40px;
            background: #050f05;
            box-shadow: 0 0 30px rgba(0, 255, 100, 0.4);
            text-align: center;
        }
        .deface-box h1 { font-size: 2.4rem; margin-bottom: 20px; text-shadow: 0 0 10px #00ff66; }

        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }
        @keyframes red-glow { 0% { background: #0d0000; } 100% { background: #220000; } }
        @keyframes pulse-border { 0% { transform: scale(1); } 50% { transform: scale(1.01); } 100% { transform: scale(1); } }
    </style>
</head>

<body class="state-<?php echo htmlspecialchars($status['state']); ?>">

    <?php if ($status['state'] === 'normal' || $status['state'] === 'data_leak'): ?>
        
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

            <?php if ($status['state'] === 'data_leak'): ?>
                <div class="leak-alert">
                    <div>
                        <strong style="font-size: 1.1rem; display: block;">🚨 FUITE DE DONNÉES EN COURS</strong>
                        <span>La base de données RH vient d'être extraite via CVE-2026-109618 !</span>
                    </div>
                    <span style="background: #b45309; color: white; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 0.85rem;">4 FICHES VOLÉES</span>
                </div>
            <?php endif; ?>

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
                        <strong>Apache</strong>
                    </div>
                    <div class="item-info">
                        <span>Upload Progress</span>
                        <?php if (ini_get('session.upload_progress.enabled')): ?>
                            <strong style="color: #dc2626;">Actif (⚠️ Vecteur CVE-2026-109618)</strong>
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
                            <strong style="color: #dc2626;">Vulnérable</strong>
                        <?php else: ?>
                            <strong style="color: #16a34a;">Sécurisé ✓</strong>
                        <?php endif; ?>
                    </div>
                </div>

                <div style="margin-top: 20px; padding: 16px; background: #f8fafc; border-radius: 8px; border-left: 4px solid #2563eb; font-size: 0.9rem; line-height: 1.6;">
                    <strong>🔍 CVE-2026-109618 (PHP2Shell) :</strong><br>
                    Use-After-Free via OOM dans Zend Engine (session.upload_progress)
                </div>
            </div>

            <div class="card">
                <h2>👥 Annuaire & Données RH</h2>
                <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 14px;">Données confidentielles internes.</p>
                <table class="emp-table">
                    <thead>
                        <tr>
                            <th>Nom & Prénom</th>
                            <th>Département</th>
                            <th>Email</th>
                            <th>Accès</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td><strong>Alice Dupont</strong></td><td>Ressources Humaines</td><td>alice.dupont@acme.corp</td><td><span class="tag-safe">Niveau RH</span></td></tr>
                        <tr><td><strong>Bob Martin</strong></td><td>Direction Informatique</td><td>bob.martin@acme.corp</td><td><span class="tag-safe">Admin Root</span></td></tr>
                        <tr><td><strong>Claire Bernard</strong></td><td>Comptabilité</td><td>claire.bernard@acme.corp</td><td><span class="tag-safe">Accès Bancaire</span></td></tr>
                        <tr><td><strong>David Leroy</strong></td><td>Ventes</td><td>david.leroy@acme.corp</td><td><span class="tag-safe">Commercial</span></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

    <?php elseif ($status['state'] === 'ransomware'): ?>
        
        <div class="ransom-box">
            <div class="ransom-siren">🚨 🚀 🚨</div>
            <h1 class="ransom-title">SYSTÈME VERROUILLÉ — RANÇONGICIEL</h1>
            <p class="ransom-subtitle">Toutes les données ont été chiffrées.</p>
            <div class="countdown-container">
                <div class="countdown-label">⏳ Temps restant avant destruction</div>
                <div class="countdown-timer" id="timer">47:58:22</div>
            </div>
            <div class="ransom-details">
                <strong>📋 Fichiers chiffrés :</strong>
                <ul class="ransom-list">
                    <li>📄 base_rh_salaires_2026.sql [CHIFFRÉ]</li>
                    <li>📄 comptabilite_rib_bancaires.xlsx [CHIFFRÉ]</li>
                    <li>📄 contrats_clients_confidentiels.pdf [CHIFFRÉ]</li>
                </ul>
                <div style="margin-top: 15px; border-top: 1px solid #440000; padding-top: 10px;">
                    💰 <strong>Rançon :</strong> 50 000 € (2.5 Bitcoins)
                </div>
            </div>
            <a href="#" class="ransom-action" onclick="alert('Démonstration : NE JAMAIS PAYER !'); return false;">Payer la rançon</a>
            <div class="ransom-footer-note">🔒 Session de Prévention Cyber : CVE-2026-109618 (PHP2Shell)</div>
        </div>

    <?php elseif ($status['state'] === 'deface'): ?>
        <div class="deface-box">
            <div style="font-size: 3rem; margin-bottom: 10px;">☠️</div>
            <h1>HACKED BY PHP2SHELL</h1>
            <p style="font-size: 1.2rem; margin-bottom: 20px;">Serveur compromis en 1 seconde !</p>
            <div style="background: #001a00; padding: 20px; text-align: left; border: 1px solid #00ff66; margin-bottom: 25px; line-height: 1.8;">
                [+] Cible : Acme Technologies<br>
                [+] Vulnérabilité : CVE-2026-109618 (PHP2Shell)<br>
                [+] Privilèges : Contrôle total (RCE)<br>
                [+] Motif : Absence de correctif
            </div>
            <p style="color: #fff; font-size: 0.95rem;">🔒 Démonstration : Mettez vos logiciels à jour !</p>
        </div>
    <?php endif; ?>

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

        const timerElem = document.getElementById('timer');
        if (timerElem) {
            let seconds = 47 * 3600 + 58 * 60 + 22;
            setInterval(() => {
                seconds--;
                if (seconds < 0) seconds = 0;
                const h = String(Math.floor(seconds / 3600)).padStart(2, '0');
                const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
                const s = String(seconds % 60).padStart(2, '0');
                timerElem.textContent = `${h}:${m}:${s}`;
            }, 1000);
        }
    </script>
</body>
</html>
