# Django SQL Console

Sqlconsole is a django app that allows for the execution of sql queries from the admin section of a django site.
An appropriate use case is when you don't have access to the database especially in a production environment.

SqlConsole is really meant to be used for database read queries eg:
```
SELECT * FROM <some_table>

SELECT count(*) FROM <some_table>
```

For queries that modify data eg:
```
DELETE FROM <some_table> WHERE ID=<some_id>
```

only a success or error message will be shown

## Install

```
pip install django-sqlconsole
```

Add the app to ```INSTALLED_APPS```

```
INSTALLED_APPS = [
...
'sqlconsole'
]
```

SqlConsole will be included in the admin section with a history of executed queries.

Permissions will be required to execute queries
`sqlconsole.can_execute_query`




## Screenshot
![Example Query](screenshot/query.png)
