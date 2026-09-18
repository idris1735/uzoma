const yaml = require("js-yaml");
const { requireSession } = require("../lib/auth");
const { readFile, writeFile } = require("../lib/github");
const CONTENT_TYPES = require("../lib/content-types");

/** Only ever takes what the schema says is a field, and for a locked
 * list-group item, only what isn't locked — this is the actual
 * guardrail, not the admin UI. A crafted request that tries to move a
 * storyboard's video ID or a slide onto some other path still can't:
 * whatever isn't allowed here is silently kept at its stored value. */
function mergeField(field, current, incoming) {
  switch (field.type) {
    case "text":
    case "date":
    case "markdown-lite":
      return typeof incoming === "string" ? incoming : current;

    case "list-text":
    case "list-markdown":
      return Array.isArray(incoming) ? incoming.filter((s) => typeof s === "string") : current;

    case "list-group": {
      const currentList = Array.isArray(current) ? current : [];
      const incomingList = Array.isArray(incoming) ? incoming : [];

      if (field.addable) {
        return incomingList.map((item) => {
          const clean = {};
          field.itemFields.forEach((f) => {
            if (typeof item[f.key] === "string") clean[f.key] = item[f.key];
          });
          return clean;
        });
      }

      // fixed-length: same count as what's stored, editable fields only
      return currentList.map((currentItem, i) => {
        const incomingItem = incomingList[i] || {};
        const merged = { ...currentItem };
        field.itemFields.forEach((f) => {
          if (!f.locked && typeof incomingItem[f.key] === "string") merged[f.key] = incomingItem[f.key];
        });
        return merged;
      });
    }

    default:
      return current;
  }
}

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.status(405).json({ error: "method not allowed" });
    return;
  }
  if (!requireSession(req, res)) return;

  const { type: typeName, data, sha } = req.body || {};
  const type = CONTENT_TYPES[typeName];
  if (!type) {
    res.status(400).json({ error: `unknown content type: ${typeName}` });
    return;
  }
  if (!data || typeof data !== "object") {
    res.status(400).json({ error: "missing data" });
    return;
  }

  const file = await readFile(type.file);
  if (!file) {
    res.status(404).json({ error: `${type.file} does not exist` });
    return;
  }
  if (file.sha && sha && file.sha !== sha) {
    res.status(409).json({ error: "This was edited elsewhere since you loaded it. Reload and redo your change." });
    return;
  }

  const current = yaml.load(file.text, { schema: yaml.CORE_SCHEMA }) || {};
  const merged = { ...current };
  type.fields.forEach((f) => {
    merged[f.key] = mergeField(f, current[f.key], data[f.key]);
  });

  const text = yaml.dump(merged, { lineWidth: -1, noRefs: true });
  const result = await writeFile(type.file, text, file.sha, `cms: update ${type.label}`);
  res.status(200).json({ ok: true, sha: result.sha });
};
