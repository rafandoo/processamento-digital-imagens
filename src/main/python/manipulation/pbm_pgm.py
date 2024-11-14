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

def apply_threshold(pixels: list[int], threshold: int) -> list[int]:
    """
    Aplica limiar binário para gerar imagem em preto e branco.
    
    Args:
        pixels (list[int]): lista de pixels.
        threshold (int): valor do limiar.
    
    Returns:
        list[int]: lista de pixels binarizada (0 ou 1).
    """
    return [1 if p > threshold else 0 for p in pixels]

def save_pbm(width: int, height: int, data: list[int]) -> None:
    """
    Salva uma imagem PBM (P1 ASCII).
    
    Args:
        width (int): largura.
        height (int): altura.
        data (list[int]): dados da imagem binarizada.
    """
    with open(f'image_{width}x{height}_pbm.pbm', 'w') as f:
        f.write(f"P1\n{width} {height}\n")
        for i in range(height):
            f.write(" ".join(map(str, data[i * width:(i + 1) * width])) + "\n")

def invert_binary_image(pixels: list[int]) -> list[int]:
    """
    Inverte uma imagem binária (0 -> 1, 1 -> 0) para gerar o negativo.
    
    Args:
        pixels (list[int]): lista de pixels binários (0 ou 1).
    
    Returns:
        list[int]: lista de pixels invertidos.
    """
    return [1 - p for p in pixels]

def save_pgm(width: int, height: int, bits: int, data: list[int]) -> None:
    """
    Salva uma imagem PGM.
    
    Args:
        width (int): largura.
        height (int): altura.
        bits (int): valor máximo de intensidade (deve ser 1 para imagem binária invertida).
        data (list[int]): dados da imagem invertida.
    """
    with open(f'image_{width}x{height}_pgm_{bits}.pgm', 'w') as f:
        f.write(f"P2\n{width} {height}\n{bits}\n")
        for i in range(height):
            f.write(" ".join(map(str, data[i * width:(i + 1) * width])) + "\n")

# Lê a imagem original
width, height, bits, pixels = read_image("src/main/resources/Entrada_EscalaCinza.pgm")

# Aplica limiar (threshold) para converter em PBM
threshold = 128  # Define o valor do limiar
binary_pixels = apply_threshold(pixels, threshold)
save_pbm(width, height, binary_pixels)

# Aplica o negativo da imagem binária e salva no formato P2
negative_pixels = invert_binary_image(binary_pixels)
save_pgm(width, height, 1, negative_pixels)
