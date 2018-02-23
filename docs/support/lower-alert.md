# (Force) Lowering an alert

Sometimes there can be an alert that won't get lowered despite the condition that it's alerting about not being true.

The steps to force such an alert to be lowered are:

```
IML-manager# chroma-config stop
IML-manager# su postgres -c "echo \"update chroma_core_alertstate set active=NULL where active=true and message='<exact message of alert you want to lower>';\" | psql chroma"
IML-manager# chroma-config start
```

The `chroma-config stop` and `chroma-config start` are optional but help ensure that all browsers see the alert lowered.  As an alternative, you can omit those two commands and just refresh the page on any browsers current viewing the manager page.
