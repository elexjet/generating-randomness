### Stage 3/4: Predicting future input
import random

def data_string_generator():
    """ Prints Final data string of 100 digits of 0 or 1"""
    global triad_dictionary

    print("""Please give AI some data to learn...
The current data length is 0, 100 symbols left""")
    string_list = []

    """Get string from user input. If the input is less than 100 store string and ask for more input."""
    while len(string_list) < 100:
        dataset = input("Print a random string containing 0 or 1: \n\n")
        for num in dataset:
            if num == '0' or num == '1':
                string_list.append(num)
        print(f'Current data length is {len(string_list)}, {100 - len(string_list)} symbols left')
    final_string = "".join(string_list)
    print()
    print(f'Final data string:\n{final_string}')
    print()

    # Generate the dictionary keys as a list of triad binary numbers
    n = 3  # for 3 digits
    binary_triad = []
    for i in range(8):
        b = bin(i)[2:]
        l = len(b)
        b = str(0) * (n - l) + b
        binary_triad.append(b)

    final_list = [final_string[binary:binary+4] for binary in range(0, len(final_string))]

    triad_dictionary = dict.fromkeys(binary_triad)

    count_list = []
    for triad in binary_triad:
        count_list = []
        count_one = 0
        count_zero = 0
        for quad in final_list:
            if triad == quad[:-1]:
                if quad[3:] == '1':
                    count_one += 1
                elif quad[3:] == '0':
                    count_zero += 1
        count_list.append(count_zero)
        count_list.append(count_one)
        triad_dictionary[triad] = count_list
    print("""You have $1000. Every time the system successfully predicts your next press, you lose $1.
Otherwise, you earn $1. Print "enough" to leave the game. Let's go!""")

### Stage 4/4 ”Generate randomness” game


def user_input():
    #Ask the user to enter test strings or type enough to exit the game.
    global test_string

    while True:
        print()
        test_string = input("Print a random string containing 0 or 1:\n")
        contains_only_digits = any(map(str.isdigit, test_string))
        if test_string == "enough":
            print("Game over!")
            break
        elif contains_only_digits == True:
            if ("0" or "1") in test_string:
                test_string = [num for num in test_string if num == '0' or num == '1']
                test_string = ''.join(test_string)
                prediction()
                total_balance()
            else:
                continue

def prediction():
    """Learn user patterns by collecting triad statistics (from the Final data string) by asking a random string of 0 or 1 and makes a prediction"""
    global correct
    global incorrect
    global prediction_string

    prediction_string = ''
    ## Predictions
    # Generate first 3 predicted numbers randomly
    first_digits = []
    for _ in range(3):
        x = random.randint(0,1)
        first_digits.append(str(x))
    first_three = ''.join(first_digits)

    # Prediction
    """Iterate the length of the string and search with slices for matches with the keys from the dictionary
     'profile'. If the next number to the last in the triad index is 0 or 1 store in the values of the dict."""
    prediction_string += first_three
    for slice in range(len(test_string) - 3):
        triad = test_string[slice:slice + 3]
        if triad_dictionary[str(triad)][0] > triad_dictionary[str(triad)][1]:
            prediction_string += '0'
        else:
            prediction_string += '1'

    print(f"prediction:\n{prediction_string}\n")

    # Computer correct guesses
    correct = 0
    incorrect = 0
    for index in range(len(prediction_string)-3):
        if prediction_string[3:][index] == test_string[3:][index]:
            correct += 1
        else:
            incorrect += 1
    percentage = correct * 100 / (correct + incorrect)
    print(f'Computer guessed right {correct} out of {len(prediction_string) - 3} symbols ({percentage:.2f}%)')

def total_balance():
    """Calculates the remaining balance"""
    global balance
    balance -= correct - incorrect
    print(f'Your balance is now ${balance}')


### Game execution
if __name__ == "__main__":
    balance = 1000
    data_string_generator()
    user_input()