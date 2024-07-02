from random import choice, randint
import re


def get_response(user_message: str) -> str:
    # simple example
    if user_message == '':
        return "Wise words"
    if user_message == "hey ava":  # A casual sanity check
        return "Hey"

    if user_message.startswith("Roll"):
        return handle_dice_rolls(user_message)

    return "Placeholder something"


def handle_dice_rolls(user_message: str) -> str:
    valid_dice = {4, 6, 8, 10, 12, 20}
    pattern = r'(\d+)D(\d+)'  # Pattern to match dice notation (e.g., 2D6, 1D8, etc.)
    dice_notations = re.findall(pattern, user_message)

    if not dice_notations:
        return "Something's wrong. Use 'Roll xDy', where x is the number of dice and y is the number of faces."

    results = []
    for notation in dice_notations:
        number, sides = map(int, notation)
        if sides not in valid_dice:
            results.append("Bad face count. Only D4, D6, D8, D10, D12 and D20 are accepted.")
        else:
            rolls = roll_dice(number, sides)
            results.append(f'{number}D{sides} rolls: {rolls} (Total: {sum(rolls)})')

    return "\n".join(results)


def roll_dice(number, sides):
    return [randint(1, sides) for _ in range(number)]
