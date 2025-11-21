// Système d'affichage du visage émotionnel de Milo
const faceCanvas = document.getElementById("face-canvas");
const faceCtx = faceCanvas.getContext("2d");

faceCanvas.width = 400;
faceCanvas.height = 400;

const centerX = faceCanvas.width / 2;
const centerY = faceCanvas.height / 2;

// État émotionnel actuel
let currentEmotion = "neutre";
let emotionIntensity = 0.5;
let animationProgress = 0;

// Paramètres du visage
const face = {
    // Yeux
    leftEye: { x: centerX - 60, y: centerY - 40 },
    rightEye: { x: centerX + 60, y: centerY - 40 },
    eyeWidth: 30,
    eyeHeight: 35,
    
    // Sourcils
    leftBrow: { x: centerX - 60, y: centerY - 80 },
    rightBrow: { x: centerX + 60, y: centerY - 80 },
    browLength: 40,
    
    // Bouche
    mouth: { x: centerX, y: centerY + 60 },
    mouthWidth: 80,
    
    // Nez
    nose: { x: centerX, y: centerY + 10 }
};

// Configurations émotionnelles avec couleurs et animations
const emotions = {
    neutre: {
        eyeHeight: 35,
        browAngle: 0,
        browY: -80,
        mouthCurve: 0,
        blinkSpeed: 3000,
        color: "rgb(0, 0, 128)", // Bleu marine
        bgColor: "rgb(0, 0, 139)", // Navy
        particleColor: "rgb(0, 0, 128)",
        animationSpeed: 1.0
    },
    joyeux: {
        eyeHeight: 40,
        browAngle: 5,
        browY: -85,
        mouthCurve: 30,
        blinkSpeed: 2000,
        color: "rgb(255, 200, 0)", // Jaune/orange
        bgColor: "rgb(255, 165, 0)", // Orange vif
        particleColor: "rgb(255, 215, 0)", // Or
        animationSpeed: 1.5
    },
    triste: {
        eyeHeight: 30,
        browAngle: -15,
        browY: -75,
        mouthCurve: -25,
        blinkSpeed: 4000,
        color: "rgb(70, 130, 180)", // Bleu acier
        bgColor: "rgb(25, 25, 112)", // Bleu nuit
        particleColor: "rgb(100, 149, 237)", // Bleu ciel
        animationSpeed: 0.5
    },
    colere: {
        eyeHeight: 25,
        browAngle: -25,
        browY: -70,
        mouthCurve: -15,
        blinkSpeed: 1500,
        color: "rgb(220, 20, 60)", // Rouge cramoisi
        bgColor: "rgb(139, 0, 0)", // Rouge foncé
        particleColor: "rgb(255, 0, 0)", // Rouge vif
        animationSpeed: 2.5 // Animations très rapides et agressives
    },
    pensif: {
        eyeHeight: 32,
        browAngle: -8,
        browY: -78,
        mouthCurve: -5,
        blinkSpeed: 3500,
        color: "rgb(138, 43, 226)", // Violet
        bgColor: "rgb(75, 0, 130)", // Indigo
        particleColor: "rgb(147, 112, 219)", // Violet moyen
        animationSpeed: 0.8
    }
};

// Animation de clignement
let isBlinking = false;
let blinkTimer = null;

function scheduleBlink() {
    const config = emotions[currentEmotion] || emotions.neutre;
    const delay = config.blinkSpeed + (Math.random() * 1000);
    
    clearTimeout(blinkTimer);
    blinkTimer = setTimeout(() => {
        blink();
        scheduleBlink();
    }, delay);
}

function blink() {
    isBlinking = true;
    setTimeout(() => {
        isBlinking = false;
    }, 150);
}

// Variables pour transition de couleur
let currentColor = "rgb(0, 0, 128)";
let targetColor = "rgb(0, 0, 128)";
let currentBgColor = "rgb(0, 0, 139)";
let targetBgColor = "rgb(0, 0, 139)";

// Dessin du visage
function drawFace() {
    faceCtx.clearRect(0, 0, faceCanvas.width, faceCanvas.height);
    
    const config = emotions[currentEmotion] || emotions.neutre;
    
    // Interpolation douce vers l'émotion cible
    animationProgress += (1 - animationProgress) * 0.1;
    
    // Transition douce des couleurs
    currentColor = interpolateColor(currentColor, config.color, 0.1);
    currentBgColor = interpolateColor(currentBgColor, config.bgColor, 0.1);
    
    // Mettre à jour les couleurs globales
    updateGlobalColors(config);
    
    // Dessiner les yeux
    drawEyes(config);
    
    // Dessiner les sourcils
    drawEyebrows(config);
    
    // Dessiner la bouche
    drawMouth(config);
    
    // Dessiner le nez (simple point)
    drawNose();
}

