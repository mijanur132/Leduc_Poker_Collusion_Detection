def kuhn_eval(card, public):
    return card.rank


def leduc_eval(hole_card, board):
    cards = [hole_card] + board
    #print("leduc eval:",cards)
    #print("cards.count(hole_card)",cards.count(hole_card))
    #print("hole_card.rank", hole_card.rank)
    #print("max(cards).rank, min(cards).rank)",max(cards).rank , min(cards).rank)


    if cards.count(hole_card) > 1:
        return 15 * 14 + hole_card.rank

    return 14 * max(cards).rank + min(cards).rank
