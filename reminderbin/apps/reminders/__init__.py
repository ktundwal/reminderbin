# needed for South compatibility
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^reminderbin\.apps\.reminders\.models\.MultiSelectField"])