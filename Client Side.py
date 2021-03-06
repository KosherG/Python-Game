# Python Game Client Side 2021 - by A.G.
# Python Exercise in "Socket", GUI with "Tkinter";
# Game to Guess the random number generated by server.

from tkinter import *                                   # Modules used in project
import socket


# Exit Button function (Cross window)
def exit_b(window):
    window.destroy()                                    # Close destination window
    main_win.deiconify()                                # Bring back Main Window
    b_new_game["state"] = "normal"                      # Bring back Main Menu Buttons state to normal
    b_score["state"] = "normal"


# New Game window / Socket connection
def new_game():
    def reset():
        game_win.destroy()
        new_game()

    # Winner function updates Score Board
    def winner(_server_data):
        canvas_game.itemconfig(server_print, text="You  Won")
        turn = _server_data[-1]
        canvas_game.itemconfig(attempt, text=("Attempt: " + turn))
        b_submit.place_forget()

        b_new_game_l = Button(game_win, text="N E W  G A M E", height=2, width=26, bg="#d262f9", relief="raised",
                              activebackground="#7e3a95", state=NORMAL, font="Forte 16", command=reset)
        b_new_game_l.place(x=400, y=400, anchor="center")
        place_score = user_name+" "+turn+"\n\n"
        f = open("scoreBoard.txt", "a")
        f.write(place_score)
        f.close()

    # Responsible for socket session
    def send_to_server():
        user_data = user_entry.get()                    # Save Entry field to variable
        tcpSocket.send(user_data.encode())              # Send to Server
        server_data = tcpSocket.recv(2048).decode()     # Receive from server
        user_entry.delete(0, END)                       # Clear Entry field

        if "Lost" in server_data:                                                       # Player lost scenario
            canvas_game.itemconfig(server_print, text="You  Lost")
            b_submit.place_forget()

            b_new_game_l = Button(game_win, text="N E W  G A M E", height=2, width=26, bg="#d262f9", relief="raised",
                                  activebackground="#7e3a95", state=NORMAL, font="Forte 16", command=reset)

            b_new_game_l.place(x=400, y=400, anchor="center")
        elif "Win" in server_data:                                                       # Correct number guessed
            winner(server_data)
        elif "High" in server_data:                                                      # To high number guessed
            canvas_game.itemconfig(server_print, text="Too High")
            turn = server_data[-1]
            canvas_game.itemconfig(attempt, text=("Attempt: "+turn))
        elif "Low" in server_data:                                                       # To low number guessed
            canvas_game.itemconfig(server_print, text="Too Low")
            turn = server_data[-1]
            canvas_game.itemconfig(attempt, text=("Attempt: " + turn))
        else:
            canvas_game.itemconfig(server_print, text=server_data)

    b_new_game["state"] = "disable"                                                       # Disable Main Menu Button
    b_score["state"] = "disable"                                                          # Disable Main Menu Button

    game_win = Toplevel(main_win)
    game_win.geometry("800x600")
    game_win.resizable(0, 0)
    game_win.title("G A M E")
    canvas_game = Canvas(game_win, width=640, height=480)                                 # Canvas to host other objects
    canvas_game.pack(fill="both", expand=True)                                            # Canvas position
    canvas_game.create_image(0, 0, image=bg_game, anchor="nw")                            # Place Image "bg_game"

    canvas_game.create_rectangle(50, 120, 750, 450, fill="#3f1d4a", outline='#edc0fc')

    canvas_game.create_text(400, 50, text="Guess the Number", fill="#edc0fc",             # Title
                            font="Forte 38", justify="center", anchor="n")
    attempt = canvas_game.create_text(60, 130, text="Attempt: 1", fill="#edc0fc",                       # Turn indicator
                                      font="Forte 18", justify="center", anchor="nw")

    canvas_game.create_text(60, 160, text=("Player: "+user_name), fill="#edc0fc",                       # User_name
                            font="Forte 18", anchor="nw")

    server_print = canvas_game.create_text(400, 180, text="Guess Number in range\n1-20", fill="white",  # Server output
                                           font="Forte 34", justify="center", anchor="n")

    user_entry = Entry(game_win, width=4, font="Forte 26 bold", justify="center", bg="#df91fa")
    canvas_game.create_window(400, 300,  window=user_entry)

    b_submit = Button(game_win, text="S U B M I T", height=2, width=26, bg="#d262f9", relief="raised",  # Submit Button
                      activebackground="#7e3a95", state=NORMAL, font="Forte 16", command=send_to_server)

    b_submit.place(x=400, y=400, anchor="center")
    b_submit.bind("<Enter>", hover_in)
    b_submit.bind("<Leave>", hover_out)

    b_exit_score = Button(game_win, text="E X i T", height=2, width=26, bg="#d262f9", relief="raised",    # Exit Button
                          activebackground="#7e3a95", command=lambda: exit_b(game_win), state=NORMAL, font="Forte 16")

    b_exit_score.place(x=400, y=530, anchor="center")
    b_exit_score.bind("<Enter>", hover_in)
    b_exit_score.bind("<Leave>", hover_out)

    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                               # Connection to socket
    tcpSocket.connect(("127.0.0.1", 8000))                                                      # Socket IP and Port


