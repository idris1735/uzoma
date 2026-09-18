const { requireSession } = require("../lib/auth");
const CONTENT_TYPES = require("../lib/content-types");

module.exports = async (req, res) => {
  if (req.method !== "GET") {
    res.status(405).json({ error: "method not allowed" });
    return;
  }
  if (!requireSession(req, res)) return;

  res.status(200).json(CONTENT_TYPES);
};
