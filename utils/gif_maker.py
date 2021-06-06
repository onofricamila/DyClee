import glob
from PIL import Image

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
def generate_gif(folder_in, folder_out, name = 'gif'):
    imgs = glob.glob(folder_in + "/*")
    frames = []
    for i in sorted(imgs):
        new_frame = Image.open(i)
        frames.append(new_frame)
    frames[0].save(folder_out + name + '.gif', format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=2000, loop=0)