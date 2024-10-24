import random

def generate_ppm(width: int, height: int, bits: int) -> None:
    """
    Gera uma imagem no formato PPM conforme os parâmetros passados.
    
    Args:
        width (int): largura.
        height (int): altura.
        bits (int): intensidade.
    """
    
    # Cabeçalho do formato PPM
    header = f"P3\n{width} {height}\n{bits - 1}\n"

    # Gera a imagem com valores aleatórios entre 0 e {bits - 1} para R, G e B
    data = ""
    for y in range(height):
        row = ""
        for x in range(width):
            r = random.randint(0, (bits - 1))
            g = random.randint(0, (bits - 1))
            b = random.randint(0, (bits - 1))
            row += f"{r} {g} {b} "
        data += row.strip() + "\n"

    with open(f"image_{bits}.ppm", "w") as f:
        f.write(header + data)

generate_ppm(100, 100, 16)

generate_ppm(1000, 1000, 256)
