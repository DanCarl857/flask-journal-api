from project import database

class Entry(database.Model):
    """Class that represents a journal entry."""
    __tablename__ = 'entries'
    
    id = database.Column(database.Integer, primary_key=True)
    entry = database.Column(database.String, nullable=False)
    
    def __init__(self, entry: str):
        self.entry = entry
        
    def update(self, entry: str):
        self.entry = entry
        
    def __repr__(self):
        return f'<Entry: {self.entry}>'