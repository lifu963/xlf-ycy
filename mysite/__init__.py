from .settings.production import DEBUG

if DEBUG==True:
  import pymysql
  pymysql.install_as_MySQLdb()