// Fonction pour interpoler les couleurs RGB
function interpolateColor(color1, color2, factor) {
    const rgb1 = parseColor(color1);
    const rgb2 = parseColor(color2);
    
    const r = Math.round(rgb1.r + (rgb2.r - rgb1.r) * factor);
    const g = Math.round(rgb1.g + (rgb2.g - rgb1.g) * factor);
    const b = Math.round(rgb1.b + (rgb2.b - rgb1.b) * factor);
    
    return `rgb(${r}, ${g}, ${b})`;
}

// Parser une couleur RGB en objet
function parseColor(color) {
    const match = color.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
    if (match) {
        return {
            r: parseInt(match[1]),
            g: parseInt(match[2]),
            b: parseInt(match[3])
        };
    }
    return { r: 0, g: 0, b: 128 }; // Par défaut bleu marine
}

// Mettre à jour les couleurs globales (fond, particules, etc.)
function updateGlobalColors(config) {
    // Mettre à jour le fond avec transition
    document.body.style.backgroundColor = currentBgColor;
    
    // Ajouter des classes CSS pour les animations selon l'émotion
    document.body.className = `emotion-${currentEmotion}`;
    
    // Mettre à jour les particules (via une fonction globale)
    if (window.updateParticleColors) {
        window.updateParticleColors(config.particleColor, config.animationSpeed);
    }
    
    // Mettre à jour la couleur du texte
    const textZone = document.getElementById("text-zone");
    if (textZone) {
        textZone.style.color = currentColor;
        // Ajouter classe pour animations du texte
        textZone.className = `emotion-${currentEmotion}`;
    }
}

function drawEyes(config) {
    const eyeHeight = isBlinking ? 2 : config.eyeHeight * animationProgress + 35 * (1 - animationProgress);
    
    // Utiliser la couleur actuelle (avec transition)
    faceCtx.fillStyle = currentColor;
    
    // Pour la colère, ajouter un effet de "rougeoiement"
    if (currentEmotion === "colere" && emotionIntensity > 0.7) {
        const pulse = Math.sin(Date.now() * 0.01) * 0.3 + 0.7;
        const r = Math.min(255, parseColor(currentColor).r * (1 + pulse * 0.2));
        faceCtx.fillStyle = `rgb(${Math.round(r)}, ${parseColor(currentColor).g}, ${parseColor(currentColor).b})`;
    }
    
    // Œil gauche
    faceCtx.beginPath();
    faceCtx.ellipse(
        face.leftEye.x, 
        face.leftEye.y, 
        face.eyeWidth / 2, 
        eyeHeight / 2, 
        0, 0, 2 * Math.PI
    );
    faceCtx.fill();
    
    // Œil droit
    faceCtx.beginPath();
    faceCtx.ellipse(
        face.rightEye.x, 
        face.rightEye.y, 
        face.eyeWidth / 2, 
        eyeHeight / 2, 
        0, 0, 2 * Math.PI
    );
    faceCtx.fill();
    
    // Pupilles (si pas en train de cligner)
    if (!isBlinking) {
        faceCtx.fillStyle = "white";
        const pupilSize = currentEmotion === "colere" ? 8 : 6; // Pupilles plus grandes pour la colère
        
        faceCtx.beginPath();
        faceCtx.arc(face.leftEye.x, face.leftEye.y, pupilSize, 0, 2 * Math.PI);
        faceCtx.fill();
        
        faceCtx.beginPath();
        faceCtx.arc(face.rightEye.x, face.rightEye.y, pupilSize, 0, 2 * Math.PI);
        faceCtx.fill();
    }
}

