""" LCCS GUI ver. """

import tkinter as tk
import coin_sim as lccs

# 文字フォントを設定
font1 = ("Meiryo",10)
font2 = ("",7)


# entryの数値を上げ下げする関数
def increment(entry:tk.Entry):
    current_value = entry.get()
    if current_value.lstrip("-").isdigit():
        new_value = int(current_value) + 1
        entry.delete(0, tk.END)
        entry.insert(0, str(new_value))

def decrement(entry:tk.Entry):
    current_value = entry.get()
    if current_value.lstrip("-").isdigit():
        new_value = int(current_value) - 1
        entry.delete(0, tk.END)
        entry.insert(0, str(new_value))


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
                    font= font1,
                    justify= tk.CENTER,
                    bd= 2, relief= "flat",
                    )
        self.entry.pack(side=tk.LEFT)
        self.entry.insert(0,"0")

        up_btn = tk.Button(self,
                    width= 2,
                    text= "▲", font= font2,
                    bd=1, relief= "raised",
                    command= lambda: increment(self.entry),
                    repeatdelay= 100, repeatinterval= 120,
                    )
        up_btn.pack(side=tk.TOP)

        dwn_btn = tk.Button(self,
                    width= 2,
                    text= "▼", font= font2,
                    bd=1, relief= "raised",
                    command= lambda: decrement(self.entry),
                    repeatdelay= 100, repeatinterval= 120,
                    )
        dwn_btn.pack(side=tk.BOTTOM)



class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master,
            padx= 20,
            pady= 20,
        )
        self.create_widget()
        self.create_button()
        self.create_output()

    # ヘッダーと入力欄の作成
    def create_widget(self):
        row0 = []
        self.row1:list[tk.Label|tk.Frame] = []
        self.row2:list[tk.Label|tk.Frame] = []

        text1 = ("","基礎威力","コイン威力","コイン枚数","精神力")
        for text in text1:
            row0.append(tk.Label(self,
                text= text,
                font= font1,
                width= 8,
                ))

        self.row1.append(tk.Label(self, width= 8,
                text= "味方スキル", font= font1,)
                )
        self.row2.append(tk.Label(self, width= 8,
                text= "敵スキル", font= font1,)
                )
        for i in range(4):
            self.row1.append(EntryFrame(self))
            self.row2.append(EntryFrame(self))

        table = [row0, self.row1, self.row2]

        # grid()を用いて配置
        for r in range( len(table) ):
            for c in range( len( table[r] ) ):
                table[r][c].grid(row= r, column= c)


    # 演算ボタンの作成
    def create_button(self):
        btn = tk.Button(self,
            text= "演算",
            font= font1,
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
            ally_data[i]  = ally_data[i].entry.get()
            enemy_data[i] = enemy_data[i].entry.get()

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
            self.result_text["bg"] = "black"

        return "break"


    # 計算結果の出力欄を作成
    def create_output(self):
        self.result_text = tk.Label(self,
            text= ( "初回勝率: -----%\n"
                    "最終勝率: -----%" ),
            font= font1,
            )
        self.result_text.grid(row= 4, column= 0, columnspan= 5, pady= 10)



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Limbus Company Coin Simulator")
        self.geometry("550x250")

        #フレームを配置
        frame = MainFrame(self)
        frame.pack()



if __name__ == "__main__":
    App().mainloop()
