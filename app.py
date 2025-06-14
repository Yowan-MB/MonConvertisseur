from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# === Routes HTML ===

@app.route("/")
def accueil():
    return render_template("index.html")

@app.route("/a-propos")
def a_propos():
    return render_template("a-propos.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/en-construction')
def en_construction():
    return render_template('en-construction.html')


@app.route('/site.webmanifest')
def manifest():
    return send_from_directory('static/img', 'site.webmanifest', mimetype='application/manifest+json')

# === Devises personnalisées ===

custom_symbols = {
    "XAF": "Franc CFA (BEAC)",
    "XOF": "Franc CFA (UEMOA)",
    "NGN": "Naira nigérian",
    "ZAR": "Rand sud-africain",
    "EGP": "Livre égyptienne",
    "GHS": "Cedi ghanéen",
    "KES": "Shilling kényan",
    "MAD": "Dirham marocain",
    "TND": "Dinar tunisien",
    "DZD": "Dinar algérien",
    "ETB": "Birr éthiopien",
    "AOA": "Kwanza angolais",
    "CDF": "Franc congolais"
}

custom_rates = {
    ("XAF", "EUR"): 1 / 655.957,
    ("XOF", "EUR"): 1 / 655.957,
    ("XAF", "XOF"): 1.0,
    ("XAF", "MAD"): 0.0152,
    ("USD", "EUR"): 0.91,
    ("EUR", "AOA"): 877.19,
    ("EUR", "CDF"): 3110.00,
    ("EUR", "GHS"): 13.0,
    ("EUR", "NGN"): 1645.00,
    ("EUR", "DZD"): 146.00,
    ("EUR", "EGP"): 49.00,
    ("EUR", "KES"): 158.00,
    ("EUR", "ETB"): 63.00,
    ("EUR", "TND"): 3.27,
    ("EUR", "ZAR"): 20.40,
    ("EUR", "MAD"): 10.80
}

# Générer les taux inverses automatiquement
for (from_curr, to_curr), rate in list(custom_rates.items()):
    if rate != 0 and (to_curr, from_curr) not in custom_rates:
        custom_rates[(to_curr, from_curr)] = round(1 / rate, 6)

# === API Exchange Compatible ===

api_supported = {
    "USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY", "INR", "BRL",
    "RUB", "SEK", "NOK", "NZD", "SGD", "HKD", "ZAR", "KRW", "MXN", "TRY",
    "AED", "DKK", "PLN", "THB", "PHP", "RON", "MYR", "ISK", "ILS", "HUF",
    "CZK", "BGN"
}

def is_api_compatible(code):
    return code in api_supported

# === Endpoint : symbols ===

@app.route("/symbols")
def get_symbols():
    try:
        response = requests.get("https://api.frankfurter.app/currencies", timeout=5)
        data = response.json()
        data.update(custom_symbols)
        symbols = {code: {"description": name} for code, name in data.items()}
        return jsonify({"success": True, "symbols": symbols})
    except Exception as e:
        print("❌ Erreur /symbols :", e)
        return jsonify({"success": False, "error": str(e)}), 500

# === Conversion logic ===

def conversion_par_api(from_curr, to_curr, montant):
    url = f"https://api.frankfurter.app/latest?amount={montant}&from={from_curr}&to={to_curr}"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json().get("rates", {}).get(to_curr)

@app.route("/convert")
def convertir():
    from_curr = request.args.get("from", "").upper()
    to_curr = request.args.get("to", "").upper()
    amount = request.args.get("amount")

    if not from_curr or not to_curr or not amount:
        return jsonify({"success": False, "error": "Paramètres requis : from, to, amount."}), 400

    try:
        montant = float(amount)
    except ValueError:
        return jsonify({"success": False, "error": "Montant invalide. Entrez un nombre."}), 400

    try:
        # 1️⃣ Taux manuel direct
        if (from_curr, to_curr) in custom_rates:
            taux = custom_rates[(from_curr, to_curr)]
            return jsonify({
                "success": True,
                "result": round(montant * taux, 2),
                "from": from_curr, "to": to_curr,
                "custom": True, "via": "manuel direct"
            })

        # 2️⃣ API directe
        if is_api_compatible(from_curr) and is_api_compatible(to_curr):
            result = conversion_par_api(from_curr, to_curr, montant)
            if result:
                return jsonify({
                    "success": True,
                    "result": round(result, 2),
                    "from": from_curr, "to": to_curr,
                    "custom": False, "via": "API directe"
                })

        # 3️⃣ Fallback manuel ➝ EUR ➝ API
        if (from_curr, "EUR") in custom_rates and is_api_compatible(to_curr):
            montant_eur = montant * custom_rates[(from_curr, "EUR")]
            result = conversion_par_api("EUR", to_curr, montant_eur)
            if result:
                return jsonify({
                    "success": True,
                    "result": round(result, 2),
                    "from": from_curr, "to": to_curr,
                    "custom": True, "via": "manuel ➝ EUR ➝ API"
                })

        # 4️⃣ Fallback API ➝ EUR ➝ manuel
        if is_api_compatible(from_curr) and (to_curr, "EUR") in custom_rates:
            montant_eur = conversion_par_api(from_curr, "EUR", montant)
            if montant_eur:
                final_result = montant_eur / custom_rates[(to_curr, "EUR")]
                return jsonify({
                    "success": True,
                    "result": round(final_result, 2),
                    "from": from_curr, "to": to_curr,
                    "custom": True, "via": "API ➝ EUR ➝ manuel"
                })

        return jsonify({"success": False, "error": f"Taux non disponible pour {from_curr} ➝ {to_curr}."}), 502

    except Exception as e:
        print("❌ Erreur /convert :", e)
        return jsonify({"success": False, "error": f"Erreur serveur : {str(e)}"}), 500

# === Lancement serveur ===

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
