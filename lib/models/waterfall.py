from models.__init__ import CURSOR, CONN
from models.country import Country

class Waterfall:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, name, location, elevation, country_id, id=None):
        self.id = id
        self.name = name
        self.location = location
        self.elevation = elevation
        self.country_id = country_id

    def __repr__(self):
        return (
                    f"Name : {self.name}\n" + 
                    f"Town : {self.location}\n" +     
                    f"Elevation : {self.elevation}"
        ) 
        

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        if isinstance(location, str) and len(location):
            self._location = location
        else:
            raise ValueError(
                "location must be a non-empty string"
            )
    @property
    def elevation(self):
        return self._elevation
    @elevation.setter
    def elevation(self, elevation):
        if isinstance(elevation, int):
            self._elevation = elevation
        else:
            raise ValueError(
                "elevation must be a number"
            )
    @property
    def country_id(self):
        return self._country_id

    @country_id.setter
    def country_id(self, country_id):
        if type(country_id) is int and Country.find_by_id(country_id):
            self._country_id = country_id
        else:
            raise ValueError(
                "country_id must reference a country in the database")

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Waterfall instances """
        sql = """
            CREATE TABLE IF NOT EXISTS waterfalls (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT,
            elevation INTEGER
        )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def add_column(cls):
        """Add column to existing table waterfall"""
        sql = """
            ALTER TABLE waterfalls ADD COLUMN country_id INTEGER;
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Waterfall instances """
        sql = """
            DROP TABLE IF EXISTS waterfalls;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, location, elevation, and country id values of the current Waterfall object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO waterfalls (name, location, elevation, country_id)
                VALUES (?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.location, self.elevation, self.country_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Waterfall instance."""
        sql = """
            UPDATE waterfalls
            SET name = ?, location = ?, elevation = ?, country_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.elevation,
                             self.country_id, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Waterfall instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM waterfalls
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, name, location, elevation, country_id):
        """ Initialize a new Employee instance and save the object to the database """
        waterfall = cls(name, location, elevation, country_id)
        waterfall.save()
        return waterfall

    @classmethod
    def instance_from_db(cls, row):
        """Return an Employee object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        waterfall = cls.all.get(row[0])
        if waterfall:
            # ensure attributes match row values in case local instance was modified
            waterfall.name = row[1]
            waterfall.location = row[2]
            waterfall.elevation = row[3]
            waterfall.country_id = row[4]
        else:
            # not in dictionary, create new instance and add to dictionary
            waterfall = cls(row[1], row[2], row[3], row[4])
            waterfall.id = row[0]
            cls.all[waterfall.id] = waterfall
        return waterfall
    @classmethod
    def get_all(cls):
        """Returns a list containing Waterfall object per row in the table"""
        sql = """
            SELECT * FROM waterfalls
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM waterfalls
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * from waterfalls
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_location(cls, location):
        sql = """
            SELECT * FROM waterfalls
            WHERE location = ?
        """
        row = CURSOR.execute(sql, (location,)).fetchone()

        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_elevation(cls, elevation):
        sql = """
            SELECT * FROM waterfalls
            WHERE elevation = ?
        """
        row = CURSOR.execute(sql, (elevation,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_country_id(cls, country_id):
        sql = """
            SELECT * FROM waterfalls
            WHERE country_id = ?
        """
        row = CURSOR.execute(sql,(country_id,)).fetchone()
        return cls.instance_from_db(row) if row else None
