import sys
import rawpy
import numpy as np
from PIL import Image, ImageEnhance

# Computer\HKEY_CLASSES_ROOT\SystemFileAssociations\.arw\shell\Convert To JPG\command
# "C:\Users\dpal\Documents\code\MyContexts\ConvertRAW.bat" "%1"

def convert_arw_to_jpg(input_path):
    # Read the ARW file
    with rawpy.imread(input_path) as raw:
        # Convert to RGB
        rgb = raw.postprocess(
            use_camera_wb=True,
            no_auto_bright=False,
            output_bps=16,
            half_size=False,
            no_auto_scale=False,
            output_color=rawpy.ColorSpace.sRGB,
            bright=1.6
        )

    # Convert to uint8 format
    rgb = (rgb / 256).astype(np.uint8)  # Scale down to 0-255 and convert to uint8

    # Convert to a PIL Image
    img = Image.fromarray(rgb)

    # Check for underexposure
    # Calculate the average brightness
    grayscale = img.convert("L")
    avg_brightness = np.mean(np.array(grayscale))
    print(f"Average brightness: {avg_brightness}")

    # Define a threshold for underexposure (you can adjust this value)
    underexposure_threshold = 90  # Adjust this value based on your needs

    if avg_brightness < underexposure_threshold:
        print(
            "Underexposed image detected. Applying adjustments with 30% increase in brightness"
        )
        # Increase exposure slightly by adjusting brightness
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.3)  # Increase brightness by 30%

    # Save the image as JPG with the same name
    output_path = input_path.rsplit(".", 1)[0] + ".jpg"
    img.save(output_path, format="JPEG", quality=95)  # Save with desired quality

    print(f"Converted {input_path} to {output_path}")


def gather_args():
    args = sys.argv[1:]
    return " ".join(args)


if __name__ == "__main__":
    image_path = gather_args()
    if not image_path:
        print("Usage: python add_border.py <image_path>")
        sys.exit(1)
    convert_arw_to_jpg(image_path)
