"""BrickLog desktop. The interface is served only to this computer."""
import http.server
import mimetypes
import os
import pathlib
import re
import socketserver
import sys
import threading
import urllib.parse
import webbrowser
import webview

ROOT = pathlib.Path(getattr(sys, '_MEIPASS', pathlib.Path(__file__).resolve().parent))
# The source projects share one catalogue and artwork; bundled executables carry a copy.
ASSETS = ROOT / 'assets' if getattr(sys, 'frozen', False) else ROOT.parent / 'LegoQuest' / 'app' / 'src' / 'main' / 'assets'
HOST = '127.0.0.1'
PORT = 18765  # Stable origin: changing this port would create separate browser storage.


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.headers.get('Host') != f'{HOST}:{PORT}':
            self.send_error(403)
            return
        path = urllib.parse.urlsplit(self.path).path
        if path in ('/', '/index.html'):
            file = ASSETS / 'index.html'
        elif re.fullmatch(r'/covers/[a-f0-9]{20}\.jpg', path):
            file = ASSETS / path.lstrip('/')
        else:
            self.send_error(404)
            return
        try:
            data = file.read_bytes()
        except OSError:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Type', (mimetypes.guess_type(str(file))[0] or 'application/octet-stream') + ('; charset=utf-8' if file.suffix == '.html' else ''))
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_):
        pass


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class Api:
    def open_external(self, url):
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme in ('http', 'https') and parsed.hostname:
            webbrowser.open(url)


def main():
    try:
        server = Server((HOST, PORT), Handler)
    except OSError as exc:
        print(f'Cannot start BrickLog: port {PORT} is already in use. Close any running copy and try again. ({exc})', file=sys.stderr)
        sys.exit(1)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        webview.settings['ALLOW_DOWNLOADS'] = True
        webview.create_window('BrickLog', f'http://{HOST}:{PORT}/index.html', width=1300, height=900,
                              min_size=(780, 600), background_color='#100e17', js_api=Api())
        if sys.platform == 'win32':
            data_dir = pathlib.Path(os.environ.get('LOCALAPPDATA', pathlib.Path.home())) / 'BrickLog' / 'webview'
        elif sys.platform == 'darwin':
            data_dir = pathlib.Path.home() / 'Library' / 'Application Support' / 'BrickLog' / 'webview'
        else:
            data_dir = pathlib.Path(os.environ.get('XDG_DATA_HOME', pathlib.Path.home() / '.local' / 'share')) / 'BrickLog' / 'webview'
        data_dir.mkdir(parents=True, exist_ok=True)
        # WinForms expects an ICO for the window icon, not a PNG image.
        window_icon = ROOT / ('icon.ico' if sys.platform == 'win32' else 'icon.png')
        webview.start(private_mode=False, storage_path=str(data_dir), icon=str(window_icon))
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    main()
