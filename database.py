
import sqlite3 as sq

class Database:
    ID = 'id'
    BP = 'base_power'
    CP = 'coin_power'
    CC = 'coin_count'
    NM = 'name'
    PR = 'prisoner'

    def __init__(self, path):
        self.conn = sq.connect(path)
        self.cur = self.conn.cursor()

        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()    # -> list[ tuple(table neme,) ]
        # tableの一覧を取得

        if  not any('skills' in table for table in tables) :
            # skillsテーブルが無ければ作成
            self.cur.execute(
                "CREATE TABLE skills("
                    "id INTEGER PRIMARY KEY,"
                    "base_power INTEGER,"
                    "coin_power INTEGER,"
                    "coin_count INTEGER,"
                    "name TEXT,"
                    "prisoner TEXT DEFAULT NULL);"
            )
            self.conn.commit()


    def get_id_and_name(self, skillname='') -> tuple[tuple]:
        """ スキルのIDとスキル名を取得\n
            -> [ (id, name), ...]
            スキル名を指定しないと全てのスキルを取得する"""
            # スキル名を入力すると検索として機能する
        search_result = self.cur.execute(
            f"SELECT id,name FROM skills WHERE name LIKE '%{skillname}%';"
        )
        return tuple(search_result)


    def get_skill_data(self, id:int) -> tuple:
        """ IDを指定してスキルデータを取得
            -> (ID, BP, CP, CC, NM, PR) """
        skill_data = self.cur.execute(
            f"SELECT * FROM skills WHERE id= {id};"
        )
        return next(skill_data) # タプルとして取り出す


    def add_skill(self, skill:tuple):
        """ スキルを登録
            skill = (BP, CP, CC, NM, PR) """
        self.cur.execute(
            "INSERT INTO "
            "skills(base_power, coin_power, coin_count, name, prisoner) "
            "VALUES(?,?,?,?,?);",skill
        )
        self.conn.commit()


    def delete_skill(self, id:int):
        """ IDを指定して削除 """
        self.cur.execute(f"DELETE FROM skills WHERE id={id};")
        # 無いIDを指定しても何も起こらない
        self.conn.commit()


    def edit_skill(self, skill:tuple):
        """ IDを指定してスキルデータを編集
            skill = (ID, BP, CP, CC, NM, PR) """
        self.cur.execute(
            "UPDATE skills SET "
                f"base_power ={skill[1]},"
                f"coin_power ={skill[2]},"
                f"coin_count ={skill[3]},"
                f"name ={skill[4]},"
                f"WHERE id ={skill[0]}"
        )
        self.conn.commit()

    # def rename_skill(self, id:int, new_name:str):
    #     """ IDを指定してリネーム """
    #     self.cur.execute(f"UPDATE skills SET name='{new_name}' WHERE id={id};")
    # self.conn.commit()


    def on_closing(self):
        self.conn.close()
