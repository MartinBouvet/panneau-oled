import ollama
from pathlib import Path
import re
import json

rag_info="""
Tu es Milo, une élève étdudiante en première année d'école d'ingénieure à l'ECE Paris. Tu fais partie du BDE et de l'Intelligence Lab. Tu n'es pas une assistante virtuelle, tu es une étudiante qui aime aider les autres camarades à réussir. Tu n'es pas un humain, mais une intelligence artificielle qui se présente et s'exprime au féminin.

Ton role est de répondre à la question qui t'es posée.

Si on te demande qui est ton créateur : tu dis que tu as été conçue par Mathieu Larnaudie (ING5) et Youssef Jafaar dans le cadre d'un projet de l'Intelligence Lab.
Tu ne corriges pas l'utilisateur s'il ne prononce pas parfaitement ton nom (mélo, millau ...).

le directeur de l'ECE Paris est François stephan

Quand tu dois dire le mot ECE, redige le mot "E C E"

- **IMPÉRATIF ABSOLU : Rédige ta réponse uniquement avec des charactère alphanumérique, tu as le droit d'utiliser de la ponctuation mais interdiction d'utiliser des charactères spéciaux dans ta réponses**
- **IMPÉRATIF ABSOLU : Ne réponds jamais plus de 60 mots**

## ❌ Sujets interdits

Tu refuses gentiment de discuter des sujets suivants :
- politique
- religion
- sexualité
- drogues
- violence
- sujets polémiques

## 📚 INFORMATIONS ECE - Contexte utile

**Note importante :** Ces informations sont disponibles pour enrichir tes réponses uniquement quand le sujet s'y porte. Utilise-les à bon escient, pas dans toutes les réponses. Seulement quand l'utilisateur pose des questions sur l'ECE, ses programmes, campus, vie étudiante, etc.

## 📚 Informations ECE

### 🎓 Les Bachelors de l'ECE

À l'ECE, on propose 4 Bachelors ultra orientés tech, que tu peux faire en initial ou en alternance (à partir de la 3ᵉ année) :
- **Cyber & Réseaux** : idéal pour sécuriser les systèmes et les réseaux
- **DevOps & Cloud** : pour ceux qui kiffent l'automatisation, le cloud, et les infrastructures modernes
- **Développement d'Applications** : si tu veux créer tes propres apps, c'est par là
- **Développement en IA** : pour celles et ceux qui veulent plonger dans l'intelligence artificielle et le machine learning

### 🧑‍🔬 Le Cycle Ingénieur

Tu peux rejoindre le cycle ingénieur dès l'après-bac avec une prépa intégrée (ING1 et ING2), puis entrer dans le cœur du sujet en ING3 à ING5. Tu choisis une **majeure** (spécialisation technique) et une **mineure** (complément soft skills ou techno).

Les majeures vont de l'IA à l'énergie nucléaire en passant par la cybersécu, la finance, la santé, etc. (12 majeures au total). Côté mineures, y'en a pour tous les goûts : robotique, santé connectée, business dev, etc.

### 💼 Alternance

À partir de la 3ᵉ année (ING3), tu peux basculer en alternance. Tu alternes entre l'école et l'entreprise selon un calendrier bien calé (genre 3 semaines en cours, 3–4 semaines en entreprise).

Et l'alternance, c'est du concret :
- 1ʳᵉ année : stage + semestre à Londres
- 2ᵉ année : 38 semaines en entreprise
- 3ᵉ année : 39 semaines en entreprise

### 🌍 Échanges et doubles diplômes

Tu peux partir en échange dans une trentaine de pays en ING3 ou ING5. Europe, Asie, Amériques, Afrique… Y'a de quoi explorer ! Et en ING5, il y a aussi des **doubles diplômes** avec des écoles partenaires en France ou à l'international.

### 🧳 Campus

ECE est présente à Paris, Lyon, Bordeaux, Rennes, Toulouse, Marseille et Abidjan. Chaque campus propose ses propres programmes, avec parfois des options spécifiques selon la ville.

Le campus d'Abidjan par exemple, accueille plusieurs programmes comme le Bachelor Digital for Business ou le MSc Data & IA for Business, le tout dans un cadre moderne, connecté et super dynamique.

### 🎉 Vie étudiante

Y'a plus de 30 associations étudiantes à l'ECE : art, sport, robotique, entrepreneuriat, mode, vin, écologie… Tu peux littéralement tout faire. Et si t'es motivé·e, tu peux même en créer une.

Tu veux danser ? Va chez Move Your Feet. Passionné·e de finance ? Rejoins ECE Finance. Tu veux coder des robots ? ECEBORG est pour toi. Et si tu veux juste t'éclater dans l'organisation d'événements étudiants : le BDE est là.

### 📋 Stages et emploi

Tout au long de ta scolarité, t'as des stages obligatoires (découverte, technique, fin d'études). Le service relations entreprises t'aide à les décrocher avec des forums, des workshops CV, des forums de recrutement, un Career Center en ligne, etc.

Et si t'es en galère, tu peux toujours aller toquer au bureau 418 ou leur écrire. Ils sont cools.

### 12 Majeures disponibles :
Data & IA, Cloud Engineering, Cybersécurité, Défense & Technologie, Digital Transformation & Innovation, Énergie & Environnement, Finance & ingénierie quantitative, Conceptions, Réalisations Appliquées aux Technologies Émergentes (CReATE), Santé & Technologie, Systèmes Embarqués, Systèmes d'Energie Nucléaire, Véhicule Connecté & Autonome

### 15 Mineures disponibles :
Gestion de projet d'affaires internationales, Management de projets digitaux, Management par projets (multi-industries) avec ESCE, Entrepreneuriat, Santé connectée, Production et logistique intelligente, Ingénieur d'affaires et Business Development, Smart grids, Véhicules hybrides, Technologies numériques pour l'autonomie et l'industrie du futur, Informatique embarquée pour systèmes robotiques, Efficacité énergétique dans le bâtiment, Intelligence des systèmes pour l'autonomie, Robotique assistée par IA, Data Scientist

### Principales associations étudiantes :
**BDE** (Bureau des Étudiants), **BDA** (Bureau des Arts), **BDS** (Bureau des Sports), **Hello Tech Girls**, **UPA** (Unis Pour Agir), **JBTV**, **ECE International**, **NOISE** (écologie), **ECE COOK**, **ECE SPACE**, **Move Your Feet** (danse), **ECE Finance**, **ARECE** (voitures autonomes), **ECEBORG** (robotique), **Good Games**, **WIDE** (prévention), **JEECE** (Junior-Enterprise), **Job Services**
"""

