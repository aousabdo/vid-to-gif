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


def convert_video_to_gif(input_path, output_path, fps=15, scale=480, verbose=False):
    """
    Convert video to GIF using ffmpeg with high quality settings.
    
    Args:
        input_path (str): Path to input video file
        output_path (str): Path to output GIF file
        fps (int): Frames per second for the GIF (1-60)
        scale (int): Height to scale the GIF to (16-4096)
        verbose (bool): Whether to print detailed output
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Validate parameters
    if not 1 <= fps <= 60:
        raise ValueError("FPS must be between 1 and 60")
    
    if not 16 <= scale <= 4096:
        raise ValueError("Scale must be between 16 and 4096 pixels")
    
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
        
        if verbose:
            print("Generating color palette...")
            print(" ".join(palette_cmd))
        
        subprocess.run(palette_cmd, check=True, capture_output=not verbose)
        
        # Convert to GIF using the palette
        convert_cmd = [
            'ffmpeg', '-i', input_path, '-i', palette_path,
            '-lavfi', f'fps={fps},scale={scale}:-1:flags=lanczos [x]; [x][1:v] paletteuse',
            '-y', output_path
        ]
        
        if verbose:
            print("Converting video to GIF...")
            print(" ".join(convert_cmd))
        
        subprocess.run(convert_cmd, check=True, capture_output=not verbose)
        
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
                       help='Frames per second for the GIF (default: 15, range: 1-60)')
    parser.add_argument('--scale', type=int, default=480,
                       help='Height to scale the GIF to (default: 480, range: 16-4096)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Print detailed output')
    
    args = parser.parse_args()
    
    # Check if ffmpeg is installed
    if not check_ffmpeg():
        print("Error: ffmpeg is not installed or not in PATH", file=sys.stderr)
        print("Please install ffmpeg to use this tool:", file=sys.stderr)
        print("  - macOS: brew install ffmpeg", file=sys.stderr)
        print("  - Ubuntu/Debian: sudo apt install ffmpeg", file=sys.stderr)
        print("  - Windows: Download from https://ffmpeg.org/download.html", file=sys.stderr)
        sys.exit(1)
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        print("Please check the file path and ensure the file exists.", file=sys.stderr)
        sys.exit(1)
    
    # Check if output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        print(f"Error: Output directory does not exist: {output_dir}", file=sys.stderr)
        print("Please create the directory or specify a valid path.", file=sys.stderr)
        sys.exit(1)
    
    try:
        convert_video_to_gif(
            args.input, 
            args.output, 
            fps=args.fps, 
            scale=args.scale,
            verbose=args.verbose
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Please check your parameters and try again.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error converting video to GIF: {e}", file=sys.stderr)
        print("Please check the input file and ensure it's a valid video.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()