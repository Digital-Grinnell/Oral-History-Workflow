# Oral History Workflow

A streamlined GUI application for processing oral history audio files into structured transcripts for use with CollectionBuilder and preservation storage.

## Overview

This repository contains a Flet-based GUI application and supporting scripts for processing oral history MP3 files into structured transcripts. The workflow guides you through:

1. **Selecting an MP3 file** - Choose your oral history audio recording
2. **MS Word Online Transcription** - Step-by-step instructions with direct links
3. **Automated Conversion** - One-click conversion from DOCX to CSV and PDF formats

No command-line expertise required! The application handles the entire workflow through an intuitive graphical interface.

## Features

- 🎵 **MP3 File Selection** - Easy file picker for audio files
- 📝 **Guided Transcription** - Clear instructions with links to MS Word Online
- 🔄 **Automatic Conversion** - Convert transcripts to CSV and PDF with one button click
- 📄 **Multiple Formats** - Creates both CSV (for data analysis) and PDF (for reading/archiving)
- 📁 **Smart File Management** - All files saved with matching names in the same folder
- ✅ **Error Checking** - Validates files exist before processing

## Quick Start

Simply run:

```bash
./run.sh
```

That's it! The script will automatically:
- Create a Python virtual environment (if needed)
- Install all required dependencies
- Launch the application

## Detailed Workflow

### Step 1: Launch the Application

```bash
./run.sh
```

### Step 2: Select MP3 File

Click the "Select MP3 File" button and choose your oral history audio recording.

### Step 3: Follow Transcription Instructions

The app will display detailed instructions for:

1. Opening Microsoft Word Online (with direct link)
2. Using Word's Transcribe feature
3. Uploading your MP3 file
4. Editing speaker names
5. Saving the transcript as a .docx file

**Important:** Save the .docx file with the same name as the MP3 and in the same folder!

### Step 4: Convert to CSV and PDF

Once you've saved the .docx transcript:
- Click the "Convert DOCX to CSV & PDF" button
- The app automatically processes the file
- Both CSV and PDF files are saved in the same folder with the same base name

### Output Formats

#### CSV File
The generated CSV file contains three columns:

- **Speaker**: The speaker identifier (e.g., "Josiah", "Jason", or edited names)
- **Timestamp**: The time marker for when the text was spoken (e.g., "00:00:05")
- **Text**: The transcribed text content

Example CSV output:
```csv
Speaker,Timestamp,Text
Josiah,00:00:00,"So hello, what's your name?"
Jason,00:00:02,I'm Jason Stoller.
Josiah,00:00:03,"Jason Stoller, nice to meet you."
```

#### PDF File
The generated PDF provides a formatted, human-readable version of the transcript:

- Professional layout with speaker names in bold
- Timestamps clearly displayed for each entry
- Easy to read, print, or archive
- Perfect for sharing or long-term preservation

## Requirements

- Python 3.8 or higher
- macOS, Windows, or Linux
- Microsoft 365 subscription (for transcription feature)
- Internet connection

## Project Structure

```
Oral-History-Workflow/
├── main.py                    # Flet GUI application
├── parse_transcript.py        # DOCX to CSV converter
├── run.sh                     # Auto-setup and launch script
├── sync_to_storage.sh         # Backup and sync to network storage
├── requirements.txt           # Python dependencies
├── .venv/                     # Virtual environment (auto-created)
├── .gitignore                 # Git exclusions
├── Reunion-2025-Oral-Histories/  # Oral history files (synced but not in Git)
└── README.md                  # This file
```

## Manual Installation (Optional)

If you prefer to set up manually instead of using `./run.sh`:

1. Clone this repository:
```bash
git clone https://github.com/Digital-Grinnell/Oral-History-Workflow.git
cd Oral-History-Workflow
```

2. Create virtual environment:
```bash
python3 -m venv .venv
```

3. Activate virtual environment:
```bash
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python main.py
```

## Command-Line Usage (Advanced)

You can also use the `parse_transcript.py` script directly from the command line:

```bash
python parse_transcript.py "Audio file.docx"
```

This will create both `Audio file.csv` and `Audio file.pdf` in the same directory.

Custom CSV output filename (PDF will still use the .docx basename):
```bash
python parse_transcript.py "Audio file.docx" "custom_output.csv"
```

## Storage Synchronization

The `sync_to_storage.sh` script provides automated backup and synchronization with network storage. This ensures that your work is safely backed up and that the `Reunion-2025-Oral-Histories` directory (which is excluded from Git via `.gitignore`) stays synchronized between your local machine and the storage server.

### What It Does

The script performs up to three operations, depending on which volumes are mounted:

