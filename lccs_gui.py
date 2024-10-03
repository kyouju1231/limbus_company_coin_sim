""" LCCS GUI ver. """

import os
import tkinter as tk
import tkinter.messagebox as ms
import coin_sim as lccs

# 文字フォントの設定
from font_setting import *

from frame_i import InputFrame
from frame_d import DataFrame


class MainFrame(tk.Frame):
    def __init__(self, master, path):
        super().__init__(master,
            padx= 20,
            pady= 20,
        )

        self.create_widget(path)


    def create_widget(self, path):
        # 入力欄
        self.input_frame = InputFrame(self)

        # 登録スキル一覧
        self.data_frame = DataFrame(self, path)

        # 演算ボタン
        btn = tk.Button(self,
            text= "演算", font= mainfont,
            width= 10,
            command= self.execute,
            )

        # 出力欄
        self.result_text = tk.Label(self,
            text= ( "初回勝率: -----%\n"
                    "最終勝率: -----%" ),
            font= mainfont,
            )

        # ウィジェットを配置
        self.data_frame.pack(side= tk.RIGHT)
        self.input_frame.pack()
        btn.pack(pady= 10)
        self.result_text.pack(pady= 10)


    def execute(self):
        """ 演算ボタンを押した時の処理 """
        ally_data = self.input_frame.get_entry_values("ally")
        enemy_data = self.input_frame.get_entry_values("enemy")

        # coin_sim で計算した結果を取得
        result1,result2 = lccs.calcutate(ally_data, enemy_data)

        if (0 <= result1 <= 1) and (0 <= result2 <= 1):
            # resultの値が正常値
            self.result_text["text"] = (
                f"初回勝率: { round(result1*100,2)}%\n"
                f"最終勝率: { round(result2*100,2)}%"
            )
            self.result_text["fg"] = "black"

        elif result1 == -1: # エラー1
            self.result_text["text"] = (
                "コイン枚数、精神力または麻痺の値が正しくありません。"
            )
            self.result_text["fg"] = "red"

        elif result1 == -2: # エラー2
            self.result_text["text"] = (
                "整数以外が入力されています。"
            )
            self.result_text["fg"] = "red"

        elif result1 == -3: # エラー3
            self.result_text["text"] = (
                "引き分け率100%"
            )
            self.result_text["fg"] = "red"

        else:
            self.result_text["text"] = (
                "不明なエラーです。開発者へご報告下さい。"
            )
            self.result_text["fg"] = "red"

        return


    def skill_read(self, ally_enemy):
        """ スキル一覧から入力欄へ入力する処理 """
        skill = self.data_frame.get_skill_data()
        # DBからスキルデータを取得
        self.input_frame.enter_entry_values(skill, ally_enemy)
        # 入力欄にスキルデータを入力


    def skill_write(self, ally_enemy):
        """ 入力欄からスキル一覧へ登録する処理 """
        skill = self.input_frame.get_entry_values(ally_enemy)
        # 入力欄からスキルデータを取得
        self.data_frame.add_skill_data(skill)
        # DBへスキルデータを登録


    def on_closing(self):
        self.data_frame.on_closing()



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Limbus Company Coin Simulator")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        path = "data.db"

        path = "D:/VScode_lesson/limbus_coin_sim/00_git/data.db"
        # デバッグ用パス

        if not os.path.exists(path):
            # data.dbが同じディレクトリに無い場合に終了する
            # sqliteでは存在しないファイルを指定すると新しく作成するのでそれ防止用
            ms.showerror("Error",f"{path}が見つかりません")
            self.destroy()
        else:
            #フレームを配置
            self.main_frame = MainFrame(self, path)
            self.main_frame.pack()


    def on_closing(self):
        """ アプリを閉じる時に実行する処理 """
        self.main_frame.on_closing()
        self.destroy()



if __name__ == "__main__":
    App().mainloop()
