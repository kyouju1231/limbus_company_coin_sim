
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
                    "prisoner TEXT);"
            )
            self.conn.commit()


    def get_id_and_name(self) -> list[tuple]:
        """ 全てのIDとスキル名の情報を取得
            -> [ (id1, name1), (id2, name2), ...]"""
        rows = self.cur.execute("SELECT id,name FROM skills;")
        return list(rows)


    def get_skill_data(self, id:int) -> tuple:
        """ IDを指定してスキルデータを取得
            -> (ID, BP, CP, CC, NM, PR) """
        skill_data = self.cur.execute(
            f"SELECT * FROM skills WHERE id= {id};"
        )
        return skill_data


    def search_skills(self, culumn_name, search_word) -> list[tuple]:
        search_result = self.cur.execute(
            f"SELECT * FROM skills WHERE {culumn_name}='{search_word}';"
        )
        return list(search_result)


    def add_skill(self, skill:tuple):
        """ skill = (BP, CP, CC, NM, PR) """
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


    def rename_skill(self, id:int, new_name:str):
        """ IDを指定してリネーム """
        self.cur.execute(f"UPDATE skills SET name='{new_name}' WHERE id={id};")
        self.conn.commit()


    def on_closing(self):
        self.conn.close()
