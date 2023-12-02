from pathlib import Path
import os

def get_input_lines(dayname):
    input_dir = (Path(__file__).parent / "inputs")
    inputs = [x for x in os.listdir(str(input_dir)) if dayname in x]

    assert len(inputs) != 0, "Input not found"
    assert len(inputs) == 1, "Multiple inputs found"
    return [l.strip() for l in open(input_dir / inputs[0]).readlines() if l.strip()]
