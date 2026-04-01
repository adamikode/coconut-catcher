from tkinter import Tk, Canvas, Label, Button
from PIL import Image, ImageTk
import random

root = Tk()
root.title("Coconut Catcher")
canvas_width, canvas_height = 400, 400
canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="lightblue")
canvas.pack()

# Pontszám
score = 0
score_label = Label(root, text=f"Score: {score}", font=("Arial", 14))
score_label.pack()

# Képek
coconut_img = Image.open("img/coconut.png").resize((30, 30))
coconut_photo = ImageTk.PhotoImage(coconut_img)

basket_img = Image.open("img/basket.png").resize((70, 60))
basket_photo = ImageTk.PhotoImage(basket_img)

broken_coconut_img = Image.open("img/brokencoco.png").resize((70, 60))
broken_coconut_photo = ImageTk.PhotoImage(broken_coconut_img)

# Kosár
basket = canvas.create_image(200, 350, image=basket_photo)

# Kókuszdiók
coconuts = []
fall_speed = 5
game_running = True
game_over_items = []  # Game Over felirat és gomb tárolására

# Kosár mozgatása
def move_left(event):
    if game_running:
        canvas.move(basket, -20, 0)

def move_right(event):
    if game_running:
        canvas.move(basket, 20, 0)

root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

# Új kókuszdió
def create_coconut():
    if game_running:
        x_pos = random.randint(20, canvas_width - 20)
        coconut = canvas.create_image(x_pos, 0, image=coconut_photo)
        coconuts.append(coconut)
        root.after(random.randint(1000, 2000), create_coconut)

# Game Over kiírás és újraindítás gomb
def game_over(coconut_x, coconut_y):
    global game_running, game_over_items
    game_running = False

    # Törött kókuszdió az utolsó leesett helyén
    broken = canvas.create_image(coconut_x, coconut_y, image=broken_coconut_photo)

    # Töröljük a kosarat
    canvas.delete(basket)

    # Üzenet
    text_id = canvas.create_text(canvas_width//2, canvas_height//2 - 20,
                                 text=f"GAME OVER\nScore: {score}", font=("Arial", 20), fill="red")

    # Újraindítás gomb
    button = Button(root, text="Play Again", font=("Arial", 14), command=restart_game)
    button_window = canvas.create_window(canvas_width//2, canvas_height//2 + 30, window=button)

    game_over_items = [broken, text_id, button_window]

# Játék frissítése
def update_game():
    global score, fall_speed
    if not game_running:
        return
    for coconut in coconuts[:]:
        canvas.move(coconut, 0, fall_speed)
        x_c, y_c = canvas.coords(coconut)
        x_b, y_b = canvas.coords(basket)

        # Elkapás
        if (y_c >= y_b - 30 and y_c <= y_b + 30) and (x_c >= x_b - 35 and x_c <= x_b + 35):
            coconuts.remove(coconut)
            canvas.delete(coconut)
            score += 1
            score_label.config(text=f"Score: {score}")
            if score % 15 == 0:
                fall_speed += 1

        # Leesett
        elif y_c > canvas_height:
            coconuts.remove(coconut)
            canvas.delete(coconut)
            game_over(x_c, canvas_height - 30)
            return

    root.after(50, update_game)

# Újraindítás funkció
def restart_game():
    global score, fall_speed, game_running, basket, coconuts, game_over_items

    # Töröljük a Game Over elemeket (törött kókuszdió, szöveg, gomb)
    for item in game_over_items:
        try:
            canvas.delete(item)
        except:
            pass
    game_over_items = []

    # Töröljük az összes kókuszdiót a vászonról
    for coconut in coconuts:
        try:
            canvas.delete(coconut)
        except:
            pass
    coconuts = []

    # Kosár visszaállítása
    basket = canvas.create_image(200, 350, image=basket_photo)

    # Pontszám és gyorsaság visszaállítása
    score = 0
    score_label.config(text=f"Score: {score}")
    fall_speed = 5
    game_running = True

    # Új játék indítása
    create_coconut()
    update_game()

# Indítás
create_coconut()
update_game()
root.mainloop()
