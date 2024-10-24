
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

def resize_image(data: list[int], original_width: int, original_height: int, new_width: int, new_height: int) -> list[int]:
    """ 
    Redimensiona uma imagem PGM.
    
    Args:
        data (list[int]): dados da imagem.
        original_width (int): largura da imagem original.
        original_height (int): altura da imagem original.
        new_width (int): largura da imagem redimensionada.
        new_height (int): altura da imagem redimensionada.
    
    Returns:
        list[int]: dados da imagem redimensionada.
    """
    
    resized_image = []
    
    # Calcular a taxa de escala
    x_scale = original_width / new_width
    y_scale = original_height / new_height
    
    for y in range(new_height):
        for x in range(new_width):
            # Encontrar o pixel mais próximo na imagem original
            src_x = int(x * x_scale)
            src_y = int(y * y_scale)
            resized_image.append(data[src_y * original_width + src_x])
    
    return resized_image

# Ler a imagem original
original_width, original_height, bits, data = read_image("src/main/resources/Entrada_EscalaCinza.pgm")

# a) 10x menor que a original
new_width = original_width // 10
new_height = original_height // 10
resized_image = resize_image(data, original_width, original_height, new_width, new_height)
save_image(new_width, new_height, bits, resized_image)

# b) Padrão 480x320
resized_image = resize_image(data, original_width, original_height, 480, 320)
save_image(480, 320, bits, resized_image)

# c) Padrão 720p (1280x720)
resized_image = resize_image(data, original_width, original_height, 1280, 720)
save_image(1280, 720, bits, resized_image)

# d) Padrão 1080p Full HD (1920x1080)
resized_image = resize_image(data, original_width, original_height, 1920, 1080)
save_image(1920, 1080, bits, resized_image)

# e) Padrão 4k (3840x2160)
resized_image = resize_image(data, original_width, original_height, 3840, 2160)
save_image(3840, 2160, bits, resized_image)

# Padrão 8k (7680x4320)
resized_image = resize_image(data, original_width, original_height, 7680, 4320)
save_image(7680, 4320, bits, resized_image)
