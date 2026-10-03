// Collect features from several browser objects.
const activeFeatures = {
    language: navigator.language,
    logicalProcessors: navigator.hardwareConcurrency ?? null,
    screenResolution: `${screen.width}x${screen.height}`,
    colorDepth: screen.colorDepth,
    viewportSize: `${window.innerWidth}x${window.innerHeight}`,
    devicePixelRatio: window.devicePixelRatio,
    timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
};

console.table(activeFeatures);

// Display every collected value on the webpage.
const outputElement = document.getElementById("feature-output");
outputElement.textContent = Object.entries(activeFeatures)
    .map(([name, value]) => `${name}: ${value}`)
    .join("\n");

// A fixed feature order makes the same values produce the same fingerprint.
const fingerprintFeatureOrder = [
    "language",
    "logicalProcessors",
    "screenResolution",
    "colorDepth",
    "viewportSize",
    "devicePixelRatio",
    "timeZone",
];

const canonicalFingerprintInput = fingerprintFeatureOrder
    .map((name) => `${name}=${String(activeFeatures[name])}`)
    .join("|");

const fingerprintInputElement = document.getElementById("fingerprint-input");
const fingerprintOutputElement = document.getElementById("fingerprint-output");
const statusElement = document.getElementById("collection-status");
fingerprintInputElement.textContent = canonicalFingerprintInput;

async function createFingerprint(value) {
    const encodedValue = new TextEncoder().encode(value);
    const digest = await crypto.subtle.digest("SHA-256", encodedValue);

    return Array.from(new Uint8Array(digest))
        .map((byte) => byte.toString(16).padStart(2, "0"))
        .join("");
}

async function displayAndSendFingerprint() {
    try {
        const fingerprint = await createFingerprint(canonicalFingerprintInput);
        fingerprintOutputElement.textContent = fingerprint;

        const response = await fetch("/collect", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                collectionType: "fingerprint",
                fingerprint: fingerprint,
            }),
        });

        if (!response.ok) {
            throw new Error(`Server returned HTTP ${response.status}`);
        }

        statusElement.textContent = "Fingerprint sent successfully to Flask.";
    } catch (error) {
        fingerprintOutputElement.textContent = "Fingerprint unavailable.";
        statusElement.textContent = "Could not send the fingerprint to Flask.";
        console.error("Fingerprint generation failed:", error);
    }
}

displayAndSendFingerprint();
