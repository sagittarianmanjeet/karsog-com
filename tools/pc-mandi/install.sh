#!/usr/bin/env bash
# Installs the karsog.com mandi helper on this Ubuntu PC (no sudo needed).
#   bash <(curl -fsSL https://raw.githubusercontent.com/sagittarianmanjeet/karsog-com/main/tools/pc-mandi/install.sh)
# Runs ~10 minutes after the PC starts (or after you log in), then every 4 hours while it stays on.
# Uninstall: systemctl --user disable --now karsog-mandi.timer && rm -r ~/.local/share/karsog-mandi
set -euo pipefail

BRANCH="${KARSOG_BRANCH:-main}"
SRC="https://raw.githubusercontent.com/sagittarianmanjeet/karsog-com/${BRANCH}/tools/pc-mandi/karsog-mandi.py"
APP="$HOME/.local/share/karsog-mandi"
CONF="$HOME/.config/karsog-mandi"
UNITS="$HOME/.config/systemd/user"

echo "== karsog.com mandi helper =="
command -v python3 >/dev/null || { echo "python3 is missing: sudo apt install python3"; exit 1; }

mkdir -p "$APP" "$CONF" "$UNITS"
curl -fsSL "$SRC" -o "$APP/karsog-mandi.py"
chmod 755 "$APP/karsog-mandi.py"

if [ ! -s "$CONF/password" ]; then
  echo
  echo "Type the karsog.com mandi password (the ADMIN_KEY you set in Cloudflare), then press Enter."
  echo "(Nothing will show while you type; that's normal.)"
  read -rs KEY < /dev/tty
  echo
  KEY="$(printf '%s' "$KEY" | tr -d '[:space:]')"
  [ -n "$KEY" ] || { echo "Nothing entered. Run this command again."; exit 1; }
  ( umask 077; printf '%s\n' "$KEY" > "$CONF/password" )
else
  echo "Password already saved in $CONF/password (delete that file to enter a new one)."
fi
chmod 600 "$CONF/password"

cat > "$UNITS/karsog-mandi.service" <<EOF
[Unit]
Description=karsog.com mandi rates: fetch from data.gov.in and send to karsog.com
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/env python3 $APP/karsog-mandi.py
TimeoutStartSec=15min
EOF

cat > "$UNITS/karsog-mandi.timer" <<'EOF'
[Unit]
Description=karsog.com mandi rates: 10 min after start, then every 4 hours

[Timer]
OnStartupSec=10min
OnUnitActiveSec=4h
RandomizedDelaySec=2min

[Install]
WantedBy=timers.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now karsog-mandi.timer >/dev/null
# Lets the timer start at boot even before you log in. Fine if it isn't allowed; it then starts when you log in.
loginctl enable-linger "$USER" 2>/dev/null || true

echo
echo "Test run now:"
if python3 "$APP/karsog-mandi.py" --once; then
  echo
  echo "DONE. Prices will now update by themselves whenever this PC is on."
else
  echo
  echo "The test run failed (see the line above). The timer is installed anyway; send the message above to Claude."
fi
echo "Next automatic run: $(systemctl --user list-timers karsog-mandi.timer --no-legend 2>/dev/null | awk '{print $1, $2, $3}')"
