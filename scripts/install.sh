#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
dest_root=${CODEX_SKILLS_DIR:-"$HOME/.codex/skills"}
backup_root="$dest_root/.codex-skills-backup-$(date +%Y%m%d-%H%M%S)"

skills="
find-skills
humanize-writing
keep-codex-fast
pdf
seppuku
source-intake
startup-pressure-test
storyboard-review
thread-workspace-relink
video-perception
"

mkdir -p "$dest_root"

installed=0
skipped=0
replaced=0
backed_up=0

for skill in $skills; do
  src="$repo_root/skills/$skill"
  dest="$dest_root/$skill"

  if [ ! -d "$src" ]; then
    printf 'missing source skill: %s\n' "$src" >&2
    exit 1
  fi

  if [ -e "$dest" ]; then
    printf '%s already exists at %s\n' "$skill" "$dest"
    printf 'Replace it? [y/N] '
    answer=
    read answer || answer=
    case "$answer" in
      y|Y|yes|YES)
        mkdir -p "$backup_root"
        backup_dest="$backup_root/$skill"
        if [ -e "$backup_dest" ]; then
          printf 'backup path already exists: %s\n' "$backup_dest" >&2
          exit 1
        fi
        mv "$dest" "$backup_dest"
        backed_up=$((backed_up + 1))
        cp -R "$src" "$dest"
        printf 'replaced %s (backup: %s)\n' "$skill" "$backup_dest"
        replaced=$((replaced + 1))
        ;;
      *)
        printf 'skipped %s\n' "$skill"
        skipped=$((skipped + 1))
        ;;
    esac
  else
    cp -R "$src" "$dest"
    printf 'installed %s\n' "$skill"
    installed=$((installed + 1))
  fi
done

printf '\nDone. Installed %s, replaced %s, skipped %s.\n' "$installed" "$replaced" "$skipped"
if [ "$backed_up" -gt 0 ]; then
  printf 'Backups saved in %s\n' "$backup_root"
fi
printf 'Restart Codex or open a fresh session so the skill list reloads.\n'
