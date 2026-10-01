const cookieName = "analytics_id";

function readCookie(name) {
    const prefix = `${name}=`;
    const cookie = document.cookie
        .split("; ")
        .find((entry) => entry.startsWith(prefix));

    return cookie ? decodeURIComponent(cookie.slice(prefix.length)) : null;
}

let analyticsId = readCookie(cookieName);

if (!analyticsId) {
    analyticsId = crypto.randomUUID();
    document.cookie = `${cookieName}=${encodeURIComponent(analyticsId)}; Max-Age=31536000; Path=/`;
}
