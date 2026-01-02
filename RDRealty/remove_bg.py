from PIL import Image, ImageDraw
import os

def remove_outer_background_smart(input_path, output_path):
    try:
        # Open and convert to RGBA (Red, Green, Blue, Alpha/Transparency)
        img = Image.open(input_path).convert("RGBA")
        width, height = img.size
        
        # We assume the background color is the color at the top-left corner (0,0)
        # Usually this is white (255, 255, 255)
        # We will use the floodfill algorithm starting from the corners.
        # This acts like the "Magic Wand" tool in Photoshop with "Contiguous" checked.
        
        # Settings:
        # xy: The starting point (seed)
        # value: The color to replace with -> (255, 255, 255, 0) means White but fully Transparent
        # thresh: Tolerance. 50 allows it to eat through slightly off-white pixels (compression noise)
        
        # 1. Flood fill from Top-Left
        ImageDraw.floodfill(img, xy=(0, 0), value=(255, 255, 255, 0), thresh=50)
        
        # 2. Check other corners just in case they are isolated
        corners = [(width-1, 0), (0, height-1), (width-1, height-1)]
        for x, y in corners:
            pixel = img.getpixel((x, y))
            # If the corner is still white (and not yet transparent), flood fill from there too
            if pixel[3] != 0 and all(c > 200 for c in pixel[:3]):
                 ImageDraw.floodfill(img, xy=(x, y), value=(255, 255, 255, 0), thresh=50)

        img.save(output_path, "PNG")
        print(f"Successfully saved smart transparent image to {output_path}")
        
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    input_file = r"d:\Projects\RDRealty\static\images\RDCorp.png"
    output_file = r"d:\Projects\RDRealty\static\images\RDCorp_transparent.png"
    
    if os.path.exists(input_file):
        remove_outer_background_smart(input_file, output_file)
    else:
        print(f"Input file not found: {input_file}")
