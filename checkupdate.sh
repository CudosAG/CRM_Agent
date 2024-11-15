#!/bin/bash

# Wechsle in das Verzeichnis deines Git-Repositories
cd /root/CRM_Agent || exit

# Führe git fetch aus, um die neuesten Änderungen vom Remote-Repository abzurufen
git fetch

# Ueberprüfe den Status des Repositories
status_output=$(git status)

# Ueberprüfe, ob die Meldung "your branch is behind" im Status-Output enthalten ist
if echo "$status_output" | grep -q "Your branch is behind"; then
    echo "Der lokale Branch ist hinter dem Remote-Branch."
    # Hier rufst du dein anderes Skript auf
    # bash /pfad/zu/deinem/anderes_script.sh
    source update.sh
else
    echo "Der lokale Branch ist auf dem neuesten Stand."
fi

