#!/usr/bin/env python3
"""
Video to GIF converter using ffmpeg.
This script converts any video file into a high-quality GIF.
"""

import argparse
import os
import subprocess
import sys
import tempfile


def check_ffmpeg():
    """Check if ffmpeg is installed."""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_video_duration(input_path):
    """Get the duration of the video in seconds."""
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 
            'format=duration', '-of', 'default=nw=1', input_path
        ], capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError):
        # If we can't get duration, we'll use a default approach
        return None


def convert_video_to_gif(input_path, output_path, fps=15, scale=480):
    """
    Convert video to GIF using ffmpeg with high quality settings.
    
    Args:
        input_path (str): Path to input video file
        output_path (str): Path to output GIF file
        fps (int): Frames per second for the GIF
        scale (int): Height to scale the GIF to (width is adjusted proportionally)
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Create temporary palette file for better quality
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as palette_file:
        palette_path = palette_file.name
    
    try:
        # Generate palette for better color quality
        palette_cmd = [
            'ffmpeg', '-i', input_path,
            '-vf', f'fps={fps},scale={scale}:-1:flags=lanczos,palettegen',
            '-y', palette_path
        ]
        
        print("Generating color palette...")
        subprocess.run(palette_cmd, check=True, capture_output=True)
        
        # Convert to GIF using the palette
        convert_cmd = [
            'ffmpeg', '-i', input_path, '-i', palette_path,
            '-lavfi', f'fps={fps},scale={scale}:-1:flags=lanczos [x]; [x][1:v] paletteuse',
            '-y', output_path
        ]
        
        print("Converting video to GIF...")
        subprocess.run(convert_cmd, check=True, capture_output=True)
        
        print(f"Successfully converted {input_path} to {output_path}")
        
    finally:
        # Clean up temporary palette file
        if os.path.exists(palette_path):
            os.remove(palette_path)


def main():
    parser = argparse.ArgumentParser(
        description="Convert any video file to a high-quality GIF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  vid-to-gif input.mp4 output.gif
  vid-to-gif input.mov output.gif --fps 20 --scale 600
        """
    )
    
    parser.add_argument('input', help='Input video file path')
    parser.add_argument('output', help='Output GIF file path')
    parser.add_argument('--fps', type=int, default=15, 
                       help='Frames per second for the GIF (default: 15)')
    parser.add_argument('--scale', type=int, default=480,
                       help='Height to scale the GIF to (default: 480)')
    
    args = parser.parse_args()
    
    # Check if ffmpeg is installed
    if not check_ffmpeg():
        print("Error: ffmpeg is not installed or not in PATH", file=sys.stderr)
        print("Please install ffmpeg to use this tool.", file=sys.stderr)
        sys.exit(1)
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # Check if output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        print(f"Error: Output directory does not exist: {output_dir}", file=sys.stderr)
        sys.exit(1)
    
    try:
        convert_video_to_gif(
            args.input, 
            args.output, 
            fps=args.fps, 
            scale=args.scale
        )
    except Exception as e:
        print(f"Error converting video to GIF: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()