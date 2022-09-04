from math import comb


def power_distribution(count, base, power, inverse=True):
    polarity = 1
    if inverse:
        polarity = -1
    weights = [base**(polarity*power*x) for x in range(count)]
    # print(weights)
    # print(normalize_distribution(weights))
    # print()
    return weights


def normalize_distribution(distribution):
    sum = 0
    for i in distribution:
        sum = sum+i
    for i in distribution:
        i = i/sum*100
    return distribution


def calc_dice_likeliness(n, x, p):
    '''Calculate the probability that out of n dices x are the same, with p allowing for 1/2 '''
    return comb(n, x)*(p**x)*(1-p)**(n-x)

def calc_likeliness_of_claim(own_dices, claim, dice_count ,wild_card_in_play):
    '''Calculate the likeliness that the claim is true'''
    face = claim['face']
    num_hand = own_dices.count(face)
    num_claim = claim['num']    
    num_unclaimed = num_claim - num_hand
    unknown_dice_count = dice_count - len(own_dices)
    p = 1/6
    if wild_card_in_play:
        p = 1/3
    prob = 0
    for i in range(num_unclaimed, unknown_dice_count):
        prob = prob + calc_dice_likeliness(unknown_dice_count, num_unclaimed, p)
    return prob



if __name__ == '__main__':
    for power in range(1, 5):
        for base in range(1, 5):
            # print(base, power)
            power_distribution(5, base, power)
