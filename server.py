#!/usr/bin/env python3
"""
LocalDrop - Wireless File Transfer between iPhone & PC
Run this script, scan the QR code with your iPhone, transfer files both ways.
"""

import os
import sys
import socket
import threading
import mimetypes
import json
import time
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote, quote
import io

# ── Config ────────────────────────────────────────────────────────────────────
PORT = 8765
UPLOAD_DIR = Path.home() / "LocalDrop_Received"
SHARE_DIR = Path.home() / "LocalDrop_Share"
UPLOAD_DIR.mkdir(exist_ok=True)
SHARE_DIR.mkdir(exist_ok=True)

# ── HTML UI ───────────────────────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>LocalDrop</title>
<style>
  :root {
    --bg: #0d0d0f;
    --surface: #17171a;
    --border: #2a2a30;
    --accent: #6c63ff;
    --accent2: #a78bfa;
    --text: #e8e8f0;
    --muted: #6b6b7a;
    --success: #34d399;
    --danger: #f87171;
    --radius: 14px;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 15px;
    min-height: 100vh;
  }

  /* ── Header ── */
  header {
    padding: 20px 24px 0;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .logo {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
  }
  header h1 { font-size: 20px; font-weight: 700; letter-spacing: -0.3px; }
  header p  { font-size: 12px; color: var(--muted); margin-top: 1px; }

  /* ── Tabs ── */
  .tabs {
    display: flex;
    gap: 6px;
    padding: 20px 24px 0;
  }
  .tab {
    flex: 1;
    padding: 10px 0;
    border-radius: 10px;
    border: 1.5px solid var(--border);
    background: transparent;
    color: var(--muted);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all .2s;
  }
  .tab.active {
    background: var(--accent);
    border-color: var(--accent);
    color: #fff;
  }

  /* ── Panels ── */
  .panel { display: none; padding: 20px 24px; }
  .panel.active { display: block; }

  /* ── Upload Zone ── */
  .drop-zone {
    border: 2px dashed var(--border);
    border-radius: var(--radius);
    padding: 40px 20px;
    text-align: center;
    cursor: pointer;
    transition: all .2s;
    position: relative;
  }
  .drop-zone.drag { border-color: var(--accent); background: rgba(108,99,255,.08); }
  .drop-zone input[type=file] {
    position: absolute; inset: 0; opacity: 0; cursor: pointer; width: 100%; height: 100%;
  }
  .drop-icon { font-size: 40px; margin-bottom: 10px; }
  .drop-zone h3 { font-size: 16px; font-weight: 600; margin-bottom: 4px; }
  .drop-zone p  { font-size: 13px; color: var(--muted); }

  /* ── Progress ── */
  .progress-wrap { margin-top: 16px; display: none; }
  .progress-bar-bg {
    background: var(--border);
    border-radius: 99px;
    height: 6px;
    overflow: hidden;
  }
  .progress-bar {
    height: 6px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    border-radius: 99px;
    width: 0%;
    transition: width .1s;
  }
  .progress-label { font-size: 12px; color: var(--muted); margin-top: 6px; }

  /* ── File list ── */
  .file-list { margin-top: 20px; display: flex; flex-direction: column; gap: 10px; }
  .file-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 14px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .file-icon {
    width: 40px; height: 40px;
    background: rgba(108,99,255,.15);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
  }
  .file-info { flex: 1; min-width: 0; }
  .file-name {
    font-size: 13px; font-weight: 600;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .file-meta { font-size: 11px; color: var(--muted); margin-top: 2px; }
  .download-btn {
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    white-space: nowrap;
    text-decoration: none;
    display: inline-block;
  }
  .download-btn:hover { background: var(--accent2); }

  /* ── Toast ── */
  #toast {
    position: fixed;
    bottom: 30px; left: 50%;
    transform: translateX(-50%) translateY(80px);
    background: #1e1e24;
    border: 1px solid var(--border);
    color: var(--text);
    padding: 12px 20px;
    border-radius: 99px;
    font-size: 13px;
    font-weight: 500;
    transition: transform .3s ease;
    z-index: 999;
    white-space: nowrap;
    box-shadow: 0 8px 32px rgba(0,0,0,.5);
  }
  #toast.show { transform: translateX(-50%) translateY(0); }
  #toast.ok   { border-color: var(--success); color: var(--success); }
  #toast.err  { border-color: var(--danger);  color: var(--danger);  }

  /* ── Section label ── */
  .section-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 12px;
  }

  .empty {
    text-align: center;
    color: var(--muted);
    font-size: 13px;
    padding: 30px 0;
  }

  /* ── Received list ── */
  #refresh-btn {
    background: transparent;
    border: 1.5px solid var(--border);
    color: var(--text);
    border-radius: 8px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    float: right;
    margin-top: -4px;
  }
  #refresh-btn:hover { border-color: var(--accent); color: var(--accent); }

  .clearfix::after { content: ''; display: table; clear: both; }
</style>
</head>
<body>

<header>
  <div class="logo">📡</div>
  <div>
    <h1>LocalDrop</h1>
    <p>Wireless file transfer — no internet needed</p>
  </div>
