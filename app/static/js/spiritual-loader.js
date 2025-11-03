/**
 * Spiritual Loader - SACRA
 * Affiche un loader avec des messages spirituels rotatifs
 */

const SPIRITUAL_MESSAGES = [
    "🔮 Consultation de l'Univers...",
    "✨ Connexion aux guides spirituels...",
    "🌙 Décryptage des énergies cosmiques...",
    "💫 Interprétation des messages divins...",
    "🌟 Analyse de ton chemin d'âme...",
    "🕉️ Harmonisation des chakras...",
    "🔯 Lecture des archives akashiques...",
    "🌺 Canalisation de la sagesse ancienne...",
    "🦋 Décodage des synchronicités...",
    "🌈 Alignement avec les fréquences supérieures...",
    "🎴 Consultation des gardiens...",
    "🧘 Méditation sur ton intention...",
    "🌌 Exploration des plans subtils...",
    "💎 Révélation des vérités cachées...",
    "🕊️ Message des anges en cours...",
    "⚡ Activation de l'intuition divine...",
    "🌿 Purification énergétique...",
    "🔥 Transmutation alchimique...",
    "🌊 Navigation dans les eaux de l'âme...",
    "☀️ Illumination spirituelle..."
];

let loadingInterval = null;

/**
 * Affiche le loader spirituel
 * @param {string} containerId - ID du container où afficher le loader
 */
function showSpiritualLoader(containerId = 'spiritual-loader') {
    const container = document.getElementById(containerId);
    if (!container) return;

    // HTML du loader
    container.innerHTML = `
        <div class="spiritual-loader-wrapper" style="text-align: center; padding: 60px 20px;">
            <div class="spiritual-spinner"></div>
            <p id="spiritual-message" class="spiritual-message">
                ${SPIRITUAL_MESSAGES[0]}
            </p>
        </div>
    `;

    container.style.display = 'block';

    // Rotation des messages toutes les 2.5 secondes
    let index = 0;
    loadingInterval = setInterval(() => {
        index = (index + 1) % SPIRITUAL_MESSAGES.length;
        const messageEl = document.getElementById('spiritual-message');
        if (messageEl) {
            messageEl.style.opacity = '0';
            setTimeout(() => {
                messageEl.textContent = SPIRITUAL_MESSAGES[index];
                messageEl.style.opacity = '1';
            }, 300);
        }
    }, 2500);
}

/**
 * Cache le loader spirituel
 * @param {string} containerId - ID du container
 */
function hideSpiritualLoader(containerId = 'spiritual-loader') {
    if (loadingInterval) {
        clearInterval(loadingInterval);
        loadingInterval = null;
    }

    const container = document.getElementById(containerId);
    if (container) {
        container.style.display = 'none';
        container.innerHTML = '';
    }
}

/**
 * Affiche un skeleton screen (placeholder animé)
 * @param {string} containerId - ID du container
 * @param {number} lines - Nombre de lignes à afficher
 */
function showSkeletonScreen(containerId, lines = 3) {
    const container = document.getElementById(containerId);
    if (!container) return;

    let html = '<div class="skeleton-wrapper" style="padding: 20px;">';
    for (let i = 0; i < lines; i++) {
        const width = i === lines - 1 ? '80%' : '100%';
        html += `<div class="skeleton-line" style="width: ${width};"></div>`;
    }
    html += '</div>';

    container.innerHTML = html;
    container.style.display = 'block';
}
