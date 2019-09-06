import mysql.connector

lista = [
    'pbi',
    'bot',
    'usb',
    'acv',
    'fbi',
    'gta',
    'cti',
    'hiv',
    'nba',
    'cr7',
    'atr',
    'pes',
    'cfk',
    'wos',
    'lpm',
    'teg',
    'ypf',
    'msn',
    'fit',
    'sol',
    'ajo',
    'kgb',
    'ipc',
    'dni',
    'iva',
    'rae',
    'afa',
    'rip',
    'pdf',
    'cpu',
    'ssd',
    'cbu',
    'pin',
    'man',
    'abs',
    'b2b',
    'dvd',
    'gif',
    'led',
    'lcd',
    'jpg',
    'sql',
    'ufo',
    'vga',
    'vip',
    'xml',
    'ftp',
    'rey',
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
    "CREATE TABLE IF NOT EXISTS `acronimos` (`id` INT NOT NULL AUTO_INCREMENT,`acronimo` VARCHAR(4) NOT NULL,`leido` TINYINT NOT NULL DEFAULT 0,PRIMARY KEY (`id`),UNIQUE INDEX `acronimo_UNIQUE` (`acronimo` ASC) VISIBLE)"
)
for item in lista:
    mycursor.execute("INSERT IGNORE INTO acronimos (acronimo) VALUES ('"+item+"')")

mydb.commit()