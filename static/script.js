// 🔹 Liste des devises prioritaires
const topDevises = [
    "USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY", "INR", "BRL",
    "RUB", "SEK", "NOK", "NZD", "SGD", "HKD", "ZAR", "KRW", "MXN", "TRY",
    "AED", "DKK", "PLN", "THB", "XAF", "XOF", "NGN", "GHS", "KES", "MAD", "TND", "DZD", "CDF"
];

// 🔹 Chargement dynamique des devises
async function chargerDevises() {
    const selectFrom = document.getElementById("from");
    const selectTo = document.getElementById("to");

    if (!selectFrom || !selectTo) return; // 🔒 sécurise les pages sans formulaire

    try {
        const res = await fetch("/symbols");
        const data = await res.json();

        if (!data.symbols) throw new Error("Clé 'symbols' manquante");

        const allCodes = Object.keys(data.symbols);
        const prioritaires = topDevises.filter(code => data.symbols[code]);
        const secondaires = allCodes.filter(code => !prioritaires.includes(code)).sort();
        const listeFinale = [...prioritaires, ...secondaires];

        listeFinale.forEach(code => {
            const label = `${code} - ${data.symbols[code].description || "Devise inconnue"}`;
            selectFrom.appendChild(new Option(label, code));
            selectTo.appendChild(new Option(label, code));
        });

        selectFrom.value = "USD";
        selectTo.value = "XAF";
    } catch (e) {
        console.error("❌ Erreur chargement devises :", e);
        alert("Erreur de chargement des devises. Vérifie que le backend fonctionne.");
    }
}

// 🔹 Formatage champ montant
function configurerFormatMontant() {
    const montantInput = document.getElementById("montant");
    if (!montantInput) return;

    montantInput.addEventListener("input", () => {
        const value = montantInput.value.replace(/\s/g, "").replace(",", ".");
        const number = parseFloat(value);
        if (!isNaN(number)) {
            montantInput.value = number.toLocaleString("fr-FR", {
                minimumFractionDigits: 0,
                maximumFractionDigits: 2
            });
        }
    });
}

// 🔹 Soumission du formulaire
function configurerFormulaire() {
    const form = document.getElementById("convert-form");
    const montantInput = document.getElementById("montant");
    const resultElt = document.getElementById("resultat");

    if (!form || !montantInput || !resultElt) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const from = document.getElementById("from").value;
        const to = document.getElementById("to").value;
        const raw = montantInput.value.replace(/\s/g, "").replace(",", ".");
        const montant = parseFloat(raw);

        if (isNaN(montant)) {
            alert("Veuillez saisir un montant valide.");
            return;
        }

        try {
            const res = await fetch(`/convert?from=${from}&to=${to}&amount=${montant}`);
            const data = await res.json();

            if (data.success) {
                const formattedFrom = montant.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                const formattedTo = Number(data.result).toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

                resultElt.textContent = `${formattedFrom} ${from} → ${formattedTo} ${to}`;
            } else {
                resultElt.textContent = `Erreur : ${data.error}`;
            }

            resultElt.classList.remove("hidden");
        } catch (err) {
            console.error("❌ Erreur conversion :", err);
            resultElt.textContent = "Erreur réseau ou serveur lors de la conversion.";
            resultElt.classList.remove("hidden");
        }
    });
}

// 🔹 Menu mobile responsive
function configurerMenu() {
    const menuBtn = document.getElementById("menu-btn");
    const mobileMenu = document.getElementById("mobile-menu");
    if (!menuBtn || !mobileMenu) return;

    menuBtn.addEventListener("click", () => {
        mobileMenu.classList.toggle("hidden");
        menuBtn.classList.toggle("open");
    });

    document.querySelectorAll("#mobile-menu a").forEach(link => {
        link.addEventListener("click", () => {
            mobileMenu.classList.add("hidden");
            menuBtn.classList.remove("open");
        });
    });
}

// 🔹 Initialisation globale
window.addEventListener("DOMContentLoaded", () => {
    configurerMenu();
    configurerFormatMontant();
    configurerFormulaire();
    chargerDevises();
});
