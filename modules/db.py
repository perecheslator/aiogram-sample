import sqlite3 as s

def main(msg):
	with s.connect('modules/db.db') as db:
		c = db.cursor()

		info = c.execute('SELECT * FROM users WHERE id = ?', (msg.chat.id, )).fetchone()

		if info is None:
			c.execute('INSERT INTO users(ID) VALUES(?)', (msg.chat.id,))
		else:
			pass

		return info

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