# Read information from VASP files
# @Author: Marco A. Villena (marcoantonio.villena@kaust.edu.sa)
# @Date: 16/03/2023

__author__ = 'Marco A. Villena'
__email__ = 'marcoantonio.villena@kaust.edu.sa'
__version__ = '0.3'

# ----- Modules -----
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from vasp_functions import f_total_atoms
from vasp_functions import f_postions_forces

# ------ Input variables -----
files_path_ini = os.path.join(os.getcwd(), 'ini_state')
files_path_end = os.path.join(os.getcwd(), 'end_state')

marker_size = 150
vector_length = 50  # 5

# ---------- MAIN ----------
total_atoms = f_total_atoms(files_path_ini)
print('Total number of atoms = ', total_atoms)

data_first = np.array(f_postions_forces(files_path_ini, total_atoms, 1))
data_last = np.array(f_postions_forces(files_path_end, total_atoms, 1))
data_dif = np.sqrt(((data_last[:, 0] - data_first[:, 0])**2) + ((data_last[:, 1] - data_first[:, 1])**2) + ((data_last[:, 2] - data_first[:, 2])**2))

# ------ Plots ------
# FIGURE forces of both, the initial and final state
# Create the figure and the 3D axes
fig, axs = plt.subplots(2, 3, figsize=(25, 10), subplot_kw={'projection': '3d'})

# Draw the scatter with the given colors and add a color bar for each plot
scatter1 = axs[0, 0].scatter(data_first[:, 0], data_first[:, 1], data_first[:, 2], c=data_first[:, 3], s=marker_size)
cbar1 = fig.colorbar(scatter1, ax=axs[0, 0], orientation='vertical', shrink=0.65)
title_label = 'X-Forces = [' + str(round(np.min(data_first[:, 3]), 4)) + ', ' + str(round(np.max(data_first[:, 3]), 4)) + '] (eV/Angst)'
cbar1.set_label(title_label, fontsize=10)

scatter2 = axs[0, 1].scatter(data_first[:, 0], data_first[:, 1], data_first[:, 2], c=data_first[:, 4], s=marker_size)
cbar2 = fig.colorbar(scatter2, ax=axs[0, 1], orientation='vertical', shrink=0.65)
title_label = 'Y-Forces = [' + str(round(np.min(data_first[:, 4]), 4)) + ', ' + str(round(np.max(data_first[:, 4]), 4)) + '] (eV/Angst)'
cbar2.set_label(title_label, fontsize=10)

scatter3 = axs[0, 2].scatter(data_first[:, 0], data_first[:, 1], data_first[:, 2], c=data_first[:, 5], s=marker_size)
cbar3 = fig.colorbar(scatter3, ax=axs[0, 2], orientation='vertical', shrink=0.65)
title_label = 'Z-Forces = [' + str(round(np.min(data_first[:, 5]), 4)) + ', ' + str(round(np.max(data_first[:, 5]), 4)) + '] (eV/Angst)'
cbar3.set_label(title_label, fontsize=10)

# ----
scatter5 = axs[1, 0].scatter(data_last[:, 0], data_last[:, 1], data_last[:, 2], c=data_last[:, 3], s=marker_size)
cbar5 = fig.colorbar(scatter5, ax=axs[1, 0], orientation='vertical', shrink=0.65)
title_label = 'X-Forces = [' + str(round(np.min(data_last[:, 3]), 4)) + ', ' + str(round(np.max(data_last[:, 3]), 4)) + '] (eV/Angst)'
cbar5.set_label(title_label, fontsize=10)

scatter6 = axs[1, 1].scatter(data_last[:, 0], data_last[:, 1], data_last[:, 2], c=data_last[:, 4], s=marker_size)
cbar6 = fig.colorbar(scatter6, ax=axs[1, 1], orientation='vertical', shrink=0.65)
title_label = 'Y-Forces = [' + str(round(np.min(data_last[:, 4]), 4)) + ', ' + str(round(np.max(data_last[:, 4]), 4)) + '] (eV/Angst)'
cbar6.set_label(title_label, fontsize=10)

