""" LCCS GUI ver. """

import csv
import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.messagebox as ms
import coin_sim as lccs

# 文字フォントを設定
mainfont = ("Meiryo",10)
boldfont = ("Meiryo",10,"bold")
buttonfont = ("",7)



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



class DataFrame(tk.Frame):
    def __init__(self, master, filepath):
        super().__init__(master,
            padx= 10, pady= 10,
        )
        # csv読み込み
        with open(filepath, newline= "", encoding= "utf-8_sig") as cf:
            reader = csv.reader(cf)
            # リストボックスに追加する初期値
            self.data = list(reader)

        self.make_widget()
        self.init_listbox(self.data)


    def make_widget(self):
        self.listbox = tk.Listbox(self,
            font= mainfont,
            width= 30, height= 12,
            selectmode= "single",
        )
        self.listbox.grid(row= 0, column= 0,
            columnspan= 2,
        )
        scrollbar = tk.Scrollbar(self,
            orient= tk.VERTICAL,
            command= self.listbox.yview,
        )
        self.listbox["yscrollcommand"] = scrollbar.set
        scrollbar.grid(row= 0, column= 3,
        )

        del_btn = tk.Button(self,
        text= "削除", font= mainfont,
        width= 10,
        command= self.del_skill_data,
        )
        del_btn.grid(row= 1, column= 0
        )

        ren_btn = tk.Button(self,
        text= "リネーム", font= mainfont,
        width= 10,
        command= self.rename_skill_data,
        )
        ren_btn.grid(row= 1, column= 1
        )


    # データをリストボックスに反映
    def init_listbox(self, data:list[list[str]]):
        self.listbox.delete(0,tk.END)
        for value in data:
            self.listbox.insert(tk.END, value[0])

    # リストボックスの選択中の項目のスキルデータを返す
    def get_skill_data(self) -> list[str]|None:
        # インデックスを取得 -> (n,)
        indexes:tuple = self.listbox.curselection()
        if len(indexes) == 1:
            # 要素数が1の場合のみデータを返す
            return self.data[indexes[0]]
        else:
            # 要素数0ならNoneを返す
            return

    # リストボックスにスキルを登録
    def add_skill_data(self, skill_data:list):
        text = ( "このスキルを登録しますか？\n"
                f"スキル名: {skill_data[0]}\n"
                f"基礎威力: {skill_data[1]}\n"
                f"コイン威力: {skill_data[2]}\n"
                f"コイン枚数: {skill_data[3]}\n")

        if ms.askokcancel("確認", text):
            self.data.append(skill_data)
            self.init_listbox(self.data)

    def del_skill_data(self):
        # インデックスを取得 -> (n,)
        indexes:tuple = self.listbox.curselection()
        if len(indexes) == 1:
            del self.data[ indexes[0] ]
            self.init_listbox(self.data)

    def rename_skill_data(self):
        # インデックスを取得 -> (n,)
        indexes:tuple = self.listbox.curselection()
        if len(indexes) == 1:
            new_name = ""
            while new_name == "":
                new_name = sd.askstring("リネーム",
                    "スキル名を入力してください", initialvalue= "skill")

            index = indexes[0]
            self.data[index][0] = new_name

            self.init_listbox(self.data)



