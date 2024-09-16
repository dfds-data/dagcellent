# design
- simple
- easy to use
- easy to understand
- easy to change
- easy to maintain

# features
1. daily full load
Use it to load small tables. Performs a full load every day.

1. partitioned full load
Use it to full load a large, partitioned table. Usually, this should be ran only once, so these DAGs are not scheduled.

1. partitioned daily load
Use it to update daily large, partitioned table.


# design and limitations

```python
# BUCKET
# we always use the following s3 path:
# <bucket name>/airflow/<table name>/<? if not partition: dump.parquet>
#                                   /<partition name>/dump.parquet
# s3_bucket_cnv = Variable.get(
#    "S3_bucket_passenger", default_var="dfds-passenger-staging"
# )
#                                       /-n-> ( CreateExternalTableQuery )
# (BatchLoad) -> <Is ExtTable Exist?> -|                                    -> (ExecuteQuery)
#                                      \-y--> ( AddPartitionQuery )
```

