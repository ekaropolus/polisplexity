from flask import render_template, request, jsonify
from PIL import Image, ImageDraw
import random
from io import BytesIO
from base64 import b64encode
import cmath
import qrcode


def lis_vg_ctr():
    if request.method == 'POST':
        try:
            # Generate a random number to select a function
            input_text = request.form['input_text']
            if input_text:
                return render_template('lis_index.html', image_data=lis_vg_ctr_qrc(input_text))
        except Exception as e:
            return jsonify({'error': f'Error: {e}'}), 400
    return render_template('lis_index.html')


def lis_vg_ctr_qrc(text):
    # Create a QR code image
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a byte buffer
    buffer = BytesIO()
    qr_img.save(buffer, format='PNG')
    buffer.seek(0)

    # Render the image in an HTML template
    return b64encode(buffer.getvalue()).decode()

def lis_vg_ctr_pen():
    # Set up image parameters
    image_size = 256
    pixel_size = 16
    num_pixels = image_size // pixel_size
    background_color = (255, 255, 255)  # white
    penguin_color = (0, 0, 0)  # black

    # Create a new image and drawing context
    image = Image.new('RGB', (image_size, image_size), color=background_color)
    draw = ImageDraw.Draw(image)

    # Draw random black pixels to form penguin shape
    for x in range(num_pixels):
        for y in range(num_pixels):
            if random.random() < 0.5:  # 50% chance to draw black pixel
                draw.rectangle(
                    (x * pixel_size, y * pixel_size, (x+1) * pixel_size, (y+1) * pixel_size),
                    fill=penguin_color
                )

    # Save the image to a byte buffer
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    # Render the image in an HTML template
    return b64encode(buffer.getvalue()).decode()


def lis_vg_ctr_pan():
    # Define image size and background color
    size = (400, 400)
    background_color = (255, 255, 255)

    # Create a new PIL Image object with the given size and background color
    image = Image.new('RGB', size, background_color)

    # Create a PIL ImageDraw object to draw on the image
    draw = ImageDraw.Draw(image)

    # Define penguin parameters
    head_size = (200, 200)
    head_position = (100, 100)
    body_size = (250, 200)
    body_position = (75, 250)
    eye_size = 20
    eye_position = (150, 150)
    pupil_size = 10
    pupil_position = (150, 150)
    beak_size = (40, 20)
    beak_position = (175, 180)
    wing_size = (150, 50)
    wing_position = (75, 225)

    # Draw penguin head
    draw.ellipse((head_position, (head_position[0] + head_size[0], head_position[1] + head_size[1])), fill=(0, 0, 0))

    # Draw penguin body
    draw.ellipse((body_position, (body_position[0] + body_size[0], body_position[1] + body_size[1])), fill=(0, 0, 0))

    # Draw penguin eye
    draw.ellipse((eye_position, (eye_position[0] + eye_size, eye_position[1] + eye_size)), fill=(255, 255, 255))

    # Draw penguin pupil
    pupil_position = (random.randint(eye_position[0], eye_position[0] + eye_size - pupil_size), random.randint(eye_position[1], eye_position[1] + eye_size - pupil_size))
    draw.ellipse((pupil_position, (pupil_position[0] + pupil_size, pupil_position[1] + pupil_size)), fill=(0, 0, 0))

    # Draw penguin beak
    draw.polygon([beak_position, (beak_position[0] - beak_size[0] / 2, beak_position[1] + beak_size[1]), (beak_position[0] + beak_size[0] / 2, beak_position[1] + beak_size[1])], fill=(255, 165, 0))

    # Draw penguin wing
    wing_position = (random.randint(body_position[0], body_position[0] + body_size[0] - wing_size[0]), wing_position[1])
    draw.ellipse((wing_position, (wing_position[0] + wing_size[0], wing_position[1] + wing_size[1])), fill=(0, 0, 0))

    # Save the image to a byte buffer
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    # Render the image in an HTML template
    return b64encode(buffer.getvalue()).decode()



