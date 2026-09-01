def load_data(filename):
    stock_data = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                item, quantity = line.strip().split(",")
                stock_data[item] = int(quantity)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except ValueError:
        print(f"File '{filename}' is corrupted.")
    return stock_data
def show_stock(stock_data):
    if not stock_data:
        print("No stock available.")
    else:
        for index, (item, quantity) in enumerate(stock_data.items()):
            print(f"{index+1}. {item}: {quantity}")
def save_data(filename, stock_data):
    with open(filename, "w") as file:
                for item, quantity in stock_data.items():
                    file.write(f"{item},{quantity}\n")
def print_menu():
    print("enter 1 to add stock")
    print("enter 2 to remove stock")
    print("enter 3 to show stock’s contents")
    print("enter 4 to exit the program")
def stock_name(index, stock_data):
    index = int(index)
    if 1 <= index <= len(stock_data):
        return list(stock_data.keys())[index-1]
    return None
def add_stock(stock_data):
    show_stock(stock_data)
    add_name = input('Enter a name or id to add to, e.g. "banana" or "1", or a new name: ')
    if add_name.isdigit():
        add_name = stock_name(add_name , stock_data)
        if add_name is None:
            print("That id does not exist.")
            return
    while True:
        amount = input("Enter the quantity to add: ")
        if amount.isdigit():
            break
    amount = int(amount)
    add_name=add_name.lower()
    if add_name in stock_data:
        stock_data[add_name] += amount
    else:
        stock_data[add_name] = amount
def remove_stock(stock_data):
    show_stock(stock_data)
    remove_name = input('Enter a name or id to remove from, e.g. "banana" or "1": ')
    if remove_name.isdigit():
        remove_name = stock_name(remove_name , stock_data)
        if remove_name is None:
            print("That id does not exist.")
            return
    while True:
        amount = input("Enter the quantity to remove: ")
        if amount.isdigit():
            break
    amount = int(amount)
    remove_name=remove_name.lower()
    if remove_name not in stock_data:
        print(f"{remove_name} not found in stock.")
        return
    if stock_data[remove_name] - amount < 0:
        print("You cannot remove more than what is in stock.")
        return
    stock_data[remove_name] -= amount
def main():
    stock_data = load_data("stock.txt")
    while True:
        print_menu()
        choice = input("Enter your choice: ")
        if choice not in ("1", "2", "3", "4"):
            print("Invalid choice. Please try again.")
            continue
        choice = int(choice)
        if choice == 1:
            add_stock(stock_data)
        elif choice == 2:
            remove_stock(stock_data)
        elif choice == 3:
            show_stock(stock_data)
        elif choice == 4:
            save_data("stock.txt", stock_data)
            break
if __name__ == "__main__":
    main()