1. **MEDIADB Network Storage Sync** (if mounted):
   - Syncs the entire Oral-History-Workflow directory to network storage
   - Excludes `.git/`, `.venv/`, and other hidden directories
   - Uses `--delete` to mirror the source exactly
   - Removes hidden flags from synced files for compatibility
   - Includes bidirectional sync for Reunion-2025-Oral-Histories:
     * First pulls any changes **from storage to local** (gets remote updates)
     * Then pushes any changes **from local to storage** (sends local updates)
     * Preserves changes made on either side

2. **Acasis1TB Local Backup** (if mounted):
   - Syncs the entire workspace to `/Volumes/Acasis1TB/Oral-History-Workflow/`
   - Same exclusions as network backup (`.git/`, `.venv/`, hidden directories)
   - Provides local redundancy and faster access

**Note:** At least one volume must be mounted for the script to run. Both can be used simultaneously for maximum redundancy.

### Prerequisites

Before running the script, you must mount at least one backup volume:

**Network Storage (MEDIADB):**
- **Network Path**: `smb://storage/MEDIADB/DGIngest/Oral-History-Workflow/`
- **Mount Point**: `/Volumes/MEDIADB/`
- Includes bidirectional sync for Reunion-2025-Oral-Histories

**Local Backup (Acasis1TB):**
- **Mount Point**: `/Volumes/Acasis1TB/`
- Local external drive backup

The script will check for both volumes and use whichever is available. If neither is mounted, it will exit with an error message.

### How to Use

Simply run the script from the project root:

```bash
./sync_to_storage.sh
```

The script will:
1. Check which backup volumes are mounted
2. Exit with error if neither volume is available
3. Sync to MEDIADB (if mounted):
   - Full workspace backup
   - Bidirectional sync for Reunion-2025-Oral-Histories
4. Sync to Acasis1TB (if mounted):
   - Full workspace backup
5. Display progress and status messages
6. Report success or any errors

### When to Use

Run the sync script:
- **After processing oral histories** to back up your work
- **Before starting new work** to pull any changes from storage
- **At the end of each work session** for safety
- **When switching between computers** to keep data synchronized

### Technical Details

- Uses `rsync` with archive mode (`-a`) to preserve permissions and attributes
- Shows progress with `-vh` (verbose + human-readable)
- Creates the storage directory structure if it doesn't exist
- Exit code indicates success (0) or failure (non-zero)

## Troubleshooting

**Virtual environment issues:**
- Delete the `.venv` folder and run `./run.sh` again

**"DOCX file not found" error:**
- Ensure you saved the Word document with the same name as the MP3
- Verify the file is in the same folder as the MP3
- Check the file has a `.docx` extension

**"parse_transcript.py not found" error:**
- Make sure you're running the app from the correct directory
- Verify `parse_transcript.py` exists in the same folder as `main.py`

**Transcription format issues:**
- The parser expects Word's automatic transcription format
- Manually formatted documents may not parse correctly
- Ensure speaker lines follow the format: "Speaker Name 0:00:00"

**Import errors:**
- Run `./run.sh` which auto-installs dependencies
- Or manually: `pip install -r requirements.txt`

## File Naming Convention

For best results, all files should have the same base name:

```
my-interview.mp3          ← Original audio file
my-interview.docx         ← Word transcript (same folder, same name)
my-interview.csv          ← Generated CSV (automatically created)
my-interview.pdf          ← Generated PDF (automatically created)
```

## Notes

- The parser is designed specifically for Microsoft Word's transcription format
- Speaker names can be edited in Word before saving the .docx file
- Both CSV and PDF files are automatically generated from the DOCX
- Timestamps are preserved in the CSV output
- The script handles various timestamp formats (e.g., "0:05", "0:00:05", "1:23:45")
- All processing happens locally - no data is uploaded to external services

## Future Enhancements

Potential improvements to consider:
- Support for additional audio transcription formats
- Automatic speaker name mapping
- Integration with CollectionBuilder
- Batch processing of multiple files
- Direct audio upload to Word Online
- Support for SRT/VTT subtitle formats

## License

This project is maintained by Digital Grinnell for processing oral history collections.

## Support

For issues or questions:
- Check the Troubleshooting section above
- Review the step-by-step instructions in the app
- Ensure all files are named correctly and in the same folder

---

**Version:** 2.1  
**Last Updated:** April 3, 2026  
**Status:** ✅ Production Ready

## Changelog

### Version 2.1 (April 3, 2026)
- Added support for Acasis1TB volume backup in sync_to_storage.sh
- Both MEDIADB and Acasis1TB volumes are now optional (at least one required)
- Script detects which volumes are mounted and syncs to all available
- Improved error handling and status reporting for multiple backup destinations

### Version 2.0 (February 2026)
- Initial production release with Flet GUI application
- MS Word Online transcription workflow
- Automated DOCX to CSV and PDF conversion
- Network storage synchronization
