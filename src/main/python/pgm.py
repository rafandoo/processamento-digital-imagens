import random

def generate_pgm(width, height):
    """Gera uma imagem no formato PGM conforme os parâmetros passados.
    
    Args:
        width (int): largura.
        height (int): altura.
    """
    
    # Cabeçalho do formato PGM
    header = f"P2\n{width} {height}\n15\n"

    # Gera a imagem com valores aleatórios de 0 a 15
    data = ""
    for y in range(height):
        row = ""
        for x in range(width):
            row += str(random.randint(0, 15)) + " "
        data += row.strip() + "\n"

    with open("image-pgm.pgm", "w") as f:
        f.write(header + data)

generate_pgm(100, 100)
