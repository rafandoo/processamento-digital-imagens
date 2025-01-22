def read_ppm(filename: str) -> tuple[int, int, int, list[list[list[int]]]]:
    """
    Lê uma imagem no formato PPM e retorna o cabeçalho e os dados da imagem.
    
    Args:
        filename (str): Caminho para o arquivo de imagem.
    
    Returns:
        tuple[int, int, int, list[list[list[int]]]]: Uma tupla contendo a largura, altura, intensidade máxima e os dados da imagem.
    """
    with open(filename, 'r') as f:
        if f.readline().strip() != 'P3':
            raise ValueError("Apenas o formato P3 é suportado.")

        dimensions = f.readline().strip()
        while dimensions.startswith('#'):
            dimensions = f.readline().strip()

        width, height = map(int, dimensions.split())
        
        bits = int(f.readline().strip())

        pixels = []
        for line in f:
            pixels.extend(map(int, line.split()))

        # Converter a lista de pixels em uma matriz 3D (altura x largura x 3)
        image_data = []
        for i in range(height):
            row = []
            for j in range(width):
                idx = (i * width + j) * 3
                row.append(pixels[idx:idx + 3])
            image_data.append(row)

        return (width, height, bits, image_data)

def rle_compress(width: int, height: int, image_data: list[list[list[int]]]) -> tuple[int, int, list[int]]:
    """
    Aplica compressão RLE nos dados da imagem.
    
    Args:
        width (int): Largura da imagem.
        height (int): Altura da imagem.
        image_data (list[list[list[int]]]): Dados da imagem.
    
    Returns:
        tuple[int, int, list[int]]: Uma tupla contendo a largura, altura e os dados comprimidos da imagem.
    """
    compressed_data = []

    for row in image_data:
        for channel in zip(*row):
            i = 0
            while i < len(channel):
                # Contar valores repetidos
                run_length = 1
                while (i + run_length < len(channel) and 
                       channel[i] == channel[i + run_length] and 
                       run_length < 127):
                    run_length += 1

                if run_length > 1:
                    # Adicionar sequência comprimida
                    compressed_data.append(run_length)
                    compressed_data.append(channel[i])
                    i += run_length
                else:
                    # Encontrar valores únicos consecutivos
                    start = i
                    while (i < len(channel) and 
                           (i + 1 == len(channel) or 
                            channel[i] != channel[i + 1]) and 
                           i - start < 127):
                        i += 1

                    compressed_data.append(-(i - start))  # Número negativo para valores únicos
                    compressed_data.extend(channel[start:i])

    return (width, height, compressed_data)

def rle_decompress(width: int, height: int, compressed_data: list[list[list[int]]]) -> list[list[list[int]]]:
    """
    Descomprime dados RLE para reconstruir a imagem original.
    
    Args:
        width (int): Largura da imagem.
        height (int): Altura da imagem.
        compressed_data (list[int]): Dados comprimidos da imagem.
        
    Returns:
        list[list[list[int]]]: Dados da imagem descomprimida.
    
    """
    decompressed_data = []
    i = 0

    for _ in range(height):
        row = []
        for _ in range(3):  # Processar R, G e B separadamente
            channel = []
            while len(channel) < width:
                count = compressed_data[i]
                i += 1

                if count > 0:
                    # Repetir o próximo valor 'count' vezes
                    channel.extend([compressed_data[i]] * count)
                    i += 1
                else:
                    # Copiar os próximos '-count' valores diretamente
                    count = -count
                    channel.extend(compressed_data[i:i + count])
                    i += count

            row.append(channel)

        decompressed_data.append(list(zip(*row)))

    return decompressed_data

def write_ppm(file_path: str, width: int, height: int, max_color: int, image_data: list[list[int]]) -> None:
    """
    Escreve os dados da imagem no formato PPM.
    
    Args:
        file_path (str): Caminho para o arquivo de saída.
        width (int): Largura da imagem.
        height (int): Altura da imagem.
        max_color (int): Intensidade máxima da imagem.
        image_data (list[list[int]]): Dados da imagem.
    """
    with open(file_path, 'w') as file:
        file.write("P3\n")
        file.write(f"{width} {height}\n")
        file.write(f"{max_color}\n")

        for row in image_data:
            for pixel in row:
                file.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")
            file.write("\n")

def write_rle(file_path: str, width: int, height: int, compressed_data: list[int]) -> None:
    """
    Escreve os dados comprimidos no formato RLE.
    
    Args:
        file_path (str): Caminho para o arquivo de saída.
        width (int): Largura da imagem.
        height (int): Altura da imagem.
        compressed_data (list[int]): Dados comprimidos da imagem.
    """
    with open(file_path, 'w') as file:
        file.write(f"{width} {height}\n")
        for value in compressed_data:
            file.write(f"{value} ")
        file.write("\n")


ppm_file = "src/main/resources/bclc.ppm"

width, height, max_color, image_data = read_ppm(ppm_file)
print(f"Imagem carregada: {width}x{height}, Max Color: {max_color}")

compressed = rle_compress(width, height, image_data)
write_rle("src/main/resources/bclc.rle", compressed[0], compressed[1], compressed[2])

decompressed = rle_decompress(compressed[0], compressed[1], compressed[2])
print(f"Imagem descomprimida com sucesso. Dimensões: {len(decompressed)}x{len(decompressed[0])}")
write_ppm("src/main/resources/bclc_decompressed.ppm", width, height, max_color, decompressed)

