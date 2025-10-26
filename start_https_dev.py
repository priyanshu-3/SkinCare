#!/usr/bin/env python3
"""
HTTPS Development Server for GPS Testing
This script creates a self-signed SSL certificate and starts an HTTPS server
to enable GPS functionality in development.
"""

import http.server
import ssl
import socketserver
import os
import subprocess
import sys
from pathlib import Path

def create_self_signed_cert():
    """Create a self-signed SSL certificate for HTTPS development"""
    cert_file = "localhost.pem"
    key_file = "localhost-key.pem"
    
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print("✅ SSL certificate already exists")
        return cert_file, key_file
    
    print("🔐 Creating self-signed SSL certificate...")
    
    # Create certificate using OpenSSL
    cmd = [
        "openssl", "req", "-x509", "-newkey", "rsa:4096", "-keyout", key_file,
        "-out", cert_file, "-days", "365", "-nodes", "-subj",
        "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print("✅ SSL certificate created successfully")
        return cert_file, key_file
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create SSL certificate: {e}")
        print("💡 Install OpenSSL: brew install openssl")
        return None, None
    except FileNotFoundError:
        print("❌ OpenSSL not found. Installing...")
        try:
            subprocess.run(["brew", "install", "openssl"], check=True)
            subprocess.run(cmd, check=True, capture_output=True)
            print("✅ SSL certificate created successfully")
            return cert_file, key_file
        except subprocess.CalledProcessError:
            print("❌ Failed to install OpenSSL. Please install manually:")
            print("   brew install openssl")
            return None, None

def start_https_server(port=8443):
    """Start HTTPS server with SSL certificate"""
    cert_file, key_file = create_self_signed_cert()
    
    if not cert_file or not key_file:
        print("❌ Cannot start HTTPS server without SSL certificate")
        return
    
    class HTTPSHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Add CORS headers for GPS testing
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    try:
        with socketserver.TCPServer(("", port), HTTPSHandler) as httpd:
            # Create SSL context
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(cert_file, key_file)
            
            # Wrap socket with SSL
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            
            print(f"🚀 HTTPS Development Server started")
            print(f"📍 URL: https://localhost:{port}")
            print(f"🔐 GPS will work on this HTTPS URL")
            print(f"⚠️  Accept the security warning in your browser")
            print(f"🛑 Press Ctrl+C to stop")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error starting HTTPS server: {e}")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8443
    start_https_server(port)
