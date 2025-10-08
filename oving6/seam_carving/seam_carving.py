from PIL import Image, ImageFilter

# Endre disse variablene for å bytte bilde og hvor mye av bildet som
# skal fjernes.
image_name = "tower.jpg"
row_reduction = 100


def find_path(weights):
    # Skriv koden din her
    pass


def img_to_rgb(img):
    return [
        [img.getpixel((j, i)) for j in range(img.width)]
        for i in range(img.height)
    ]


def rgb_to_img(rgb):
    img = Image.new("RGB", (len(rgb[1]), len(rgb)))
    img.putdata([pixel for row in rgb for pixel in row])
    return img


def get_weights(img):
    # Et enkelt Sobel-filter brukes til å finne kanter i bildet. Disse
    # kan brukes som vekter, siden kantene er som regel de viktigste
    # detaljene i bildet.
    edges = img.filter(
        ImageFilter.Kernel((3, 3), (1, 0, -1, 2, 0, -2, 1, 0, -1), scale=1, offset=0)
    )
    return [[sum(pixel) for pixel in row] for row in img_to_rgb(edges)]


def seam_carving(image, n_rows):
    for _ in range(n_rows):
        # Finn vektene med et filter
        weights = get_weights(image)

        # Finn den beste stien som kan fjernes fra bildet
        path = find_path(weights)

        # Fjern denne stien fra bildet
        image_rgb = img_to_rgb(image)
        for column, row in path:
            image_rgb[row] = (
                image_rgb[row][:column] + image_rgb[row][column + 1 :]
            )
        image = rgb_to_img(image_rgb)

    return image


if __name__ == "__main__":
    image = Image.open(image_name)
    image = seam_carving(image, row_reduction)
    image.save("seam_carved_{:}_{:}".format(row_reduction, image_name))

