#!/usr/bin/env python3
"""
Convert image to C array bitmap for OLED display
"""
from PIL import Image
import sys
import os

def image_to_bitmap_array(image_path, width=128, height=64, invert=False):
    """
    Convert image to C array bitmap format for OLED displays
    
    Args:
        image_path: Path to image file
        width: Target width (default 128 for SSD1306)
        height: Target height (default 64 for SSD1306)
        invert: Invert black/white (default False - black=0, white=1)
    """
    # Open and process image
    img = Image.open(image_path)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Resize to target dimensions
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    # Convert to black and white (1-bit)
    img = img.convert('1', dither=Image.Dither.FLOYDSTEINBERG)
    
    # Get pixel data
    pixels = list(img.getdata())
    
    # Calculate bytes per row (round up to nearest byte)
    bytes_per_row = (width + 7) // 8
    
    # Generate C array
    bitmap_array = []
    for y in range(height):
        row_bytes = []
        for x_byte in range(bytes_per_row):
            byte_val = 0
            for bit in range(8):
                x = x_byte * 8 + bit
                if x < width:
                    pixel_index = y * width + x
                    # In PIL's 1-bit mode: 0=black, 255=white
                    # For OLED: typically 1=white/on, 0=black/off
                    pixel_on = pixels[pixel_index] > 0
                    if invert:
                        pixel_on = not pixel_on
                    if pixel_on:
                        byte_val |= (0x80 >> bit)  # Set bit from MSB
            row_bytes.append(byte_val)
        bitmap_array.extend(row_bytes)
    
    return bitmap_array, width, height

def format_c_array(bitmap_array, name="myBitmap"):
    """Format bitmap array as C code"""
    output = f"const unsigned char {name}[] PROGMEM = {{\n"
    
    for i, byte in enumerate(bitmap_array):
        if i % 16 == 0:
            output += "  "
        output += f"0x{byte:02x}"
        if i < len(bitmap_array) - 1:
            output += ","
        if i % 16 == 15 or i == len(bitmap_array) - 1:
            output += "\n"
        elif i < len(bitmap_array) - 1:
            output += " "
    
    output += "};\n"
    return output

if __name__ == "__main__":
    # Get image path
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    else:
        img_path = "../img/image.png"
    
    # Get dimensions
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 128
    height = int(sys.argv[3]) if len(sys.argv) > 3 else 64
    
    # Check if invert flag is set
    invert = "--invert" in sys.argv or "-i" in sys.argv
    
    if not os.path.exists(img_path):
        print(f"Error: Image file '{img_path}' not found!")
        sys.exit(1)
    
    print(f"Converting: {img_path}")
    print(f"Target size: {width}x{height}")
    print(f"Invert colors: {invert}")
    print()
    
    # Convert image
    bitmap_array, w, h = image_to_bitmap_array(img_path, width, height, invert)
    
    # Generate C code
    c_code = format_c_array(bitmap_array)
    
    # Print results
    print(f"// Bitmap: {w}x{h} pixels")
    print(f"// Array size: {len(bitmap_array)} bytes")
    print()
    print(c_code)
    
    # Save to file
    output_file = "bitmap_output.txt"
    with open(output_file, 'w') as f:
        f.write(f"// Bitmap from: {img_path}\n")
        f.write(f"// Size: {w}x{h} pixels ({len(bitmap_array)} bytes)\n\n")
        f.write(c_code)
    
    print(f"\nBitmap code saved to: {output_file}")
