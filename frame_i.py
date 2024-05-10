""" 入力欄フレーム """

import tkinter as tk

from font_setting import *


class EntryFrame(tk.Frame):
    """ エントリと横の数値を上下させるボタンをまとめたウィジェット """
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


    def increment(self, entry:tk.Entry):
        """ エントリの数値を上げる関数 """
        current_value = entry.get()
        if current_value.lstrip("-").isdigit():
            new_value = int(current_value) + 1
            entry.delete(0, tk.END)
            entry.insert(0, str(new_value))

    def decrement(self, entry:tk.Entry):
        """ エントリの数値を下げる関数 """
        current_value = entry.get()
        if current_value.lstrip("-").isdigit():
            new_value = int(current_value) - 1
            entry.delete(0, tk.END)
            entry.insert(0, str(new_value))


    def get_value(self) -> int:
        """ エントリの値を返す """
        return int(self.entry.get())


    def enter_value(self, value):
        """ エントリに値を入れる """
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


    def get_entry_values(self, ally_enemy) -> tuple:
        """ エントリの値を取得\n
            -> [BP, CP, CC, Men] """
        if ally_enemy == "ally":
            tmp_data:list[EntryFrame] = list(self.row1)
        elif ally_enemy == "enemy":
            tmp_data:list[EntryFrame] = list(self.row2)

        del tmp_data[0]     # 列見出しのラベルを削除

        data = (
            tmp_data[0].get_value(),
            tmp_data[1].get_value(),
            tmp_data[2].get_value(),
            tmp_data[3].get_value(),
        )

        return data


    def enter_entry_values(self, data:tuple, ally_enemy):
        """ エントリへ値を入力\n
            data = (ID, BP, CP, CC, NM, PR)"""
        if ally_enemy == "ally":
            for i in range(1,4):
                self.row1[i].enter_value( data[i] )
        elif ally_enemy == "enemy":
            for i in range(1,4):
                self.row2[i].enter_value( data[i] )


    def create_button(self, master):
        """ スキルリストからエントリに入出力するボタンを作成 """
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

