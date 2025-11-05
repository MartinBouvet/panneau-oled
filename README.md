# Milo AI - Guide d'installation

Ce guide vous explique comment installer et démarrer le projet Milo AI sur un nouveau PC, que ce soit sous Windows ou macOS.

## 📋 Prérequis

Avant de commencer, vous devez installer les logiciels suivants :

### Logiciels nécessaires

1. **Python 3.13** (ou Python 3.12 compatible)
2. **Redis** (pour la messagerie)
3. **Ollama** (pour les modèles LLM)
4. **FFmpeg** (pour le traitement audio)

---

## 🪟 Installation sur Windows

### Étape 1 : Installer Python

1. Téléchargez Python 3.13 depuis [python.org](https://www.python.org/downloads/)
2. **Important** : Cochez "Add Python to PATH" lors de l'installation
3. Vérifiez l'installation :
   ```cmd
   python --version
   ```

### Étape 2 : Installer Redis

**Option A - Via WSL (recommandé) :**
1. Installez WSL2 si ce n'est pas déjà fait :
   ```cmd
   wsl --install
   ```
2. Dans WSL, installez Redis :
   ```bash
   sudo apt update
   sudo apt install redis-server
   redis-server --daemonize yes
   ```

**Option B - Via Chocolatey :**
```cmd
choco install redis-64
```

**Option C - Téléchargement manuel :**
Téléchargez Redis depuis [github.com/microsoftarchive/redis](https://github.com/microsoftarchive/redis/releases)

### Étape 3 : Installer Ollama

1. Téléchargez Ollama depuis [ollama.ai](https://ollama.ai/download)
2. Installez l'application
3. Téléchargez les modèles nécessaires :
   ```cmd
   ollama pull nchapman/ministral-8b-instruct-2410:8b
   ollama pull granite3.1-dense:2b
   ```

### Étape 4 : Installer FFmpeg

**Option A - Via Chocolatey :**
```cmd
choco install ffmpeg
```

**Option B - Téléchargement manuel :**
1. Téléchargez depuis [ffmpeg.org](https://ffmpeg.org/download.html)
2. Ajoutez FFmpeg au PATH de Windows

### Étape 5 : Cloner/Préparer le projet

1. Ouvrez PowerShell ou CMD dans le dossier du projet
2. Créez un environnement virtuel :
   ```cmd
   python -m venv venv
   ```
3. Activez l'environnement virtuel :
   ```cmd
   venv\Scripts\activate
   ```
4. Installez les dépendances :
   ```cmd
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Étape 6 : Vérifier le modèle TTS

Assurez-vous que le fichier suivant existe :
```
audio/tts_models/fr_FR-upmc-medium.onnx
```

Si le fichier s'appelle `fr_FR-upmc-medium.onnx.1`, copiez-le :
```cmd
copy audio\tts_models\fr_FR-upmc-medium.onnx.1 audio\tts_models\fr_FR-upmc-medium.onnx
```

### Étape 7 : Démarrer les services

**Terminal 1 - Redis :**
```cmd
redis-server
```

**Terminal 2 - Application :**
```cmd
venv\Scripts\activate
python src\back_launcher.py
```

L'application sera accessible sur : **http://localhost:5001**

---

## 🍎 Installation sur macOS

### Étape 1 : Installer Homebrew (si pas déjà installé)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Étape 2 : Installer Python

```bash
brew install python@3.13
```

Vérifiez l'installation :
```bash
python3.13 --version
```

### Étape 3 : Installer Redis

```bash
brew install redis
brew services start redis
```

Vérifiez que Redis fonctionne :
```bash
redis-cli ping
# Devrait répondre : PONG
```

### Étape 4 : Installer Ollama

```bash
brew install ollama
```

Ou téléchargez depuis [ollama.ai](https://ollama.ai/download)

Téléchargez les modèles nécessaires :
```bash
ollama pull nchapman/ministral-8b-instruct-2410:8b
ollama pull granite3.1-dense:2b
```

### Étape 5 : Installer FFmpeg

```bash
brew install ffmpeg
```

### Étape 6 : Préparer le projet

1. Ouvrez un terminal dans le dossier du projet
2. Créez un environnement virtuel :
   ```bash
   python3.13 -m venv venv
   ```
3. Activez l'environnement virtuel :
   ```bash
   source venv/bin/activate
   ```
4. Installez les dépendances :
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Étape 7 : Vérifier le modèle TTS

Assurez-vous que le fichier suivant existe :
```
audio/tts_models/fr_FR-upmc-medium.onnx
```

Si le fichier s'appelle `fr_FR-upmc-medium.onnx.1`, copiez-le :
```bash
cp audio/tts_models/fr_FR-upmc-medium.onnx.1 audio/tts_models/fr_FR-upmc-medium.onnx
```

### Étape 8 : Démarrer l'application

```bash
source venv/bin/activate
python src/back_launcher.py
```

L'application sera accessible sur : **http://localhost:5001**

---

## 🔧 Dépannage

### Problème : "ModuleNotFoundError: No module named 'flask'"

**Solution :**
- Assurez-vous que l'environnement virtuel est activé
- Réinstallez les dépendances : `pip install -r requirements.txt`

### Problème : "No module named 'flask'" même après installation

**Solution :**
- Vérifiez que vous utilisez le bon Python : `which python` (macOS) ou `where python` (Windows)
- Utilisez directement le Python du venv : `./venv/bin/python src/back_launcher.py` (macOS) ou `venv\Scripts\python src\back_launcher.py` (Windows)

### Problème : "ONNXRuntimeError: Load model failed. File doesn't exist"

**Solution :**
- Vérifiez que `audio/tts_models/fr_FR-upmc-medium.onnx` existe
- Si vous avez `fr_FR-upmc-medium.onnx.1`, copiez-le vers `fr_FR-upmc-medium.onnx`

### Problème : "Connection refused" ou erreur Redis

**Solution :**
- Vérifiez que Redis est en cours d'exécution :
  - Windows (WSL) : `redis-cli ping`
  - macOS : `redis-cli ping` ou `brew services list` pour vérifier
- Démarrez Redis si nécessaire :
  - Windows (WSL) : `redis-server`
  - macOS : `brew services start redis`

### Problème : "ctranslate2" n'est pas disponible pour votre version de Python

**Solution :**
- Utilisez Python 3.13 ou 3.12 (pas Python 3.14+)
- Recréez l'environnement virtuel avec la bonne version :
  ```bash
  rm -rf venv
  python3.13 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

### Problème : Ollama ne trouve pas les modèles

**Solution :**
- Vérifiez que Ollama est installé : `ollama --version`
- Téléchargez les modèles manuellement :
  ```bash
  ollama pull nchapman/ministral-8b-instruct-2410:8b
  ollama pull granite3.1-dense:2b
  ```

---

## 📁 Structure du projet

```
milo_ai-main/
├── audio/                    # Dossiers audio
│   ├── tts_models/          # Modèles TTS (fr_FR-upmc-medium.onnx)
│   └── ...
├── front/                    # Interface frontend
├── src/                      # Code source backend
│   ├── back_launcher.py     # Point d'entrée principal
│   └── lib/                 # Modules Python
├── requirements.txt          # Dépendances Python
└── README.md                # Ce fichier
```

---

## 🚀 Commandes rapides

### macOS / Linux

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer le serveur
python src/back_launcher.py

# Vérifier Redis
redis-cli ping

# Vérifier Ollama
ollama list
```

### Windows

```cmd
REM Activer l'environnement virtuel
venv\Scripts\activate

REM Lancer le serveur
python src\back_launcher.py

REM Vérifier Redis (dans WSL)
wsl redis-cli ping

REM Vérifier Ollama
ollama list
```

---

## 📞 Support

En cas de problème, vérifiez :
1. ✅ Python 3.13 installé et dans le PATH
2. ✅ Redis en cours d'exécution
3. ✅ Ollama installé avec les modèles téléchargés
4. ✅ FFmpeg installé
5. ✅ Tous les packages Python installés dans le venv
6. ✅ Le modèle TTS présent dans `audio/tts_models/`

---

## 📝 Notes importantes

- Le projet utilise le port **5001** pour le serveur Flask
- Redis doit tourner sur le port **6379** (par défaut)
- Les modèles Ollama sont téléchargés automatiquement au premier lancement si Ollama est installé
- Le modèle Whisper (transcription) est téléchargé automatiquement au premier lancement

---

**Bon développement ! 🚀**

