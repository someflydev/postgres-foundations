# Fix a search_path exploit scenario

## Scenario

A SECURITY DEFINER function owned by a powerful role calls `SELECT * FROM some_table` without schema qualification. A lower-privileged role injects a shim table earlier in search_path. Propose the fix by setting search_path on the function definition.
