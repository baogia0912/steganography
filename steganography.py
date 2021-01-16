import click
from PIL import Image

class Steganography(object):

    @staticmethod
    def __int_to_bin(rgb):
        r, g, b = rgb
        return ('{0:08b}'.format(r),
                '{0:08b}'.format(g),
                '{0:08b}'.format(b))

    @staticmethod
    def __bin_to_int(rgb):
        r, g, b = rgb
        return (int(r, 2),
                int(g, 2),
                int(b, 2))

    @staticmethod
    def __merge_rgb(rgb1, rgb2):
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:4] + r2[:4],
               g1[:4] + g2[:4],
               b1[:4] + b2[:4])
        return rgb

    @staticmethod
    def merge(img1, img2):

        # Get the pixel map of the two images
        pixel_map1 = img1.load()
        pixel_map2 = img2.load()

        # Create a new image that will be outputted
        new_image = Image.new(img1.mode, img1.size)
        pixels_new = new_image.load()

        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb1 = Steganography.__int_to_bin(pixel_map1[i, j])

                # Use a black pixel as default
                rgb2 = Steganography.__int_to_bin((0, 0, 0))

                # Check if the pixel map position is valid for the second image
                if i < img2.size[0] and j < img2.size[1]:
                    rgb2 = Steganography.__int_to_bin(pixel_map2[i, j])
                
                # Merge the two pixels and convert it to a integer tuple
                rgb = Steganography.__merge_rgb(rgb1, rgb2)

                pixels_new[i, j] = Steganography.__bin_to_int(rgb)
        
        return new_image, (img2.size[0], img2.size[1])
    @staticmethod
    def unmerge(img, key):

        # Load the pixel map
        pixel_map = img.load()
        
        # Create the new image and load the pixel map
        new_image = Image.new(img.mode, img.size)
        pixels_new = new_image.load()

        # Tuple used to store the image original size
        original_size = key

        for i in range(key[0]):
            for j in range(key[1]):
                # Get the RGB (as a string tuple) from the current pixel
                r, g, b = Steganography.__int_to_bin(pixel_map[i, j])

                # Extract the last 4 bits (corresponding to the hidden image)
                # Concatenate 4 zero bits because we are working with 8 bit
                rgb = (r[4:] + '0000',
                    g[4:] + '0000',
                    b[4:] + '0000')

                # Convert it to an integer tuple
                pixels_new[i, j] = Steganography.__bin_to_int(rgb)

        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

        return new_image
    

def cli():
    merge('Mona.jpg', 'Jon.jpg', 'stego.png')
    key = (251,256)
    unmerge('stego.png', key, 'HiddenJon.png')
    
def merge(img1, img2, output):
    merged_image, key = Steganography.merge(Image.open(img1), Image.open(img2))
    merged_image.save(output)
    print("merge sucsessfully")
    print("the key to unmerge is: ", key)

def unmerge(img, key, output):
    unmerged_image = Steganography.unmerge(Image.open(img), key)
    unmerged_image.save(output)
    print("unmerge sucsessfully")

if __name__ == '__main__':
    cli()