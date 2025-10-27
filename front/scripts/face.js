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

// Configurations émotionnelles
const emotions = {
    neutre: {
        eyeHeight: 35,
        browAngle: 0,
        browY: -80,
        mouthCurve: 0,
        blinkSpeed: 3000
    },
    joyeux: {
        eyeHeight: 40,
        browAngle: 5,
        browY: -85,
        mouthCurve: 30,
        blinkSpeed: 2000
    },
    triste: {
        eyeHeight: 30,
        browAngle: -15,
        browY: -75,
        mouthCurve: -25,
        blinkSpeed: 4000
    },
    colere: {
        eyeHeight: 25,
        browAngle: -25,
        browY: -70,
        mouthCurve: -15,
        blinkSpeed: 1500
    },
    pensif: {
        eyeHeight: 32,
        browAngle: -8,
        browY: -78,
        mouthCurve: -5,
        blinkSpeed: 3500
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

// Dessin du visage
function drawFace() {
    faceCtx.clearRect(0, 0, faceCanvas.width, faceCanvas.height);
    
    const config = emotions[currentEmotion] || emotions.neutre;
    
    // Interpolation douce vers l'émotion cible
    animationProgress += (1 - animationProgress) * 0.1;
    
    // Couleur du visage (bleu marine comme l'identité Milo)
    const faceColor = "rgb(0, 0, 128)";
    
    // Dessiner les yeux
    drawEyes(config);
    
    // Dessiner les sourcils
    drawEyebrows(config);
    
    // Dessiner la bouche
    drawMouth(config);
    
    // Dessiner le nez (simple point)
    drawNose();
}

function drawEyes(config) {
    const eyeHeight = isBlinking ? 2 : config.eyeHeight * animationProgress + 35 * (1 - animationProgress);
    
    faceCtx.fillStyle = "rgb(0, 0, 128)";
    
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
        const pupilSize = 6;
        
        faceCtx.beginPath();
        faceCtx.arc(face.leftEye.x, face.leftEye.y, pupilSize, 0, 2 * Math.PI);
        faceCtx.fill();
        
        faceCtx.beginPath();
        faceCtx.arc(face.rightEye.x, face.rightEye.y, pupilSize, 0, 2 * Math.PI);
        faceCtx.fill();
    }
}

function drawEyebrows(config) {
    faceCtx.strokeStyle = "rgb(0, 0, 128)";
    faceCtx.lineWidth = 4;
    faceCtx.lineCap = "round";
    
    const browY = config.browY * animationProgress + (-80) * (1 - animationProgress);
    const angleRad = (config.browAngle * Math.PI / 180) * animationProgress;
    
    // Sourcil gauche
    faceCtx.beginPath();
    const leftStartX = face.leftBrow.x - face.browLength / 2;
    const leftEndX = face.leftBrow.x + face.browLength / 2;
    const leftStartY = face.leftBrow.y + browY - Math.tan(angleRad) * (face.browLength / 2);
    const leftEndY = face.leftBrow.y + browY + Math.tan(angleRad) * (face.browLength / 2);
    faceCtx.moveTo(leftStartX, leftStartY);
    faceCtx.lineTo(leftEndX, leftEndY);
    faceCtx.stroke();
    
    // Sourcil droit
    faceCtx.beginPath();
    const rightStartX = face.rightBrow.x - face.browLength / 2;
    const rightEndX = face.rightBrow.x + face.browLength / 2;
    const rightStartY = face.rightBrow.y + browY + Math.tan(angleRad) * (face.browLength / 2);
    const rightEndY = face.rightBrow.y + browY - Math.tan(angleRad) * (face.browLength / 2);
    faceCtx.moveTo(rightStartX, rightStartY);
    faceCtx.lineTo(rightEndX, rightEndY);
    faceCtx.stroke();
}

function drawMouth(config) {
    faceCtx.strokeStyle = "rgb(0, 0, 128)";
    faceCtx.lineWidth = 4;
    faceCtx.lineCap = "round";
    
    const mouthCurve = config.mouthCurve * animationProgress;
    
    faceCtx.beginPath();
    
    if (mouthCurve > 0) {
        // Sourire (arc vers le bas)
        faceCtx.arc(
            face.mouth.x,
            face.mouth.y - mouthCurve,
            face.mouthWidth / 2,
            0.2 * Math.PI,
            0.8 * Math.PI
        );
    } else if (mouthCurve < 0) {
        // Tristesse (arc vers le haut)
        faceCtx.arc(
            face.mouth.x,
            face.mouth.y - mouthCurve,
            face.mouthWidth / 2,
            0.8 * Math.PI,
            1.2 * Math.PI,
            true
        );
    } else {
        // Neutre (ligne droite)
        faceCtx.moveTo(face.mouth.x - face.mouthWidth / 2, face.mouth.y);
        faceCtx.lineTo(face.mouth.x + face.mouthWidth / 2, face.mouth.y);
    }
    
    faceCtx.stroke();
}

function drawNose() {
    faceCtx.fillStyle = "rgb(0, 0, 128)";
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