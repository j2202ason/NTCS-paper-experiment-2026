import matplotlib.pyplot as plt
import numpy as np
import textwrap,os,datetime
from matplotlib.font_manager import FontProperties


def getdata(input_dict):
    labels = list(input_dict.keys())
    values = list(input_dict.values())
    return labels, values

def wrap_labels(labels, max_length):
    wrapped_labels = []
    for label in labels:
        if len(label) > max_length:
            if ' ' in label:
                words = label.split(' ')
                lines = []
                current_line = ""

                for word in words:
                    if len(current_line) + len(word) + 1 <= max_length:
                        if current_line:
                            current_line += " " + word
                        else:
                            current_line = word
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word

                if current_line:
                    lines.append(current_line)

                wrapped_label = "\n".join(lines)
            else:
                wrapped_label = textwrap.fill(label, width=max_length)

            wrapped_labels.append(wrapped_label)
        else:
            wrapped_labels.append(label)

    return wrapped_labels

def create_radar_chart(labels, values, max_length, title):
    wrapped_labels = wrap_labels(labels, max_length)
    plt.rcParams['font.sans-serif'] =['Arial Unicode MS']  #['Arial Unicode MS','SimHei'] #, ]  #, 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    num_vars = len(wrapped_labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    wrapped_labels_closed = wrapped_labels + [wrapped_labels[0]]
    values_closed = values + [values[0]]
    angles_closed = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(5,4), subplot_kw=dict(projection='polar'))

    ax.plot(angles_closed, values_closed, 'o-', linewidth=3, color='darkblue',
            markersize=10, markerfacecolor='lightblue', markeredgewidth=2,
            markeredgecolor='darkblue')

    ax.fill(angles_closed, values_closed, alpha=0.25, color='steelblue')

    ax.set_xticks(angles)

    ax.set_xticklabels(wrapped_labels, fontsize=8, ha='center', va='center')  #  fontsize for radar labels

    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle == 0:
            label.set_horizontalalignment('center')
            # label.set_verticalalignment('top')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('center')  # left
        else:
            label.set_horizontalalignment('center')  # right

    max_value = max(values)
    ax.set_ylim(0, max_value + 2)
    ax.set_yticks(np.arange(0, max_value + 3, 2))
    ax.set_yticklabels([str(int(i)) for i in np.arange(0, max_value + 3, 2)], fontsize=8)

    ax.yaxis.grid(True, linestyle='--', alpha=0.7)

    ax.xaxis.grid(True, linestyle='-', alpha=0.5)

    ax.set_ylabel('', fontsize=8, labelpad=20)  # ylabel:'Frequency/Value'

    plt.title(title, fontsize=10, fontweight='bold', pad=16)

    # 添加图例
    ax.plot([], [], 'o-', linewidth=3, color='darkblue', markersize=10,
            markerfacecolor='lightblue', markeredgewidth=2,
            markeredgecolor='darkblue', label='Method Value')

    for angle, value in zip(angles, values):
        label_radius = value + 0.5
        ax.text(angle, label_radius, str(value),
                ha='center', va='center', fontsize=8, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor="gray", alpha=0.8))  # edgecolor="gray"

    plt.figtext(0.5, 0.02,
                f"Total Methods: {len(labels)} | Max Value: {max(values)} | Min Value: {min(values)} | Mean Value: {np.mean(values):.2f}",
                ha="center", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.5))

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])

    return fig, ax


def visualdata(dctinput,i,fp,tmcode):
    ship_stability_methods, method_values = getdata(dctinput)
    fig, ax = create_radar_chart(ship_stability_methods, method_values, 18,
                                 title=f"Solutions Distribution of Case{i}")  # Solutions Distribution of Case{i}
    plt.show()

    # 可选：保存图形
    curpath = os.path.join(fp, "visualdata")
    fname_chart = os.path.join(curpath, f'Case{i}_chart_{tmcode}.png')
    fig.savefig(fname_chart, dpi=300, bbox_inches='tight')

    print(f"Final Result of Case{i}:")
    print("=" * 60)
    for i, (method, value) in enumerate(zip(ship_stability_methods, method_values), 1):
        print(f"{i:2d}. {method:40s} : {value:3d}")
    print("=" * 60)
    print(f"Methods Count: {len(ship_stability_methods)}")
    print(f"max: {max(method_values)} (method: {ship_stability_methods[method_values.index(max(method_values))]})")
    print(f"min: {min(method_values)}")
    print(f"means: {np.mean(method_values):.2f}")