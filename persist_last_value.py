from pydblite.pydblite import Base

from constants import persistent_store


class PersistLastValue:
    def __init__(self):
        self.persist_db = Base(persistent_store, sqlite_compat=True)
        if self.persist_db.exists():
            self.persist_db.open()
            if len(self.persist_db) < 1:
                self.persist_db.insert(sell_flag=False, buy_flag=False, high_band=0, low_band=0)
                self.persist_db.commit()
        else:
            self.persist_db.create("sell_flag", "buy_flag")
            self.persist_db.insert(sell_flag=False, buy_flag=False, high_band=0, low_band=0)
            self.persist_db.commit()

    def persist_value(self, buy_flag=False, sell_flag=False, high_band=0, low_band=0):
        record = self.persist_db[0]
        if low_band != 0:
            record['low_band'] = low_band
            self.persist_db.update(record, __id__=0)
        if high_band != 0:
            record['high_band'] = high_band
            self.persist_db.update(record, __id__=0)
        record['buy_flag'] = buy_flag
        record['sell_flag'] = sell_flag
        self.persist_db.update(record, __id__=0)
        self.persist_db.commit()

    def get_persisted_value(self):
        return self.persist_db[0]

    def reset_persist_db(self):
        self.persist_db.delete(self.persist_db)
        self.persist_db.commit()


if __name__ == "__main__":
    pv = PersistLastValue()
    #pv.reset_persist_db()
    print pv.get_persisted_value()
