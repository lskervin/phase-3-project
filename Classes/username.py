from __init__ import CURSOR, CONN
import random
import string

class Username:
    all = {}
    def __init__ (self, username, user_id, id=None):
        self.id = id
        self.username = username
        self.user_id = user_id
        # Username.all.append(self) #working to resolve

    def __repr__(self):
        return (
            f"<Username {self.username}, " +
            f"User ID: {self.user_id}>"
        )

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if isinstance(username, str) and len(username):
            self._username = username
        else:
            raise ValueError(
                "Username must be a non-empty string"
            )

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        from user import User
        if type(user_id) is int and User.find_by_id(user_id):
            self._user_id = user_id
        else:
            raise ValueError(
                "user_id must reference a user in the database")

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Username instances """
        sql = """
            CREATE TABLE IF NOT EXISTS usernames (
            id INTEGER PRIMARY KEY,
            username TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Username instances """
        sql = """
            DROP TABLE IF EXISTS usernames;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        from password import Password
        """ Insert a new row with the username and user_id values of the current Username object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO usernames (username, user_id)
                VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.username, self.user_id))
        CONN.commit()

        self.user_id = CURSOR.lastrowid
        type(self).all[self.id] = self
        # Generate and create a password for the user
        Password.create_table()
        password = Password.create(password =self.generate_password(), username_id=self.user_id)


    def generate_password(self):
        """Generate a password based on the user's first name and last name."""
        while True:  # Loop indefinitely until a valid password is generated
            password_length = random.randint(1, 3)
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=password_length))
            if password_length == 3:  # Check if the password length is valid
                return password  # Return the password if valid

    def update(self):
        """Update the table row corresponding to the current Username instance."""
        sql = """
            UPDATE usernames
            SET username = ?, user_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.username, self.user_id, self.id))
        CONN.commit()

    def delete(self):
        
        """Delete the table row corresponding to the current Username instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM usernames
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None
        

    @classmethod
    def create(cls, username, user_id):
        """ Initialize a new Username instance and save the object to the database """
        username = cls(username, user_id)
        username.save()
        return username

    @classmethod
    def instance_from_db(cls, row):
        """Return an Username object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        username = cls.all.get(row[0])
        if username:
            # ensure attributes match row values in case local instance was modified
            username.username = row[1]
            username.user_id = row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            username = cls(row[1], row[2])
            username.id = row[0]
            cls.all[username.id] = username
        return username
    
    @classmethod
    def get_all(cls):
        """Return a list containing one Username object per table row"""
        sql = """
            SELECT *
            FROM usernames
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, user_id):
        """Return Username object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM usernames
            WHERE user_id = ?
        """

        row = CURSOR.execute(sql, (user_id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, username):
        """Return Username object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM usernames
            WHERE username is ?
        """

        row = CURSOR.execute(sql, (username,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def user(self):
        from user import User
        """Return user associated with current username"""
        sql = """
            SELECT * FROM users
            WHERE user_id = ?
        """
        CURSOR.execute(sql, (self.user_id,),)

        rows = CURSOR.fetchall()
        return User.instance_from_db(row)
        
