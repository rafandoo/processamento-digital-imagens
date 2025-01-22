from PIL import Image
import numpy as np
import os

# Função para gerar os planos de bits
def generate_bit_planes(image_array: np.ndarray) -> list[np.ndarray]:
    """
    Gera os planos de bits a partir da imagem.

    Args:
        image_array (np.ndarray): Matriz da imagem.

    Returns:
        list[np.ndarray]: Planos de bits.
    """
    bit_planes = []
    for i in range(8):
        bit_plane = (image_array >> i) & 1 
        bit_planes.append(bit_plane)
    return bit_planes

def generate_gray_planes(bit_planes: list[np.ndarray]) -> list[np.ndarray]:
    """
    Gera os planos de cinza a partir dos planos de bits.

    Args:
        bit_planes (list[np.ndarray]): planos de bits.

    Returns:
        list[np.ndarray]: planos de cinza.
    """
    gray_planes = []
    for i, bit_plane in enumerate(bit_planes):
        gray_plane = bit_plane * (2**i)  # Multiplicar pelo valor posicional
        gray_planes.append(gray_plane)
    return gray_planes

def reconstruct_image_from_msb(bit_planes: list[np.ndarray]) -> np.ndarray:
    """
    Reconstruir a imagem com os 3 bits mais significativos (MSB).

    Args:   
        bit_planes (list[np.ndarray]): Planos de bits.

    Returns:
        np.ndarray: Imagem reconstruida.
    """
    msb_planes = bit_planes[-3:]  # Planos 6, 7 e 8 (3 mais significativos)
    reconstructed_image = sum(plane * (2**(5 + i)) for i, plane in enumerate(msb_planes))
    return reconstructed_image

image_path = 'src/main/resources/Fig0314(a)(100-dollars).tif'
image = Image.open(image_path).convert('L') 
image_array = np.array(image)

bit_planes = generate_bit_planes(image_array)

gray_planes = generate_gray_planes(bit_planes)

reconstructed_image = reconstruct_image_from_msb(bit_planes)

output_dir = "src/main/resources/"
os.makedirs(output_dir, exist_ok=True)

bit_plane_paths = []
gray_plane_paths = []

for i, (bit_plane, gray_plane) in enumerate(zip(bit_planes, gray_planes)):
    bit_plane_image = Image.fromarray((bit_plane * 255).astype(np.uint8))
    gray_plane_image = Image.fromarray(gray_plane.astype(np.uint8))

    bit_plane_path = os.path.join(output_dir, f"bit_plane_{i+1}.png")
    gray_plane_path = os.path.join(output_dir, f"gray_plane_{i+1}.png")
    
    bit_plane_image.save(bit_plane_path)
    gray_plane_image.save(gray_plane_path)

    bit_plane_paths.append(bit_plane_path)
    gray_plane_paths.append(gray_plane_path)

# Salvar a imagem reconstruída
reconstructed_path = os.path.join(output_dir, "reconstructed_image_3_msb.png")
Image.fromarray(reconstructed_image.astype(np.uint8)).save(reconstructed_path)

bit_plane_paths, gray_plane_paths, reconstructed_path
