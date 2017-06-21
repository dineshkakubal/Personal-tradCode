from pydblite.pydblite import Base
from constants import db_name


db = Base(db_name, sqlite_compat=True)

if not db.exists():
	raise Exception("Nothing to read")
db.open()

for record in db:
	print record