function drawEyebrows(config) {
    faceCtx.strokeStyle = currentColor;
    // Pour la colère, sourcils plus épais et plus marqués
    faceCtx.lineWidth = currentEmotion === "colere" ? 6 : 4;
    faceCtx.lineCap = "round";
    
    const browY = config.browY * animationProgress + (-80) * (1 - animationProgress);
    const angleRad = (config.browAngle * Math.PI / 180) * animationProgress;
    
    // Pour la colère, ajouter un léger tremblement
    let offsetX = 0;
    let offsetY = 0;
    if (currentEmotion === "colere" && emotionIntensity > 0.7) {
        offsetX = (Math.random() - 0.5) * 2;
        offsetY = (Math.random() - 0.5) * 2;
    }
    
    // Sourcil gauche
    faceCtx.beginPath();
    const leftStartX = face.leftBrow.x - face.browLength / 2 + offsetX;
    const leftEndX = face.leftBrow.x + face.browLength / 2 + offsetX;
    const leftStartY = face.leftBrow.y + browY - Math.tan(angleRad) * (face.browLength / 2) + offsetY;
    const leftEndY = face.leftBrow.y + browY + Math.tan(angleRad) * (face.browLength / 2) + offsetY;
    faceCtx.moveTo(leftStartX, leftStartY);
    faceCtx.lineTo(leftEndX, leftEndY);
    faceCtx.stroke();
    
    // Sourcil droit
    faceCtx.beginPath();
    const rightStartX = face.rightBrow.x - face.browLength / 2 + offsetX;
    const rightEndX = face.rightBrow.x + face.browLength / 2 + offsetX;
    const rightStartY = face.rightBrow.y + browY + Math.tan(angleRad) * (face.browLength / 2) + offsetY;
    const rightEndY = face.rightBrow.y + browY - Math.tan(angleRad) * (face.browLength / 2) + offsetY;
    faceCtx.moveTo(rightStartX, rightStartY);
    faceCtx.lineTo(rightEndX, rightEndY);
    faceCtx.stroke();
}

function drawMouth(config) {
    faceCtx.strokeStyle = currentColor;
    // Pour la colère, bouche plus épaisse
    faceCtx.lineWidth = currentEmotion === "colere" ? 5 : 4;
    faceCtx.lineCap = "round";
    
    const mouthCurve = config.mouthCurve * animationProgress;
    
    // Pour la colère, ajouter un léger tremblement
    let offsetX = 0;
    let offsetY = 0;
    if (currentEmotion === "colere" && emotionIntensity > 0.7) {
        offsetX = (Math.random() - 0.5) * 1.5;
        offsetY = (Math.random() - 0.5) * 1.5;
    }
    
    faceCtx.beginPath();
    
    if (mouthCurve > 0) {
        // Sourire (arc vers le bas)
        faceCtx.arc(
            face.mouth.x + offsetX,
            face.mouth.y - mouthCurve + offsetY,
            face.mouthWidth / 2,
            0.2 * Math.PI,
            0.8 * Math.PI
        );
    } else if (mouthCurve < 0) {
        // Tristesse (arc vers le haut)
        faceCtx.arc(
            face.mouth.x + offsetX,
            face.mouth.y - mouthCurve + offsetY,
            face.mouthWidth / 2,
            0.8 * Math.PI,
            1.2 * Math.PI,
            true
        );
    } else {
        // Neutre (ligne droite)
        faceCtx.moveTo(face.mouth.x - face.mouthWidth / 2 + offsetX, face.mouth.y + offsetY);
        faceCtx.lineTo(face.mouth.x + face.mouthWidth / 2 + offsetX, face.mouth.y + offsetY);
    }
    
    faceCtx.stroke();
}

function drawNose() {
    faceCtx.fillStyle = currentColor;
    faceCtx.beginPath();
    faceCtx.arc(face.nose.x, face.nose.y, 3, 0, 2 * Math.PI);
    faceCtx.fill();
}

// Fonction publique pour changer l'émotion
function setEmotion(emotion, intensity = 0.8) {
    console.log(`😊 Changement d'émotion : ${emotion} (intensité: ${intensity})`);
    
    // Mapper "confus" vers "pensif" (le modèle invente parfois)
    if (emotion === "confus") {
        emotion = "pensif";
    }
    
    // Vérifier que l'émotion existe
    if (!emotions[emotion]) {
        console.warn(`⚠️ Émotion inconnue: ${emotion}, utilisation de "neutre"`);
        emotion = "neutre";
    }
    
    currentEmotion = emotion;
    emotionIntensity = intensity;
    animationProgress = 0; // Reset pour transition douce
    
    // Mettre à jour les couleurs cibles
    const config = emotions[emotion] || emotions.neutre;
    targetColor = config.color;
    targetBgColor = config.bgColor;
}

// Boucle d'animation
function animate() {
    drawFace();
    requestAnimationFrame(animate);
}

// Initialisation
scheduleBlink();
animate();

// Export de la fonction pour l'utiliser depuis d'autres scripts
window.setMiloEmotion = setEmotion;