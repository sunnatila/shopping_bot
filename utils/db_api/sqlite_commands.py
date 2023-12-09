import sqlite3


class Database:
    def __init__(self, db_path: str = 'db.sqlite3'):
        self.db_path = db_path

    @property
    def connect(self):
        return sqlite3.connect(self.db_path)

    def select_users(self):
        cur = self.connect.cursor()
        SQL = "select * from product_user"
        res = cur.execute(SQL).fetchall()
        self.connect.close()
        return res

    def select_user(self, user_id):
        cur = self.connect.cursor()
        SQL = "select * from product_user where user_id=?"
        res = cur.execute(SQL, (user_id,)).fetchone()
        self.connect.close()
        return res

    def add_user(self, user_id, fullname, phone_number, mention, commit=True):
        con = self.connect
        cur = con.cursor()
        SQL = """
            insert into product_user(user_id, fullname, phone_number, mention)
            values
            (?, ?, ?, ?)
        """
        cur.execute(SQL, (user_id, fullname, phone_number, mention))
        if commit:
            con.commit()
        self.connect.close()
        print(f"{fullname} bazaga qo'shildi!")

    def del_user(self, user_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = "DELETE FROM product_user WHERE user_id=?"
        cur.execute(SQL, (user_id,))
        conn.commit()
        conn.close()
        print("User bazadan o'chirildi!")

    def column_names_users(self):
        cur = self.connect.cursor()
        cursor = cur.execute('select * from product_user')
        names = list(map(lambda x: x[0], cursor.description))
        self.connect.close()
        return names

    def show_tables(self):
        cur = self.connect.cursor()
        SQL = "SELECT name FROM sqlite_master"
        res = cur.execute(SQL)
        self.connect.close()
        return res.fetchall()

    def select_categories(self):
        cur = self.connect.cursor()
        SQL = "SELECT * FROM product_category"
        res = cur.execute(SQL).fetchall()
        self.connect.close()
        return res

    def select_category(self, category_id):
        cur = self.connect.cursor()
        SQL = "SELECT * FROM product_category WHERE id=?"
        res = cur.execute(SQL, (category_id, )).fetchone()
        self.connect.close()
        return res

    def column_names_category(self):
        cur = self.connect.cursor()
        cursor = cur.execute('select * from product_category')
        names = list(map(lambda x: x[0], cursor.description))
        self.connect.close()
        return names

    def select_products(self):
        cur = self.connect.cursor()
        SQL = "SELECT * FROM product_product"
        res = cur.execute(SQL).fetchall()
        self.connect.close()
        return res

    def select_category_products(self, category_id):
        cur = self.connect.cursor()
        SQL = "select * from product_product where category_id=?"
        res = cur.execute(SQL, (category_id,)).fetchall()
        self.connect.close()
        return res

    def select_product(self, product_id):
        cur = self.connect.cursor()
        SQL = "select * from product_product where id=?"
        res = cur.execute(SQL, (product_id,)).fetchone()
        self.connect.close()
        return res

    def column_names_products(self):
        cur = self.connect.cursor()
        cursor = cur.execute('select * from product_product')
        names = list(map(lambda x: x[0], cursor.description))
        self.connect.close()
        return names


# db = Database()
# print(db.show_tables()[-2:-5:-1])
# print(db.column_names_products())
# print(db.column_names_category())
# print(db.column_names_users())
