import ollama
import json

# Télécharge le modèle (à faire une seule fois)
# ollama pull granite3.1-dense:2b

EMOTION_PROMPT = """Tu es un analyseur d'émotions. Analyse le texte suivant et détermine l'émotion dominante.

Émotions possibles : joyeux, triste, colere, pensif, neutre

Réponds UNIQUEMENT avec un JSON dans ce format exact :
{
  "emotion": "joyeux",
  "intensite": 0.8,
  "raison": "courte explication"
}

Texte à analyser :
"""

def analyze_emotion(text):
    """Analyse l'émotion d'un texte avec Granite"""
    
    response = ollama.chat(
        model="granite3.1-dense:2b",
        messages=[
            {
                "role": "user",
                "content": EMOTION_PROMPT + text
            }
        ],
        options={
            "temperature": 0.3,  # Bas pour plus de cohérence
            "num_predict": 150
        }
    )
    
    raw_output = response["message"]["content"]
    print(f"\n🤖 Réponse brute du modèle :\n{raw_output}\n")
    
    # Extraction du JSON (nettoyage des markdown)
    try:
        # Retire les balises markdown si présentes
        json_str = raw_output.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0]
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0]
        
        emotion_data = json.loads(json_str.strip())
        return emotion_data
    except json.JSONDecodeError as e:
        print(f"❌ Erreur parsing JSON : {e}")
        return {"emotion": "neutre", "intensite": 0.5, "raison": "erreur parsing"}


# Tests avec différents types de réponses
test_cases = [
    "Super ! L'ECE Paris propose 4 Bachelors en tech : Cyber & Reseaux, DevOps & Cloud, Developpement d'Applications et Developpement en IA. Tu peux les faire en initial ou en alternance des la 3e annee !",
    
    "Hmm, je ne suis pas sure de bien comprendre ta question. Tu peux reformuler s'il te plait ?",
    
    "Desolé, mais je ne peux pas repondre aux questions sur la politique. C'est un sujet que j'evite. Je peux t'aider avec autre chose ?",
    
    "Excellente question ! Le directeur de l'ECE Paris est Francois Stephan. Il dirige l'ecole avec passion.",
    
    "Ah zut, je n'ai pas cette information dans ma base de donnees pour le moment. Ca m'embete de ne pas pouvoir t'aider la-dessus."
]

print("="*60)
print("🧪 TEST DE L'ANALYSEUR D'ÉMOTIONS")
print("="*60)

for i, test_text in enumerate(test_cases, 1):
    print(f"\n📝 Test {i}/{len(test_cases)}")
    print(f"Texte : {test_text[:80]}...")
    
    result = analyze_emotion(test_text)
    
    print(f"✨ Émotion détectée : {result['emotion']}")
    print(f"📊 Intensité : {result['intensite']}")
    print(f"💭 Raison : {result['raison']}")
    print("-"*60)

print("\n✅ Tests terminés !")