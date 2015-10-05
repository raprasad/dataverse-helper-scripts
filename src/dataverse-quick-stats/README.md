#### Quick DB Stats


### DvObject additions

```sql
Select id, owner_id, dtype, createdate, modificationtime, publicationdate from dvobject;
```
- all dvobjects by month
```sql
select date_trunc('month', createdate) as cdate, count(id) from dvobject group by cdate ORDER BY cdate;
```


#### Dataverses

- dataverses by day
```sql
select date_trunc('day', createdate) as cdate, count(id) from dvobject where dtype='Dataverse' group by cdate ORDER BY cdate;
```

- dataverses by month
```sql
select date_trunc('month', createdate) as cdate, count(id) from dvobject where dtype='Dataverse' group by cdate ORDER BY cdate;
```

#### Datasets

- Datasets by day
```sql
select date_trunc('day', createdate) as cdate, count(id) from dvobject where dtype='Dataset' group by cdate ORDER BY cdate;
```

- Dataverses by month
```sql
select date_trunc('month', createdate) as cdate, count(id) from dvobject where dtype='Dataset' group by cdate ORDER BY cdate;
```

#### Files

- Files by day
```sql
select date_trunc('day', createdate)  as cdate, count(id) from dvobject where dtype='DataFile' group by cdate ORDER BY cdate;
```

- Files by month
```sql
select date_trunc('month', createdate) as cdate, count(id) from dvobject where dtype='DataFile' group by cdate ORDER BY cdate;
```



Copy (Select id, owner_id, dtype, createdate, modificationtime, publicationdate from dvobject) To '~/2015-0819-dvobject-info.csv' With CSV;


psql -h (host) -U (user) -p (port) (dbname) -F $'\t' --no-align --pset footer -c "Select id, dataset_id, createtime, releasetime, versionstate, versionnumber from datasetversion;" > /tmp/2015-0819-dvobject-info.csv


### Dataset Version

```sql
Select id, dataset_id, createtime, releasetime, versionstate, versionnumber from datasetversion;
```

```
select date_trunc('month', createtime) as cdate, count(id) from datasetversion group by cdate ORDER BY cdate;
```

Copy (Select id, dataset_id, createtime, releasetime, versionstate, versionnumber from datasetversion) To '~/2015-0819-ds-version-info.csv' With CSV;

psql -h (host) -U (user) -p (port) (dbname)  -F $'\t' --no-align --pset footer -c "Select id, dataset_id, createtime, releasetime, versionstate, versionnumber from datasetversion;" > /tmp/2015-0819-ds-version-info.csv




### Users

No info....
