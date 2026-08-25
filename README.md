<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation - Structured Extraction AI</title>
</head>
<body>

<div class="container">
    <header>
        <h1>Structured Extraction AI</h1>
        <p class="intro">Documentation minimaliste de l'architecture du projet de LLM information extraction.</p>
    </header>

    <div class="module">
        <h2>Aperçu du Projet</h2>
        <p>Ce projet permet l'extraction d'informations structurées (nom, âge, etc.) à partir de différentes sources de données non structurées :</p>
        <ul>
            <li><strong>Audio :</strong> Fichiers vocaux (mp3, wav, ...)</li>
            <li><strong>Images :</strong> Fichiers contenant du texte (png, jpg, ...)</li>
            <li><strong>Texte :</strong> Fichiers textuels purs (txt, docx, ...)</li>
        </ul>
        <p>Le système s'appuie sur l'API <strong>Groq</strong> (et des modèles comme gpt-oss-20b) pour analyser le contenu et renvoyer des données conformes à un modèle Pydantic.</p>
    </div>

    <div class="module">
        <h2>Core & Abstractions (<code>extractor.py</code>)</h2>
        <p><span class="class-name">Classe: Extractor (Abstract Base Class)</span></p>
        <p>Classe de base gérant l'instanciation du client Groq et définissant le contrat pour les extracteurs spécifiques.</p>
        <div class="method">
            <span class="method-name">_make_prompt(**kwargs)</span>
            <p>Construit le prompt final pour l'IA en utilisant les arguments fournis.</p>
        </div>
        <div class="method">
            <span class="method-name">_ask_ai(content: str)</span>
            <p>Méthode abstraite/générique pour envoyer la requête à l'API LLM.</p>
        </div>
        <div class="method">
            <span class="method-name">extract_value(input: str | bytes, max_retry: int)</span>
            <p>Méthode principale pour traiter l'entrée et extraire le modèle JSON structuré.</p>
        </div>
    </div>

    <div class="module">
        <h2>Les Extracteurs Spécifiques</h2>

        <h3><code>textExtractor.py</code></h3>
        <p><span class="class-name">Classe: TextExtractor</span></p>
        <p>Hérite de <code>Extractor</code>. Spécialisé dans le traitement de chaînes de caractères. Surcharge <code>_ask_ai</code> pour communiquer avec le modèle IA (ex: openai/gpt-oss-20b) et force le format JSON.</p>

        <h3><code>audioExtractor.py</code></h3>
        <p><span class="class-name">Classe: AudioExtractor</span></p>
        <p>Hérite de <code>Extractor</code>. Prend un nom de fichier audio en entrée lors de l'instanciation pour transcrire ou analyser le contenu audio.</p>

        <h3><code>imageExtractor.py</code></h3>
        <p><span class="class-name">Classe: ImageExtractor</span></p>
        <p>Hérite de <code>Extractor</code>. Gère l'extraction d'informations à partir d'images. S'instancie avec l'extension de fichier (<code>file_extension</code>) et traite le contenu binaire (bytes) pour l'envoyer à un modèle de vision via l'API.</p>
    </div>

    <div class="module">
        <h2>Utilitaires & Modèles</h2>

        <h3><code>filter.py</code></h3>
        <p>Contient la logique de routage du fichier selon son type MIME (via <code>python-magic</code>).</p>
        <div class="method">
            <span class="method-name">Enum: InputType</span>
            <p>Définit les types supportés : <code>TEXT</code>, <code>AUDIO</code>, <code>IMAGE</code>.</p>
        </div>
        <div class="method">
            <span class="method-name">get_input_type(path) -> InputType</span>
            <p>Retourne l'énumération correspondante en fonction du type MIME du fichier.</p>
        </div>

        <h3><code>person.py</code></h3>
        <p>Modèle de données cible utilisant <strong>Pydantic</strong>.</p>
        <p><span class="class-name">Classe: Person(BaseModel)</span></p>
        <ul>
            <li><code>name: str | None</code></li>
            <li><code>age: PositiveInt | None</code></li>
        </ul>
    </div>

</div>
</body>
</html>
