# Structured Extraction AI

_Documentation minimaliste de l'architecture du projet d'extraction d'informations par LLM._

## Aperçu du Projet

Ce projet permet l'extraction d'informations structurées (nom, âge, etc.) à partir de différentes sources de données non structurées :

- **Audio :** Fichiers vocaux (mp3, wav, ...)
- **Images :** Fichiers contenant du texte (png, jpg, ...)
- **Texte :** Fichiers textuels purs (txt, docx, ...)

Le système s'appuie sur l'API **Groq** (et des modèles comme `gpt-oss-20b`) pour analyser le contenu et renvoyer des données conformes à un modèle Pydantic.

---

## Core & Abstractions (`extractor.py`)

### Classe : `Extractor` (Abstract Base Class)

Classe de base gérant l'instanciation du client Groq et définissant le contrat pour les extracteurs spécifiques.

- `_make_prompt(**kwargs)` : Construit le prompt final pour l'IA en utilisant les arguments fournis.
- `_ask_ai(content: str)` : Méthode abstraite/générique pour envoyer la requête à l'API LLM.
- `extract_value(input: str | bytes, max_retry: int)` : Méthode principale pour traiter l'entrée et extraire le modèle JSON structuré.

---

## Les Extracteurs Spécifiques

### `textExtractor.py`

**Classe : `TextExtractor`**  
Hérite de `Extractor`. Spécialisé dans le traitement de chaînes de caractères. Surcharge `_ask_ai` pour communiquer avec le modèle IA (ex: openai/gpt-oss-20b) et force le format JSON.

### `audioExtractor.py`

**Classe : `AudioExtractor`**  
Hérite de `Extractor`. Prend un nom de fichier audio en entrée lors de l'instanciation pour transcrire ou analyser le contenu audio.

### `imageExtractor.py`

**Classe : `ImageExtractor`**  
Hérite de `Extractor`. Gère l'extraction d'informations à partir d'images. S'instancie avec l'extension de fichier (`file_extension`) et traite le contenu binaire (bytes) pour l'envoyer à un modèle de vision via l'API.

---

## Utilitaires & Modèles

### `filter.py`

Contient la logique de routage du fichier selon son type MIME (via `python-magic`).

- **Enum `InputType`** : Définit les types supportés : `TEXT`, `AUDIO`, `IMAGE`.
- **`get_input_type(path) -> InputType`** : Retourne l'énumération correspondante en fonction du type MIME du fichier.

### `person.py`

Modèle de données cible utilisant **Pydantic**.

- **Classe : `Person(BaseModel)`**
  - `name: str | None`
  - `age: PositiveInt | None`
