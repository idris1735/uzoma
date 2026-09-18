/**
 * The client's login is unrelated to GitHub — this is what makes that
 * true. A correct username/password gets a signed, time-limited cookie;
 * every other CMS endpoint just checks that cookie. Deliberately not a
 * JWT library: the whole thing is HMAC-SHA256 over one JSON payload,
 * which is all a single-admin session needs and it's a dozen lines
 * against Node's own crypto instead of a new dependency.
 */

const crypto = require("crypto");

const COOKIE = "cms_session";
const MAX_AGE_S = 12 * 60 * 60; // 12 hours

function secret() {
  const s = process.env.CMS_SESSION_SECRET;
  if (!s) throw new Error("CMS_SESSION_SECRET is not set");
  return s;
}

function b64url(buf) {
  return Buffer.from(buf).toString("base64url");
}

function sign(payload) {
  const body = b64url(JSON.stringify({ ...payload, exp: Date.now() + MAX_AGE_S * 1000 }));
  const mac = b64url(crypto.createHmac("sha256", secret()).update(body).digest());
  return `${body}.${mac}`;
}

function verify(token) {
  if (!token || !token.includes(".")) return null;
  const [body, mac] = token.split(".");
  const expected = b64url(crypto.createHmac("sha256", secret()).update(body).digest());
  const a = Buffer.from(mac);
  const b = Buffer.from(expected);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  let payload;
  try {
    payload = JSON.parse(Buffer.from(body, "base64url").toString("utf8"));
  } catch {
    return null;
  }
  if (!payload.exp || payload.exp < Date.now()) return null;
  return payload;
}

function parseCookies(req) {
  const header = req.headers.cookie || "";
  const out = {};
  header.split(";").forEach((part) => {
    const i = part.indexOf("=");
    if (i === -1) return;
    out[part.slice(0, i).trim()] = decodeURIComponent(part.slice(i + 1).trim());
  });
  return out;
}

function sessionFromRequest(req) {
  return verify(parseCookies(req)[COOKIE]);
}

function setSessionCookie(res, payload) {
  const token = sign(payload);
  res.setHeader("Set-Cookie",
    `${COOKIE}=${token}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=${MAX_AGE_S}`);
}

function clearSessionCookie(res) {
  res.setHeader("Set-Cookie", `${COOKIE}=; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=0`);
}

function timingSafeStringEqual(a, b) {
  const ab = Buffer.from(String(a));
  const bb = Buffer.from(String(b));
  if (ab.length !== bb.length) return false;
  return crypto.timingSafeEqual(ab, bb);
}

/** Writes 401 and returns null if there's no valid session, so a route
 * can just do `const session = requireSession(req, res); if (!session) return;` */
function requireSession(req, res) {
  const session = sessionFromRequest(req);
  if (!session) {
    res.status(401).json({ error: "not logged in" });
    return null;
  }
  return session;
}

module.exports = {
  sessionFromRequest, setSessionCookie, clearSessionCookie, timingSafeStringEqual, requireSession,
};
