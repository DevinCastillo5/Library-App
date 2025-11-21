from databases import Database

# Connection String
# DATABASE_URL = "mysql+aiomysql://username:password@host:port/databaseName"

DATABASE_URL = "mysql+aiomysql://root:@localhost:3306/librarydb"
database = Database(DATABASE_URL)
