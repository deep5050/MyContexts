import sys
import os
from PIL import Image, ImageOps, ImageDraw


def add_rounded_border(draw, width, height, border_color, outer_roundness):
    # Create rounded rectangle for the outer border
    draw.rounded_rectangle(
        [(0, 0), (width, height)],
        radius=outer_roundness,
        fill=border_color
    )

def add_border(input_image_path):
    # Define local variables for border settings
    border_width = 100  # Width of the border
    border_color = "white"  # Color of the border
    output_quality = 95  # Quality of the output image
    outer_roundness = 0  # Outer roundness (0 for square, higher for more rounded)
    inner_roundness = 0  # Inner roundness (0 for square, higher for more rounded)

    # Open the original image and handle orientation
    with Image.open(input_image_path) as img:
        img = ImageOps.exif_transpose(img)  # Correct orientation based on EXIF data
        
        # Create a new image with a transparent background
        bordered_img = Image.new("RGBA", (img.width + border_width, img.height + border_width), (255, 255, 255, 0))
        
        # Create a draw object
        draw = ImageDraw.Draw(bordered_img)

        # Add the outer rounded border
        add_rounded_border(draw, bordered_img.width, bordered_img.height, border_color, outer_roundness)

        # Paste the original image onto the bordered image
        bordered_img.paste(img, (border_width // 2, border_width // 2), img.convert("RGBA"))  # Use alpha channel for transparency

        # Create the output file path
        base, ext = os.path.splitext(input_image_path)
        output_image_path = f"{base}_bordered{ext}"

        # Save the new image with quality parameter
        if ext.lower() in ['.jpg', '.jpeg']:
            bordered_img.convert("RGB").save(output_image_path, quality=output_quality)  # Convert to RGB for JPEG
        else:
            bordered_img.save(output_image_path)  # Save as is for other formats

        print(f"Saved bordered image as: {output_image_path}")


# sometimes a filename with spaces is passed as a single argument
# but program is splitting it into multiple arguments
# so wee need to gather all arguments into a single string

def gather_args():
    args = sys.argv[1:]
    return ' '.join(args)

if __name__ == "__main__":
    image_path = gather_args()
    if not image_path:
        print("Usage: python add_border.py <image_path>")
        sys.exit(1)
    add_border(image_path)