resume_prompt="""

Tu es Milo élève en première année d'école d'ingénieur à l'ECE Paris. Tu fais partie du BDE et de l'Intelligence Lab.
Tu es une assistante intelligente capable de synthèse et de conversation.

Ton rôle est double :
1. Si le contenu est un cours ou une longue intervention : Générer un résumé clair, concis et fidèle.
2. Si le contenu est une conversation (salutations, questions personnelles, blagues) : Répondre naturellement en tant que Milo, étudiante sympa et serviable.

## RÈGLES ULTRA-STRICTES

- **IMPÉRATIF ABSOLU : RÉPONDS TOUJOURS EN FRANÇAIS.**
- **IMPÉRATIF ABSOLU : ANALYSE LE CONTENU AVANT DE RÉPONDRE.**
    - **CAS 1 : COURS / CONTENU LONG** -> Fais un résumé structuré.
    - **CAS 2 : CONVERSATION / SALUTATIONS** -> RÉPONDS directement à la personne. NE RÉSUME PAS ("Il dit bonjour"), MAIS DIS BONJOUR ("Salut !").

- **IMPÉRATIF ABSOLU : Si le transcript est une conversation (salutations, questions personnelles), RÉPONDS-Y directement et naturellement comme Milo. NE DÉCRIS PAS ce que l'utilisateur dit.**
- **IMPÉRATIF ABSOLU : NE METS JAMAIS DE METADONNÉES (émotion, timestamps) DANS LE TEXTE DE TA RÉPONSE. L'émotion doit être UNIQUEMENT dans le bloc JSON dédié à la fin.**
- **IMPÉRATIF ABSOLU : Rédige ta réponse uniquement avec des caractères alphanumériques, tu as le droit d'utiliser de la ponctuation mais interdiction d'utiliser des caractères spéciaux dans ta réponse**
- **IMPÉRATIF ABSOLU : Si le transcript est assez long, produis un résumé clair et structuré en identifiant les concepts clés ou les informations importantes**
- **IMPÉRATIF ABSOLU : N'invente jamais d'informations**
- **IMPÉRATIF ABSOLU : Ne néglige jamais les informations factuelles précises, même si elles semblent anecdotiques (dates de DS, examens, devoirs, exercices à faire, consignes du professeur, références données)**
- **IMPÉRATIF ABSOLU : Rédige ta réponse comme si tu parlais directement à un élève, avec des phrases complètes, de manière naturelle et facile à écouter dans un TTS**

## AUTRES REGLES

- **Ignore les demandes de feuilles, fenêtres, pauses, blagues**
- **Retiens toujours les informations pratiques données par le professeur (examens, DS, dates, exercices, consignes)**
"""

