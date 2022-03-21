import sqlite3
import sys


def _seed():
    conn.execute("INSERT INTO product(prod_unit_qty, prod_retail_price, prod_total_price) VALUES "
                 "(3, 400, 1200),"
                 "(6, 100, 600), "
                 "(2, 150, 300);")
    print("Table [product] has been seeded")


def _migrate():
    conn.execute("CREATE TABLE staff "
                 "(staff_id INTEGER PRIMARY KEY, "
                 "staff_email TEXT NOT NULL UNIQUE,"
                 "staff_password  TEXT NOT NULL)"
                 )
    print("Table [staff] created successfully")

    conn.execute("CREATE TABLE product ("
                 "prod_id INTEGER PRIMARY KEY,"
                 "prod_unit_qty INTEGER,"
                 "prod_retail_price FLOAT,"
                 "prod_total_price FLOAT"
                 ")")
    print("Table [product] created successfully")

    conn.execute("CREATE TABLE 'transaction' ("
                 "cust_id INTEGER PRIMARY KEY,"
                 "cust_firstname TEXT,"
                 "cust_lastname TEXT,"
                 "trans_date DATETIME,"
                 "trans_location TEXT,"
                 "prod_id INTEGER,"
                 "FOREIGN KEY (prod_id) REFERENCES product(prod_id)"
                 ")")
    print("Table [transaction] created successfully")


def _rollback():
    conn.execute("DROP TABLE 'transaction';")
    conn.execute("DROP TABLE product;")
    conn.execute("DROP TABLE staff;")

    print("Table [transaction,product,staff] has been drop")


def _main(argv):
    if argv == 'migrate':
        _migrate()

    elif argv == 'rollback':
        _rollback()

    elif argv == 'seed':
        _seed()

    else:
        print("Undefined command")


if __name__ == "__main__":
    conn = sqlite3.connect('hmat.db')
    print("Opened database successfully")

    _main(sys.argv[1])

    conn.close()
    print("Closed database successfully")
