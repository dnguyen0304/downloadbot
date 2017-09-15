# How to Add a Log Record Handler
- In the `Battle` class, define the new log record handler method. Remember to update the
`handler_mapping` attribute and to create tests. The key is the log record class. The value is the
name of the corresponding handler method, which **must** follow the convention
"handle_<log_record_type>_record".
