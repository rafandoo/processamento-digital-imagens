import random

def generate_pbm(width: int, height: int) -> None:
    """
    Gera uma imagem no formato PBM conforme os parâmetros passados.
    
    Args:
        width (int): largura.
        height (int): altura.
    """
    
    # Cabeçalho do formato PBM
    header = f"P1\n{width} {height}\n"

    # Gera a imagem com valores aleatórios de 0 e 1
    data = ""
    for y in range(height):
        row = ""
        for x in range(width):
            row += str(random.randint(0, 1)) + " "
        data += row.strip() + "\n"

    with open("image-pbm.pbm", "w") as f:
        f.write(header + data)

generate_pbm(100, 100)
