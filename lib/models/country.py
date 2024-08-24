from models.__init__ import CONN, CURSOR

class Country:

    all = {}

    def __init__(self, name, id = None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f' {self.name}'

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self._name = name

    @classmethod
    def create_table(cls):
        """Create new table to persist attributes of Country instance"""
        sql = """
            CREATE TABLE IF NOT EXISTS countries(
            id INTEGER PRIMARY KEY,
            name TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        """Drop table that persists Country instance"""
        sql = """
            DROP TABLE IF EXISTS countries;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name 
        value of the current Country object. Update object id attribute 
        using the primary key value of new row. Save the object in 
        local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO countries (name) 
            VALUES(?)
        """
        CURSOR.execute(sql, (self.name,))

        self.id = CURSOR.lastrowid

        Country.all[self.id] = self
    
    def update(self):
        """Update table row corresponding to current Country instance"""
        sql = """
            UPDATE countries
            SET name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    def delete(self):
        """Delete table row correspoding to Country instance"""
        sql = """
            DELETE FROM countries
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]

    @classmethod
    def create(cls, name):
        country = cls(name)
        country.save()
        return country
    @classmethod
    def instance_from_db(cls, row):
        country = cls.all.get(row[0])
        if country:
            country.name = row[1]
        else:
            country = cls(row[1])
            country.id = row[0]
            cls.all[country.id] = country
        return country
    
    @classmethod
    def get_all(cls):
        "Return a list containing Country Object per row on the table"
        sql = """
            SELECT * FROM countries
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM countries
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()

        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM countries
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()

        return cls.instance_from_db(row) if row else None
    
    def waterfalls(self):
        """Returns a list of waterfalls associated to countries"""
        from models.waterfall import Waterfall
        sql = """
            SELECT * FROM waterfalls
            WHERE country_id = ?
        """
        CURSOR.execute(sql,(self.id,),)
        
        rows = CURSOR.fetchall()

        return [Waterfall.instance_from_db(row) for row in rows]
    
    
    
    