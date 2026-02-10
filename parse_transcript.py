#!/usr/bin/env python3
"""
Parse MS Word transcription .docx files to CSV and PDF formats.

This script parses .docx files produced by MS Word's audio transcription feature
and converts them to both CSV and PDF files with Speaker, Timestamp, and Text.

MS Word transcription format:
    00:00:05 Speaker Name
    Transcribed text goes here.
    
    00:00:15 Another Speaker
    More transcribed text.

Output:
    - CSV file: Structured data with Speaker, Timestamp, Text columns
    - PDF file: Formatted, human-readable transcript for archiving/sharing

Usage:
    python parse_transcript.py <input.docx> [output.csv]
    
    Note: PDF is always created with the same basename as the .docx file
"""

import sys
import csv
import re
from pathlib import Path
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT


# Constants
TIMESTAMP_PATTERN = r'(\d+:\d+(?::\d+)?)'
DEFAULT_SPEAKER = 'Unknown'
DEFAULT_TIMESTAMP = '0:00:00'


def parse_timestamp(timestamp_str):
    """
    Parse timestamp string to a standardized format.
    Handles formats like "0:00:05", "00:05", etc.
    
    Args:
        timestamp_str: String containing the timestamp
        
    Returns:
        Formatted timestamp string
    """
    timestamp_str = timestamp_str.strip()
    # Remove any brackets or parentheses
    timestamp_str = re.sub(r'[\[\]\(\)]', '', timestamp_str)
    return timestamp_str


def parse_docx_transcript(docx_path):
    """
    Parse a .docx transcript file and extract speaker, timestamp, and text.
    
    MS Word transcription creates paragraphs in this format:
    - Timestamp followed by speaker name (e.g., "00:00:05 Speaker 1" or "0:00:05 Josiah")
    - Text content in following paragraphs
    
    Args:
        docx_path: Path to the .docx file
        
    Returns:
        List of dictionaries with keys: Speaker, Timestamp, Text
    """
    doc = Document(docx_path)
    transcript_data = []
    
    current_speaker = None
    current_timestamp = None
    current_text = []
    
    # Skip header lines (like "Audio file", "Transcript", etc.)
    skip_patterns = [
        r'^Audio file',
        r'^Transcript\s*$',
        r'^\s*$'
    ]
    
    for para in doc.paragraphs:
        text = para.text.strip()
        
        if not text:
            continue
        
        # Skip header/intro lines
        if any(re.match(pattern, text, re.IGNORECASE) for pattern in skip_patterns):
            continue
            
        # Check if this is a timestamp/speaker line
        # MS Word format: "00:00:05 Speaker Name" or "0:05 Jason"
        timestamp_speaker_pattern = rf'^{TIMESTAMP_PATTERN}\s+(.+)$'
        match = re.match(timestamp_speaker_pattern, text)
        
        if match:
            # Save previous entry if exists
            if current_speaker and current_text:
                transcript_data.append({
                    'Speaker': current_speaker.strip(),
                    'Timestamp': current_timestamp,
                    'Text': ' '.join(current_text).strip()
                })
                current_text = []
            
            # Start new entry (timestamp is first group, speaker is second)
            current_timestamp = parse_timestamp(match.group(1))
            current_speaker = match.group(2).strip()
        else:
            # This is text content - add to current entry
            if current_speaker:
                current_text.append(text)
    
    # Don't forget the last entry
    if current_speaker and current_text:
        transcript_data.append({
            'Speaker': current_speaker.strip(),
            'Timestamp': current_timestamp,
            'Text': ' '.join(current_text).strip()
        })
    
    return transcript_data


def write_csv(transcript_data, output_path):
    """
    Write transcript data to CSV file.
    
    Args:
        transcript_data: List of dictionaries with Speaker, Timestamp, Text
        output_path: Path to output CSV file
    """
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Speaker', 'Timestamp', 'Text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in transcript_data:
            writer.writerow(row)


def write_pdf(transcript_data, output_path, source_file=None):
    """
    Write transcript data to PDF file.
    
    Args:
        transcript_data: List of dictionaries with Speaker, Timestamp, Text
        output_path: Path to output PDF file
        source_file: Optional source file name to include in header
    """
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for the 'Flowable' objects
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        alignment=TA_LEFT
    )
    
    speaker_style = ParagraphStyle(
        'Speaker',
        parent=styles['Normal'],
        fontSize=11,
        textColor='#1a5490',
        spaceAfter=4,
        fontName='Helvetica-Bold'
    )
    
    text_style = ParagraphStyle(
        'Text',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12,
        alignment=TA_LEFT
    )
    
    # Add title
    if source_file:
        title = Paragraph(f"Oral History Transcript: {source_file}", title_style)
    else:
        title = Paragraph("Oral History Transcript", title_style)
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # Add transcript entries
    for entry in transcript_data:
        # Speaker and timestamp
        speaker_text = f"<b>{entry['Speaker']}</b> [{entry['Timestamp']}]"
        speaker_para = Paragraph(speaker_text, speaker_style)
        story.append(speaker_para)
        
        # Text content
        text_para = Paragraph(entry['Text'], text_style)
        story.append(text_para)
        story.append(Spacer(1, 0.1*inch))
    
    # Build PDF
    doc.build(story)


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_transcript.py <input.docx> [output.csv]")
        print("\nExample:")
        print("  python parse_transcript.py 'Audio file.docx'")
        print("  python parse_transcript.py 'Audio file.docx' transcript.csv")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)
    
    if not input_path.suffix.lower() == '.docx':
        print(f"Error: Input file must be a .docx file.")
        sys.exit(1)
    
    # Determine output path
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.with_suffix('.csv')
    
    # Also create PDF with same basename
    pdf_path = input_path.with_suffix('.pdf')
    
    print(f"Parsing transcript from: {input_path}")
    
    try:
        transcript_data = parse_docx_transcript(input_path)
        
        if not transcript_data:
            print("Warning: No transcript data found in the document.")
            print("\nExpected format (Microsoft Word transcription):")
            print("  00:00:05 Speaker Name")
            print("  Transcribed text goes here.")
            print("\nPlease check that your document follows Microsoft Word's transcription format.")
            sys.exit(1)
        
        # Write CSV
        write_csv(transcript_data, output_path)
        print(f"✓ Created CSV with {len(transcript_data)} entries: {output_path}")
        
        # Write PDF
        write_pdf(transcript_data, pdf_path, source_file=input_path.stem)
        print(f"✓ Created PDF transcript: {pdf_path}")
        
        print(f"\nSuccessfully processed transcript!")
        
    except Exception as e:
        print(f"Error processing transcript: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
