# How to Add a Log Record
- In the `models` package, define a Log Record class that implements the `IRecord` interface. The
module name **must** follow the convention "<log_record_type>_record". Remember to update the
package index and to create tests.
- In the `MessageParser` class, update the `record_mapping` attribute. The key is the topic, which
is usually the first value of the pipe-separated message. The value is the model. Remember to
update the module import statements.
