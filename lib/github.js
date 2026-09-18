/**
 * Reads and writes files in the repo. With GITHUB_TOKEN set, that means
 * real commits via GitHub's Contents API — every save is a normal git
 * commit, which is what triggers Vercel's own auto-deploy, so there is
 * no separate deploy step to write. Without it (local dev), the same
 * calls just read/write the working tree directly, so the whole CMS
 * flow — login, edit, save, rebuild — can be exercised on a laptop
 * with no GitHub credentials at all.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const API = "https://api.github.com";

function repoConfig() {
  const repo = process.env.GITHUB_REPO;
  const branch = process.env.GITHUB_BRANCH || "main";
  const token = process.env.GITHUB_TOKEN;
  return { repo, branch, token };
}

function isLive() {
  return Boolean(repoConfig().token);
}

async function ghFetch(url, options) {
  const { token } = repoConfig();
  const res = await fetch(url, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      ...(options && options.headers),
    },
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`GitHub API ${res.status} ${res.statusText}: ${body.slice(0, 500)}`);
  }
  return res.json();
}

/** Returns { text, sha } — sha is null in local-dev mode (there is no
 * such thing outside git), and callers that need it for a write only
 * do so in live mode anyway. */
async function readFile(repoPath) {
  if (!isLive()) {
    const full = path.join(ROOT, repoPath);
    if (!fs.existsSync(full)) return null;
    return { text: fs.readFileSync(full, "utf8"), sha: null };
  }
  const { repo, branch } = repoConfig();
  try {
    const data = await ghFetch(
      `${API}/repos/${repo}/contents/${encodeURI(repoPath)}?ref=${branch}`);
    return { text: Buffer.from(data.content, "base64").toString("utf8"), sha: data.sha };
  } catch (err) {
    if (String(err.message).startsWith("GitHub API 404")) return null;
    throw err;
  }
}

/** Writes text (or raw base64 for images) to repoPath and commits it.
 * sha must be the value readFile last returned for this path (or null
 * for a new file) — GitHub rejects the write if the file moved under
 * us, which is the whole point: two edits can't silently clobber each
 * other. */
async function writeFile(repoPath, content, sha, message, { base64 = false } = {}) {
  const encoded = base64 ? content : Buffer.from(content, "utf8").toString("base64");
  if (!isLive()) {
    const full = path.join(ROOT, repoPath);
    fs.mkdirSync(path.dirname(full), { recursive: true });
    fs.writeFileSync(full, Buffer.from(encoded, "base64"));
    return { sha: "local" };
  }
  const { repo, branch } = repoConfig();
  const body = { message, content: encoded, branch };
  if (sha) body.sha = sha;
  const data = await ghFetch(`${API}/repos/${repo}/contents/${encodeURI(repoPath)}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return { sha: data.content.sha };
}

module.exports = { readFile, writeFile, isLive };