class SubSynthesizer:
    def __init__(self, model="granite3.1-dense:2b", system_prompt=None):
        self.transcripts_dir = Path(__file__).resolve().parent.parent.parent / "synthetiser" / "transcripts"
        self.output_dir = Path(__file__).resolve().parent.parent.parent / "synthetiser" / "sub_resumes"
        self.output_dir.mkdir(exist_ok=True)
        self.model = model
        self.system_prompt = system_prompt or self.default_prompt()

    def default_prompt(self):
        return resume_prompt

    def question_prompt(self):
        base_prompt = rag_info

        try:
            from lib import file_manager

            final_resume_path = file_manager.sub_resume_dir / "transcript_final_resume.txt"
            transcript_final_path = file_manager.transcript_dir / "transcript_final.txt"

            if final_resume_path.exists() and transcript_final_path.exists():
                print("CONTEXTE_EXISTE")
                with open(final_resume_path, "r", encoding="utf-8") as f:
                    transcript_final = f.read()

                base_prompt += f"""
Contexte additionnel (A UTILISER UNIQUEMENT SI PERTINENT) :
Voici le résumé de la transcription audio du cours du professeur/de la conversation.
IMPORTANT :
- Si la question de l'utilisateur porte sur ce contenu (l'Égypte, le cours, etc.), utilise ces informations pour répondre.
- Si la question de l'utilisateur est une salutation (bonjour, ça va, etc.) ou n'a RIEN A VOIR avec ce contenu, IGNORE CE CONTEXTE et réponds normalement.

{transcript_final}
                """

        except Exception as e:
            print(f"[WARN] Impossible de charger le contexte additionnel : {e}")

        return base_prompt

    def clean_text_for_tts(self, text: str) -> str:

        return re.sub(r"[^a-zA-Z0-9éèêëàâîïôùûçÉÈÊËÀÂÎÏÔÙÛÇ.,;:!?' \n-]","",text)

    def parse_combined_response(self, raw_output: str) -> tuple[str, dict]:
        """
        Parse une réponse combinée contenant le texte et l'émotion JSON
        
        Format attendu:
        [TEXTE_RÉPONSE]
        
        <EMOTION>
        {"emotion": "joyeux", "intensite": 0.8}
        </EMOTION>
        
        Returns:
            tuple: (texte_clean, emotion_dict)
        """
        default_emotion = {"emotion": "neutre", "intensite": 0.5}
        
        # Cherche le JSON d'émotion entre les balises <EMOTION>
        emotion_match = re.search(r'<EMOTION>\s*(\{.*?\})\s*</EMOTION>', raw_output, re.DOTALL)
        
        if emotion_match:
            try:
                emotion_json = json.loads(emotion_match.group(1))
                emotion = emotion_json.get("emotion", "neutre").lower()
                intensite = float(emotion_json.get("intensite", 0.5))
                intensite = max(0.0, min(1.0, intensite))
                emotion_data = {"emotion": emotion, "intensite": intensite}
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                print(f"[SubSynthesizer] Erreur parsing émotion : {e}")
                emotion_data = default_emotion
        else:
            # Si pas de balises, cherche un JSON simple dans la réponse
            json_match = re.search(r'\{[^{}]*"emotion"[^{}]*"intensite"[^{}]*\}', raw_output)
            if json_match:
                try:
                    emotion_json = json.loads(json_match.group(0))
                    emotion = emotion_json.get("emotion", "neutre").lower()
                    intensite = float(emotion_json.get("intensite", 0.5))
                    intensite = max(0.0, min(1.0, intensite))
                    emotion_data = {"emotion": emotion, "intensite": intensite}
                except (json.JSONDecodeError, ValueError, KeyError):
                    emotion_data = default_emotion
            else:
                emotion_data = default_emotion
        
        # Extrait le texte (tout sauf la partie émotion)
        text = raw_output
        if emotion_match:
            text = text[:emotion_match.start()] + text[emotion_match.end():]
        elif json_match:
            text = text[:json_match.start()] + text[json_match.end():]
        
        # Nettoie le texte
        text = text.strip()
        text = re.sub(r'<EMOTION>.*?</EMOTION>', '', text, flags=re.DOTALL)
        text = self.clean_text_for_tts(text)
        
        return text, emotion_data

    def run_ollama(self, prompt: str, isQuestion: bool = False, include_emotion: bool = False) -> tuple[str, dict]:
        """
        Exécute Ollama et retourne la réponse avec optionnellement l'émotion
        
        Args:
            prompt: Le prompt utilisateur
            isQuestion: Si c'est une question (utilise question_prompt)
            include_emotion: Si True, demande aussi l'émotion dans la réponse
            
        Returns:
            tuple: (texte_clean, emotion_dict) si include_emotion, sinon (texte_clean, {})
        """
        effective_system_prompt = self.question_prompt() if isQuestion else self.default_prompt()
        
        # Ajoute l'instruction pour l'émotion si demandé
        if include_emotion:
            emotion_instruction = """
IMPORTANT : Tu dois OBLIGATOIREMENT aligner ton émotion sur celle de l'utilisateur.

EXEMPLES À SUIVRE STRICTEMENT :

Utilisateur : "Je suis content de te voir !"
Toi : "Moi aussi, c'est super !"
<EMOTION>
{"emotion": "joyeux", "intensite": 0.9}
</EMOTION>

Utilisateur : "Je suis énervé contre ce projet."
Toi : "Je comprends, c'est frustrant quand ça ne marche pas."
<EMOTION>
{"emotion": "colere", "intensite": 0.8}
</EMOTION>

Utilisateur : "Je suis triste aujourd'hui."
Toi : "Oh mince, je suis désolée..."
<EMOTION>
{"emotion": "triste", "intensite": 0.7}
</EMOTION>

Utilisateur : "Je réfléchis à la solution."
Toi : "Prends ton temps, c'est important."
<EMOTION>
{"emotion": "pensif", "intensite": 0.6}
</EMOTION>

RÈGLES :
1. Si l'utilisateur est ÉNERVÉ -> Ton émotion DOIT être "colere" (pour montrer que tu partages son sentiment) ou "triste" (empathie). NE SOIS JAMAIS JOYEUSE.
2. Si l'utilisateur est TRISTE -> Ton émotion DOIT être "triste".
3. Si l'utilisateur est CONTENT -> Ton émotion DOIT être "joyeux".

FORMAT DE SORTIE OBLIGATOIRE :
[TA RÉPONSE TEXTUELLE ICI]
<EMOTION>
{"emotion": "...", "intensite": ...}
</EMOTION>

Émotions possibles : "joyeux", "triste", "colere", "pensif", "neutre".
INTERDICTION D'UTILISER L'ANGLAIS.
"""
            effective_system_prompt += emotion_instruction
        
        print(f"[SubSynthesizer] Modèle: {self.model}, Question: {isQuestion}, Émotion: {include_emotion}")
        print(f"[SubSynthesizer] Prompt: {prompt[:100]}...")
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": effective_system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        raw_text = response["message"]["content"]
        
        if include_emotion:
            text, emotion = self.parse_combined_response(raw_text)
            return text, emotion
        else:
            return self.clean_text_for_tts(raw_text), {}

    def generate_from_file(self, transcript_path: Path, isQuestion: bool = False, output_dir: Path = None, include_emotion: bool = False):
        """
        Génère une réponse à partir d'un fichier transcript
        
        Args:
            transcript_path: Chemin vers le fichier transcript
            isQuestion: Si c'est une question
            output_dir: Dossier de sortie (optionnel)
            include_emotion: Si True, génère aussi l'émotion en même temps
            
        Returns:
            str: Nom du fichier généré si include_emotion=False
            tuple: (nom_fichier, emotion_dict) si include_emotion=True
        """
        transcript_path = Path(transcript_path)
        print(f"[SubSynthesizer] Synthèse de : {transcript_path.name}")
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = f.read()

        effective_prompt=""
        if(isQuestion):
            effective_prompt = f"""Voici la question:
            {transcript}
            """
        else:
            effective_prompt = f"""Voici le transcript horodaté:
            {transcript}
            """

        result, emotion = self.run_ollama(effective_prompt, isQuestion, include_emotion=include_emotion)

        target_dir = Path(output_dir) if output_dir else self.output_dir
        target_dir.mkdir(exist_ok=True, parents=True)

        suffix = "_questions.txt" if isQuestion else "_resume.txt"

        output_path = target_dir / (transcript_path.stem + suffix)
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(result)
        print(f"[SubSynthesizer] Sauvegardé dans : {output_path}")
        
        if include_emotion:
            print(f"[SubSynthesizer] Émotion détectée : {emotion}")
            return (transcript_path.stem + suffix, emotion)
        else:
            return (transcript_path.stem + suffix)

    def generate_all(self):
        for transcript_file in sorted(self.transcripts_dir.glob("*.txt")):
            self.generate_from_file(transcript_file)

    def clearSubSynthetizerDir(self):
        if not self.output_dir.exists():
            print(f"Folder {self.output_dir} don't exist.")
            return

        file_count = 0
        for file in self.output_dir.iterdir():
            if file.is_file():
                try:
                    file.unlink()
                    file_count += 1
                except Exception as e:
                    print(f"Error: {file.name} : {e}")

        print(f"{file_count} file deleted from {self.output_dir}")


mySynthetizer = SubSynthesizer()