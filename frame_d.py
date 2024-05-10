""" スキル一覧フレーム """

import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.messagebox as ms

from database import Database as DB

from font_setting import *


class DataFrame(tk.Frame):
    """ スキル一覧を表示するためのフレーム """
    def __init__(self, master, filepath):
        super().__init__(master,
            padx= 10, pady= 10,
        )

        # DBへアクセス
        self.db = DB(filepath)


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


    def init_listbox(self):
        """ self.id_name_listとself.listboxを同期 """
        self.listbox.delete(0,tk.END)

        self.id_name_list = self.db.get_id_and_name()

        for value in self.id_name_list:
            self.listbox.insert(tk.END, value[0])


    def get_skill_data(self) -> tuple|None:
        """ self.listboxの選択中のスキルのデータを得る\n
            -> (ID, BP, CP, CC, NM, PR) """
        indexes:tuple = self.listbox.curselection()
        # listboxの選択中のスキルのインデックスを取得 -> (index,)
        if len(indexes) == 1:
            index = indexes[0]
            id = self.id_name_list[index][0]
            return self.db.get_skill_data(id)
        else:
            # 選択中の項目が0ならNoneを返す
            return


    def add_skill_data(self, skill_data:tuple):
        """ DBへスキルを登録、listboxを更新\n
            skill_data = (BP, CP, CC, Men)"""
        if skill_data[2] < 1:
            # コイン枚数が0以下
            ms.showerror("error","コイン枚数が不正です")
            return

        skill_name = sd.askstring("登録",
            "スキル名を入力してください", initialvalue= "skill")

        if not skill_name:
            ms.showerror("error","スキル名を入力してください")
            return self.add_skill_data(skill_data)

        text = ( "このスキルを登録しますか？\n"
                f"スキル名: {skill_name}\n"
                f"基礎威力: {skill_data[0]}\n"
                f"コイン威力: {skill_data[1]}\n"
                f"コイン枚数: {skill_data[2]}\n")

        if ms.askokcancel("確認", text):
            skill_data = (skill_data[0], skill_data[1], skill_data[2], skill_name, None)
            # tupleのデータを整えてDBへ渡す
            self.db.add_skill(skill_data)
            self.init_listbox()


    def del_skill_data(self):
        """ リストボックスから選択中のスキルを削除 """
        indexes = self.listbox.curselection()
        # 選択中の項目のインデックスを取得 indexes = (index,)

        if len(indexes) == 1:
            id = self.id_name_list[ indexes[0] ]
            self.db.delete_skill(id)
            self.init_listbox()


    def rename_skill_data(self):
        """ リストボックスの選択中のスキルをリネーム """
        indexes = self.listbox.curselection()
        # 選択中の項目のインデックスを取得 indexes = (index,)

        if len(indexes) == 1:
            new_name = ""

            while new_name == "":
                new_name = sd.askstring("リネーム",
                    "スキル名を入力してください", initialvalue= "skill")

            id = self.id_name_list[ indexes[0] ]
            self.db.rename_skill(id, new_name)

            self.init_listbox()


    def on_closing(self):
        """ アプリを閉じる時にスキルデータ群を保存する """
        self.db.on_closing()

