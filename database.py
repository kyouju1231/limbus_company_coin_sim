
import sqlite3 as sq

class Database:
    def __init__(self, path):
        self.conn = sq.connect(path)
        self.cur = self.conn.cursor()

        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()    # -> list[ tuple(table neme,) ]

        if  any('skills' in table for table in tables) :
            # skillsテーブルが無ければ作成
            self.cur.execute(
                "CREATE TABLE skills("
                    "id INTEGER PRIMARY KEY"
                    "base_power INTEGER,"
                    "coin_power INTEGER,"
                    "coin_count INTEGER,"
                    "name TEXT,"
                    "prisoner TEXT)"
            )


    def get_name_and_id(self) -> list[tuple]:
        rows = self.cur.execute("SELECT name,id FROM skills;")
        return list(rows)


    def search_skills(self, culumn_name, search_word) -> list[tuple]:
        result = self.cur.execute(
            f"SELECT * FROM skills WHERE {culumn_name}='{search_word}';"
            )
        return list(result)


    def add_skill(self, skill:tuple):
        # skill = [id, base_power, coin_power, coin_count, name, prisoner]
        self.cur.execute("INSERT INTO skills value(?,?,?,?,?);",skill)
        self.conn.commit()


    def delete_skill(self, id:int):
        self.cur.execute(f"DELETE FROM skills WHERE id={id};")
        self.conn.commit()


    def change_skill_name(self, id:int, new_name:str):
        self.cur.execute(f"UPDATE skills SET name={new_name} WHERE id={id}")


    def on_closing(self):
        self.conn.close()
