# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 20:16:05 2023
@author: graciella favoreto
"""

import os
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import nrrd
import glob

def process_images(x, vertebra, ponderacao):
    nome_arquivo_imagem = f"{x}-SAG-T" + ponderacao + "-8Bits.nii"
    nome_arquivo_mascara = f"{x}-SAG-T" + ponderacao + "-8Bits-L" + vertebra + ".seg.nrrd"

    # Diretório contendo os arquivos NIfTI e máscaras NRRD
    root_dir = "GSF_MR_corpos-vertebrais_anonimizada/segmentações"
    diretorio = os.path.join(root_dir, x)
    Patient = "GSF_MR_corpos-vertebrais_anonimizada/patients"
    Patient = os.path.join(Patient, f"Patient_{x}")

    # Verificar se a pasta de destino 'Patient' existe ou criar se necessário
    if not os.path.exists(Patient):
        os.makedirs(Patient)

    # Carregar a imagem NIfTI
    img = nib.load(os.path.join(diretorio, nome_arquivo_imagem))
    dados = {'imagem': img.get_fdata()}

    # Carregar a máscara NRRD
    mascara, _ = nrrd.read(os.path.join(diretorio, nome_arquivo_mascara))
    dados['mascara'] = mascara
    
    # Verificar se as imagens têm o formato correto (16, 704, 704), para as (14, 704, 704) foi alterado
    if dados['imagem'].shape != (16, 704, 704):
        # Redimensionar e transpor a imagem para (16, 704, 704) ou (14, 704, 704) se for determinados pacientes
        imagem_corrigida = np.zeros((16, 704, 704))
        imagem_corrigida[:, :dados['imagem'].shape[0], :dados['imagem'].shape[1]] = dados['imagem'].transpose()
        dados['imagem'] = imagem_corrigida

    if dados['mascara'].shape != (16, 704, 704):
        # Redimensionar e transpor a imagem para (16, 704, 704) ou (14, 704, 704) se for determinados pacientes
        mascara_corrigida = np.zeros((16, 704, 704))
        mascara_corrigida[:, :dados['mascara'].shape[0], :dados['mascara'].shape[1]] = dados['mascara'].transpose()
        dados['mascara'] = mascara_corrigida

    # Verificar se a imagem e a máscara foram carregadas
    if 'imagem' in dados and 'mascara' in dados:
        # Percorrer todas as imagens e máscaras
        for i in range(len(dados['imagem'])):
            # Carregar a imagem e a máscara atual
            imagem = dados['imagem'][i]
            mascara = dados['mascara'][i]

            # Inverter verticalmente a imagem e máscara e girar pois estavam de cabeça para baixo
            imagem = np.flipud(imagem)
            #imagem = np.rot90(imagem, k=1) rotacao imagem e mascara nao sao necessarias nas imagens com resolucao errada

            mascara = np.flipud(mascara)
            #mascara = np.rot90(mascara, k=1)

            if nome_arquivo_mascara.endswith('.nrrd'):
                nome_arquivo_sem_extensao = nome_arquivo_mascara.replace('.seg.nrrd', '')
            else:
                nome_arquivo_sem_extensao = nome_arquivo_imagem.replace('.nii', '')

            # Verificar se a máscara contém pelo menos 10 pixels brancos
            if np.count_nonzero(mascara) >= 10:
                mascara_contem_10_pixels_brancos = "Sim"
                nome_arquivo_imagem_salvo = f"{nome_arquivo_sem_extensao}_{i}.jpg"
                nome_arquivo_mascara_salvo = f"{nome_arquivo_sem_extensao}_Mask_{i}.jpg"

                caminho_salvar_imagem = os.path.join(Patient, nome_arquivo_imagem_salvo)
                caminho_salvar_mascara = os.path.join(Patient, nome_arquivo_mascara_salvo)

                if 'L' in nome_arquivo_sem_extensao:
                    print("salva como", nome_arquivo_sem_extensao)
                    # Salvar a imagem
                    plt.imsave(caminho_salvar_imagem, imagem, cmap='gray')

                    # Salvar a máscara
                    plt.imsave(caminho_salvar_mascara, mascara, cmap='gray')

                else:
                    print("eh uma imagem sem L", nome_arquivo_sem_extensao)

            else:
                mascara_contem_10_pixels_brancos = "Não"

            # Exibir a imagem
            plt.subplot(1, 2, 1)
            plt.imshow(imagem, cmap='gray')
            plt.title(f"{nome_arquivo_sem_extensao}_{i} - pixels brancos? {mascara_contem_10_pixels_brancos}")
            plt.axis('on')

            # Exibir a máscara
            plt.subplot(1, 2, 2)
            plt.imshow(mascara, cmap='gray')
            plt.title(f"{nome_arquivo_sem_extensao}_Mask_{i}")
            plt.axis('on')

            # Ajustar o layout
            plt.tight_layout()

            # Mostrar o plot
            plt.show()

        print("Imagem:", imagem.shape)
        print("Máscara:", mascara.shape)

# Directory to create patient folders
patient_folder_root = "GSF_MR_corpos-vertebrais_anonimizada/patients"

# Criacao de diretorios de Patient_01 ate Patient_65
for patient_num in range(1, 66):
    patient_name = f"Patient_{str(patient_num).zfill(2)}"
    patient_folder_path = os.path.join(patient_folder_root, patient_name)
    if not os.path.exists(patient_folder_path):
        os.makedirs(patient_folder_path)
        print("aqui foram criados")


# Esses exames estavam em formato estranho, foram excluidos desse ponto
excluded_values = [34, 46, 50, 55, 57, 58, 59, 63] #50 nao existe, e os demais estao faltando dimensao 
excluded_values_14 = [34, 46, 59, 63]
excluded_values_16 = [55, 57, 58]

# Loop para processar as imagens corretas
for x_value in range(1, 65):
    if x_value not in excluded_values:
        x_value_str = str(x_value).zfill(2)  # convertendo o inteiro para uma string com dois dígitos, adicionando zeros à esquerda, se necessário
        for vertebra in range(1, 6):
            for ponderacao in range(1, 3):  # Modificado para range(1, 3) para abranger 1 e 2
                process_images(x_value_str, str(vertebra), str(ponderacao))
                print("aqui executa a funcao")
                
# Loop para processar as imagens com dimensao errada
for x_value in excluded_values_16:
    x_value_str = str(x_value).zfill(2)  # convertendo o inteiro para uma string com dois dígitos, adicionando zeros à esquerda, se necessário
    for vertebra in range(1, 6):
        for ponderacao in range(1, 3):  # Modificado para range(1, 3) para abranger 1 e 2
            process_images(x_value_str, str(vertebra), str(ponderacao))
            print("aqui executa a funcao que salva os que faltavam dimensao")
                
from PIL import Image

def get_image_resolution(image_path, target_resolution):
    with Image.open(image_path) as img:
        # Redimensiona a immagem
        if img.size == (640, 640) and target_resolution == (704, 704):
            img = img.resize(target_resolution, Image.ANTIALIAS)
            img.save(image_path)

        return img.size
    
def count_images_and_resolutions(root_dir):
    target_resolution = (704, 704)  # Define uma resolucao fixa para todas as imagens
    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder)
        if os.path.isdir(folder_path):
            image_files_T1 = [f for f in os.listdir(folder_path) if f.endswith('.jpg') and 'T1' in f]
            image_files_T2 = [f for f in os.listdir(folder_path) if f.endswith('.jpg') and 'T2' in f]
            image_resolutions = set()
            
            for image_file in image_files_T1 + image_files_T2:
                image_path = os.path.join(folder_path, image_file)
                resolution = get_image_resolution(image_path, target_resolution)  # passando a resolucao fixa aqui
                image_resolutions.add(resolution)

            num_images_T1 = len(image_files_T1)
            num_images_T2 = len(image_files_T2)
            num_unique_resolutions = len(image_resolutions)

            resolutions_str = ', '.join(f"{res[0]}x{res[1]}" for res in image_resolutions)

            print(f"{folder} possui {num_images_T1} imagens T1 e {num_images_T2} imagens T2 com resolução {resolutions_str}, sendo {num_unique_resolutions} resoluções únicas.")

if __name__ == "__main__":
    root_directory = "GSF_MR_corpos-vertebrais_anonimizada/patients"
    count_images_and_resolutions(root_directory)
    
