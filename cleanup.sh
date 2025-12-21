#!/usr/bin/env bash
set -e

echo "========== Linux Safe Cleanup Started =========="

echo "[1/8] Cleaning APT cache..."
sudo apt clean
sudo apt autoclean

echo "[2/8] Removing unused packages..."
sudo apt autoremove --purge -y

echo "[3/8] Clearing user cache (~/.cache)..."
rm -rf ~/.cache/* || true

echo "[4/8] Clearing pip cache (if available)..."
python3 -m pip cache purge 2>/dev/null || true

echo "[5/8] Cleaning systemd journal logs (last 7 days kept)..."
sudo journalctl --vacuum-time=7d

echo "[6/8] Cleaning /tmp directory..."
sudo rm -rf /tmp/* || true

if command -v docker >/dev/null 2>&1; then
    echo "[7/8] Cleaning Docker unused data..."
    docker system prune -f
else
    echo "[7/8] Docker not installed, skipping..."
fi

echo "[8/8] Dropping Linux filesystem caches (RAM cleanup)..."
sync
echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null

echo "========== Cleanup Completed Successfully =========="
echo "Recommended: If using WSL, run 'wsl --shutdown' from PowerShell for full RAM reclaim."