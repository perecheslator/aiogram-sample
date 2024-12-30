import sqlite3 as s


def start_bot():
	print('Проверка базы данных')
	with s.connect('modules/db.db') as db:
		c = db.cursor()
		c.execute('''
			CREATE TABLE IF NOT EXISTS users (
				id INT,
				agree TEXT
			)
		''')
		c.execute('''
			CREATE TABLE IF NOT EXISTS admins (id INT)
			''')
		c.execute('''
			CREATE TABLE IF NOT EXISTS ban (
				id INT)
			''')
		c.execute('''
			CREATE TABLE IF NOT EXISTS admin_settings (
				meet TEXT,
				new_user TEXT,
				referals_system TEXT 
			
			)
			''')

def admin_add(id):
    with s.connect('modules/db.db') as db:
        c = db.cursor()
        c.execute("INSERT INTO admins(id) VALUES (?)", (id, ))
def admin_remove(id):
    with s.connect('modules/db.db') as db:
        c = db.cursor()
        c.execute("DELETE FROM admins WHERE id = ?", (id, ))
def check_repeat_admin(id):
    with s.connect('modules/db.db') as db:
        c = db.cursor()
        info = c.execute("SELECT id FROM admins WHERE id=?", (id, )).fetchone()
        return info
def ban_user_db(id):
    with s.connect('modules/db.db') as db:
        c = db.cursor()
        c.execute("INSERT INTO ban(id) VALUES (?)", (id, ))
def remove_ban_db(id):
    with s.connect('modules/db.db') as db:
        c = db.cursor()
        c.execute("DELETE FROM ban WHERE id = ?", (id, ))
def check_repeat_ban(id):
    with s.connect('modules/db.db') as db:
        c = db.cursor()
        info = c.execute("SELECT id FROM ban WHERE id=?", (id, )).fetchone()
        return info


def main(msg):
	with s.connect('modules/db.db') as db:
		c = db.cursor()

		info = c.execute('SELECT * FROM users WHERE id = ?', (msg.chat.id, )).fetchone()

		if info is None:
			c.execute('INSERT INTO users(ID) VALUES(?)', (msg.chat.id,))
		else:
			pass

		return info

def admins_in_db():
    with s.connect('modules/db.db') as db:
        c = db.cursor()
        c.execute('SELECT id FROM admins')

        rows = c.fetchall()
        column_data = [row[0] for row in rows]

        return column_data


def all():
	with s.connect('modules/db.db') as db:
		c = db.cursor()

		al = c.execute('SELECT * FROM users').fetchall()

		return al

def all_count():
	with s.connect('modules/db.db') as db:
		c = db.cursor()

		al = c.execute('SELECT COUNT(*) FROM users').fetchall()

		return al

def check_meet_admin():
	with s.connect('modules/db.db') as db:
		c = db.cursor()

		check = c.execute('SELECT * FROM admin_settings').fetchall()

		return check

def change_meet_admin():
	with s.connect('modules/db.db') as db:
		c = db.cursor()

		check = c.execute('SELECT * FROM admin_settings').fetchall()[0][0]

		if check == 'True':
			c.execute('UPDATE admin_settings SET meet = ? WHERE meet = ?', ('False', 'True'))
		if check == 'False':
			c.execute('UPDATE admin_settings SET meet = ? WHERE meet = ?', ('True', 'False'))

		return 0




def check_new_user_admin():
	with s.connect('modules/db.db') as db:
		c = db.cursor()

		check = c.execute('SELECT * FROM admin_settings').fetchall()[0][1]
		

		return check

def change_new_user_admin():
	with s.connect('modules/db.db') as db:
		c = db.cursor()

		check = c.execute('SELECT * FROM admin_settings').fetchall()[0][1]

		if check == 'True':
			c.execute('UPDATE admin_settings SET new_user = ? WHERE new_user = ?', ('False', 'True'))
		if check == 'False':
			c.execute('UPDATE admin_settings SET new_user = ? WHERE new_user = ?', ('True', 'False'))

		return 0
	
def check_referal_system_admin():
	with s.connect('modules/db.db') as db:
		c = db.cursor()

		check = c.execute('SELECT * FROM admin_settings').fetchall()[0][2]

		return check

def add_ref(id, ref, msg):
	print(ref)
	if main(msg)[1] == 'None':
		print('Записываю реферала')		


		with s.connect('modules/db.db') as db:
			c = db.cursor()
			print(id)
			c.execute('UPDATE users SET ref = ? WHERE id = ?', (ref, id))
			print('OK')
	else:
		print('else')
		pass

	return 0

def change_referal_system():
	with s.connect('modules/db.db') as db:
		c = db.cursor()

		check = c.execute('SELECT * FROM admin_settings').fetchall()[0][2]

		if check == 'True':
			c.execute('UPDATE admin_settings SET referals_system = ? WHERE referals_system = ?', ('False', 'True'))
		if check == 'False':
			c.execute('UPDATE admin_settings SET referals_system = ? WHERE referals_system = ?', ('True', 'False'))

		return 0
