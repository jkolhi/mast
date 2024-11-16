from PIL import Image
import subprocess
import tempfile
import os

def create_iconset(svg_file, iconset_path):
    """Create an iconset directory with all required sizes for macOS"""
    sizes = {
        '16x16': '16',
        '32x32': '32',
        '64x64': '64',
        '128x128': '128',
        '256x256': '256',
        '512x512': '512',
    }
    
    # Create iconset directory
    os.makedirs(iconset_path, exist_ok=True)
    
    for name, size in sizes.items():
        # Normal resolution
        output_path = os.path.join(iconset_path, f'icon_{name}.png')
        subprocess.run([
            'rsvg-convert',
            '-w', size,
            '-h', size,
            svg_file,
            '-o', output_path
        ], check=True)
        
        # High resolution (2x)
        size_2x = str(int(size) * 2)
        output_path_2x = os.path.join(iconset_path, f'icon_{name}@2x.png')
        subprocess.run([
            'rsvg-convert',
            '-w', size_2x,
            '-h', size_2x,
            svg_file,
            '-o', output_path_2x
        ], check=True)

def svg_to_icons(svg_file, ico_path, icns_path):
    """Convert SVG to both ICO and ICNS formats"""
    try:
        # Create temporary iconset directory
        with tempfile.TemporaryDirectory() as temp_dir:
            iconset_path = os.path.join(temp_dir, 'icon.iconset')
            create_iconset(svg_file, iconset_path)
            
            # Convert iconset to icns using iconutil (macOS only)
            subprocess.run([
                'iconutil',
                '-c', 'icns',
                iconset_path,
                '-o', icns_path
            ], check=True)
            
            # Create ICO file
            images = []
            ico_sizes = [16, 32, 48, 64, 128, 256]
            
            for size in ico_sizes:
                png_path = os.path.join(iconset_path, f'icon_{size}x{size}.png')
                if os.path.exists(png_path):
                    img = Image.open(png_path)
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    images.append(img)
            
            # Save as ICO
            images[0].save(
                ico_path,
                format='ICO',
                sizes=[(img.width, img.height) for img in images],
                append_images=images[1:]
            )
            
        print(f"Successfully created {ico_path} and {icns_path}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error converting icons: {e}")
    except Exception as e:
        print(f"Error: {e}")

# SVG data
svg_data = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="45" fill="#1A365D"/>
    <path d="M30 50 Q40 20, 50 50 T70 50" 
          fill="none" 
          stroke="#4299E1" 
          stroke-width="4"
          stroke-linecap="round"/>
    <path d="M25 50 Q40 10, 50 50 T75 50" 
          fill="none" 
          stroke="#63B3ED" 
          stroke-width="3"
          stroke-linecap="round"/>
    <path d="M20 50 Q40 0, 50 50 T80 50" 
          fill="none" 
          stroke="#90CDF4" 
          stroke-width="2"
          stroke-linecap="round"/>
</svg>'''

# Save SVG to a temporary file
with tempfile.NamedTemporaryFile(suffix='.svg', mode='w', delete=False) as tmp_svg:
    tmp_svg.write(svg_data)
    svg_file_path = tmp_svg.name

try:
    # Convert SVG to both ICO and ICNS
    svg_to_icons(svg_file_path, 'app_icon.ico', 'app_icon.icns')
finally:
    # Clean up the temporary SVG file
    os.unlink(svg_file_path)