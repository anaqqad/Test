#!/usr/bin/env bash
# Install Blender (headless) + Rhubarb Lip Sync on an Ubuntu/Debian VPS, then render a test frame.
#   sudo bash blender/install_vps.sh
set -euo pipefail
BLENDER_SERIES=4.2   # long-term-support line
apt-get update -q
apt-get install -y -q libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1 libegl1 libegl-mesa0 libgl1-mesa-dri \
  libxkbcommon0 libsm6 xz-utils wget unzip ca-certificates
# newest 4.2.x build
FILE=$(wget -qO- "https://download.blender.org/release/Blender${BLENDER_SERIES}/" | grep -oE "blender-${BLENDER_SERIES}\.[0-9]+-linux-x64\.tar\.xz" | sort -uV | tail -1)
echo "downloading $FILE"
cd /opt && wget -q "https://download.blender.org/release/Blender${BLENDER_SERIES}/$FILE"
tar -xf "$FILE" && rm "$FILE" && rm -rf /opt/blender && mv "${FILE%.tar.xz}" /opt/blender
ln -sf /opt/blender/blender /usr/local/bin/blender
# Rhubarb Lip Sync (mouth shapes from narration audio)
wget -q https://github.com/DanielSWolf/rhubarb-lip-sync/releases/download/v1.13.0/Rhubarb-Lip-Sync-1.13.0-Linux.zip -O /tmp/rhubarb.zip
rm -rf /opt/rhubarb && unzip -q /tmp/rhubarb.zip -d /opt && mv /opt/Rhubarb-Lip-Sync-1.13.0-Linux /opt/rhubarb && ln -sf /opt/rhubarb/rhubarb /usr/local/bin/rhubarb
blender --version | head -1
rhubarb --version
blender -b --factory-startup --python-expr "import bpy; s=bpy.context.scene; s.render.engine='BLENDER_EEVEE_NEXT'; s.render.filepath='/tmp/blender_test.png'; bpy.ops.render.render(write_still=True)" 2>&1 | grep -E "Saved|Error" || true
ls -la /tmp/blender_test.png && echo "Blender OK"
