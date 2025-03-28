from CaesarSQLDB.caesarcrud import CaesarCRUD
class CaesarCreateTables:
    def __init__(self) -> None:
        self.usersfields = ("email","password")

        

    def create(self,caesarcrud :CaesarCRUD):
        caesarcrud.create_table("userid",self.usersfields,
        ("varchar(255) NOT NULL","varchar(255) NOT NULL"),
        "users")
