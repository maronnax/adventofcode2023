from collections import namedtuple
import re
import numpy as np
from scipy.signal import convolve2d
from helpers import get_input_lines

@np.vectorize
def make_symbol_indicator(elmt):
    return int(bool(re.match(r"[^0-9.]", elmt)))

def dist(i1, i2):
    return np.sqrt((i1[0]-i2[0])**2 + (i1[1]-i2[1])**2)


lines = get_input_lines("day3")

char_array = np.array([list(l) for l in lines])
kernel = np.ones((3,3))
symbol_adjacency_mask = convolve2d(make_symbol_indicator(char_array), kernel, mode='same')

parts={}
symbols={}

SchematicObject = namedtuple("SchematicObject", ("value", "ind", "adj_mask"))

# Parse the parts/numbers
for row_ndx in range(len(lines)):
    for match in re.finditer(r"\d+", lines[row_ndx]):
        col_low, col_high = match.span()
        ind = np.zeros(char_array.shape)
        ind[row_ndx,col_low:col_high]=1
        if np.any(ind * symbol_adjacency_mask):
            parts[(row_ndx, col_low)] = SchematicObject(
                value=int(match.group()),
                ind=ind,
                adj_mask=convolve2d(ind, kernel, mode="same"),
            )

# Parse the symbols
for index, char in np.ndenumerate(char_array):
    if match := re.match(r"[^0-9.]", char):
        ind = np.zeros(char_array.shape)
        ind[index] = 1
        adj_mask = convolve2d(ind, kernel, mode='same')
        symbols[index] = SchematicObject(value=match.group(), ind=ind, adj_mask=adj_mask)



# Problem 1
print(sum([p.value for p in parts.values()]))

# Problem 2
gears = []
pgears = [(ind, g) for ind, g in symbols.items() if g.value == '*']
max_label_length = max(map(lambda p: len(str(p.value)), parts.values()))

for idx_gear, pgear in pgears:
    close_labels = [
        label
        for (idx_label, label) in parts.items()
        if dist(idx_gear, idx_label) < max_label_length + 1
    ]
    touching_labels = [l for l in close_labels if np.any(l.ind * pgear.adj_mask)]
    if len(touching_labels) == 2:
        gears.append(touching_labels)

print(sum([ g1.value * g2.value for (g1, g2) in gears]))
