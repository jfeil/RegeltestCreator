# Development

## Database migration

1. Create datatypes based on Base
2. `alembic revision --autogenerate` to generate a new revision file
3. Fix renaming (it is generated as dropping and new creating) with e.g.
   `op.alter_column(table_name='question', column_name='rule_id', new_column_name='question_id')`
4. `alembic upgrade head` to use the previously generated revision file and upgrade the existing database