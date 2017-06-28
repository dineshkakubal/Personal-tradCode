from pydblite.pydblite import Base
from constants import persistent_store


class PersistLastValue:
	def __init__(self):
		self.persist_db = Base(persistent_store, sqlite_compat=True)
		if self.persist_db.exists():
			self.persist_db.open()
			if len(self.persist_db) < 1:
				self.persist_db.insert(previous_hiband=0, previous_loband=0)
				self.persist_db.commit()
		else:
			self.persist_db.create("previous_hiband", "previous_loband")
			self.persist_db.insert(previous_hiband=0, previous_loband=0)
			self.persist_db.commit()

	def persist_value(self, previous_hiband=0, previous_loband=0):
		if previous_loband != 0:
			record = self.persist_db[0]
			record['previous_lowband'] = previous_loband
			self.persist_db.update(record, __id__=0)
		if previous_hiband != 0:
			record = self.persist_db[0]
			record['previous_hiband'] = previous_hiband
			self.persist_db.update(record, __id__=0)

		self.persist_db.commit()

	def get_persisted_value(self):
		return self.persist_db[0]

	def reset_persist_db(self):
		self.persist_db.delete(self.persist_db)


if __name__ == "__main__":
	pv = PersistLastValue()
	#pv.reset_persist_db()
	print pv.get_persisted_value()