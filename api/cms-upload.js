const { requireSession } = require("../lib/auth");
const { readFile, writeFile } = require("../lib/github");
const CONTENT_TYPES = require("../lib/content-types");

const EXT_OK = /^[a-z0-9]{2,5}$/;

function extOf(filename) {
  const m = /\.([a-zA-Z0-9]+)$/.exec(filename || "");
  return m ? m[1].toLowerCase() : "";
}

function slugOf(filename) {
  return (filename || "image").replace(/\.[^.]+$/, "")
    .toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "image";
}

function parseDataUrl(dataUrl) {
  const m = /^data:([^;]+);base64,(.+)$/.exec(dataUrl || "");
  return m ? { mime: m[1], base64: m[2] } : null;
}

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.status(405).json({ error: "method not allowed" });
    return;
  }
  if (!requireSession(req, res)) return;

  const { type: typeName, imageKey, slideUpload, filename, dataUrl } = req.body || {};
  const type = CONTENT_TYPES[typeName];
  if (!type) {
    res.status(400).json({ error: `unknown content type: ${typeName}` });
    return;
  }

  const parsed = parseDataUrl(dataUrl);
  if (!parsed || !parsed.mime.startsWith("image/")) {
    res.status(400).json({ error: "expected an image data URL" });
    return;
  }
  const ext = extOf(filename);
  if (!EXT_OK.test(ext)) {
    res.status(400).json({ error: "unrecognised file extension" });
    return;
  }

  let repoPath;
  if (slideUpload) {
    if (!type.imageDir) {
      res.status(400).json({ error: `${typeName} has no slide image directory` });
      return;
    }
    repoPath = `${type.imageDir}/${slugOf(filename)}-${Date.now().toString(36)}.${ext}`;
  } else {
    const spec = (type.images || []).find((i) => i.key === imageKey);
    if (!spec) {
      res.status(400).json({ error: `${typeName} has no image field "${imageKey}"` });
      return;
    }
    // always content/uploads/<key>.<ext> — build_site.py's next run turns
    // this into the real, correctly-sized asset; overwrite in place, no
    // history of old extensions left behind
    repoPath = `content/uploads/${imageKey}.${ext}`;
  }

  const existing = await readFile(repoPath);
  await writeFile(repoPath, parsed.base64, existing ? existing.sha : null,
    `cms: upload ${repoPath}`, { base64: true });
  res.status(200).json({ ok: true, path: repoPath });
};
