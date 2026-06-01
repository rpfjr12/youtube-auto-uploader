# video_generator.py
import os
from pathlib import Path
from datetime import datetime

def generate_video(script_text, title, topic="general", duration_seconds=45):
    """
    Generate a 1080x1920 (vertical) video with text overlay.
    
    Args:
        script_text: The script or text to display
        title: Title for the video
        topic: Topic for file naming
        duration_seconds: Duration of video (30-60)
    
    Returns:
        Path to the generated .mp4 file
    """
    try:
        from moviepy.editor import TextClip, ColorClip, CompositeVideoClip, AudioFileClip
        import random
    except ImportError:
        raise ImportError("moviepy is required. Install with: pip install moviepy")
    
    # Ensure uploads folder exists
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{topic}_{timestamp}.mp4"
    output_path = str(uploads_dir / filename)
    
    # Video dimensions (vertical: 1080x1920)
    width, height = 1080, 1920
    duration = float(duration_seconds)
    
    # Choose a background color (randomized for variety)
    colors = [(25, 25, 112), (220, 20, 60), (34, 139, 34), (65, 105, 225), (178, 34, 34)]
    bg_color = random.choice(colors)
    
    # Create background
    background = ColorClip(size=(width, height), color=bg_color)
    
    # Create text clip with the script
    # Split script into lines for better readability
    lines = script_text.split('\n')
    text_content = '\n'.join(line.strip() for line in lines if line.strip())
    
    try:
        text_clip = TextClip(
            text_content,
            fontsize=48,
            font="Arial",
            color="white",
            method="caption",
            size=(width - 80, height - 200),
            align="center"
        )
    except Exception:
        # Fallback if caption method fails
        text_clip = TextClip(
            text_content,
            fontsize=40,
            font="Arial",
            color="white",
            size=(width - 80, height - 200),
            align="center"
        )
    
    # Duration of text display
    text_clip = text_clip.set_duration(duration)
    
    # Center text vertically
    text_clip = text_clip.set_position("center")
    
    # Create composite
    video = CompositeVideoClip(
        [background, text_clip],
        size=(width, height)
    )
    video.duration = duration
    
    # Write video file
    video.write_videofile(
        output_path,
        fps=24,
        verbose=False,
        logger=None
    )
    
    return output_path


def generate_simple_video(script_text, title, topic="general", duration_seconds=45):
    """
    Fallback: Generate a simpler video without moviepy dependencies.
    Uses PIL to create image frames and ffmpeg-python to compose video.
    
    Args:
        script_text: The script or text to display
        title: Title for the video
        topic: Topic for file naming
        duration_seconds: Duration of video (30-60)
    
    Returns:
        Path to the generated .mp4 file
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        import subprocess
        import tempfile
        import shutil
    except ImportError:
        raise ImportError("PIL and ffmpeg are required")
    
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{topic}_{timestamp}.mp4"
    output_path = str(uploads_dir / filename)
    
    width, height = 1080, 1920
    fps = 24
    total_frames = fps * duration_seconds
    
    # Create temp directory for frames
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create frames
        bg_color = (25, 25, 112)  # Dark blue
        
        for frame_idx in range(total_frames):
            img = Image.new("RGB", (width, height), color=bg_color)
            draw = ImageDraw.Draw(img)
            
            # Try to use a standard font
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            except:
                font = ImageFont.load_default()
            
            # Wrap text
            lines = script_text.split('\n')
            y_offset = height // 4
            for line in lines:
                if line.strip():
                    bbox = draw.textbbox((0, 0), line, font=font)
                    line_width = bbox[2] - bbox[0]
                    x = (width - line_width) // 2
                    draw.text((x, y_offset), line, fill=(255, 255, 255), font=font)
                    y_offset += 100
            
            frame_path = os.path.join(tmpdir, f"frame_{frame_idx:06d}.png")
            img.save(frame_path)
        
        # Use ffmpeg to create video
        try:
            cmd = [
                "ffmpeg",
                "-framerate", str(fps),
                "-i", os.path.join(tmpdir, "frame_%06d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-y",
                output_path
            ]
            subprocess.run(cmd, capture_output=True, check=True)
        except Exception as e:
            raise RuntimeError(f"Failed to create video with ffmpeg: {e}")
    
    return output_path


if __name__ == "__main__":
    script = "This is a test script.\n\nIt demonstrates video generation.\n\nSwipe up to learn more!"
    try:
        output = generate_video(script, "Test Video", "test", duration_seconds=10)
        print(f"Video generated: {output}")
    except Exception as e:
        print(f"Note: {e}")
        print("MoviePy requires ffmpeg. Install with: pip install moviepy")
