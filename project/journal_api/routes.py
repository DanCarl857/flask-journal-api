from apifairy import body, other_responses, response
from flask import abort

from project import ma, database
from project.models import Entry
from . import journal_api_blueprint
# -------
# Schemas
# -------
class NewEntrySchema(ma.Schema):
    """Schema defining the attributes when creating a new journal entry."""
    entry = ma.String(required=True)
    
class EntrySchema(ma.Schema):
    """Schema defining the attributes in a journal entry"""
    id = ma.Integer()
    entry = ma.String()
    
new_entry_schema = NewEntrySchema()
entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)

@journal_api_blueprint.route('/', methods=['GET'])
@response(entries_schema)
def journal():
    """Return all journal entries"""
    return Entry.query.all()


@journal_api_blueprint.route('/', methods=['POST'])
@body(new_entry_schema)
@response(entry_schema, 201)
def add_journal_entry(kwargs):
    """Add a new journal entry"""
    new_message = Entry(**kwargs)
    database.session.add(new_message)
    database.session.commit()
    return new_message

@journal_api_blueprint.route('/<int:index>', methods=['GET'])
@response(entry_schema)
@other_responses({404: 'Entry not found'})
def get_journal_entry(index):
    """Return a journal entry"""
    entry = Entry.query.filter_by(id=index).first_or_404()
    return entry

@journal_api_blueprint.route('/<int:index>', methods=['PUT'])
@body(new_entry_schema)
@response(entry_schema)
@other_responses({404: 'Entry not found'})
def update_journal_entry(data, index):
    """Return a journal entry"""
    entry = Entry.query.filter_by(id=index).first_or_404()
    entry.update(data['entry'])
    database.session.add(entry)
    database.session.commit()
    return entry

@journal_api_blueprint.route('/<int:index>', methods=['DELETE'])
@other_responses({404: 'Entry not found'})
def delete_journal_entry(index):
    """Delete a journal entry"""
    entry = Entry.query.filter_by(id=index).first_or_404()
    database.session.delete(entry)
    database.session.commit()
    return '', 204