import os
STORAGE_FOLDER = os.environ.get('STORAGE_FOLDER')
STORAGE_BASE_URL = os.environ.get('STORAGE_BASE_URL')

def save_pil_image(image, id, name):
    output = os.path.join(STORAGE_FOLDER,id)
    os.makedirs(output, exist_ok=True)
    image.save(os.path.join(output, name))
    return f'{STORAGE_BASE_URL}/{id}/{name}'

def save_input(image, id):
    return save_pil_image(image, id, 'input.jpg')

def save_aligned(image, id):
    return save_pil_image(image, id, 'aligned.jpg')

def save_layout(image, id):
    return save_pil_image(image, id, 'layout.jpg')

