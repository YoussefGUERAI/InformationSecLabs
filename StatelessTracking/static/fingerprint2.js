const targetElement = document.getElementById("target-sentence");
const typingInput = document.getElementById("typing-input");
const restartButton = document.getElementById("restart-button");
const typingResults = document.getElementById("typing-results");

const targetSentence = targetElement.textContent;

let startTime = null;
let correctionCount = 0;
let experimentComplete = false;

typingInput.addEventListener("keydown", function (event) {
    if (experimentComplete) {
        return;
    }

    const isPrintableCharacter =
        event.key.length === 1 && !event.ctrlKey && !event.metaKey && !event.altKey;

    if (startTime === null && isPrintableCharacter) {
        startTime = performance.now();
    }

    if (event.key === "Backspace" && startTime !== null && typingInput.value.length > 0) {
        correctionCount += 1;
    }
});

typingInput.addEventListener("input", function () {
    if (experimentComplete || startTime === null || typingInput.value !== targetSentence) {
        return;
    }

    const endTime = performance.now();
    const totalTimeSeconds = (endTime - startTime) / 1000;
    const charactersPerMinute = (targetSentence.length / totalTimeSeconds) * 60;

    experimentComplete = true;
    typingInput.disabled = true;

    const behavioralFeatures = {
        totalTimeSeconds: Number(totalTimeSeconds.toFixed(2)),
        typingSpeedCPM: Number(charactersPerMinute.toFixed(2)),
        correctionCount: correctionCount,
    };

    typingResults.textContent = [
        `Total typing time: ${behavioralFeatures.totalTimeSeconds} seconds`,
        `Typing speed: ${behavioralFeatures.typingSpeedCPM} characters per minute`,
        `Corrections: ${behavioralFeatures.correctionCount}`,
        "Sending results to Flask...",
    ].join("\n");

    fetch("/collect", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            collectionType: "behavioral",
            features: behavioralFeatures,
        }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Server returned HTTP ${response.status}`);
            }
            return response.json();
        })
        .then(() => {
            typingResults.textContent = typingResults.textContent.replace(
                "Sending results to Flask...",
                "Results sent successfully to Flask.",
            );
        })
        .catch((error) => {
            typingResults.textContent = typingResults.textContent.replace(
                "Sending results to Flask...",
                "Could not send results to Flask.",
            );
            console.error("Behavioral collection failed:", error);
        });
});

restartButton.addEventListener("click", function () {
    startTime = null;
    correctionCount = 0;
    experimentComplete = false;
    typingInput.disabled = false;
    typingInput.value = "";
    typingResults.textContent = "";
    typingInput.focus();
});
