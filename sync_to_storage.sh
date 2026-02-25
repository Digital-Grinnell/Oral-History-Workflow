#!/bin/bash

# Rsync script to backup Oral-History-Workflow to storage
# This creates a complete copy including all files (no .gitignore omissions)

SOURCE="/Users/mcfatem/GitHub/Oral-History-Workflow/"
DEST="/Volumes/MEDIADB/DGIngest/Oral-History-Workflow/"

# Check if the MEDIADB volume is mounted
if [ ! -d "/Volumes/MEDIADB" ]; then
  echo "Error: MEDIADB volume is not mounted at /Volumes/MEDIADB"
  echo "Please mount the network share first."
  exit 1
fi

echo "Starting sync from $SOURCE to $DEST"
echo "================================================"

rsync -avh \
  --progress \
  --delete \
  --exclude='.git/' \
  --exclude='.venv/' \
  --exclude='.*/' \
  "$SOURCE" "$DEST"

if [ $? -eq 0 ]; then
  echo "================================================"
  echo "Removing hidden flags from synced files..."
  chflags -R nohidden "$DEST" 2>/dev/null || true
  echo "Sync completed successfully!"
else
  echo "================================================"
  echo "Sync failed with error code $?"
  exit 1
fi
