import csv

crashes = []


def load_data(filename):
    global crashes
    crashes = []
    with open(filename) as csvfile:
        csv_data = csv.reader(csvfile)
        header = True
        for row in csv_data:
            if not header:
                crashes.append(float(row[0]))
            else:
                header = False


def mock(bet_amount, threshold, start_bet_row, multiplier, result_message):
    bet_amount_reset = bet_amount
    profit = 0
    max_negative = 0
    total_money_out = 0
    losses_in_a_row_max = 0
    losses_in_a_row = 0
    print("~~~ Simulating CRASH with betting amount of $" + str(bet_amount) +
          "\nand auto cash-out amount of $" + str(threshold) + "~~~")
    for crash in crashes:
        print("Crashed at: " + str(crash))
        if threshold < crash:
            if losses_in_a_row >= start_bet_row:
                print("CASHED OUT at: " + str(threshold))
                print("bet amt is: " + str(bet_amount) + " multiply by " + str(threshold) + " gives us")
                new_cash = round(bet_amount * threshold, 2)
                print(new_cash)
                print("our profit before hand was " + str(profit))
                profit = round(profit + new_cash - bet_amount, 2)
                print("new profit is: " + str(profit))
            if losses_in_a_row > losses_in_a_row_max:
                losses_in_a_row_max = losses_in_a_row
                losses_in_a_row = 0
            else:
                losses_in_a_row = 0
            print()
            # reset bet amount
            bet_amount = bet_amount_reset
        else:
            if losses_in_a_row >= start_bet_row:
                # crashed before cashed out, lose the amt bet
                print("CRASHED :(((")
                print("we had bet: " + str(bet_amount))
                print("Profit was: " + str(profit))
                profit = round(profit - bet_amount, 2)
                print("profit is now: " + str(profit))
                # multiply the bet amt by the multiplier
                bet_amount *= multiplier
                print("our new betting amount is now " + str(bet_amount))
            losses_in_a_row += 1
            print("Loss in a row: " + str(losses_in_a_row))
            print()
            if profit < max_negative:
                max_negative = profit
                total_money_out = round(max_negative - bet_amount, 2)
    result_message += "Max negative profit: $" + str(max_negative) + "\n"
    result_message += "Total money out at once: $" + str(total_money_out) + "\n"
    result_message += "Number of losses in a row: " + str(losses_in_a_row_max) + "\n\n"
    result_message += "Total profits: $" + str(profit) + "\n\n\n"
    return result_message


filenames = ['data/crash_data-500.csv', 'data/crash_data-1187.csv', 'data/crash_data-1262.csv',
             'data/crash_data-1443.csv', 'data/crash_data-1482.csv', 'data/crash_data-1801.csv',
             'data/crash_data-1887.csv']

base = float(input("Enter base bet amount: "))
start_betting = int(input("How many crashes in a row until you start betting: "))
multiply = float(input("How much to multiply bet by when losing: "))
cash_out = float(input("enter cash-out amount: "))

message = "\n\n"

for files in filenames:
    message += "RESULTS for file: " + files + "\n\n"
    load_data(files)
    print("STARTING FOR: " + files + "\n")
    message = mock(base, cash_out, start_betting, multiply, message)
print(message)
