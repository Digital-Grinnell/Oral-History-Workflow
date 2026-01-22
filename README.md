# Oral History Workflow

A home for Oral History workflow documents and scripts for use with CollectionBuilder and possibly Document Alma.

## Overview

This repository contains tools and documentation for processing oral history audio files into structured transcripts. The workflow uses Microsoft Word's built-in transcription feature to convert audio files into text, then processes the resulting .docx files into CSV format for easier data management and analysis.

## Workflow

### 1. Audio Transcription with Microsoft Word

Microsoft Word (Office 365) includes a built-in transcription feature that can process .mp3 and other audio files:

1. Open Microsoft Word
2. Go to the **Home** tab
3. Click **Dictate** dropdown → **Transcribe**
4. Upload your .mp3 audio file
5. Wait for transcription to complete
6. Word will create a transcript with:
   - Speaker identification (Speaker 1, Speaker 2, etc.)
   - Timestamps for each segment
   - Transcribed text

7. Save or export the transcript as a .docx file

The resulting .docx file will have a structure similar to:
```
Speaker 1 0:00:05
This is the first thing that was said in the recording.

Speaker 2 0:00:15
This is a response from another speaker.

Speaker 1 0:00:28
Continuation of the conversation...
```

### 2. Converting .docx to CSV

Once you have the .docx transcript file from Microsoft Word, you can convert it to a structured CSV format using the `parse_transcript.py` script.

## Usage

### Prerequisites

- Python 3.6 or higher
- Required Python packages (install using requirements.txt)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/Digital-Grinnell/Oral-History-Workflow.git
cd Oral-History-Workflow
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Parser

Convert a .docx transcript to CSV:

```bash
python parse_transcript.py "Audio file.docx"
```

This will create a CSV file with the same name (e.g., `Audio file.csv`) in the same directory.

You can also specify a custom output filename:

```bash
python parse_transcript.py "Audio file.docx" "transcript.csv"
```

### Output Format

The generated CSV file contains three columns:

- **Speaker**: The speaker identifier (e.g., "Speaker 1", "Speaker 2")
- **Timestamp**: The time marker for when the text was spoken (e.g., "0:00:05")
- **Text**: The transcribed text content

Example CSV output:
```csv
Speaker,Timestamp,Text
Speaker 1,0:00:05,This is the first thing that was said in the recording.
Speaker 2,0:00:15,This is a response from another speaker.
Speaker 1,0:00:28,Continuation of the conversation...
```

## Files in This Repository

- **parse_transcript.py**: Python script to convert .docx transcripts to CSV format
- **requirements.txt**: Python package dependencies
- **README.md**: This documentation file

## Notes

- The parser is designed to work with the specific format produced by Microsoft Word's transcription feature
- Speaker names in the .docx file may need to be manually edited if you want to use actual names instead of "Speaker 1", "Speaker 2", etc.
- The script handles various timestamp formats (e.g., "0:05", "0:00:05", "1:23:45")

## Troubleshooting

**Error: Input file not found**
- Make sure the file path is correct and the file exists
- Use quotes around filenames with spaces

**Error: No transcript data found**
- Check that the .docx file contains properly formatted transcript data
- Ensure the document follows the expected format (Speaker + Timestamp, then Text)

**Import errors**
- Make sure you've installed the requirements: `pip install -r requirements.txt`

## Future Enhancements

Potential improvements to consider:
- Support for additional audio transcription formats
- Automatic speaker name mapping
- Integration with CollectionBuilder
- Batch processing of multiple files
- Support for SRT/VTT subtitle formats

## License

This project is maintained by Digital Grinnell for processing oral history collections.
