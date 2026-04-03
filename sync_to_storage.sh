#!/bin/bash

# Rsync script to backup Oral-History-Workflow to storage
# This creates a complete copy including all files (no .gitignore omissions)

SOURCE="/Users/mcfatem/GitHub/Oral-History-Workflow/"

# Check if at least one volume is mounted
MEDIADB_MOUNTED=false
ACASIS_MOUNTED=false

if [ -d "/Volumes/MEDIADB" ]; then
  MEDIADB_MOUNTED=true
fi

if [ -d "/Volumes/Acasis1TB" ]; then
  ACASIS_MOUNTED=true
fi

if [ "$MEDIADB_MOUNTED" = false ] && [ "$ACASIS_MOUNTED" = false ]; then
  echo "Error: No backup volumes are mounted!"
  echo "Please mount at least one of:"
  echo "  - /Volumes/MEDIADB (network storage)"
  echo "  - /Volumes/Acasis1TB (local backup)"
  exit 1
fi

echo "Backup volumes detected:"
echo "  MEDIADB: $MEDIADB_MOUNTED"
echo "  Acasis1TB: $ACASIS_MOUNTED"
echo ""

# Sync to MEDIADB if mounted
if [ "$MEDIADB_MOUNTED" = true ]; then
  DEST="/Volumes/MEDIADB/DGIngest/Oral-History-Workflow/"
  
  echo "================================================"
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
    echo "MEDIADB sync completed successfully!"
  else
    echo "================================================"
    echo "MEDIADB sync failed with error code $?"
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
else
  echo "Note: MEDIADB volume not mounted, skipping network storage sync."
fi

# Sync to Acasis1TB if mounted
if [ "$ACASIS_MOUNTED" = true ]; then
  echo ""
  echo "================================================"
  echo "Syncing to Acasis1TB volume"
  echo "================================================"
  
  ACASIS_DEST="/Volumes/Acasis1TB/Oral-History-Workflow/"
  
  echo "Starting sync from $SOURCE to $ACASIS_DEST"
  
  rsync -avh \
    --progress \
    --delete \
    --exclude='.git/' \
    --exclude='.venv/' \
    --exclude='.*/' \
    "$SOURCE" "$ACASIS_DEST"
  
  if [ $? -eq 0 ]; then
    echo "================================================"
    echo "Removing hidden flags from synced files..."
    chflags -R nohidden "$ACASIS_DEST" 2>/dev/null || true
    echo "Acasis1TB sync completed successfully!"
  else
    echo "================================================"
    echo "Acasis1TB sync failed with error code $?"
    exit 1
  fi
else
  echo ""
  echo "Note: Acasis1TB volume not mounted, skipping local backup."
fi

echo ""
echo "================================================"
echo "All available backups completed successfully!"
echo "================================================"
