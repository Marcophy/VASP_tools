# Read information from VASP files
# @Author: Marco A. Villena (marcoantonio.villena@kaust.edu.sa)
# @Date: 16/03/2023

__author__ = 'Marco A. Villena'
__email__ = 'marcoantonio.villena@kaust.edu.sa'
__version__ = '1.2'

# ----- Modules -----
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import vasp_functions as vf
import general_funcitions as gf

# ------ Input variables -----
manual = False  # Enable/disable the manual mode of folder selection.
plot_flag = False  # Enable/disable the plots
marker_size = 150  # Size of the marker of all plots
vector_length = 50  # Length of the vectors in the vectorial plots

if manual:
    print('MANUAL MODE')
    files_path_ini = os.path.join(os.getcwd(), 'examples', 'ini_state')
    files_path_end = os.path.join(os.getcwd(), 'examples', 'end_state')
else:
    print('AUTOMATIC MODE')
    key_string = 'state'
    folder_list = gf.find_folders_with_string(os.path.join(os.getcwd(), 'examples'),  key_string)
    if len(folder_list) == 2:
        files_path_ini = os.path.join(os.getcwd(), 'examples', folder_list[0])
        files_path_end = os.path.join(os.getcwd(), 'examples', folder_list[1])

        print('Initial step folder: ', files_path_ini)
        print('Final step folder: ', files_path_end, '\n')
    elif len(folder_list) == 0:
        print('ERROR: Folders not found!')
        exit()
    else:
        print('WATNING: I could not find only two valid folder. Please, check the data folders')
        exit()

# ---------- MAIN ----------
total_atoms = vf.total_atoms(files_path_ini)
if total_atoms == 0:
    raise ValueError('ERROR: No atoms detected in the POSCAR file.')


force_ini = np.array(vf.postions_forces(files_path_ini, total_atoms, 1))
force_end = np.array(vf.postions_forces(files_path_end, total_atoms, 1))
force_dif = np.sqrt(((force_end[:, 0] - force_ini[:, 0]) ** 2) + ((force_end[:, 1] - force_ini[:, 1]) ** 2) + ((force_end[:, 2] - force_ini[:, 2]) ** 2))

toten_ini = vf.find_string_in_file(os.path.join(files_path_ini, 'OUTCAR'), 'free  energy   TOTEN')
en_ini = float(toten_ini[-1].split()[4])
toten_end = vf.find_string_in_file(os.path.join(files_path_ini, 'OUTCAR'), 'free  energy   TOTEN')
en_end = float(toten_end[-1].split()[4])


print('Total number of atoms = ', total_atoms)
print(vf.find_string_in_file(os.path.join(files_path_ini, 'OUTCAR'), 'EDIFF =')[0])
print(vf.find_string_in_file(os.path.join(files_path_ini, 'OUTCAR'), 'EDIFFG =')[0])

print('\n\t\t\t\t\t\t\t[------------------------ Maximum -------------------------]')
print('Name\t\tTOTEN (eV)\t\t|Fx|\t\t|Fy|\t\t|Fz|\t\tDisplacement [2nd - 1st]')
print(89 * '-')
print('Step 1\t\t%1.2f\t\t%1.3f\t\t%1.3f\t\t%1.3f' % (en_ini, np.max(np.absolute(force_ini[:, 3])), np.max(np.absolute(force_ini[:, 4])), np.max(np.absolute(force_ini[:, 5]))))
print('Step 2\t\t%1.2f\t\t%1.3f\t\t%1.3f\t\t%1.3f\t\t%1.3f' % (en_end, np.max(np.absolute(force_end[:, 3])), np.max(np.absolute(force_end[:, 4])), np.max(np.absolute(force_end[:, 5])), np.max(force_dif)))

