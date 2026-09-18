const { setSessionCookie, timingSafeStringEqual } = require("../lib/auth");

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.status(405).json({ error: "method not allowed" });
    return;
  }

  const { username, password } = req.body || {};
  const wantUser = process.env.CMS_USERNAME;
  const wantPass = process.env.CMS_PASSWORD;

  if (!wantUser || !wantPass) {
    res.status(500).json({ error: "CMS_USERNAME / CMS_PASSWORD are not configured" });
    return;
  }

  const ok = typeof username === "string" && typeof password === "string"
    && timingSafeStringEqual(username, wantUser) && timingSafeStringEqual(password, wantPass);

  if (!ok) {
    res.status(401).json({ error: "wrong username or password" });
    return;
  }

  setSessionCookie(res, { u: username });
  res.status(200).json({ ok: true });
};
