project_home = '/Users/rafaelmersant/Documents/PythonApps/cooperativa/acgm/'

from django.conf import settings

settings.configure()

from administracion.models import CategoriaPrestamo

from django.contrib.auth.models import User
from django.core.wsgi import get_wsgi_application

import sys, os
import csv, sqlite3
import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'acgm.settings'
application = get_wsgi_application()

f = open('catprest.csv', 'r')
for line in f:
	line = line.split('|')
	cp = CategoriaPrestamo()
	cp.descripcion = line[0]
	cp.tipo = line[1]
	cp.interesAnualSocio = line[2]
	cp.userLog = User.objects.get(username='coop')
	cp.save()
f.close()

# conn = sqlite3.connect("db.sqlite3")
# curs = conn.cursor()
# reader = csv.reader(open('catprest.csv', 'r'), delimiter='|')

# for row in reader:
# 	try:
# 		ncat = CategoriaPrestamo()

# 		ncat.descripcion = row[0]
# 		ncat.tipo = row[1]
# 		ncat.interesAnualSocio = row[2]
# 		ncat.save()

# 		# to_db = [unicode(row[0], 'utf8'), unicode(row[1], 'utf8'), unicode(row[2], 'utf8'), datetime.datetime.now(), 1]
# 		# curs.execute("INSERT INTO administracion_categoriaPrestamo(descripcion, tipo, interesAnualSocio, datetimeServer, userLog_id) VALUES (?, ?, ?, ?, ?);", to_db)
# 		# conn.commit()
# 	except Exception as e:
# 		print e

# conn.close()
# print 'CARGA COMPLETADA'
