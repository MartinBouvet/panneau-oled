from faster_whisper import WhisperModel
from pathlib import Path
import time
import os

from lib import file_manager
from lib import message_queue

class Transcriber:

    def __init__(self, model_size="medium", device="cpu", compute_type="int8"):
        """
        Initialise le transcripteur
        
        IMPORTANT : 
        - device="cpu" par défaut pour compatibilité Mac (change en "cuda" si GPU disponible)
        - compute_type="int8" pour Mac (utilise "int8_float16" sur GPU)
        """
        self._model_size = model_size
        self._device = device
        self._compute_type = compute_type
        self._model = None
        
        # Chemins des dossiers
        self._output_dir = file_manager.transcript_dir
        self._output_dir.mkdir(exist_ok=True, parents=True)

        self._audio_dir = file_manager.wav_dir
        self._audio_dir.mkdir(exist_ok=True, parents=True)
        
        print(f"[Transcriber] Initialisation avec modèle={model_size}, device={device}")

    def setModelSize(self, model_size):
        self._model_size = model_size

    def setOutputDir(self, output_dir):
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(exist_ok=True, parents=True)

    def setAudioDir(self, audio_dir):
        self._audio_dir = Path(audio_dir)
        self._audio_dir.mkdir(exist_ok=True, parents=True)

    def setup_model(self, model_size, output_dir, audio_dir):
        self.setModelSize(model_size)
        self.setOutputDir(output_dir)
        self.setAudioDir(audio_dir)

    def load_model(self):
        """Charge le modèle Whisper avec gestion d'erreur"""
        if self._model is not None:
            print("[Transcriber] ✅ Modèle déjà chargé")
            return
            
        print(f"[Transcriber] 📥 Téléchargement/chargement du modèle {self._model_size}...")
        print(f"[Transcriber] ⏳ Première fois = téléchargement (~1.5GB), patience...")
        
        try:
            # SOLUTION : Utilise le modèle de Guillaumekln (créateur de faster-whisper)
            # au lieu de Systran qui bloque l'accès
            model_name = f"guillaumekln/faster-whisper-{self._model_size}"
            
            self._model = WhisperModel(
                model_name,
                device=self._device, 
                compute_type=self._compute_type,
                download_root=None,  # Utilise le cache par défaut
                local_files_only=False
            )
            print("[Transcriber] ✅ Modèle chargé avec succès !")
            
        except Exception as e:
            print(f"[Transcriber] ❌ Erreur lors du chargement du modèle : {e}")
            print(f"[Transcriber] 💡 Essai avec le modèle par défaut...")
            
            # Fallback : essaie sans spécifier le dépôt
            try:
                self._model = WhisperModel(
                    self._model_size,
                    device=self._device,
                    compute_type=self._compute_type,
                    local_files_only=False
                )
                print("[Transcriber] ✅ Modèle chargé avec le fallback !")
            except Exception as e2:
                print(f"[Transcriber] ❌ ÉCHEC CRITIQUE : {e2}")
                print(f"[Transcriber] 📖 Solutions :")
                print(f"   1. Utilise un modèle plus petit : model_size='base'")
                print(f"   2. Télécharge manuellement : huggingface-cli download guillaumekln/faster-whisper-medium")
                raise

    def clearTransciptDir(self):
        if not self._output_dir.exists():
            print(f"Folder {self._output_dir} don't exist.")
            return

        file_count = 0
        for file in self._output_dir.iterdir():
            if file.is_file():
                try:
                    file.unlink()
                    file_count += 1
                except Exception as e:
                    print(f"Error: {file.name} : {e}")

        print(f"{file_count} file deleted from {self._output_dir}")

    def transcribe_all_files(self):
        audio_files = list(self._audio_dir.glob("*.wav"))
        if not audio_files:
            print(f"No audio file found in dir : {self._audio_dir}")
            return

        for audio_path in audio_files:
            self.transcribe_file(audio_path)

    def transcribe_file(self, audio_path, output_dir=None):
        # Charge le modèle si nécessaire
        if self._model is None:
            print("[Transcriber] Modèle non chargé, chargement...")
            self.load_model()
        
        audio_path = Path(audio_path)

        if output_dir is not None:
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True, parents=True)
        else:
            output_dir = self._output_dir

        output_path = output_dir / (audio_path.stem + ".txt")

        if output_path.exists():
            print(f"{output_path.name} already exist, pass")
            return output_path.name

        print(f"[Transcriber] 🎤 Transcription de : {audio_path.name}")
        start_time = time.time()

        try:
            segments, info = self._model.transcribe(str(audio_path), beam_size=5)

            print(f"[Transcriber] 🌍 Langue détectée : {info.language} (confiance: {info.language_probability:.2f})")

            with open(output_path, "w", encoding="utf-8") as f:
                for segment in segments:
                    start = segment.start
                    end = segment.end
                    text = segment.text.strip()
                    f.write(f"[{start:.2f} - {end:.2f}] {text}\n")

            delta = time.time() - start_time
            print(f"[Transcriber] ✅ Sauvegardé : {output_path}")
            print(f"[Transcriber] ⏱️  Temps : {delta:.2f}s")

        except Exception as e:
            print(f"[Transcriber] ❌ Erreur de transcription : {e}")
            raise

        return output_path.name


myTranscrib = Transcriber(model_size="base", device="cpu")