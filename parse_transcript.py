#!/usr/bin/env python3
"""
Parse MS Word transcription .docx files to CSV format.

This script parses .docx files produced by MS Word's audio transcription feature
and converts them to a CSV file with Speaker, Timestamp, and Text columns.

Usage:
    python parse_transcript.py <input.docx> [output.csv]
"""

import sys
import csv
import re
from pathlib import Path
from docx import Document


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
    
    MS Word transcription typically creates paragraphs in this format:
    - Speaker name followed by timestamp (e.g., "Speaker 1 0:00:05")
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
    
    for para in doc.paragraphs:
        text = para.text.strip()
        
        if not text:
            continue
            
        # Check if this is a speaker/timestamp line
        # Typical format: "Speaker 1 0:00:05" or "Speaker 1: 0:00:05"
        speaker_pattern = r'^(.+?)\s+(\d+:\d+(?::\d+)?)\s*$'
        match = re.match(speaker_pattern, text)
        
        if match:
            # Save previous entry if exists
            if current_speaker and current_text:
                transcript_data.append({
                    'Speaker': current_speaker.strip(),
                    'Timestamp': current_timestamp,
                    'Text': ' '.join(current_text).strip()
                })
                current_text = []
            
            # Start new entry
            current_speaker = match.group(1).strip()
            current_timestamp = parse_timestamp(match.group(2))
        else:
            # This is text content
            if current_speaker:
                current_text.append(text)
            else:
                # Text without a speaker - check if it contains timestamp
                # Sometimes format is: "0:00:05 Some text here"
                time_first_pattern = r'^(\d+:\d+(?::\d+)?)\s+(.+)'
                match = re.match(time_first_pattern, text)
                if match:
                    if current_text:
                        # Save previous entry
                        transcript_data.append({
                            'Speaker': current_speaker or 'Unknown',
                            'Timestamp': current_timestamp or '0:00:00',
                            'Text': ' '.join(current_text).strip()
                        })
                        current_text = []
                    
                    current_timestamp = parse_timestamp(match.group(1))
                    current_text.append(match.group(2))
                else:
                    # Just text, add to current entry
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
    
    print(f"Parsing transcript from: {input_path}")
    
    try:
        transcript_data = parse_docx_transcript(input_path)
        
        if not transcript_data:
            print("Warning: No transcript data found in the document.")
            sys.exit(1)
        
        write_csv(transcript_data, output_path)
        
        print(f"Successfully created CSV with {len(transcript_data)} entries.")
        print(f"Output file: {output_path}")
        
    except Exception as e:
        print(f"Error processing transcript: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
