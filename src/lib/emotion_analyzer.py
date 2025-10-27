import ollama
import json
import re

EMOTION_PROMPT = """Tu es un analyseur d'émotions pour Milo, une IA étudiante à l'ECE Paris.

Analyse le texte suivant et détermine l'émotion dominante que Milo devrait exprimer.

Émotions disponibles : joyeux, triste, colere, pensif, neutre

Règles importantes :
- "joyeux" : réponses enthousiastes, positives, qui donnent des infos utiles
- "triste" : désolé, ne peut pas aider, manque d'information
- "colere" : refus, interdictions, sujets sensibles
- "pensif" : incertitude, réflexion, questions
- "neutre" : informations factuelles simples

Réponds UNIQUEMENT avec un JSON dans ce format exact (sans markdown) :
{
  "emotion": "joyeux",
  "intensite": 0.8
}

Texte à analyser :
"""

class EmotionAnalyzer:
    def __init__(self, model="granite3.1-dense:2b"):
        """
        Initialise l'analyseur d'émotions
        
        Args:
            model: Nom du modèle Ollama à utiliser
        """
        self.model = model
        self.default_emotion = {"emotion": "neutre", "intensite": 0.5}
        
        # Mapping des émotions alternatives vers les émotions standard
        self.emotion_mapping = {
            "confus": "pensif",
            "inquiet": "pensif",
            "heureux": "joyeux",
            "content": "joyeux",
            "fache": "colere",
            "enerve": "colere",
            "melancolique": "triste",
            "decu": "triste"
        }
    
    def clean_text_for_analysis(self, text: str) -> str:
        """Nettoie le texte avant analyse"""
        # Retire les caractères spéciaux qui pourraient perturber l'analyse
        text = re.sub(r'[^\w\s.,;:!?\'"àâäéèêëïîôùûüç-]', '', text, flags=re.IGNORECASE)
        return text.strip()
    
    def parse_emotion_response(self, raw_output: str) -> dict:
        """
        Parse la réponse du modèle et extrait le JSON
        
        Args:
            raw_output: Sortie brute du modèle
            
        Returns:
            Dict avec emotion et intensite
        """
        try:
            # Nettoie les balises markdown si présentes
            json_str = raw_output.strip()
            
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0]
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0]
            
            emotion_data = json.loads(json_str.strip())
            
            # Normalise l'émotion si nécessaire
            emotion = emotion_data.get("emotion", "neutre").lower()
            emotion = self.emotion_mapping.get(emotion, emotion)
            
            # Valide que l'émotion est dans la liste autorisée
            valid_emotions = ["joyeux", "triste", "colere", "pensif", "neutre"]
            if emotion not in valid_emotions:
                print(f"[EmotionAnalyzer] Émotion inconnue '{emotion}', utilisation de 'neutre'")
                emotion = "neutre"
            
            intensite = float(emotion_data.get("intensite", 0.5))
            intensite = max(0.0, min(1.0, intensite))  # Clamp entre 0 et 1
            
            return {
                "emotion": emotion,
                "intensite": intensite
            }
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"[EmotionAnalyzer] Erreur parsing : {e}")
            print(f"[EmotionAnalyzer] Réponse brute : {raw_output[:200]}")
            return self.default_emotion
    
    def analyze(self, text: str) -> dict:
        """
        Analyse l'émotion d'un texte
        
        Args:
            text: Texte à analyser (réponse de Milo)
            
        Returns:
            Dict avec emotion et intensite
        """
        if not text or len(text.strip()) < 3:
            return self.default_emotion
        
        cleaned_text = self.clean_text_for_analysis(text)
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": EMOTION_PROMPT + cleaned_text
                    }
                ],
                options={
                    "temperature": 0.3,  # Bas pour plus de cohérence
                    "num_predict": 100,   # Court pour juste le JSON
                    "top_p": 0.9
                }
            )
            
            raw_output = response["message"]["content"]
            emotion_data = self.parse_emotion_response(raw_output)
            
            print(f"[EmotionAnalyzer] Texte: '{text[:50]}...'")
            print(f"[EmotionAnalyzer] → Émotion: {emotion_data['emotion']} ({emotion_data['intensite']:.2f})")
            
            return emotion_data
            
        except Exception as e:
            print(f"[EmotionAnalyzer] Erreur lors de l'analyse : {e}")
            return self.default_emotion
    
    def analyze_from_file(self, file_path: str) -> dict:
        """
        Analyse l'émotion à partir d'un fichier texte
        
        Args:
            file_path: Chemin vers le fichier contenant la réponse de Milo
            
        Returns:
            Dict avec emotion et intensite
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return self.analyze(text)
        except FileNotFoundError:
            print(f"[EmotionAnalyzer] Fichier non trouvé : {file_path}")
            return self.default_emotion
        except Exception as e:
            print(f"[EmotionAnalyzer] Erreur lecture fichier : {e}")
            return self.default_emotion


# Instance globale
myEmotionAnalyzer = EmotionAnalyzer()