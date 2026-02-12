#!/usr/bin/env python3
"""
Oral History Workflow - Flet App
A GUI application to streamline the oral history transcription workflow:
1. Select an MP3 file
2. Guide user through MS Word Online transcription
3. Convert DOCX to CSV using parse_transcript.py
"""

import flet as ft
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


def main(page: ft.Page):
    page.title = "Oral History Workflow"
    page.padding = 20
    page.window.width = 900
    page.window.height = 700
    
    # State variables
    selected_mp3_path = None
    
    # UI Components
    status_text = ft.Text(
        "Ready to begin",
        color=ft.Colors.BLUE_400,
        size=14,
        italic=True
    )
    
    result_text = ft.Text(
        "Select an MP3 file to get started",
        size=14,
        selectable=True
    )
    
    instructions_container = ft.Container(
        visible=False,
        padding=15,
        bgcolor=ft.Colors.BLUE_50,
        border=ft.Border.all(2, ft.Colors.BLUE_300),
        border_radius=8
    )
    
    convert_button = ft.Container(visible=False)
    
    async def pick_mp3_file(e):
        nonlocal selected_mp3_path
        
        status_text.value = "Opening file picker..."
        status_text.color = ft.Colors.BLUE_400
        page.update()
        
        files = await file_picker.pick_files(
            allowed_extensions=["mp3"],
            dialog_title="Select an MP3 file to transcribe"
        )
        
        if files:
            selected_mp3_path = files[0].path
            mp3_file = Path(selected_mp3_path)
            
            result_text.value = f"Selected: {mp3_file.name}\nLocation: {mp3_file.parent}"
            status_text.value = "MP3 file selected"
            status_text.color = ft.Colors.GREEN_400
            
            # Show instructions
            show_transcription_instructions(mp3_file)
            page.update()
        else:
            result_text.value = "No file selected"
            status_text.value = "File selection cancelled"
            status_text.color = ft.Colors.ORANGE_400
            instructions_container.visible = False
            convert_button.visible = False
            page.update()
    
    def show_transcription_instructions(mp3_file):
        """Display step-by-step transcription instructions."""
        expected_docx = mp3_file.with_suffix('.docx')
        
        instructions_content = ft.Column([
            ft.Text(
                "📝 TRANSCRIPTION INSTRUCTIONS",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900
            ),
            ft.Divider(height=10, color=ft.Colors.BLUE_200),
            
            ft.Text(
                "STEP 1: Open Microsoft Word Online",
                size=14,
                weight=ft.FontWeight.BOLD
            ),
            ft.Row([
                ft.Icon(ft.Icons.OPEN_IN_BROWSER, color=ft.Colors.BLUE_700),
                ft.TextButton(
                    "Click here to open Word Online",
                    url="https://www.office.com/launch/word",
                    style=ft.ButtonStyle(
                        color=ft.Colors.BLUE_700,
                    )
                ),
            ]),
            ft.Column([
                ft.Text("(Microsoft 365 subscription required)", size=12, italic=True),
                ft.Text("• Click 'Create blank document'", size=12, weight=ft.FontWeight.BOLD),
                ft.Text("• Copy this document name:", size=12, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text(
                        mp3_file.stem,
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        selectable=True
                    ),
                    bgcolor=ft.Colors.BLUE_900,
                    padding=8,
                    border_radius=4
                ),
                ft.Text("• Click on 'Document X' at the top of the Word window", size=12),
                ft.Text("• Paste the name to replace it", size=12),
                ft.Text("• Press Enter to confirm", size=12),
            ], spacing=3),
            
            ft.Container(height=10),
            ft.Text(
                "STEP 2: Start Transcription",
                size=14,
                weight=ft.FontWeight.BOLD
            ),
            ft.Column([
                ft.Text("• Click the 'Home' tab (if not already selected)"),
                ft.Text("• Click 'Dictate' dropdown → Select 'Transcribe'"),
                ft.Text("• In the Transcribe pane, click 'Upload audio'"),
                ft.Text(f"• Browse to and select: {mp3_file.name}", weight=ft.FontWeight.BOLD),
                ft.Text("• Wait for transcription to complete (may take several minutes)"),
            ], spacing=5),
            
            ft.Container(height=10),
            ft.Text(
                "STEP 3: Edit & Save",
                size=14,
                weight=ft.FontWeight.BOLD
            ),
            ft.Column([
                ft.Text("• Edit speaker names if needed (e.g., replace 'Speaker 1' with actual names)"),
                ft.Text("• When complete, click 'Add to document'"),
                ft.Text("• Save the document with this EXACT name:", weight=ft.FontWeight.BOLD),
                ft.Text("  - Click the File menu in Word", style=ft.TextStyle(italic=True)),
                ft.Text("  - Select 'Create a Copy'", style=ft.TextStyle(italic=True)),
                ft.Text("  - Select 'Download a Copy'", style=ft.TextStyle(italic=True)),
                ft.Text("  - Click 'Download a Copy' to confirm", style=ft.TextStyle(italic=True)),
                ft.Text("  - The file will be saved to your Downloads folder", style=ft.TextStyle(italic=True)),
                ft.Container(
                    content=ft.Text(
                        expected_docx.name,
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    bgcolor=ft.Colors.BLUE_900,
                    padding=8,
                    border_radius=4
                ),
                ft.Text(
                    f"• Save it in the SAME folder as the MP3:",
                    weight=ft.FontWeight.BOLD
                ),
                ft.Container(
                    content=ft.Text(
                        str(mp3_file.parent),
                        size=12,
                        selectable=True
                    ),
                    bgcolor=ft.Colors.GREY_100,
                    padding=8,
                    border_radius=4
                ),
            ], spacing=5),
            
            ft.Container(height=10),
            ft.Text(
                "STEP 4: Convert to CSV and PDF",
                size=14,
                weight=ft.FontWeight.BOLD
            ),
            ft.Text("Once you've saved the DOCX file, click the button below to create both CSV and PDF versions."),
        ], spacing=8)
        
        instructions_container.content = instructions_content
        instructions_container.visible = True
        convert_button.visible = True
    
    async def convert_docx_to_csv(e):
        """Run parse_transcript.py to convert DOCX to CSV."""
        if not selected_mp3_path:
            result_text.value = "Error: No MP3 file selected"
            status_text.value = "Error"
            status_text.color = ft.Colors.RED_400
            page.update()
            return
        
        mp3_file = Path(selected_mp3_path)
        expected_docx = mp3_file.with_suffix('.docx')
        expected_csv = mp3_file.with_suffix('.csv')
        expected_pdf = mp3_file.with_suffix('.pdf')
        
        # Check if DOCX exists
        if not expected_docx.exists():
            result_text.value = f"❌ Error: DOCX file not found!\n\nExpected file:\n{expected_docx}\n\nPlease complete the transcription steps above and save the file."
            status_text.value = "DOCX file not found"
            status_text.color = ft.Colors.RED_400
            page.update()
            return
        
        status_text.value = "Converting DOCX to CSV and PDF..."
        status_text.color = ft.Colors.BLUE_400
        result_text.value = "Processing transcript, please wait..."
        page.update()
        
        try:
            # Get the path to parse_transcript.py in the same directory
            script_dir = Path(__file__).parent
            parse_script = script_dir / "parse_transcript.py"
            
            if not parse_script.exists():
                result_text.value = f"❌ Error: parse_transcript.py not found at:\n{parse_script}"
                status_text.value = "Script not found"
                status_text.color = ft.Colors.RED_400
                page.update()
                return
            
            # Run parse_transcript.py
            result = subprocess.run(
                [sys.executable, str(parse_script), str(expected_docx), str(expected_csv)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Success!
                result_text.value = f"✅ Success!\n\nFiles created:\n• CSV: {expected_csv}\n• PDF: {expected_pdf}\n\n{result.stdout}"
                status_text.value = "Conversion complete!"
                status_text.color = ft.Colors.GREEN_400
            else:
                # Error occurred
                result_text.value = f"❌ Error during conversion:\n\n{result.stderr}\n\n{result.stdout}"
                status_text.value = "Conversion failed"
                status_text.color = ft.Colors.RED_400
                
        except Exception as ex:
            result_text.value = f"❌ Error running conversion:\n{str(ex)}"
            status_text.value = "Error"
            status_text.color = ft.Colors.RED_400
        
        page.update()
    
    # Create FilePicker
    file_picker = ft.FilePicker()
    page.services.append(file_picker)
    
    # Configure convert button
    convert_button.content = ft.Button(
        "Convert DOCX to CSV & PDF",
        icon=ft.Icons.TRANSFORM,
        on_click=convert_docx_to_csv,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREEN_700,
        )
    )
    
    # Build UI
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    # Header
                    ft.Text(
                        "Oral History Workflow",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900
                    ),
                    ft.Text(
                        "MP3 → Transcription → CSV Pipeline",
                        size=16,
                        color=ft.Colors.GREY_700
                    ),
                    ft.Divider(height=20, color=ft.Colors.BLUE_200),
                    
                    # File picker button
                    ft.Container(
                        content=ft.Button(
                            "1. Select MP3 File",
                            icon=ft.Icons.AUDIO_FILE,
                            on_click=pick_mp3_file,
                            style=ft.ButtonStyle(
                                color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.BLUE_700,
                            )
                        ),
                        padding=ft.padding.only(bottom=10)
                    ),
                    
                    # Status
                    status_text,
                    ft.Container(height=5),
                    
                    # Result display
                    ft.Container(
                        content=result_text,
                        bgcolor=ft.Colors.GREY_100,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                        padding=15,
                    ),
                    
                    ft.Container(height=15),
                    
                    # Instructions (hidden initially)
                    instructions_container,
                    
                    ft.Container(height=10),
                    
                    # Convert button (hidden initially)
                    convert_button,
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=5,
                expand=True
            ),
            expand=True
        )
    )


if __name__ == "__main__":
    ft.run(main)
