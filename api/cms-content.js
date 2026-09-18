const yaml = require("js-yaml");
const { requireSession } = require("../lib/auth");
const { readFile } = require("../lib/github");
const CONTENT_TYPES = require("../lib/content-types");

module.exports = async (req, res) => {
  if (req.method !== "GET") {
    res.status(405).json({ error: "method not allowed" });
    return;
  }
  if (!requireSession(req, res)) return;

  const type = CONTENT_TYPES[req.query.type];
  if (!type) {
    res.status(400).json({ error: `unknown content type: ${req.query.type}` });
    return;
  }

  const file = await readFile(type.file);
  if (!file) {
    res.status(404).json({ error: `${type.file} does not exist` });
    return;
  }

  // CORE_SCHEMA, not the default — the default schema auto-parses an
  // unquoted yyyy-mm-dd scalar into a JS Date, which then serializes
  // over JSON as a full ISO timestamp and breaks a <input type="date">
  res.status(200).json({ data: yaml.load(file.text, { schema: yaml.CORE_SCHEMA }), sha: file.sha });
};