</header>

<div class="tabs">
  <button class="tab active" onclick="switchTab('send')">📤 Send to PC</button>
  <button class="tab"        onclick="switchTab('receive')">📥 Get from PC</button>
</div>

<!-- SEND panel -->
<div id="panel-send" class="panel active">
  <p class="section-label">Upload files from this device to your PC</p>
  <div class="drop-zone" id="dropZone">
    <input type="file" id="fileInput" multiple accept="*/*">
    <div class="drop-icon">📁</div>
    <h3>Tap to choose files</h3>
    <p>Photos, videos, documents — anything</p>
  </div>
  <div class="progress-wrap" id="progressWrap">
    <div class="progress-bar-bg"><div class="progress-bar" id="progressBar"></div></div>
    <div class="progress-label" id="progressLabel">Uploading…</div>
  </div>
  <div class="file-list" id="uploadedList"></div>
</div>

<!-- RECEIVE panel -->
<div id="panel-receive" class="panel">
  <div class="clearfix">
    <p class="section-label" style="float:left">Files shared from your PC</p>
    <button id="refresh-btn" onclick="loadShared()">↻ Refresh</button>
  </div>
  <div id="sharedList"><div class="empty">Loading…</div></div>
</div>

<div id="toast"></div>

<script>
// ── Tab switching ──────────────────────────────────────────────────────────
function switchTab(id) {
  document.querySelectorAll('.tab').forEach((t,i) =>
    t.classList.toggle('active', ['send','receive'][i] === id));
  document.querySelectorAll('.panel').forEach(p =>
    p.classList.toggle('active', p.id === 'panel-' + id));
  if (id === 'receive') loadShared();
}

// ── Toast ─────────────────────────────────────────────────────────────────
function toast(msg, type='ok') {
  const el = document.getElementById('toast');
  el.textContent = (type==='ok'?'✓ ':'✕ ') + msg;
  el.className = 'show ' + type;
  setTimeout(() => el.className = '', 2800);
}

// ── File icon helper ───────────────────────────────────────────────────────
function fileIcon(name) {
  const ext = name.split('.').pop().toLowerCase();
  const map = {
    jpg:'🖼️', jpeg:'🖼️', png:'🖼️', gif:'🖼️', heic:'🖼️', webp:'🖼️',
    mp4:'🎬', mov:'🎬', avi:'🎬', mkv:'🎬',
    mp3:'🎵', aac:'🎵', wav:'🎵', m4a:'🎵',
    pdf:'📄', doc:'📝', docx:'📝', xls:'📊', xlsx:'📊',
    zip:'🗜️', rar:'🗜️', gz:'🗜️',
  };
  return map[ext] || '📎';
}

function fmtSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1048576) return (bytes/1024).toFixed(1) + ' KB';
  return (bytes/1048576).toFixed(1) + ' MB';
}

// ── Upload ─────────────────────────────────────────────────────────────────
const dropZone   = document.getElementById('dropZone');
const fileInput  = document.getElementById('fileInput');
const progressWrap = document.getElementById('progressWrap');
const progressBar  = document.getElementById('progressBar');
const progressLabel= document.getElementById('progressLabel');
const uploadedList = document.getElementById('uploadedList');

fileInput.addEventListener('change', () => uploadFiles([...fileInput.files]));

dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag'); });
dropZone.addEventListener('dragleave', ()=> dropZone.classList.remove('drag'));
dropZone.addEventListener('drop', e => {
  e.preventDefault(); dropZone.classList.remove('drag');
  uploadFiles([...e.dataTransfer.files]);
});

async function uploadFiles(files) {
  if (!files.length) return;
  progressWrap.style.display = 'block';

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    progressLabel.textContent = `Uploading ${i+1}/${files.length}: ${file.name}`;

    const fd = new FormData();
    fd.append('file', file);

    await new Promise((resolve) => {
      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/upload');
      xhr.upload.onprogress = e => {
        if (e.lengthComputable)
          progressBar.style.width = (e.loaded/e.total*100).toFixed(1) + '%';
      };
      xhr.onload = () => {
        if (xhr.status === 200) {
          progressBar.style.width = '100%';
          addUploadedCard(file);
          toast(file.name + ' sent!');
        } else {
          toast('Failed: ' + file.name, 'err');
        }
        resolve();
      };
      xhr.onerror = () => { toast('Upload error', 'err'); resolve(); };
      xhr.send(fd);
    });
  }

  progressLabel.textContent = `Done — ${files.length} file(s) saved to PC`;
  setTimeout(() => { progressWrap.style.display='none'; progressBar.style.width='0%'; }, 3000);
  fileInput.value = '';
}

function addUploadedCard(file) {
  const card = document.createElement('div');
  card.className = 'file-card';
  card.innerHTML = `
    <div class="file-icon">${fileIcon(file.name)}</div>
    <div class="file-info">
      <div class="file-name">${file.name}</div>
      <div class="file-meta">${fmtSize(file.size)} · just now</div>
    </div>
    <span style="color:var(--success);font-size:18px">✓</span>
  `;
  uploadedList.prepend(card);
}

