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
  echo "Main sync completed successfully!"
else
  echo "================================================"
  echo "Main sync failed with error code $?"
  exit 1
fi

echo ""
echo "================================================"
echo "Bidirectional sync for Reunion-2025-Oral-Histories"
echo "================================================"

REUNION_LOCAL="/Users/mcfatem/GitHub/Oral-History-Workflow/Reunion-2025-Oral-Histories/"
REUNION_STORAGE="/Volumes/MEDIADB/DGIngest/Oral-History-Workflow/Reunion-2025-Oral-Histories/"

# Create storage directory if it doesn't exist
mkdir -p "$REUNION_STORAGE"

# First sync: Storage -> Local (get remote changes)
echo "Syncing from storage to local..."
rsync -avh \
  --progress \
  "$REUNION_STORAGE" "$REUNION_LOCAL"

if [ $? -ne 0 ]; then
  echo "Warning: Sync from storage to local had errors (code $?)"
fi

# Second sync: Local -> Storage (push local changes)
echo ""
echo "Syncing from local to storage..."
rsync -avh \
  --progress \
  "$REUNION_LOCAL" "$REUNION_STORAGE"

if [ $? -eq 0 ]; then
  echo "================================================"
  echo "Bidirectional sync completed successfully!"
else
  echo "================================================"
  echo "Bidirectional sync failed with error code $?"
  exit 1
fi