# Score Window
def score_board():                              # Score Window

    main_win.iconify()                          # Minimize window

    f = open("scoreBoard.txt", "r")             # Read score-board from file
    scoreList = f.read()
    f.close()
    score_window = Toplevel(main_win)
    score_window.title("S C O R E")
    score_window.geometry("480x640")
    score_window.resizable(0, 0)
    canvas_score = Canvas(score_window, width=480, height=640)           # Canvas to host other objects
    canvas_score.pack(fill="both", expand=True)                          # Canvas position
    canvas_score.create_image(0, 0, image=bg_score, anchor="nw")         # Place Image "bg_score"

    canvas_score.create_text(240, 100, text="S C O R E\nB O A R D",
                             fill="#d262f9", font="Forte 30 bold",
                             justify="center")
    canvas_score.create_text(240, 240, text=scoreList,
                             fill="white", font="Forte 18",
                             justify="center", anchor="n")
    b_exit_score = Button(score_window, text="E X i T", height=2, width=26, bg="#d262f9",
                          relief="raised", activebackground="#7e3a95",
                          command=lambda: exit_b(score_window), state=NORMAL, font="Forte 16")

    b_exit_score.place(x=240, y=580, anchor="center")
    b_exit_score.bind("<Enter>", hover_in)
    b_exit_score.bind("<Leave>", hover_out)


# Login Window / Enter Name
def login():                                    # Login / Enter Name
    main_win.iconify()                          # Minimize window

    def start_b():
        global user_name
        user_name = enter_name.get()            # Save User name
        print(user_name)
        login_window.destroy()
        new_game()
    login_window = Toplevel(main_win)
    login_window.title("L O G I N")
    login_window.geometry("400x250")
    login_window.resizable(0, 0)
    canvas_login = Canvas(login_window, width=400, height=250)
    canvas_login.pack(fill="both", expand=True)
    canvas_login.create_image(0, 0, image=bg_login, anchor="nw")

    canvas_login.create_text(200, 40, text="Enter Your Name",
                             fill="#d262f9", font="Forte 26 bold",
                             justify="center")
    enter_name = Entry(canvas_login, width=16, font="Forte 26 bold", justify="center", bg="#df91fa")
    canvas_login.create_window(200, 100, window=enter_name)

    b_start = Button(login_window, text="S T A R T", height=1, width=20, bg="#d262f9", relief="raised",      # Start
                     activebackground="#7e3a95", command=start_b, state=NORMAL, font="Forte 16")
    b_exit_login = Button(login_window, text="E X i T", height=1, width=20, bg="#d262f9", relief="raised",   # Exit
                          activebackground="#7e3a95", command=lambda: exit_b(login_window),
                          state=NORMAL, font="Forte 16")

    b_start.place(x=200, y=170, anchor="center")
    b_start.bind("<Enter>", hover_in)
    b_start.bind("<Leave>", hover_out)

    b_exit_login.place(x=200, y=220, anchor="center")
    b_exit_login.bind("<Enter>", hover_in)
    b_exit_login.bind("<Leave>", hover_out)


def hover_in(e):                                                          # Cursor over button effect / in
    e.widget["background"] = "#df91fa"


def hover_out(e):                                                         # Cursor over button effect / out
    e.widget["background"] = "#d262f9"


# Main Menu / Window GUI
main_win = Tk()                                                           # Main window
main_win.geometry("640x480")                                              # Main Window size
main_win.resizable(0, 0)                                                  # Window resize set to 0
main_win.title("L i v e  N u m b e r  G a m e")                           # Window Title


# Username and images variables
user_name = ""                                                       # User name
bg_main = PhotoImage(file="menu.png")                                # Background Image - Main Menu
bg_score = PhotoImage(file="score.png")                              # Background Image - Score board
bg_login = PhotoImage(file="login.png")                              # Background Image - User name/ Login
bg_game = PhotoImage(file="game.png")                                # Background Image - Game screen


canvas_main = Canvas(main_win, width=640, height=480)                     # Canvas to host other objects
canvas_main.pack(fill="both", expand=True)                                # Canvas position
canvas_main.create_image(0, 0, image=bg_main, anchor="nw")                # Place Image "bg_main"

canvas_main.create_text(320, 60, text="Guess the Number", fill="#3f1d4a",        # Title shadow
                        font="Forte 60 bold", justify="center", anchor="n")
canvas_main.create_text(320, 80, text="Guess the Number", fill="#edc0fc",        # Title
                        font="Forte 38 bold", justify="center", anchor="n")

b_new_game = Button(canvas_main, text="N E W   G A M E", height=2, width=26, bg="#d262f9", relief="raised",  # New Game
                    activebackground="#7e3a95", command=login, state=NORMAL, font="Forte 16")
b_score = Button(canvas_main, text="S C O R E", height=2, width=26, bg="#d262f9", relief="raised",           # Score
                 activebackground="#7e3a95", command=score_board, state=NORMAL, font="Forte 16")
b_exit = Button(canvas_main, text="E X i T", height=2, width=26, bg="#d262f9", relief="raised",              # Exit
                activebackground="#7e3a95", command=main_win.destroy, state=NORMAL, font="Forte 16")

b_new_game.place(x=320, y=220, anchor="center")     # Button place
b_new_game.bind("<Enter>", hover_in)                # Hover in / out
b_new_game.bind("<Leave>", hover_out)

b_score.place(x=320, y=290, anchor="center")        # Button place
b_score.bind("<Enter>", hover_in)                   # Hover in / out
b_score.bind("<Leave>", hover_out)

b_exit.place(x=320, y=380, anchor="center")         # Button place
b_exit.bind("<Enter>", hover_in)                    # Hover in / out
b_exit.bind("<Leave>", hover_out)


main_win.mainloop()                                 # Main loop