class MainFrame(tk.Frame):
    def __init__(self, master, csvpath):
        super().__init__(master,
            padx= 20,
            pady= 20,
        )
        self.create_widget()
        self.create_button()
        self.create_output()
        self.create_skill_list(csvpath)

    # ヘッダーと入力欄の作成
    def create_widget(self):
        row0 = []
        self.row1:list[tk.Label|EntryFrame] = []
        self.row2:list[tk.Label|EntryFrame] = []

        text1 = ("","基礎威力","コイン威力","コイン枚数","精神力")
        for text in text1:
            row0.append(tk.Label(self,
                text= text,
                font= mainfont,
                width= 8,
                ))

        self.row1.append(tk.Label(self, width= 8,
                text= "味方スキル", font= mainfont,)
                )
        self.row2.append(tk.Label(self, width= 8,
                text= "敵スキル", font= mainfont,)
                )
        for i in range(4):
            self.row1.append(EntryFrame(self))
            self.row2.append(EntryFrame(self))

        table = [row0, self.row1, self.row2]

        # grid()を用いて配置
        for r in range( len(table) ):
            for c in range( len( table[r] ) ):
                table[r][c].grid(row= r, column= c)


    # スキルリストとエントリに入出力するボタン
    def create_skill_list(self, csvpath):
        self.lb = DataFrame(self,csvpath)
        self.lb.grid(row=0, column= 7,
            rowspan= 5,
        )

        a_read_btn = tk.Button(self,
            text= "←", font= boldfont,
            command= lambda: self.skill_read("ally"),
        )
        a_read_btn.grid(row= 1, column= 5, padx=5,)

        e_read_btn = tk.Button(self,
            text= "←", font= boldfont,
            command= lambda: self.skill_read("enemy"),
        )
        e_read_btn.grid(row= 2, column= 5, padx= 5,)

        a_write_btn = tk.Button(self,
            text= "→", font= boldfont,
            command= lambda: self.skill_write("ally"),
        )
        a_write_btn.grid(row= 1, column= 6, padx= 5,)

        a_write_btn = tk.Button(self,
            text= "→", font= boldfont,
            command= lambda: self.skill_write("enemy"),
        )
        a_write_btn.grid(row= 2, column= 6, padx= 5,)

    def skill_read(self, ally_or_enemy:str):
        skill_data = self.lb.get_skill_data()
        if  skill_data :    # 何かしらの値が入っていればエントリへ入力

            if ally_or_enemy == "ally":
                # 味方スキルへ入力
                for i in range(1,4):
                    self.row1[i].enter_value(skill_data[i])

            elif ally_or_enemy == "enemy":
                # 敵スキルへ入力
                for i in range(1,4):
                    self.row2[i].enter_value(skill_data[i])

    def skill_write(self, ally_or_enemy:str):
        skill_data = ["",]
        # 現在のエントリの値を取得してリストに格納
        for i in range(1,4):
            if ally_or_enemy == "ally":
                skill_data.append( self.row1[i].get_value() )
            if ally_or_enemy == "enemy":
                skill_data.append( self.row2[i].get_value() )
            # skill_data = [名前, 基礎威力, コイン威力, コイン枚数]

        if int(skill_data[3]) < 1:
            # コイン枚数が0以下
            ms.showerror("error","コイン枚数が不正です")
        else:
            skill_data[0] = sd.askstring("登録",
                "スキル名を入力してください",initialvalue= "skill")

            if skill_data[0]:
                self.lb.add_skill_data(skill_data)
            else:
                # スキル名が空欄
                ms.showerror("error","スキル名を入力して下さい")


    # 演算ボタンの作成
    def create_button(self):
        btn = tk.Button(self,
            text= "演算", font= mainfont,
            width= 10,
            command= self.execute
            )
        btn.grid(row= 3, column= 0, columnspan= 5, pady= 10)

    # 演算ボタンを押した時の処理
    def execute(self):
        ally_data:list[EntryFrame]  = list(self.row1)
        enemy_data:list[EntryFrame] = list(self.row2)

        del ally_data[0]    # 列見出しを削除
        del enemy_data[0]

        for i in range( len(ally_data) ):
            ally_data[i]  = ally_data[i].get_value()
            enemy_data[i] = enemy_data[i].get_value()

        # coin_sim で計算した結果を取得
        result1,result2 = lccs.calcutate(ally_data, enemy_data)

        if (0 <= result1 <= 1) and (0 <= result2 <= 1):
            # resultの値が正常値
            self.result_text["text"] = (
                f"初回勝率: { round(result1*100,2)}%\n"
                f"最終勝率: { round(result2*100,2)}%" )
            self.result_text["fg"] = "black"

        elif result1 == -1: # エラー1
            self.result_text["text"] = (
                "コイン枚数または精神力の値が正しくありません。")
            self.result_text["fg"] = "red"

        elif result1 == -2: # エラー2
            self.result_text["text"] = (
                "整数以外が入力されています。")
            self.result_text["fg"] = "red"

        else:
            self.result_text["text"] = (
                "不明なエラーです。開発者へご報告下さい。")
            self.result_text["fg"] = "red"

        return "break"


    # 計算結果の出力欄を作成
    def create_output(self):
        self.result_text = tk.Label(self,
            text= ( "初回勝率: -----%\n"
                    "最終勝率: -----%" ),
            font= mainfont,
            )
        self.result_text.grid(row= 4, column= 0, columnspan= 5, pady= 10)



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Limbus Company Coin Simulator")
        # self.geometry("550x250")
        self.protocol("WM_DELETE_WINDOW",lambda: self.on_closing(csvpath))

        csvpath = "D:/VScode_lesson/limbus_coin_sim/00_git/data.csv"

        #フレームを配置
        self.frame1 = MainFrame(self, csvpath)
        self.frame1.pack(side= tk.LEFT)

    def on_closing(self, path):
        with open(path, mode= "w", newline= "",encoding= "utf-8_sig") as cf:
            writer = csv.writer(cf)
            writer.writerows(self.frame1.lb.data)

        self.destroy()



if __name__ == "__main__":
    App().mainloop()
