from PIL import Image
import numpy as np
import math

class SeamCarver:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.width, self.height = self.image.size
        self.pixels = np.array(self.image)

    def calculate_energy_map(self):
        # Pad the image to handle edges
        padded_pixels = np.pad(self.pixels, ((1, 1), (1, 1), (0, 0)), mode='edge')
        
        # Calculate gradients
        grad_x = np.sum((padded_pixels[1:-1, 2:, :] - padded_pixels[1:-1, :-2, :]) ** 2, axis=2)
        grad_y = np.sum((padded_pixels[2:, 1:-1, :] - padded_pixels[:-2, 1:-1, :]) ** 2, axis=2)
        
        # Combine gradients into energy
        return np.sqrt(grad_x + grad_y)

    def find_vertical_seam(self):
        energy_map = self.calculate_energy_map()
        rows, cols = energy_map.shape
        dp = energy_map.copy()
        backtrack = np.zeros_like(dp, dtype=int)

        for row in range(1, rows):
            for col in range(cols):
                left = dp[row - 1, col - 1] if col > 0 else float('inf')
                up = dp[row - 1, col]
                right = dp[row - 1, col + 1] if col < cols - 1 else float('inf')

                min_energy = min(left, up, right)
                backtrack[row, col] = col + np.argmin([left, up, right]) - 1
                dp[row, col] += min_energy

        seam = []
        col = np.argmin(dp[-1])
        for row in range(rows - 1, -1, -1):
            seam.append(col)
            col = backtrack[row, col]

        return seam[::-1]

    def find_horizontal_seam(self):
        self.transpose_image()
        seam = self.find_vertical_seam()
        self.transpose_image()
        return seam

    def remove_vertical_seam(self, seam):
        mask = np.ones((self.height, self.width), dtype=bool)
        for row, col in enumerate(seam):
            mask[row, col] = False

        self.pixels = self.pixels[mask].reshape((self.height, self.width - 1, 3))
        self.width -= 1

    def remove_horizontal_seam(self, seam):
        self.transpose_image()
        self.remove_vertical_seam(seam)
        self.transpose_image()

    def transpose_image(self):
        self.pixels = np.transpose(self.pixels, (1, 0, 2))
        self.width, self.height = self.height, self.width

    def save_image(self, output_path):
        output_image = Image.fromarray(self.pixels)
        output_image.save(output_path)

    def resize_image(self, scale_factor):
        new_width = int(self.width * scale_factor)
        new_height = int(self.height * scale_factor)
        self.image = self.image.resize((new_width, new_height), Image.ANTIALIAS)
        self.pixels = np.array(self.image)
        self.width, self.height = self.image.size

