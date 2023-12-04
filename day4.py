from dataclasses import dataclass
from typing import List
from helpers import get_input_lines

@dataclass
class CardHistory:
    id: str
    card_numbers: List[int]
    winning_numbers: List[int]

    @property
    def num_matches(self) -> int:
        return len(self.card_numbers & self.winning_numbers)

    @property
    def score(self) -> int:
        wins = self.num_matches
        if wins == 0:
            return 0
        else:
            return 2**(wins-1)

#lines = [l.strip() for l in INPUT.splitlines() if l.strip()]
lines = get_input_lines("day4")

cards = []
for l in lines:
    card_id, data = l.split(':')
    win_num_str, card_num_str = data.split("|")

    card_numbers = set(card_num_str.split())
    winning_numbers = set(win_num_str.split())

    cards.append(
        CardHistory(
            id=card_id, card_numbers=card_numbers, winning_numbers=winning_numbers
        )
    )

print(sum(c.score for c in cards))

card_count = {cid.id: 1 for cid in cards}
for card_ndx, card in enumerate(cards):
    for extra_ndx in range(card.num_matches):
        card_count[cards[card_ndx + 1 + extra_ndx].id] += card_count[cards[card_ndx].id]

print(sum(card_count.values()))