scatter7 = axs[1, 2].scatter(data_last[:, 0], data_last[:, 1], data_last[:, 2], c=data_last[:, 5], s=marker_size)
cbar7 = fig.colorbar(scatter7, ax=axs[1, 2], orientation='vertical', shrink=0.65)
title_label = 'Z-Forces = [' + str(round(np.min(data_last[:, 5]), 4)) + ', ' + str(round(np.max(data_last[:, 5]), 4)) + '] (eV/Angst)'
cbar7.set_label(title_label, fontsize=10)

# Label the axes of each plot
for i in range(2):
    for j in range(3):
        axs[i, j].set_xlabel('a-axis')
        axs[i, j].set_ylabel('b-axis')
        axs[i, j].set_zlabel('c-axis')

axs[0, 0].text(0.5, 1.1, 1, 'Initial state', horizontalalignment='center', transform=axs[0, 0].transAxes)
axs[1, 0].text(0.5, 1.1, 1, 'Final state', horizontalalignment='center', transform=axs[1, 0].transAxes)


# FIGURE vectorial forces
# Create the figure and the 3D axes
fig2, axs = plt.subplots(1, 2, figsize=(25, 10), subplot_kw={'projection': '3d'})

# Draw the scatter with the given colors and add a color bar for each plot
color_first = np.linalg.norm(data_first[:, 3:], axis=1)
title_label = 'Forces = [' + str(round(np.min(color_first), 3)) + ', ' + str(round(np.max(color_first), 3)) + '] (eV/Angst)'
color_first = color_first / np.max(color_first)
axs[0].scatter(data_first[:, 0], data_first[:, 1], data_first[:, 2], c='black', s=15)
vector1 = axs[0].quiver(data_first[:, 0], data_first[:, 1], data_first[:, 2], data_first[:, 3], data_first[:, 4], data_first[:, 5], color=plt.cm.jet(color_first), length=vector_length, arrow_length_ratio=0.2, cmap='jet')
cbar1 = fig2.colorbar(vector1, ax=axs[0], orientation='horizontal', shrink=0.65)
cbar1.set_label(title_label, fontsize=10)


color_last = np.linalg.norm(data_last[:, 3:], axis=1)
title_label = 'Forces = [' + str(round(np.min(color_last), 3)) + ', ' + str(round(np.max(color_last), 3)) + '] (eV/Angst)'
color_last = color_last / np.max(color_last)
axs[1].scatter(data_last[:, 0], data_last[:, 1], data_last[:, 2], c='black', s=15)
vector2 = axs[1].quiver(data_last[:, 0], data_last[:, 1], data_last[:, 2], data_last[:, 3], data_last[:, 4], data_last[:, 5], color=plt.cm.jet(color_last), length=vector_length, arrow_length_ratio=0.2, cmap='jet')
cbar2 = fig2.colorbar(vector2, ax=axs[1], orientation='horizontal', shrink=0.65)
cbar2.set_label(title_label, fontsize=10)


# Label the axes of each plot
for j in range(2):
    axs[j].set_xlabel('a-axis')
    axs[j].set_ylabel('b-axis')
    axs[j].set_zlabel('c-axis')

axs[0].set_title('Initial state')
axs[1].set_title('Final state')


# FIGURE displacement
fig3 = plt.figure('Displacement', figsize=(12, 12))
ax = fig3.add_subplot(111, projection='3d')

# Draw the scatter with the given colors and add a color bar
scatter = ax.scatter(data_first[:, 0], data_first[:, 1], data_first[:, 2], c=data_dif, s=marker_size)
cbar = fig3.colorbar(scatter, ax=ax, orientation='vertical', shrink=0.5)
title_label = 'Max. Displacement = ' + str(round(np.max(data_dif), 4)) + ' (Angst)'
cbar.set_label(title_label, fontsize=10)
ax.set_xlabel('a-axis')
ax.set_ylabel('b-axis')
ax.set_zlabel('c-axis')

# Show the figures
plt.show()

print('END')
