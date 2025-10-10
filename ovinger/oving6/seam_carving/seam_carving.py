from PIL import Image, ImageFilter
import numpy as np
from numba import njit
from pathlib import Path

current_dir = Path(__file__).parent
image_name = "tower.jpg"
row_reduction = 200


def find_path_old(weights):
    # assembling pieces
    n = len(weights)
    if n == 0:
        return []
    m = len(weights[0])
    if m == 0:
        return []
    elif n == 1:
        return [(weights[0].index(min(weights[0])), 0)]
    elif m == 1:
        path = []
        for i in range(n):
            path.append((0, i))
        return path

    memo = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(m):
        memo[0][i] = weights[0][i]

    # finding cumulative path length for each position
    for i in range(1, n):
        for j in range(m):
            path = memo[i - 1][j]
            if j != 0:
                path = min(path, memo[i - 1][j - 1])
            if j != m - 1:
                path = min(path, memo[i - 1][j + 1])
            memo[i][j] = weights[i][j] + path

    # building the path (O(n))
    path = []
    j = memo[n - 1].index(min(memo[n - 1]))
    path.append((j, n - 1))
    for i in range(n - 2, -1, -1):
        candidates = [(j, memo[i][j])]
        if j > 0:
            candidates.append((j - 1, memo[i][j - 1]))
        if j < m - 1:
            candidates.append((j + 1, memo[i][j + 1]))
        j = min(candidates, key=lambda x: x[1])[0]
        path.append((j, i))
    path.reverse()
    return path


@njit
def find_path_njit(weights):
    n = weights.shape[0]
    m = weights.shape[1]

    if n == 0 or m == 0:
        return np.empty((0, 2), dtype=np.int64)

    if n == 1:
        min_idx = np.argmin(weights[0])
        return np.array([[min_idx, 0]], dtype=np.int64)

    if m == 1:
        path = np.empty((n, 2), dtype=np.int64)
        for i in range(n):
            path[i, 0] = 0
            path[i, 1] = i
        return path

    # Create memo table
    memo = np.zeros((n, m), dtype=weights.dtype)
    memo[0, :] = weights[0, :]

    # Finding cumulative path length for each position
    for i in range(1, n):
        for j in range(m):
            path_cost = memo[i - 1, j]
            if j > 0:
                path_cost = min(path_cost, memo[i - 1, j - 1])
            if j < m - 1:
                path_cost = min(path_cost, memo[i - 1, j + 1])
            memo[i, j] = weights[i, j] + path_cost

    # Building the path
    path = np.empty((n, 2), dtype=np.int64)
    j = np.argmin(memo[n - 1])
    path[n - 1, 0] = j
    path[n - 1, 1] = n - 1

    for i in range(n - 2, -1, -1):
        min_val = memo[i, j]
        next_j = j

        if j > 0 and memo[i, j - 1] < min_val:
            min_val = memo[i, j - 1]
            next_j = j - 1
        if j < m - 1 and memo[i, j + 1] < min_val:
            next_j = j + 1

        j = next_j
        path[i, 0] = j
        path[i, 1] = i

    return path


def find_path(weights):
    """Wrapper function that calls njit version and converts output to list of tuples"""
    # Convert to numpy array if needed (for backward compatibility)
    if not isinstance(weights, np.ndarray):
        weights = np.array(weights)
    path_array = find_path_njit(weights)
    # Convert back to list of tuples for compatibility
    return [(int(row[0]), int(row[1])) for row in path_array]


def img_to_rgb(img):
    return [[img.getpixel((j, i)) for j in range(img.width)] for i in range(img.height)]


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
    rgb_data = img_to_rgb(edges)
    # Return as numpy array for better performance with njit
    return np.array([[sum(pixel) for pixel in row] for row in rgb_data])


def seam_carving(image, n_rows):
    for i in range(n_rows):
        print(f"Removing row {i} of {n_rows}")
        # Finn vektene med et filter
        weights = get_weights(image)

        # Finn den beste stien som kan fjernes fra bildet
        path = find_path(weights)

        # Fjern denne stien fra bildet
        image_rgb = img_to_rgb(image)
        for column, row in path:
            image_rgb[row] = image_rgb[row][:column] + image_rgb[row][column + 1 :]
        image = rgb_to_img(image_rgb)

    return image


if __name__ == "__main__":
    image = Image.open(current_dir / image_name)
    image = seam_carving(image, row_reduction)
    image.save(current_dir / f"seam_carved_{row_reduction}_{image_name}")