def lis_vg_ctr_man():
    # Generate random values for width, height, and max_iter
    width = 500
    height = 500
    max_iter = random.randint(100, 200)

    # Generate a random center point
    center_x = random.uniform(-2, 1)
    center_y = random.uniform(-1, 1)

    # Create a new image
    image = Image.new('RGB', (width, height), color='black')

    # Create a list to store the RGB values of each pixel
    pixels = []

    # Loop through each pixel in the image
    for x in range(width):
        for y in range(height):
            # Convert pixel coordinates to Mandelbrot coordinates
            c = complex(center_x + (4 * (x - width / 2) / width),
                        center_y + (4 * (y - height / 2) / width))

            # Calculate the Mandelbrot value for this coordinate
            z = 0
            for i in range(max_iter):
                if abs(z) > 2:
                    break
                z = z * z + c

            # Convert the Mandelbrot value to an RGB value
            if i == max_iter - 1:
                color = (0, 0, 0)
            else:
                color = (255 - i * 10 % 255, 255 - i * 20 % 255, 255 - i * 30 % 255)

            # Add the RGB value to the list of pixels
            pixels.append(color)

    # Create a new image from the list of pixels
    image.putdata(pixels)

    # Save the image to a byte buffer
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    # Render the image in an HTML template
    return b64encode(buffer.getvalue()).decode()

def lis_vg_ctr_geo():
    # Define the number of colors in the palette
    num_colors = 8

    # Generate a random palette of colors
    palette = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for i in range(num_colors)]

    # Define a list of geometric shapes
    shapes = [
        'rectangle',
        'ellipse',
        'polygon',
        'line'
    ]

    # Generate a random geometric figure
    width = 500
    height = 500
    shape_width = int(width * 0.1)
    shape_height = int(height * 0.1)

    image = Image.new('RGB', (width, height), palette[0])
    draw = ImageDraw.Draw(image)

    for i in range(20):
        shape = random.choice(shapes)
        x, y = random.randint(0, width), random.randint(0, height)
        # x2, y2 = random.randint(0, width), random.randint(0, height)
        color = random.choice(palette)
        if shape == 'rectangle':
            draw.rectangle((x, y, x + shape_width, y + shape_height), fill=color)
        elif shape == 'ellipse':
            draw.ellipse((x, y, x + shape_width, y + shape_height), fill=color)
        elif shape == 'polygon':
            points = [(random.randint(0, width), random.randint(0, height)) for i in range(3)]
            draw.polygon(points, fill=color)
        elif shape == 'line':
            draw.line((x, y, x + shape_width, y + shape_height), fill=color, width=2)

    # Change any white pixel to a random color
    pixels = image.load()
    for x in range(width):
        for y in range(height):
            if pixels[x, y] == palette[0]:
                pixels[x, y] = random.choice(palette[1:])

    # Save the image to a byte buffer
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    # Render the image in an HTML template
    return b64encode(buffer.getvalue()).decode()

def lis_vg_ctr_frac():
    # Generate random values for width, height, and max_iter
    width = 500
    height = 500
    max_iter = random.randint(100, 200)

    # Generate a random list of complex numbers to define the fractal
    fractal_points = [complex(random.uniform(-2, 2), random.uniform(-2, 2)) for i in range(10)]

    # Create a new image
    image = Image.new('RGB', (width, height), color='black')

    # Create a list to store the RGB values of each pixel
    pixels = []

    # Loop through each pixel in the image
    for x in range(width):
        for y in range(height):
            # Convert pixel coordinates to complex number
            c = complex(x / width * 4 - 2, y / height * 4 - 2)

            # Calculate the value of the fractal function at this point
            z = 0
            for i in range(max_iter):
                for point in fractal_points:
                    z += point * cmath.exp(1j * cmath.phase(c - point))

                if abs(z) > 2:
                    break

            # Convert the fractal value to an RGB value
            if i == max_iter - 1:
                color = (0, 0, 0)
            else:
                color = (255 - i * 10 % 255, 255 - i * 20 % 255, 255 - i * 30 % 255)

            # Add the RGB value to the list of pixels
            pixels.append(color)

    # Create a new image from the list of pixels
    image.putdata(pixels)

    # Save the image to a byte buffer
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    # Render the image in an HTML template
    return b64encode(buffer.getvalue()).decode()
