import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def draw_block_diagram():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    # Add blocks
    ax.add_patch(Rectangle((1, 8), 3, 1, edgecolor='black', facecolor='lightblue', label="Input"))
    ax.text(2.5, 8.5, "Workflow Details", ha="center", va="center")
    
    ax.add_patch(Rectangle((1, 5), 3, 1, edgecolor='black', facecolor='lightgreen', label="Performance RL"))
    ax.text(2.5, 5.5, "Performance RL", ha="center", va="center")
    
    ax.add_patch(Rectangle((6, 5), 3, 1, edgecolor='black', facecolor='salmon', label="Security RL"))
    ax.text(7.5, 5.5, "Security RL", ha="center", va="center")
    
    ax.add_patch(Rectangle((3.5, 2), 3, 1, edgecolor='black', facecolor='yellow', label="Output"))
    ax.text(5, 2.5, "Decision: Cluster", ha="center", va="center")
    
    # Add arrows
    ax.arrow(2.5, 8, 0, -2, head_width=0.2, head_length=0.3, fc='black', ec='black')
    ax.arrow(7.5, 8, 0, -2, head_width=0.2, head_length=0.3, fc='black', ec='black')
    ax.arrow(4, 5, 2, 0, head_width=0.2, head_length=0.3, fc='black', ec='black')
    ax.arrow(5, 4, 0, -1, head_width=0.2, head_length=0.3, fc='black', ec='black')
    
    # Add labels
    ax.text(0.5, 8.5, "Input", fontsize=12, weight='bold')
    ax.text(0.5, 5.5, "RL Models", fontsize=12, weight='bold')
    ax.text(0.5, 2.5, "Output", fontsize=12, weight='bold')
    
    plt.axis('off')
    plt.title("RL Decision System for Volunteer Edge Computing")
    plt.legend()
    plt.show()

draw_block_diagram()
