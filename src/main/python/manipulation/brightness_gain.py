
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
        data = []
        for line in f:
            data.extend(map(int, line.split()))
        
        # Retorna a largura, altura, valor máximo e os dados da imagem
        return width, height, bits, data

def apply_brightness_gain(pixels: list[int], gain: float, max_value: int) -> list[int]:
    """
    Aplica um ganho de brilho aos pixels.
    
    Args:
        pixels (list[int]): lista de pixels.
        gain (float): fator de ganho de brilho.
        max_value (int): valor máximo de intensidade.
    
    Returns:
        list[int]: lista de pixels com o ganho de brilho aplicado.
    """
    return [min(int(p * gain), max_value) for p in pixels]


def save_image(width: int, height: int, bits: int, data: list[int]) -> None:
    """
    Salva uma imagem PGM.
    
    Args:
        width (int): largura.
        height (int): altura.
        bits (int): valor máximo (intensidade).
        data (list[int]): dados da imagem.
    """
    with open(f"image_{width}x{height}_{bits}_brightness_gain.pgm", 'w') as f:
        f.write(f"P2\n{width} {height}\n{bits}\n")
        for i in range(height):
            f.write(" ".join(map(str, data[i * width:(i + 1) * width])) + "\n")

# Lê a imagem original
width, height, bits, pixels = read_image("src/main/resources/image_800x800_31.pgm")

# Aplica ganho de brilho de 20%
bright_pixels = apply_brightness_gain(pixels, gain=1.2, max_value=bits)

# Salva a imagem processada
save_image(width, height, bits, bright_pixels)
