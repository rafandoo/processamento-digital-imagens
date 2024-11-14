
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

def convert_to_5_bits(pixels: list[int]) -> list[int]:
    """
    Fator de conversão de 8 bits (0-255) para 5 bits (0-31)

    Args:
        pixels (list[int]): pixels de entrada em 8 bits.

    Returns:
        list[int]: pixels em 5 bits.
    """
    return [(p * 31) // 255 for p in pixels]

def save_image(width: int, height: int, bits: int, data: list[int]) -> None:
    """
    Salva uma imagem PGM.
    
    Args:
        width (int): largura.
        height (int): altura.
        bits (int): valor máximo (intensidade).
        data (list[int]): dados da imagem.
    """
    
    with open(f"image_{width}x{height}_{bits}.pgm", 'w') as f:
        f.write(f"P2\n{width} {height}\n{bits}\n")
        for i in range(height):
            f.write(" ".join(map(str, data[i * width:(i + 1) * width])) + "\n")

width, height, bits, pixels = read_image("src/main/resources/Entrada_EscalaCinza.pgm")
    
if bits == 255:
    converted_pixels = convert_to_5_bits(pixels)
    save_image(width, height, 31, converted_pixels)
