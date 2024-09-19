""" スキル一覧フレーム """

import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.messagebox as ms

from database import Database as DB
from window_edit_skill import edit_skill_window

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
        self.update_listbox()

    def make_widget(self):
        self.search_box = tk.Entry(self,
            font= mainfont,
        )
        search_btn = tk.Button(self,
            font= mainfont,
            text= '検索',
            command= self.search,
        )

        self.listbox = tk.Listbox(self,
            font= mainfont,
            width= 30, height= 12,
            selectmode= "single",
        )

        scrollbar = tk.Scrollbar(self,
            orient= tk.VERTICAL,
            command= self.listbox.yview,
        )
        self.listbox["yscrollcommand"] = scrollbar.set

        del_btn = tk.Button(self,
            text= "削除", font= mainfont,
            width= 10,
            command= self.del_skill_data,
        )

        ren_btn = tk.Button(self,
            text= "編集", font= mainfont,
            width= 10,
            command= self.rename_skill_data,
        )

        self.search_box .grid(row= 0, column= 0, columnspan=2,)
        search_btn      .grid(row= 0, column= 2,)
        self.listbox    .grid(row= 1, column= 0, columnspan= 3, pady= 5,)
        scrollbar       .grid(row= 1, column= 4, sticky= tk.N + tk.S,)
        del_btn         .grid(row= 2, column= 0,)
        ren_btn         .grid(row= 2, column= 1,)


    def search(self):
        word = self.search_box.get()
        self.update_listbox(word)


    def update_listbox(self, search_word=''):
        """ self.listboxに表示される内容を更新してself.id_name_listと同期
            search_word:スキル名検索用文字列 """
        self.listbox.delete(0,tk.END)

        self.id_name_list = self.db.get_id_and_name(search_word)

        for id_name in self.id_name_list:
            self.listbox.insert(tk.END, id_name[1])


    def get_skill_data(self) -> tuple|None:
        """ self.listboxの選択中のスキルのデータを得る\n
            -> (ID, BP, CP, CC, NM, PR) """
        indexes:tuple = self.listbox.curselection()
        # listboxの選択中のスキルのインデックスを取得 -> (index,)
        if len(indexes) == 1:
            index = indexes[0]
            id = self.id_name_list[index][0]
            # インデックスからDBのIDを取得
            return self.db.get_skill_data(id)   # IDを指定してスキルデータを取得
        else:
            # 選択中の項目が0ならNoneを返す
            return


    def add_skill_data(self, skill_data:tuple):
        """ DBへスキルを登録、listboxを更新\n
            skill_data = (BP, CP, CC, Men)"""
        if skill_data[2] < 1:
            # コイン枚数が0以下
            if ms.askokcancel("error","コイン枚数が不正です"):
                pass
            else:
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
            self.update_listbox()


    def del_skill_data(self):
        """ リストボックスから選択中のスキルを削除 """
        indexes = self.listbox.curselection()
        # 選択中の項目のインデックスを取得 indexes = (index,)

        if len(indexes) == 1:
            id = self.id_name_list[ indexes[0] ][0]
            # self.id_name_list = [(id1,name1),(id2,name2),... ]
            self.db.delete_skill(id)
            self.update_listbox()


    def rename_skill_data(self):
        """ リストボックスの選択中のスキルをリネーム """
        indexes = self.listbox.curselection()
        # 選択中の項目のインデックスを取得 indexes = (index,)

        if len(indexes) == 1:
            index = indexes[0]
            id = self.id_name_list[index][0]
            # インデックスからDBのIDを取得

            skilldata = self.db.get_skill_data(id)
            # DBからスキルデータを取得

            edited_skilldata = edit_skill_window(skilldata)
            # スキル編集

            if edited_skilldata != skilldata:
                # 編集前後のスキル内容が違うなら
                self.db.edit_skill(edited_skilldata)
                # 編集後のスキルをDBへ登録

            self.update_listbox()


    def on_closing(self):
        """ アプリを閉じる時にスキルデータ群を保存する """
        self.db.on_closing()

