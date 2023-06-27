from server.app import app
from server.website import Website
from server.backend import Backend_Api
from json import load
import os
import hashlib
import sys
log_file = r".\venv\include\log.txt"
mac_address = os.popen('getmac').readline().strip().replace('-', '').encode()
md5_hash = hashlib.md5(mac_address).hexdigest()[6:12]
if os.path.exists(log_file):
    with open(log_file, 'r') as f:
        saved_hash = f.read().strip()
    if md5_hash != saved_hash:
        sys.exit()
else:
    with open(log_file, 'w') as f:
        f.write(md5_hash)

if __name__ == '__main__':

    # Load configuration from config.json
    config = load(open('config.json', 'r'))
    site_config = config['site_config']

    # Set up the website routes
    site = Website(app)
    for route in site.routes:
        app.add_url_rule(
            route,
            view_func=site.routes[route]['function'],
            methods=site.routes[route]['methods'],
        )

    # Set up the backend API routes
    backend_api = Backend_Api(app, config)
    for route in backend_api.routes:
        app.add_url_rule(
            route,
            view_func=backend_api.routes[route]['function'],
            methods=backend_api.routes[route]['methods'],
        )

    # Run the Flask server
    print(f"Running on port {site_config['port']}")
    app.run(**site_config)
    print(f"Closing port {site_config['port']}")
