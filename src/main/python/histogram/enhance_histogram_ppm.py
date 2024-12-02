import csv
import matplotlib.pyplot as plt
from collections import Counter


def read_image(filename: str) -> tuple[int, int, int, list[tuple[int, int, int]]]:
    """
    Lê uma imagem PPM e retorna sua largura, altura, valor máximo e dados dos canais (R, G, B).

    Args:
        filename (str): nome do arquivo PPM.

    Returns:
        tuple[int, int, int, list[tuple[int, int, int]]]: largura, altura, valor máximo, dados RGB.
    """
    with open(filename, 'r') as f:
        if f.readline().strip() != 'P3':
            raise ValueError("Este não é um arquivo PPM ASCII (P3).")

        dimensions = f.readline().strip()
        while dimensions.startswith("#"):
            dimensions = f.readline().strip()
        width, height = map(int, dimensions.split())

        bits = int(f.readline().strip())
        data = []
        for line in f:
            data.extend(map(int, line.split()))

        pixels = [(data[i], data[i + 1], data[i + 2])
                  for i in range(0, len(data), 3)]
        return width, height, bits, pixels


def save_image(width: int, height: int, bits: int, pixels: list[tuple[int, int, int]]) -> None:
    """
    Salva uma imagem PPM.

    Args:
        width (int): largura.
        height (int): altura.
        bits (int): valor máximo (intensidade).
        pixels (list[tuple[int, int, int]]): dados da imagem.
    """
    with open(f"image_{width}x{height}_{bits}_enhanced.ppm", 'w') as f:
        f.write(f"P3\n{width} {height}\n{bits}\n")
        for r, g, b in pixels:
            f.write(f"{r} {g} {b}\n")


def enhance_histogram_ppm(filename: str):
    """
    Realça o histograma de uma imagem PPM usando a transformação Y = aX + b para cada canal.

    Args:
        filename (str): Arquivo de entrada PPM.
    """
    width, height, bits, pixels = read_image(filename)

    r_values = [pixel[0] for pixel in pixels]
    g_values = [pixel[1] for pixel in pixels]
    b_values = [pixel[2] for pixel in pixels]

    Rmin, Rmax = min(r_values), max(r_values)
    Gmin, Gmax = min(g_values), max(g_values)
    Bmin, Bmax = min(b_values), max(b_values)

    # Calcula os parâmetros para cada canal
    a_r = 255.0 / (Rmax - Rmin)
    b_r = -a_r * Rmin

    a_g = 255.0 / (Gmax - Gmin)
    b_g = -a_g * Gmin

    a_b = 255.0 / (Bmax - Bmin)
    b_b = -a_b * Bmin

    # Aplica a transformação para cada canal
    enhanced_pixels = [
        (
            int(a_r * r + b_r),
            int(a_g * g + b_g),
            int(a_b * b + b_b)
        ) for r, g, b in pixels
    ]

    save_image(width, height, bits, enhanced_pixels)

    r_counter = Counter(pixel[0] for pixel in enhanced_pixels)
    g_counter = Counter(pixel[1] for pixel in enhanced_pixels)
    b_counter = Counter(pixel[2] for pixel in enhanced_pixels)

    with open('histogram_ppm_enhanced.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["intensidade", "R", "G", "B"])
        for intensity in range(bits + 1):
            writer.writerow([
                intensity,
                r_counter.get(intensity, 0),
                g_counter.get(intensity, 0),
                b_counter.get(intensity, 0)
            ])


def plot_histogram_rgb() -> None:
    """
    Plota o histograma de uma imagem RGB (PPM).
    """

    r_counter = {}
    g_counter = {}
    b_counter = {}

    with open('histogram_ppm_enhanced.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            intensidade = int(row[0])
            r_counter[intensidade] = int(row[1])
            g_counter[intensidade] = int(row[2])
            b_counter[intensidade] = int(row[3])

    # Gera gráficos para cada canal
    for channel, counter, color, label in zip(
        ['R', 'G', 'B'], [r_counter, g_counter, b_counter], [
            'red', 'green', 'blue'], ['Vermelho', 'Verde', 'Azul']
    ):
        plt.figure()
        plt.bar(counter.keys(), counter.values(), color=color)
        plt.title(f"Histograma - Canal {label}")
        plt.xlabel('Intensidade')
        plt.ylabel('Frequência')
        plt.savefig(f"histogram_{channel}.png")
        plt.show()


# Exemplo de uso
enhance_histogram_ppm('src/main/resources/EntradaRGB.ppm')
plot_histogram_rgb()
