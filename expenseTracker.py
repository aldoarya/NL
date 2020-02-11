import sqlite3
import tkinter as tk
import datetime
import math
from tkinter import messagebox

conn = sqlite3.connect("expenses.db")
csr = conn.cursor()

conn.execute("""CREATE TABLE IF NOT EXISTS expenses(
            Name TEXT,
            Category TEXT,
            Day INTEGER,
            Month TEXT,
            Year INTEGER,
            Amount REAL
            )""")
conn.commit()

def totalFoods():
    csr.execute("SELECT Amount FROM expenses WHERE Category = 'Foods'")
    foods = csr.fetchall()
    total = 0
    for x in range(len(foods)):
        total += foods[x][0]
    return total

def totalTransport():
    csr.execute("SELECT Amount FROM expenses WHERE Category = 'Transport'")
    trans = csr.fetchall()
    total = 0
    for x in range(len(trans)):
        total += trans[x][0]
    return total

def totalHealth():
    csr.execute("SELECT Amount FROM expenses WHERE Category = 'Health'")
    health = csr.fetchall()
    total = 0
    for x in range(len(health)):
        total += health[x][0]
    return total

def totalBill():
    csr.execute("SELECT Amount FROM expenses WHERE Category = 'Bills'")
    bills = csr.fetchall()
    total = 0
    for x in range(len(bills)):
        total += bills[x][0]
    return total

def totalCollege():
    csr.execute("SELECT Amount FROM expenses WHERE Category = 'College'")
    college = csr.fetchall()
    total = 0
    for x in range(len(college)):
        total += college[x][0]
    return total

def totalEtc():
    csr.execute("SELECT Amount FROM expenses WHERE Category = 'Etc'")
    etc = csr.fetchall()
    total = 0
    for x in range(len(etc)):
        total += etc[x][0]
    return total

def totalAll():
    csr.execute("SELECT Amount FROM expenses")
    all = csr.fetchall()
    total = 0
    for x in range(len(all)):
        total += all[x][0]
    return total

def addRecord():
    def input():
        name = name_entry.get()
        amount = amount_entry.get()
        selDay = day.get()
        selMonth = selectMonth.get()
        selYear = year.get()
        ctg = selectCategory.get()

        try:
            float(amount)
            int(selDay)
            int(selYear)
        except ValueError:
            messagebox.showwarning("Error", "Invalid Input")
        finally:
            amount = float(amount)
            selDay = int(selDay)
            selYear = int(selYear)

        if ctg == "Select Category":
            messagebox.showwarning("Error", "Please Select Category")
        else:
            csr.execute("INSERT INTO expenses (Name, Category, Day, Month, Year, Amount) VALUES (?, ?, ?, ?, ?, ?)", (name, ctg, selDay, selMonth,
                                                                                                                      selYear, amount))
            conn.commit()
            messagebox.showinfo("Success", "Record Added")
            addWindow.destroy()


    addWindow = tk.Toplevel()
    addWindow.minsize(width=200, height=200)
    addWindow.maxsize(width=200, height=200)
    dayFrame = tk.Frame(addWindow, width=200, height= 20)

    title = tk.Label(addWindow, text="Enter Your Expenses")
    name_label = tk.Label(addWindow, text="Name:")
    name_entry = tk.Entry(addWindow)
    amount_label = tk.Label(addWindow, text="Amount:")
    amount_entry = tk.Entry(addWindow)
    category_label = tk.Label(addWindow, text="Category:")
    categorylist = ["Foods", "Transport", "Health", "Bills", "College", "Etc"]
    selectCategory = tk.StringVar()
    selectCategory.set("Select Category")
    categoryMenu = tk.OptionMenu(addWindow, selectCategory, *categorylist)
    categoryMenu.config(width=14)
    submit = tk.Button(addWindow, text="Input", command=input)
    date = tk.Label(dayFrame, text="Date:")
    monthlist = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    selectMonth = tk.StringVar()
    day = tk.Entry(dayFrame, text="Day")
    day.config(width=3)
    month = tk.OptionMenu(dayFrame, selectMonth, *monthlist)
    selectMonth.set('Month')
    month.config(width=5)
    year = tk.Entry(dayFrame)
    year.config(width=5)

    title.grid(row=0, columnspan=2, sticky="N", pady=18)
    name_label.grid(row=1, column=0, sticky="W")
    name_entry.grid(row=1, column=1)
    amount_label.grid(row=2, column=0, sticky="W")
    amount_entry.grid(row=2, column=1)
    category_label.grid(row=3, column=0)
    categoryMenu.grid(row=3, column=1)
    dayFrame.grid(row=4, columnspan=2)
    date.grid(row=0, column=0, sticky="W")
    day.grid(row=0, column=1, sticky="E")
    month.grid(row=0, column=2, sticky="E")
    year.grid(row=0, column=3, sticky="E")
    submit.grid(row=5, columnspan=2, sticky="N")

