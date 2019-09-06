import mysql.connector

lista = [
    'hbo',
	'bit',
	'pov',
	'nic',
	'sex',
	'yen',
	'app',
	'bro',
	'fmi'
]

# GUARDA EN LA BD
mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = "root",
	database = "SeRobaronUnBOT"
)

mycursor = mydb.cursor()
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS `acronimos` (`id` INT NOT NULL AUTO_INCREMENT,`acronimo` VARCHAR(4) NOT NULL,`leido` TINYINT NOT NULL DEFAULT 0,PRIMARY KEY (`id`),UNIQUE INDEX `acronimo_UNIQUE` (`acronimo` ASC))"
)
for item in lista:
    mycursor.execute("INSERT IGNORE INTO acronimos (acronimo) VALUES ('"+item+"')")

mydb.commit()
