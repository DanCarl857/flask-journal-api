from apifairy import body, other_responses, response
from flask import abort

from project import ma
from . import journal_api_blueprint

# --------
# Database
# --------

messages = [
    dict(id=1, entry='The sun was shining when I woke up this morning.'),
    dict(id=2, entry='I tried a new fruit mixture in my oatmeal for breakfast.'),
    dict(id=3, entry='Today I ate a great sandwich for lunch.')
]

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
    return messages


@journal_api_blueprint.route('/', methods=['POST'])
@body(new_entry_schema)
@response(entry_schema, 201)
def add_journal_entry(kwargs):
    """Add a new journal entry"""
    new_message = dict(**kwargs, id=messages[-1]['id']+1)
    messages.append(new_message)
    return new_message

@journal_api_blueprint.route('/<int:index>', methods=['GET'])
@response(entry_schema)
@other_responses({404: 'Entry not found'})
def get_journal_entry(index):
    """Return a journal entry"""
    if index >= len(messages):
        abort(404)
        
    return messages[index]

@journal_api_blueprint.route('/<int:index>', methods=['PUT'])
@body(new_entry_schema)
@response(entry_schema)
@other_responses({404: 'Entry not found'})
def update_journal_entry(data, index):
    """Return a journal entry"""
    if index >= len(messages):
        abort(404)
        
    messages[index] = dict(data, id=index+1)
    return messages[index]

@journal_api_blueprint.route('/<int:index>', methods=['DELETE'])
@other_responses({404: 'Entry not found'})
def delete_journal_entry(index):
    """Delete a journal entry"""
    if index >= len(messages):
        abort(404)

    messages.pop(index)
    return '', 204