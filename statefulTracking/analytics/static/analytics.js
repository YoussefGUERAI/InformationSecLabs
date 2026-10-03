const cookieName = "analytics_id";
const analyticsEndpoint = "http://analytics.test:9100/collect";

function readCookie(name) {
    const prefix = `${name}=`;
    const cookie = document.cookie
        .split("; ")
        .find((entry) => entry.startsWith(prefix));

    return cookie ? decodeURIComponent(cookie.slice(prefix.length)) : null;
}

function generateIdentifier() {
    const bytes = new Uint8Array(16);
    crypto.getRandomValues(bytes);

    // Format the random bytes as a version 4 UUID.
    bytes[6] = (bytes[6] & 0x0f) | 0x40;
    bytes[8] = (bytes[8] & 0x3f) | 0x80;

    const hexadecimal = Array.from(
        bytes,
        (byte) => byte.toString(16).padStart(2, "0"),
    );

    return [
        hexadecimal.slice(0, 4).join(""),
        hexadecimal.slice(4, 6).join(""),
        hexadecimal.slice(6, 8).join(""),
        hexadecimal.slice(8, 10).join(""),
        hexadecimal.slice(10, 16).join(""),
    ].join("-");
}

function sendAnalyticsEvent(analyticsId) {
    const event = {
        analytics_id: analyticsId,
        publisher: window.location.hostname,
        page: window.location.pathname,
        page_title: document.title,
        timestamp: new Date().toISOString(),
    };

    fetch(analyticsEndpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(event),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Analytics request failed with status ${response.status}`);
            }
        })
        .catch((error) => {
            console.error("Unable to send analytics event", error);
        });
}

let analyticsId = readCookie(cookieName);

if (!analyticsId) {
    analyticsId = generateIdentifier();
    document.cookie = `${cookieName}=${encodeURIComponent(analyticsId)}; Max-Age=31536000; Path=/; SameSite=Lax`;
}

sendAnalyticsEvent(analyticsId);