def tabify(s, tabsize = 4):
    ln = ((len(s)/tabsize)+1)*tabsize
    ln = int(math.floor(ln))
    return s.ljust(ln)

def place_value(number):
    return ("{:,}".format(number))

def refresh():
    global window
    window.quit()
    GUI()

def showRecord():
    recordWindow = tk.Toplevel()
    recordWindow.minsize(width=350, height=300)
    recordWindow.maxsize(width=350, height=300)

    csr.execute('SELECT * FROM expenses')

    frame = tk.Frame(recordWindow)
    frame.grid(row=0)

    Lb = tk.Listbox(frame, height=8, width=50)
    Lb.grid(row=0)

    scroll = tk.Scrollbar(frame)
    scroll.config(command=Lb.yview)
    scroll.grid(row=0, column=1, sticky="E")
    Lb.config(yscrollcommand=scroll.set)

    Lb.insert(0, tabify('Name')+tabify('Category')+tabify('Day')+tabify('Month')+tabify('Year')+tabify('Amount'))  # first row in listbox

    data = csr.fetchall()

    for row in data:
        Lb.insert(1, row)
    conn.commit()

# ------GUI------
window = tk.Tk()
def GUI():
    window.title("Expense Tracker")
    window.minsize(width=470, height=180)
    window.maxsize(width=470, height=180)
    title = tk.Label(window, text="Personal Expense Tracker", font="Bebas")
    title.grid(row=0, column=1, sticky="S", pady=10)

    menu = tk.Menu(window)
    Add = menu.add_command(label="Add", command=addRecord)
    Record = menu.add_command(label="Record", command=showRecord)

    # -------Frame A-------
    frameA = tk.Frame(window, width=50, height=40)
    food_label = tk.Label(frameA, text="Foods")
    foodAmount = tk.Label(frameA, text="Rp"+str(place_value(totalFoods())))
    trans_label = tk.Label(frameA, text="Transport")
    transAmount = tk.Label(frameA, text="Rp"+str(place_value(totalTransport())))
    health_label = tk.Label(frameA, text="Health")
    healthAmount = tk.Label(frameA, text="Rp"+str(place_value(totalHealth())))

    frameA.grid(row=1, column=0, sticky="N", padx=5)
    food_label.grid(row=0, column=0, sticky="W")
    foodAmount.grid(row=0, column=1, sticky="W")
    trans_label.grid(row=1, column=0, sticky="W")
    transAmount.grid(row=1, column=1, sticky="W")
    health_label.grid(row=2, column=0, sticky="W")
    healthAmount.grid(row=2, column=1, sticky="W")

    # ------Frame Mid------
    frameMid = tk.Frame(window, width=10, height=60)
    frameMid.grid(row=1, column=1, sticky="N")

    # ------Frame B-------
    frameB = tk.Frame(window, width=50, height=40, padx=10)
    bills_label = tk.Label(frameB, text="Bills")
    billsAmount = tk.Label(frameB,  text="Rp"+str(place_value(totalBill())))
    col_label = tk.Label(frameB, text="College")
    colAmount = tk.Label(frameB, text="Rp"+str(place_value(totalCollege())))
    etc_label = tk.Label(frameB, text="Etc")
    etcAmount = tk.Label(frameB, text="Rp"+str(place_value(totalEtc())))

    frameB.grid(row=1, column=2, sticky="N")
    bills_label.grid(row=0, column=0, sticky="W")
    billsAmount.grid(row=0, column=1, sticky="W")
    col_label.grid(row=1, column=0, sticky="W")
    colAmount.grid(row=1, column=1, sticky="W")
    etc_label.grid(row=2, column=0, sticky="W")
    etcAmount.grid(row=2, column=1, sticky="W")

    # --------Frame Mid-Bottom-------
    frameMidBottom = tk.Frame(window, width=50, height=50)
    total_label = tk.Label(frameMidBottom, text="Total Expenses:")
    expenses_label = tk.Label(frameMidBottom, text="Rp"+str(place_value(totalAll())))
    refreshButton = tk.Button(frameMidBottom, text="Refresh", command=refresh)

    frameMidBottom.grid(row=2, column=1)
    total_label.grid(row=0, column=0, columnspan=3, sticky="N")
    expenses_label.grid(row=1, column=0, columnspan=3, sticky="N")
    refreshButton.grid(row=2, column=0, columnspan=3)

    window.config(menu=menu)
    window.mainloop()

GUI()