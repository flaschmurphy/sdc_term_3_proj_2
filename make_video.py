import cv2
import glob
from PIL import Image

path_with = "./runs/1532182063.4049609_with_initialization/"
path_without = "./runs/1532127389.1123831_without_initialization/"

input_images = [p.split('/')[-1] for p in glob.glob("runs/1532182063.4049609_with_initialization/*")]

def preprocess():
    """Load each pair of images and create a new image that is both glued together horizontally"""
    input_images = [p.split('/')[-1] for p in glob.glob("runs/1532182063.4049609_with_initialization/*")]
    for input_image in input_images:
        print("Pre-processing %s" % input_image)

        images = [Image.open(i) for i in [path_without + input_image, path_with + input_image]]

        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)

        new_img = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for img in images:
            new_img.paste(img, (x_offset,0))
            x_offset += img.size[0]
        new_img.save('movie_images/%s.jpg' % input_image.split(".")[0])

    return total_width, max_height


def make_movie(width, height):
    """Load all the preprocessed images and convert them into a movie"""
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter("video.mp4", fourcc, 20.0, (width, height))

    for input_image in glob.glob(path_with + "*"):
        image_path = input_image
        print("Processing %s" % image_path)
        frame = cv2.imread(image_path)
        out.write(frame)

    out.release()
    cv2.destroyAllWindows()


def main():
    width, height = preprocess()
    make_movie(width, height)


if __name__ == "__main__":
    main()
