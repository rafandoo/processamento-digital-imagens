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

def generate_histogram_grayscale(filename: str) -> None:
    """
    Gera um histograma da imagem PGM.

    Args:
        filename (str): nome do arquivo.
    """
    
    width, height, bits, pixels = read_image(filename)
    
    counter = Counter(pixels)
    
    with open('histogram_pgm.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['intensidade', 'frequencia'])
        for intensity in range(bits + 1):
            writer.writerow([intensity, counter.get(intensity, 0)])
            
def plot_histogram_grayscale() -> None:
    """
    Plota o histograma da imagem PGM.
    """
    
    counter = {}
    with open('histogram_pgm.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        counter = {int(row[0]): int(row[1]) for row in reader}

    plt.bar(counter.keys(), counter.values(), color='blue')
    plt.title('Histograma da Imagem PGM')
    plt.xlabel('Intensidade')
    plt.ylabel('Frequência')
    plt.savefig('histogram_pgm.png')
    plt.show()


generate_histogram_grayscale('src/main/resources/EntradaEscalaCinza.pgm')
plot_histogram_grayscale()
