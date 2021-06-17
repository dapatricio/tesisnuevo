import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as plt


labels = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21']
men_means = [1, 4, 3, 1, 3, 3, 2, 4, 4, 1, 2, 3, 3, 1, 4, 2, 2, 3, 2, 4, 1]
women_means = [1, 2, 4, 4, 2, 2, 3, 4, 1, 3, 4, 2, 1, 2, 3, 4, 2, 3, 4, 1, 4]

x = np.arange(len(labels))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, men_means, width, label='Nivel Obtenido')
rects2 = ax.bar(x + width/2, women_means, width, label='Nivel Recomendado')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Nivel')
ax.set_title('Nivel Obtenido vs Nivel Recomendado')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.tick_params(labelsize=8)

fig.tight_layout()

#plt.show()
fig.set_figheight(3.5)
fig.set_figwidth(7)
plt.savefig('../static/graphimages/saved_figure.png')