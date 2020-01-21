import msvcrt


# -*- coding: utf-8 -*- 
from tkinter import *
from tkinter import messagebox, colorchooser
import keyboard
import json
import random
import codecs
root = Tk()
root.geometry("900x600")


class MyApp:
    def __init__(self, parent):
        self.color_fg = 'black'
        self.color_bg = 'white'
        # Pokud zahájil procvičování nebo test -> self.start = 1
        self.start = 0
        # Dokončení procvičování nebo testu
        self.end = 0
        # Stisknutí textu další
        self.next=0
        self.parent = parent
        self.drawWidgets()
        # Použité slova (jejich id)
        self.used_numbers=[]
        # Odpovědi uživatele
        self.answers=[]
        # Délka slova
        self.words_number=0
        # Vygenerované anglické slovo
        self.questions=[]
        # Vygenerované české slovo
        self.questions_cz=[]
        # Zadané slovo
        self.word=[]
        # Aktuální slovo v češtině
        self.actual_word=""
        # Aktuální slovo v angličtině
        self.actual_word_eng=""
        self.practise_test=0

    
    def drawWidgets(self):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        self.container = Frame(self.parent, width=screen_width / 2, height=100, bg="gray") 
        self.canvas = Canvas(self.parent, width=screen_width / 2, height=screen_height / 2 - 100, bg=self.color_bg)
        self.canvas = Canvas(root, width=900, height=600, bg = '#afeeee')
        self.main_menu()
        self.canvas.pack(fill=BOTH,expand=True)
        self.canvas.bind('<Return>', self.enter)
        self.canvas.bind("<KeyPress>", self.keydown)
        self.canvas.bind("<Button-1>", self.on_button_press)
        button_info = Button(self.container, text="Info", command=self.info_box)
        button_info.pack(side=RIGHT)
        self.container.pack(fill=BOTH)
        self.canvas.focus_set()
        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label='Soubor',menu=filemenu)
        filemenu.add_command(label='Návrat do hlavní nabídky',command=self.back_to_main_menu)
        filemenu.add_command(label='Konec',command=self.parent.destroy)

    def clear_canvas(self):
        self.canvas.delete("all")
        print("Vyčistit canvas")

    def back_to_main_menu(self):
        # Vrácení do hlavního menu a restartování hodnot
        self.next=0  
        self.end=0
        self.words_number=0
        self.word.clear()
        self.clear_canvas()
        self.used_numbers.clear()
        self.answers.clear()
        self.start=0
        self.main_menu()

    def main_menu(self):
        self.canvas.create_text(440,200,fill="darkblue",font="Helvetica 75",
                        text="Procvičování")
        self.canvas.create_text(430,370,fill="darkblue",font="Helvetica 75",
                        text="Test")


    def generate_words(self):
        a=1
        c=1
        end=0
        if(self.practise_test==1):
            self.word.clear()
            self.words_number=0
        self.clear_canvas()
        # Otevření souboru
        with open('words.json', encoding='utf-8-sig') as f:
            data_words = json.load(f)
        i=random.randint(2,int(len(data_words)))
        # Při dokončení všech otázek u procvičování
        if (int(len(self.used_numbers))==int(len(data_words)) and self.practise_test==0):
            self.end=1
            self.start=0
        # Při dokončení 20 otázek v testu
        if (int(len(self.used_numbers))==20 and self.practise_test==1):
            self.end=1
            self.start=0
        else:
            while (1):
                # Zkontrolování vygenerovaného čísla s použitýma id 
                if i in self.used_numbers:
                    i=random.randint(1,int(len(data_words)))
                else:
                    self.used_numbers.append(i)
                    break
        for number in self.used_numbers:
            print(number)
        # Uložení nepoužitého slova
        for data in data_words:
            if(int(data['id'])==i):
                self.canvas.create_text(440,200,fill="darkblue",font="Helvetica 75",
                        text=data['english']+" ("+ str(len(data['czech'])) +")")
                self.actual_word=data['czech']
                self.actual_word_eng=data['english']
                if(self.practise_test==1):
                    self.questions_cz.append(self.actual_word)
                    self.questions.append(self.actual_word_eng)
        # Když dělá test
        if(self.practise_test==1):
            self.canvas.create_text(440,500,fill="darkblue",font="Helvetica 30",
                        text="Další")
        self.canvas.create_text(440,550,fill="darkblue",font="Helvetica 10",
                        text="Pro odeslání stiskněte enter")
        # Když projde všechny slova přesměruje uživatele  
        if(self.end==1 and self.practise_test==0):
            self.konec_procvicovani()
        # Při projetí 20 otázek při testu příjde vyhodnocení
        if(self.end==1 and self.practise_test==1):
            self.vyhodnoceni()

    def info_box(self):
        messagebox.showinfo('Message title', 'Message content')
        print("info")

    def konec_procvicovani(self):
        self.clear_canvas()
        self.canvas.create_text(440,200,fill="darkblue",font="Helvetica 75",
                        text="Konec")
        self.canvas.create_text(440,350,fill="darkblue",font="Helvetica 35",
                        text="Návrat do hlavní nabídky")

    def on_button_press(self, event):
        x=event.x
        y=event.y
        # Spuštění procvičování
        if(x<725 and x>150 and y<240 and y>150 and self.start==0 and self.end==0):
            self.questions_cz=[]
            self.questions=[]
            self.answers.clear()
            self.practise_test=0
            self.start=1
            self.clear_canvas()
            self.generate_words()
        # Spuštění testu
        if(x<550 and x>320 and y>320 and y<420 and self.start==0 and self.end==0):
            self.questions=[]
            self.questions_cz=[]
            self.answers.clear()
            self.practise_test=1
            self.start=1
            self.generate_words()
        # Vygenerovat další slovo
        if(x>390 and x<490 and y>480 and y<520 and self.start==1):
            if(self.next==1 and self.practise_test==1):
                self.practise_test=1
                self.next=0            
                self.clear_canvas()
                self.word.clear()
                self.words_number=0
            if(self.practise_test==0 and self.next==1):
                self.next=0
                self.words_number=0
                self.generate_words()
            # Testování konce stestu
            if(self.practise_test==1):
                if(len(self.questions_cz)==20):
                    self.end=1
                # Přidání odpovědi
                self.answers.append(self.word)
                self.next=0
                self.generate_words()
        # Návrat do menu
        if(x>170 and x<710 and y >320 and y <380 and self.end==1 and self.practise_test==0 or x > 160 and x < 710 and y > 185 and y < 480 and self.end==1 and self.practise_test==1):
            self.back_to_main_menu()
        if(x>170 and x<706 and y>325 and y<375  and self.start==1 and self.end==1):
            self.clear_canvas()
            self.end=0
            self.used_numbers.clear()
            self.answers.clear()
            self.main_menu()
            
    def keydown(self,event):
        event.char=event.char.lower()
        # Kontrola vložených znaků
        if(self.key_check(event.char) or event.keysym=="BackSpace"):
            # Ověření jestli může uživatel zadávat znaky
            if(self.start==1 and self.words_number < len(self.actual_word) and self.next==0 or event.keysym=="BackSpace" and self.words_number <= len(self.actual_word)):
                # Mazání znaků backspacem
                if(event.keysym=="BackSpace"):
                        if(self.words_number>0):
                            # Smazání posledního znaku
                            del self.word[int(self.words_number)-1]
                            # Vyčištění plátna a vypsání nových hodnot
                            self.words_number-=1
                            self.clear_canvas()
                            self.canvas.create_text(440,200,fill="darkblue",font="Helvetica 75",
                            text=self.actual_word_eng +" ("+ str(len(self.actual_word)) +")")
                            for q in range (1,int(self.words_number)+1):
                                self.clear_canvas()
                                self.canvas.create_text(440,200,fill="darkblue",font="Helvetica 75",
                                text=self.actual_word_eng +" ("+ str(len(self.actual_word)) +")")
                                self.canvas.create_text(440,400,fill="darkblue",font="Helvetica 50",
                                    text=self.word)
                            self.canvas.create_text(440,550,fill="darkblue",font="Helvetica 10",
                                text="Pro odeslání stiskněte enter")
                # Když zadal povolený znak, uloží se a vypíše na obrazovku
                else:
                    self.words_number+=1
                    self.word+=event.char
                    self.clear_canvas()
                    self.canvas.create_text(440,200,fill="darkblue",font="Helvetica 75",
                            text=self.actual_word_eng +" ("+ str(len(self.actual_word)) +")")
                    self.canvas.create_text(440,400,fill="darkblue",font="Helvetica 50",
                                    text=self.word)
                    self.canvas.create_text(440,550,fill="darkblue",font="Helvetica 10",
                                text="Pro odeslání stiskněte enter")
    # Kontrola znaků
    def key_check(self,char):
        # Povolené znaky
        right_chars=["ě","š","č","ř","ž","ý","á","í","é","ů","ú","ň","ď","ť"]
        for right_char in right_chars:
            if(char==right_char or char>="a"and char<="z" ):
                return True
                break
        return False

    def enter(self,event):
        # Spojení znaků
        worda=""
        if(self.start==1 and self.next==0):
            for a in self.word:
                worda+=a
            self.answers.append(worda)
            # Vygenerování nového slova a vymazání hodnot
            if(self.practise_test==1):
                self.practise_test=1
                self.next=0            
                self.words_number=0
                self.word.clear()
                self.clear_canvas()
                self.generate_words()
            # Kontrola zadaného slova jestli je správné
            if(worda!=self.actual_word and self.practise_test==0):
                print(self.word)
                self.clear_canvas()
                self.canvas.create_text(390,400,fill="red",font="Helvetica 75",
                            text=self.actual_word)
            if(worda==self.actual_word and self.practise_test==0):
                self.clear_canvas()
                self.canvas.create_text(390,400,fill="green",font="Helvetica 75",
                            text=self.actual_word)
            if(self.practise_test==0):
                    self.next=1           
                    self.words_number=0
                    self.word.clear()
                    self.canvas.create_text(440,200,fill="darkblue",font="Helvetica 75",
                            text=self.actual_word_eng)
                    self.canvas.create_text(440,500,fill="darkblue",font="Helvetica 30",
                            text="Další")
        print(self.word)

    def vyhodnoceni(self):
        self.clear_canvas()
        # Posunutí nového textu při výpisu dolů
        a=0
        # Začátek od spoda ve druhém sloupci
        c=1
        # Nový sloupec
        b=0
        true=0
        result=0
        # Kontrola správných odpovědí
        for answer in self.answers:
            if(a==10):
                c=11
                b=450
            self.canvas.create_text(240+b,60+(a-c)*40,fill="darkblue",font="Helvetica 15",
                            text=self.questions[int(a)])
            if(self.questions_cz[int(a)]==answer):
                self.canvas.create_text(100+b,60+(a-c)*40,fill="green",font="Helvetica 15",
                                text=answer)
                true+=1
            else:
                self.canvas.create_text(100+b,60+(a-c)*40,fill="red",font="Helvetica 15",
                        text=self.questions_cz[int(a)])
            a+=1
        # Výpočet úspěšnosti
        if(a==0):
            result=0
        else:
            result=int((true/a)*100) 
        if(result<80):
            self.canvas.create_text(450,500,fill="red",font="Helvetica 30",
                                        text="Úspěšnost "+str(result) + " %")
        else:
            self.canvas.create_text(450,500,fill="green",font="Helvetica 30",
                                        text="Úspěšnost "+str(result) + " %")
        with open('data.json') as f:
            data = json.load(f)
        # Vypočítaní celkové úspěšnosti
        data['pocet']=int(data['pocet'])+1
        data['uspech']=round((int(data['uspech']) * int(data['pocet']-1) + result) / (int(data['pocet'])),2)
        print(result)
        print(int(data['uspech']))
        print(int(data['pocet']))
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        self.canvas.create_text(440,450,fill="darkblue",font="Helvetica 35",
                        text="Návrat do hlavní nabídky")
        self.canvas.create_text(450,550,fill="darkblue",font="Helvetica 25",
                                        text="Celková úspěšnost "+str(data['uspech']) + " %")
        self.answers.clear()

myapp = MyApp(root)
root.mainloop()