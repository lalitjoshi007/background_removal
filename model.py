import gc
from rembg import remove
from PIL import Image
from model_loading import session  # Import the preloaded model

def process_image(input_image, bg_color="transparent", bg_file=None, output_size=(1024, 1024)):
    try:
        input_image = input_image.convert("RGBA")

        #  Step 1: Remove Background (Using preloaded session)
        output_image = remove(input_image, session=session)

        #  Step 2: Resize Image
        output_image = output_image.resize(output_size, Image.LANCZOS)

        #  Step 3: Center Image on Transparent Canvas
        canvas = Image.new("RGBA", output_size, (0, 0, 0, 0))
        x_offset = (output_size[0] - output_image.size[0]) // 2
        y_offset = (output_size[1] - output_image.size[1]) // 2
        canvas.paste(output_image, (x_offset, y_offset), output_image.convert("RGBA"))

        #  Step 4: Apply Background
        if bg_file:
            bg_image = Image.open(bg_file).convert("RGBA")
            bg_image = bg_image.resize(output_size, Image.LANCZOS)
            new_image = Image.alpha_composite(bg_image, canvas)
        elif bg_color.lower() != "transparent":
            new_image = Image.new("RGB", output_size, bg_color)
            new_image.paste(canvas, (0, 0), canvas)
        else:
            new_image = canvas  # Transparent Background

        #  Step 5: Free Up Memory
        gc.collect()

        return new_image

    except Exception as e:
        print(f"Error processing image: {e}")
        return None
