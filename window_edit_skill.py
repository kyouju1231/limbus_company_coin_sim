""" Pop-up for registering a skill """

import tkinter as tk

from frame_i import EntryFrame

from font_setting import *

def edit_skill_window(skill:tuple):
    """ スキル編集ウィンドウを開く
        data = (ID, BP, CP, CC, NM, PR)
            -> (ID, BP, CP, CC, NM, PR) """
    window = tk.Toplevel()
    window.title("スキル編集")

    # 親ウィンドウを待機させる
    window.grab_set()
    window.focus_set()


    ### 入力欄を作成
    # スキル数値欄 frame0
    frame0 = tk.Frame(
        master= window,
        padx= 12,
        pady= 12,
    )

    row0:list[tk.Label]   = []
    row1:list[EntryFrame] = []

    text1 = ("基礎威力","コイン威力","コイン枚数")

    # 配置するウィジェット作成
    for text in text1:
        row0.append(
            tk.Label(
                master= frame0,
                text= text,
                font= mainfont,
                width= 8,
            )
        )
        row1.append(EntryFrame(frame0))

    table = [row0, row1]
    # ウィジェット配置
    for r in range( len(table) ):
        for c in range( len( table[r] ) ):
            table[r][c].grid(row= r, column= c)


    ### スキル名欄 frame1
    frame1 = tk.Frame(
        master= window,
        padx= 12,
        pady= 12,
    )

    neme_label = tk.Label(
        frame1,
        text="スキル名：",
        font= mainfont,
        width= 8,
    )
    neme_entry = tk.Entry(
        frame1,
        width= 30,
        font= mainfont
    )

    neme_label.pack(side=tk.LEFT)
    neme_entry.pack()


    # dataを入力欄へ展開
    row1[0].enter_value( skill[1] )     # 基礎威力
    row1[1].enter_value( skill[2] )     # コイン威力
    row1[2].enter_value( skill[3] )     # コイン枚数
    neme_entry.insert( 0, skill[4] )    # スキル名


    ### ok,cancelボタンの動作
    edited_skill = list(skill)

    def on_ok():
        # 入力値を取得する動作
        edited_skill[1] = row1[0].get_value()   # 基礎威力
        edited_skill[2] = row1[1].get_value()   # コイン威力
        edited_skill[3] = row1[2].get_value()   # コイン枚数
        edited_skill[4] = neme_entry.get()      # スキル名
        window.destroy()

    def on_cancel():
        window.destroy()


    ### OK,Cancelボタン欄 frame2
    frame2 = tk.Frame(
        master= window,
        padx= 12,
        pady= 12,
    )
    ok_btn = tk.Button(
        master= frame2,
        text= "OK",
        font= mainfont,
        width= 10,
        command= on_ok,
    )
    cancel_btn = tk.Button(
        master= frame2,
        text= "Cancel",
        font= mainfont,
        width= 10,
        command= on_cancel
    )

    ok_btn    .pack(side= tk.LEFT,padx= 10)
    cancel_btn.pack(padx= 10)



    ### frame0~2を配置
    frame0.pack()
    frame1.pack()
    frame2.pack()


    # ウィンドウを閉じるまで待機
    window.wait_window(window)

    # 編集結果を返す
    return tuple(edited_skill)