// ── Shared files (PC → iPhone) ─────────────────────────────────────────────
async function loadShared() {
  const list = document.getElementById('sharedList');
  list.innerHTML = '<div class="empty">Loading…</div>';
  try {
    const res = await fetch('/list');
    const files = await res.json();
    if (!files.length) {
      list.innerHTML = '<div class="empty">No files shared yet.<br>Drop files into the <strong>LocalDrop_Share</strong> folder on your PC.</div>';
      return;
    }
    list.innerHTML = '';
    const wrap = document.createElement('div');
    wrap.className = 'file-list';
    files.forEach(f => {
      const card = document.createElement('div');
      card.className = 'file-card';
      card.innerHTML = `
        <div class="file-icon">${fileIcon(f.name)}</div>
        <div class="file-info">
          <div class="file-name">${f.name}</div>
          <div class="file-meta">${fmtSize(f.size)}</div>
        </div>
        <a class="download-btn" href="/download/${encodeURIComponent(f.name)}" download="${f.name}">Save</a>
      `;
      wrap.appendChild(card);
    });
    list.appendChild(wrap);
  } catch(e) { list.innerHTML = '<div class="empty">Could not load files.</div>'; }
}
</script>
</body>
</html>"""


# ── HTTP Handler ──────────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"  [{ts}] {args[0]} {args[1]} → {args[2]}")

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html):
        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/" or path == "/index.html":
            self.send_html(HTML)

        elif path == "/list":
            files = []
            for f in sorted(SHARE_DIR.iterdir()):
                if f.is_file() and not f.name.startswith("."):
                    files.append({"name": f.name, "size": f.stat().st_size})
            self.send_json(files)

        elif path.startswith("/download/"):
            fname = unquote(path[len("/download/"):])
            fpath = SHARE_DIR / fname
            if not fpath.exists() or not fpath.is_file():
                self.send_response(404);
                self.end_headers();
                return
            mime = mimetypes.guess_type(fname)[0] or "application/octet-stream"
            data = fpath.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", len(data))
            quoted_filename = quote(fname)
            self.send_header("Content-Disposition", f"attachment; filename*=UTF-8''{quoted_filename}")
            self.end_headers()
            self.wfile.write(data)

        else:
            self.send_response(404);
            self.end_headers()

    def do_POST(self):
        if self.path != "/upload":
            self.send_response(404);
            self.end_headers();
            return

        ctype = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in ctype:
            self.send_json({"error": "expected multipart"}, 400);
            return

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)

        # Extract boundary
        boundary = None
        for part in ctype.split(";"):
            part = part.strip()
            if part.startswith("boundary="):
                boundary = part[9:].strip('"').encode()

        if not boundary:
            self.send_json({"error": "no boundary"}, 400);
            return

        # Split on boundary
        parts = raw.split(b"--" + boundary)
        saved = []
        for part in parts[1:]:
            if part.startswith(b"--") or not part.strip():
                continue
            if b"\r\n\r\n" not in part:
                continue
            header_block, _, body = part.partition(b"\r\n\r\n")

            # Trim trailing CRLF before boundary marker
            if body.endswith(b"\r\n"):
                body = body[:-2]

            headers_text = header_block.decode("utf-8", errors="replace")

            fname = None
            for hline in headers_text.splitlines():
                if "filename=" in hline:
                    for seg in hline.split(";"):
                        seg = seg.strip()
                        if seg.startswith("filename="):
                            fname = seg[9:].strip('"').strip("'")
            if not fname or not body:
                continue

            # Sanitize filename
            safe = Path(fname).name
            dest = UPLOAD_DIR / safe
            # Avoid overwrite
            if dest.exists():
                stem = dest.stem;
                suf = dest.suffix;
                i = 1
                while dest.exists():
                    dest = UPLOAD_DIR / f"{stem}_{i}{suf}";
                    i += 1
            dest.write_bytes(body)
            saved.append(safe)
            print(f"  💾 Saved: {dest}")

        self.send_json({"saved": saved})


# ── QR code (optional) ────────────────────────────────────────────────────────
def print_qr(url):
    try:
        import qrcode
        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
        return
    except ImportError:
        pass
    # Fallback: simple text box
    print("\n" + "─" * 50)
    print("  Open this URL on your iPhone:")
    print(f"  {url}")
    print("─" * 50)
    print("  (Install 'qrcode' for a scannable QR code:")
    print("   pip install qrcode)")
    print("─" * 50 + "\n")


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ip = get_local_ip()
    url = f"http://{ip}:{PORT}"

    print("\n" + "═" * 52)
    print("  📡  LocalDrop — Wireless File Transfer")
    print("═" * 52)
    print(f"\n  Server running at: {url}\n")
    print(f"  📥 Files from iPhone saved to:")
    print(f"     {UPLOAD_DIR}")
    print(f"\n  📤 Put files here to share to iPhone:")
    print(f"     {SHARE_DIR}")
    print("\n  Scan the QR code below with your iPhone camera:\n")

    print_qr(url)

    print("  Press Ctrl+C to stop the server.\n")

    server = HTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n  Server stopped. Goodbye! 👋\n")
