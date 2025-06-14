💱 MonConvertisseur

**MonConvertisseur** est une application web élégante et rapide, développée avec **Flask**, **Tailwind CSS** et **JavaScript**. Elle facilite la conversion de devises — notamment africaines — dans une interface localisée, responsive et animée.


🎯 Objectifs

- Proposer un outil fiable, intuitif et accessible en français
- Mettre en avant les **devises africaines souvent négligées**
- Offrir une expérience fluide sur desktop et mobile
- Séparer clairement logique, structure et style (approche modulaire)


✨ Fonctionnalités

- 🔄 Conversion en temps réel entre 170+ devises
- 📌 Intégration étendue des devises africaines (XOF, XAF, NGN, GHS, etc.)
- 🧠 Formatage dynamique du montant (`1 250.50` plutôt que `1250.5`)
- 💬 Affichage stylisé du résultat : `1 250.00 EUR → 819 000.00 XAF`
- ⚡ Chargement des devises via une API externe + fallback personnalisé
- ✨ Animation de contenu avec Animate.css et WOW.js
- 📱 Design responsive compatible mobile/tablette
- ♿ Accessibilité : `aria-live`, contraste élevé, navigation clavier


🔌 API utilisée

Le projet utilise principalement l’API **[Frankfurter](https://www.frankfurter.app/)** (gratuite et sans clé) pour :

- Récupérer la liste des devises : `GET /currencies`
- Obtenir les taux de change : `GET /latest?amount=X&from=EUR&to=USD`

Un système de fallback avec des **taux personnalisés** assure la conversion pour certaines devises africaines non supportées.


 🛠️ Technologies

- **Frontend** : HTML, Tailwind CSS, JavaScript ES6
- **Backend** : Python 3.10+, Flask, Flask-CORS
- **Animations** : Animate.css, WOW.js
- **Architecture** : séparation claire des responsabilités (HTML / CSS / JS)
- **API** : Frankfurter + taux manuels


🧪 Installation locale

```bash
1. Clone du projet
git clone https://github.com/Yowan-Mb/monconvertisseur.git
cd monconvertisseur

2. Création de l'environnement virtuel
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

3. Installation des dépendances
pip install flask flask-cors

4. Lancement du serveur
python app.py
👉 Ouvre http://localhost:5000 dans ton navigateur.


🗂️ Arborescence du projet

monconvertisseur/
├── app.py
├── requirements.txt
├── .gitignore
├── static/
│   ├── style.css
│   ├── script.js
│   └── img/
│       ├── logo.png
│       ├── favicon.svg
│       ├── favicon.ico
│       ├── favicon-96x96.png
│       ├── apple-touch-icon.png
│       ├── site.webmanifest
│       ├── convert.png
│       ├── frais.jpg
│       └── compare.jpg
├── templates/
│   ├── index.html
│   ├── a-propos.html
│   ├── services.html
│   ├── contact.html
│   └── en-construction.html
├── README.md


📌 Roadmap
💸 Calculateur de frais (transfert, commissions bancaires…)
📤 Export PDF / CSV des résultats de conversion
🌍 Version multilingue (français / anglais)
📈 Historique et graphiques des conversions
🧾 Génération de fiche de conversion imprimable
📦 Passage à une PWA (installation + mode hors ligne)


🧠 Auteur
Développé avec passion par Yowan Mberi ➡️ Rejoignez la discussion, proposez vos idées ou soumettez une PR ✨

> Ce projet est une démonstration alliant backend Python & frontend moderne pour un cas concret utile au quotidien. Merci d’y jeter un œil, de tester, et pourquoi pas d’y contribuer.