# ------ Plots ------
if plot_flag:
    # **** FIGURE forces of both, the initial and final state
    # Create the figure and the 3D axes
    fig, axs = plt.subplots(2, 3, figsize=(25, 10), num='Forces comparison', subplot_kw={'projection': '3d'})

    # Draw the scatter with the given colors and add a color bar for each plot
    scatter1 = axs[0, 0].scatter(force_ini[:, 0], force_ini[:, 1], force_ini[:, 2], c=force_ini[:, 3], s=marker_size)
    cbar1 = fig.colorbar(scatter1, ax=axs[0, 0], orientation='vertical', shrink=0.65)
    title_label = 'X-Forces = [' + str(round(np.min(force_ini[:, 3]), 4)) + ', ' + str(round(np.max(force_ini[:, 3]), 4)) + '] (eV/Angst)'
    cbar1.set_label(title_label, fontsize=10)

    scatter2 = axs[0, 1].scatter(force_ini[:, 0], force_ini[:, 1], force_ini[:, 2], c=force_ini[:, 4], s=marker_size)
    cbar2 = fig.colorbar(scatter2, ax=axs[0, 1], orientation='vertical', shrink=0.65)
    title_label = 'Y-Forces = [' + str(round(np.min(force_ini[:, 4]), 4)) + ', ' + str(round(np.max(force_ini[:, 4]), 4)) + '] (eV/Angst)'
    cbar2.set_label(title_label, fontsize=10)

    scatter3 = axs[0, 2].scatter(force_ini[:, 0], force_ini[:, 1], force_ini[:, 2], c=force_ini[:, 5], s=marker_size)
    cbar3 = fig.colorbar(scatter3, ax=axs[0, 2], orientation='vertical', shrink=0.65)
    title_label = 'Z-Forces = [' + str(round(np.min(force_ini[:, 5]), 4)) + ', ' + str(round(np.max(force_ini[:, 5]), 4)) + '] (eV/Angst)'
    cbar3.set_label(title_label, fontsize=10)

    # ----
    scatter5 = axs[1, 0].scatter(force_end[:, 0], force_end[:, 1], force_end[:, 2], c=force_end[:, 3], s=marker_size)
    cbar5 = fig.colorbar(scatter5, ax=axs[1, 0], orientation='vertical', shrink=0.65)
    title_label = 'X-Forces = [' + str(round(np.min(force_end[:, 3]), 4)) + ', ' + str(round(np.max(force_end[:, 3]), 4)) + '] (eV/Angst)'
    cbar5.set_label(title_label, fontsize=10)

    scatter6 = axs[1, 1].scatter(force_end[:, 0], force_end[:, 1], force_end[:, 2], c=force_end[:, 4], s=marker_size)
    cbar6 = fig.colorbar(scatter6, ax=axs[1, 1], orientation='vertical', shrink=0.65)
    title_label = 'Y-Forces = [' + str(round(np.min(force_end[:, 4]), 4)) + ', ' + str(round(np.max(force_end[:, 4]), 4)) + '] (eV/Angst)'
    cbar6.set_label(title_label, fontsize=10)

    scatter7 = axs[1, 2].scatter(force_end[:, 0], force_end[:, 1], force_end[:, 2], c=force_end[:, 5], s=marker_size)
    cbar7 = fig.colorbar(scatter7, ax=axs[1, 2], orientation='vertical', shrink=0.65)
    title_label = 'Z-Forces = [' + str(round(np.min(force_end[:, 5]), 4)) + ', ' + str(round(np.max(force_end[:, 5]), 4)) + '] (eV/Angst)'
    cbar7.set_label(title_label, fontsize=10)

    # Label the axes of each plot
    for i in range(2):
        for j in range(3):
            axs[i, j].set_xlabel('a-axis')
            axs[i, j].set_ylabel('b-axis')
            axs[i, j].set_zlabel('c-axis')

    axs[0, 0].text(0.5, 1.1, 1, 'Initial state', horizontalalignment='center', transform=axs[0, 0].transAxes)
    axs[1, 0].text(0.5, 1.1, 1, 'Final state', horizontalalignment='center', transform=axs[1, 0].transAxes)

    # **** FIGURE vectorial forces
    # Create the figure and the 3D axes
    fig2, axs = plt.subplots(1, 2, figsize=(25, 10), num='Vectorial forces', subplot_kw={'projection': '3d'})

    # Draw the scatter with the given colors and add a color bar for each plot
    color_first = np.linalg.norm(force_ini[:, 3:], axis=1)
    title_label = 'Forces = [' + str(round(np.min(color_first), 3)) + ', ' + str(round(np.max(color_first), 3)) + '] (eV/Angst)'
    color_first = color_first / np.max(color_first)
    axs[0].scatter(force_ini[:, 0], force_ini[:, 1], force_ini[:, 2], c='black', s=15)
    vector1 = axs[0].quiver(force_ini[:, 0], force_ini[:, 1], force_ini[:, 2], force_ini[:, 3], force_ini[:, 4], force_ini[:, 5], color=plt.cm.jet(color_first), length=vector_length, arrow_length_ratio=0.2, cmap='jet')
    cbar1 = fig2.colorbar(vector1, ax=axs[0], orientation='horizontal', shrink=0.65)
    cbar1.set_label(title_label, fontsize=10)

    color_last = np.linalg.norm(force_end[:, 3:], axis=1)
    title_label = 'Forces = [' + str(round(np.min(color_last), 3)) + ', ' + str(round(np.max(color_last), 3)) + '] (eV/Angst)'
    color_last = color_last / np.max(color_last)
    axs[1].scatter(force_end[:, 0], force_end[:, 1], force_end[:, 2], c='black', s=15)
    vector2 = axs[1].quiver(force_end[:, 0], force_end[:, 1], force_end[:, 2], force_end[:, 3], force_end[:, 4], force_end[:, 5], color=plt.cm.jet(color_last), length=vector_length, arrow_length_ratio=0.2, cmap='jet')
    cbar2 = fig2.colorbar(vector2, ax=axs[1], orientation='horizontal', shrink=0.65)
    cbar2.set_label(title_label, fontsize=10)

    # Label the axes of each plot
    for j in range(2):
        axs[j].set_xlabel('a-axis')
        axs[j].set_ylabel('b-axis')
        axs[j].set_zlabel('c-axis')

    axs[0].set_title('Initial state')
    axs[1].set_title('Final state')

    # **** FIGURE displacement
    fig3 = plt.figure('Displacement', figsize=(12, 12))
    ax = fig3.add_subplot(111, projection='3d')

    # Draw the scatter with the given colors and add a color bar
    scatter = ax.scatter(force_ini[:, 0], force_ini[:, 1], force_ini[:, 2], c=force_dif, s=marker_size)
    cbar = fig3.colorbar(scatter, ax=ax, orientation='vertical', shrink=0.5)
    title_label = 'Max. Displacement = ' + str(round(np.max(force_dif), 4)) + ' (Angst)'
    cbar.set_label(title_label, fontsize=10)
    ax.set_xlabel('a-axis')
    ax.set_ylabel('b-axis')
    ax.set_zlabel('c-axis')

    plt.tight_layout()

    # **** FIGURE Energy
    fig4 = plt.figure('Energy evolution', figsize=(12, 12))
    aux_ini = [float(item.split()[4]) for item in toten_ini]  # Split each extracted line and save the energy value (item 4) as float
    aux_x = list(range(1, len(aux_ini) + 1))
    plt.plot(aux_x, aux_ini, '.-', label='Initial')

    aux_end = [float(item.split()[4]) for item in toten_end]  # Split each extracted line and save the energy value (item 4) as float
    aux_x = list(range(len(aux_ini) + 1, len(aux_ini) + len(aux_end) + 1))
    plt.plot(aux_x, aux_end, '.-', label='Final')

    plt.xlabel('# Step')
    plt.ylabel('TOTEN (eV)')
    plt.legend()
    plt.tight_layout()

    # Show the figures
    plt.show()

print('\nEND')
