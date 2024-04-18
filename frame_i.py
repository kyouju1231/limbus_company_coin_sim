""" 入力欄フレーム """

import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.messagebox as ms

from font_setting import *


# 入力欄と横のボタンをフレームにまとめる
class EntryFrame(tk.Frame):
    def __init__(self,master):
        super().__init__(master,
                    background= "white",
                    bd= 2, relief= "groove",
                    )
        self.create_widget()

    def create_widget(self):
        self.entry = tk.Entry(self,
                    width= 10,
                    font= mainfont,
                    justify= tk.CENTER,
                    bd= 2, relief= "flat",
                    )
        self.entry.pack(side=tk.LEFT)
        self.entry.insert(0,"0")

        up_btn = tk.Button(self,
                    width= 2,
                    text= "▲", font= buttonfont,
                    bd=1, relief= "raised",
                    command= lambda: self.increment(self.entry),
                    repeatdelay= 100, repeatinterval= 120,
                    )
        up_btn.pack(side=tk.TOP)

        dwn_btn = tk.Button(self,
                    width= 2,
                    text= "▼", font= buttonfont,
                    bd=1, relief= "raised",
                    command= lambda: self.decrement(self.entry),
                    repeatdelay= 100, repeatinterval= 120,
                    )
        dwn_btn.pack(side=tk.BOTTOM)


    # entryの数値を上げ下げする関数
    def increment(self, entry:tk.Entry):
        current_value = entry.get()
        if current_value.lstrip("-").isdigit():
            new_value = int(current_value) + 1
            entry.delete(0, tk.END)
            entry.insert(0, str(new_value))

    def decrement(self, entry:tk.Entry):
        current_value = entry.get()
        if current_value.lstrip("-").isdigit():
            new_value = int(current_value) - 1
            entry.delete(0, tk.END)
            entry.insert(0, str(new_value))


    # エントリの値を返す
    def get_value(self):
        return self.entry.get()


    # エントリに値を入れる
    def enter_value(self, value:str):
        self.entry.delete(0,tk.END)
        self.entry.insert(0,value)



class InputFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master,
            padx= 20,
            pady= 20,
        )
        self.create_widget()
        self.create_button(master)


    def create_widget(self):
        # ヘッダーと入力欄の作成
        row0 = []
        self.row1:list[tk.Label|EntryFrame] = []
        self.row2:list[tk.Label|EntryFrame] = []

        # ヘッダー行
        text1 = ("","基礎威力","コイン威力","コイン枚数","精神力")
        for text in text1:
            row0.append(tk.Label(self,
                text= text,
                font= mainfont,
                width= 8,
                ))

        # 2,3行目
        self.row1.append(tk.Label(self, width= 8,
                text= "味方スキル", font= mainfont,)
                )
        self.row2.append(tk.Label(self, width= 8,
                text= "敵スキル", font= mainfont,)
                )
        for i in range(4):
            self.row1.append(EntryFrame(self))
            self.row2.append(EntryFrame(self))

        # 3行をまとめる
        table = [row0, self.row1, self.row2]

        # grid()を用いて配置
        for r in range( len(table) ):
            for c in range( len( table[r] ) ):
                table[r][c].grid(row= r, column= c)


    # エントリの値を取得
    def get_entry_values(self, ally_enemy) -> list[str]:
        if ally_enemy == "ally":
            data:list[EntryFrame] = list(self.row1)
        elif ally_enemy == "enemy":
            data:list[EntryFrame] = list(self.row2)

        del data[0]     # 列見出しのラベルを削除

        for i in range( len(data) ):
            data[i] = data[i].get_value()

        return data


    # エントリへ値を入力
    def enter_entry_values(self, data:list, ally_enemy):
        # data = [name, base_power, coin_power, coin_count]
        if len(data) == 4:
            if ally_enemy == "ally":
                for i in range(1,4):
                    self.row1[i].enter_value( data[i] )
            elif ally_enemy == "enemy":
                for i in range(1,4):
                    self.row2[i].enter_value( data[i] )

    # スキルリストからエントリに入出力するボタンを作成
    def create_button(self, master):
        # master :MainFrame
        ally_read_btn = tk.Button(self,
            text= "←", font= boldfont,
            command= lambda: master.skill_read("ally"),
        )

        enemy_read_btn = tk.Button(self,
            text= "←", font= boldfont,
            command= lambda: master.skill_read("enemy"),
        )

        ally_write_btn = tk.Button(self,
            text= "→", font= boldfont,
            command= lambda: master.skill_write("ally"),
        )

        enemy_write_btn = tk.Button(self,
            text= "→", font= boldfont,
            command= lambda: master.skill_write("enemy"),
        )

        ally_read_btn  .grid(row= 1, column= 5, padx= 5,)
        enemy_read_btn .grid(row= 2, column= 5, padx= 5,)
        ally_write_btn .grid(row= 1, column= 6, padx= 5,)
        enemy_write_btn.grid(row= 2, column= 6, padx= 5,)

