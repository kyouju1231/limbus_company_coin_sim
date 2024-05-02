""" スキル一覧フレーム """

import csv
import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.messagebox as ms

from class_skill_data import SkillData

from font_setting import *


class DataFrame(tk.Frame):
    def __init__(self, master, filepath):
        super().__init__(master,
            padx= 10, pady= 10,
        )
        # csv読み込み
        with open(filepath, newline= "", encoding= "utf-8_sig") as cf:
            reader = csv.reader(cf)
            self.data:list[SkillData] = []
            for row in reader:
                self.data.append(SkillData(
                    base_power= row[0],
                    coin_power= row[1],
                    coin_count= row[2],
                    name= row[3])
                )

        self.make_widget()
        self.init_listbox()

    def make_widget(self):
        self.listbox = tk.Listbox(self,
            font= mainfont,
            width= 30, height= 12,
            selectmode= "single",
        )
        self.listbox.grid(row= 0, column= 0,
            columnspan= 2,
            pady= 5,
        )
        scrollbar = tk.Scrollbar(self,
            orient= tk.VERTICAL,
            command= self.listbox.yview,
        )
        self.listbox["yscrollcommand"] = scrollbar.set
        scrollbar.grid(row= 0, column= 3,
            sticky= tk.N + tk.S,
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


    # スキルデータ群とリストボックスを同期
    def init_listbox(self):
        self.listbox.delete(0,tk.END)
        for value in self.data:
            self.listbox.insert(tk.END, value.get(SkillData.NM))


    # リストボックスの選択中のスキルのスキルデータを返す
    def get_skill_data(self) -> SkillData|None:
        indexes:tuple = self.listbox.curselection()
        # インデックスを取得 -> (index,)
        if len(indexes) == 1:
            index = indexes[0]
            return self.data[index]
        else:
            # 選択中の項目が0ならNoneを返す
            return


    # リストボックスにスキルを登録
    def add_skill_data(self, skill_data:SkillData):
        if skill_data.get(SkillData.CC) < 1:
            # コイン枚数が0以下
            ms.showerror("error","コイン枚数が不正です")
            return

        skill_name = sd.askstring("登録",
            "スキル名を入力してください", initialvalue= "skill")

        if skill_name:
            skill_data.set(SkillData.NM, skill_name)
        else:
            ms.showerror("error","スキル名を入力してください")
            return self.add_skill_data(skill_data)

        text = ( "このスキルを登録しますか？\n"
                f"スキル名: {skill_data.get(SkillData.NM)}\n"
                f"基礎威力: {skill_data.get(SkillData.BP)}\n"
                f"コイン威力: {skill_data.get(SkillData.CP)}\n"
                f"コイン枚数: {skill_data.get(SkillData.CC)}\n")

        if ms.askokcancel("確認", text):
            self.data.append(skill_data)
            self.init_listbox()


    # リストボックスから選択中のスキルを削除
    def del_skill_data(self):
        # インデックスを取得 -> (index,)
        indexes:tuple = self.listbox.curselection()
        if len(indexes) == 1:
            del self.data[ indexes[0] ]
            self.init_listbox()


    # リストボックスの選択中のスキルをリネーム
    def rename_skill_data(self):
        # 選択中の項目のインデックスを取得 -> (n,)
        indexes:tuple[int] = self.listbox.curselection()

        if len(indexes) == 1:
            new_name = ""

            while new_name == "":
                new_name = sd.askstring("リネーム",
                    "スキル名を入力してください", initialvalue= "skill")

            index = indexes[0]
            self.data[index].set(SkillData.NM,new_name)

            self.init_listbox()


    # アプリを閉じる時にスキルデータ群を保存する
    def on_closing(self, path):
        with open(path, mode= "w", newline= "",encoding= "utf-8_sig") as cf:
            writer = csv.writer(cf)
            for skill_data in self.data:
                row = [ skill_data.get(SkillData.BP),
                        skill_data.get(SkillData.CP),
                        skill_data.get(SkillData.CC),
                        skill_data.get(SkillData.NM),
                        ]
                writer.writerow(row)

