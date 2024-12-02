import csv
import matplotlib.pyplot as plt
from collections import Counter

def read_image(filename: str) -> tuple[int, int, int, list[int]]:
    """
    Lê uma imagem PGM e retorna sua largura, altura, valor máximo (intensidade) e os dados da imagem.
    
    Args:
        filename (str): nome do arquivo.
    
    Returns:
        tuple[int, int, int, list[int]]: (largura, altura, valor máximo, dados da imagem).
    """
    
    with open(filename, 'r') as f:
        # Lê o cabeçalho
        if f.readline().strip() != 'P2':
            raise ValueError("Este não é um arquivo PGM ASCII (P2).")

        # Lê as dimensões
        dimensions = f.readline().strip()
        while dimensions.startswith("#"):
            dimensions = f.readline().strip()        
        width, height = map(int, dimensions.split())
        
        # Lê o valor máximo de intensidade
        bits = int(f.readline().strip())
        
        # Lê os dados da imagem
        pixels = []
        for line in f:
            pixels.extend(map(int, line.split()))
        
        # Retorna a largura, altura, valor máximo e os dados da imagem
        return width, height, bits, pixels

def save_image(width: int, height: int, bits: int, pixels: list[int]) -> None:
    """
    Salva uma imagem PGM.
    
    Args:
        width (int): largura.
        height (int): altura.
        bits (int): valor máximo (intensidade).
        pixels (list[int]): dados da imagem.
    """
    with open(f"image_{width}x{height}_{bits}_enhanced.pgm", 'w') as f:
        f.write(f"P2\n{width} {height}\n{bits}\n")
        for i in range(height):
            f.write(" ".join(map(str, pixels[i * width:(i + 1) * width])) + "\n")


def enhance_histogram_pgm(filename: str):
    """
    Realça o histograma de uma imagem PGM usando a transformação Y = aX + b.
    
    Args:
        filename (str): Arquivo de entrada PGM.
    """
    width, height, bits, pixels = read_image(filename)
    
    Xmin = min(pixels)
    Xmax = max(pixels)
    
    # Calcula os parâmetros da transformação
    a = 255.0 / (Xmax - Xmin)
    b = -a * Xmin
    
    # Aplica a transformação para gerar a nova imagem
    enhanced_pixels = [int(a * x + b) for x in pixels]
    
    save_image(width, height, 255, enhanced_pixels)
    
    counter = Counter(enhanced_pixels)
    with open('histogram_pgm_enhanced.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["intensidade", "frequencia"])
        for intensity in range(256):
            writer.writerow([intensity, counter.get(intensity, 0)])

def plot_histogram_grayscale() -> None:
    """
    Plota o histograma da imagem PGM.
    """
    
    counter = {}
    with open('histogram_pgm_enhanced.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        counter = {int(row[0]): int(row[1]) for row in reader}

    plt.bar(counter.keys(), counter.values(), color='blue')
    plt.title('Histograma da Imagem PGM')
    plt.xlabel('Intensidade')
    plt.ylabel('Frequência')
    plt.savefig('histogram_pgm.png')
    plt.show()


enhance_histogram_pgm('src/main/resources/EntradaEscalaCinza.pgm')
plot_histogram_grayscale()