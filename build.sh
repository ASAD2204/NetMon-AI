#!/bin/bash

# --- CONFIGURATION ---
PKG_NAME="netmon-ai"
VERSION="1.0.0"
ARCH="all"
BUILD_DIR="build_package"
DEB_NAME="${PKG_NAME}_${VERSION}_${ARCH}.deb"

echo "=========================================="
echo "   NetMon-AI: Auto-Builder & Installer    "
echo "=========================================="

# 1. CLEANUP (Remove old builds)
echo "[1/8] Cleaning up old build files..."
rm -rf $BUILD_DIR
rm -f *.deb

# 2. CREATE DIRECTORY STRUCTURE
echo "[2/8] Creating directory structure..."
mkdir -p $BUILD_DIR/DEBIAN
mkdir -p $BUILD_DIR/usr/bin
mkdir -p $BUILD_DIR/usr/share/$PKG_NAME
mkdir -p $BUILD_DIR/etc/$PKG_NAME

# 3. COPY SOURCE CODE
echo "[3/8] Copying source code..."
if [ -d "src" ]; then
    cp -r src/* $BUILD_DIR/usr/share/$PKG_NAME/
else
    echo "Error: 'src' directory not found!"
    exit 1
fi

# 4. GENERATE DEBIAN FILES (Dynamically)

# -> control
cat > $BUILD_DIR/DEBIAN/control <<EOF
Package: $PKG_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Depends: python3, python3-pip, debconf
Maintainer: NetMon Team
Description: Intelligent Network Monitoring Platform
 An AI-powered sysadmin tool. Prompts for Groq API key on install.
EOF

# -> templates (The Question)
cat > $BUILD_DIR/DEBIAN/templates <<EOF
Template: netmon-ai/apikey
Type: string
Description: Enter your GROQ API Key:
 Please paste your Groq Cloud API Key here. This is required for the AI features.
EOF

# -> config (The Trigger)
cat > $BUILD_DIR/DEBIAN/config <<EOF
#!/bin/bash
. /usr/share/debconf/confmodule
db_input high netmon-ai/apikey || true
db_go
EOF

# -> postinst (The Installation Logic)
cat > $BUILD_DIR/DEBIAN/postinst <<EOF
#!/bin/bash
. /usr/share/debconf/confmodule

# Get API Key from debconf
db_get netmon-ai/apikey
USER_API_KEY="\$RET"

# Create secure config directory and store base64-encoded API key
mkdir -p /etc/$PKG_NAME
echo -n "\$USER_API_KEY" | base64 > /etc/$PKG_NAME/.env.b64
chmod 600 /etc/$PKG_NAME/.env.b64

echo "=========================================="
echo "NetMon-AI Configuration Complete"
echo "=========================================="
echo ""
echo "IMPORTANT: Install Python dependencies before running:"
echo ""
echo "  Option 1 (Recommended - Virtual Environment):"
echo "    python3 -m venv /opt/netmon-ai-venv"
echo "    source /opt/netmon-ai-venv/bin/activate"
echo "    pip install -r /usr/share/$PKG_NAME/requirements.txt"
echo "    python3 -m nltk.downloader wordnet"
echo ""
echo "  Option 2 (System-wide):"
echo "    sudo apt-get install python3-pip python3-rich python3-psutil"
echo "    sudo pip3 install groq python-dotenv nltk"
echo "    python3 -m nltk.downloader wordnet"
echo ""
echo "API Key stored securely at: /etc/$PKG_NAME/.env.b64"
echo "Run 'netmon-ai' to start the shell."
echo "=========================================="

# Set permissions on wrapper
chmod +x /usr/bin/$PKG_NAME

exit 0
EOF

# 5. GENERATE EXECUTABLE WRAPPER
# This puts the command in /usr/bin so you can run it from ANYWHERE
cat > $BUILD_DIR/usr/bin/$PKG_NAME <<EOF
#!/bin/bash
export PYTHONPATH=\$PYTHONPATH:/usr/share/$PKG_NAME
python3 /usr/share/$PKG_NAME/shell.py "\$@"
EOF

# 6. SET PERMISSIONS
echo "[6/8] Setting permissions..."
chmod 755 $BUILD_DIR/DEBIAN/postinst
chmod 755 $BUILD_DIR/DEBIAN/config
chmod 755 $BUILD_DIR/usr/bin/$PKG_NAME

# 7. BUILD PACKAGE
echo "[7/8] Building .deb package..."
dpkg-deb --build $BUILD_DIR $DEB_NAME

# 8. INSTALL PACKAGE
echo "[8/8] Installing $PKG_NAME..."
sudo dpkg -i $DEB_NAME

echo "=========================================="
echo "   SUCCESS! Type 'netmon-ai' to start.    "
echo "=========================================="