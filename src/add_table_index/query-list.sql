EXPLAIN ANALYSE SELECT ID, ADVANCEDSEARCHFIELDTYPE, ALLOWCONTROLLEDVOCABULARY, ALLOWMULTIPLES, description, DISPLAYFORMAT, DISPLAYONCREATE, DISPLAYORDER, FACETABLE, FIELDTYPE, name, REQUIRED, title, WATERMARK, METADATABLOCK_ID, PARENTDATASETFIELDTYPE_ID FROM DATASETFIELDTYPE
WHERE (PARENTDATASETFIELDTYPE_ID = null) ORDER BY DISPLAYORDER ASC;


EXPLAIN ANALYSE SELECT t1.ID, t1.NAME, t1.DATASET_ID FROM FILEMETADATA_DATAFILECATEGORY t0, DATAFILECATEGORY t1 
WHERE ((t0.fileMetadatas_ID = 21130) AND (t1.ID = t0.fileCategories_ID));


SELECT t0.ID, t0.DTYPE, t0.CREATEDATE, t0.INDEXTIME, t0.MODIFICATIONTIME, t0.PERMISSIONINDEXTIME, t0.PERMISSIONMODIFICATIONTIME, t0.PUBLICATIONDATE, t0.CREATOR_ID, t0.OWNER_ID, t0.RELEASEUSER_ID, t1.ID, t1.AUTHORITY, t1.DOISEPARATOR, t1.FILEACCESSREQUEST, t1.GLOBALIDCREATETIME, t1.IDENTIFIER, t1.PROTOCOL, t1.guestbook_id, t1.thumbnailfile_id FROM DVOBJECT t0, DATASET t1 WHERE ((t0.ID =3230) AND ((t1.ID = t0.ID) AND (t0.DTYPE = 'Dataset'));

// ------------------------------------------------------------------------------------------------------------
// Missing Index on Datasetfieldvalue
// ------------------------------------------------------------------------------------------------------------

EXPLAIN ANALYSE SELECT t0.ID, t0.DTYPE, t0.CREATEDATE, t0.INDEXTIME, t0.MODIFICATIONTIME, t0.PERMISSIONINDEXTIME, t0.PERMISSIONMODIFICATIONTIME, t0.PUBLICATIONDATE, t0.CREATOR_ID, t0.OWNER_ID, t0.RELEASEUSER_ID, t1.ID, t1.AFFILIATION, t1.ALIAS, t1.DATAVERSETYPE, t1.description, t1.DISPLAYBYTYPE, t1.FACETROOT, t1.GUESTBOOKROOT, t1.METADATABLOCKROOT, t1.NAME, t1.PERMISSIONROOT, t1.TEMPLATEROOT, t1.THEMEROOT, t1.DEFAULTCONTRIBUTORROLE_ID, t1.DEFAULTTEMPLATE_ID 
FROM DVOBJECT t0, DATAVERSE t1 
WHERE ((t0.ID = 18) AND ((t1.ID = t0.ID) AND (t0.DTYPE = 'Dataverse')))

// ------------------------------------------------------------------------------------------------------------
// Why is this even being called?  Post migration, table will eventually have 800,000+ rows
// Called about 14 times -- low priority
// ------------------------------------------------------------------------------------------------------------
EXPLAIN ANALYSE SELECT DISTINCT DTYPE FROM DVOBJECT WHERE (ID = 5)

// ------------------------------------------------------------------------------------------------------------
// Missing Index on Datasetfieldvalue
// ------------------------------------------------------------------------------------------------------------

// CREATE INDEX idx_name ON table_name (column_name);
// CREATE INDEX ds_field_value_ds_id ON DATASETFIELDVALUE (DATASETFIELD_ID);
// drop index ds_field_value_ds_id;
EXPLAIN ANALYSE SELECT ID, DISPLAYORDER, value, DATASETFIELD_ID 
FROM DATASETFIELDVALUE 
WHERE (DATASETFIELD_ID = 16) ORDER BY DISPLAYORDER ASC;

> http://localhost:8080/dataset.xhtml?id=3231

https://dataverse.harvard.edu/dataset.xhtml?persistentId=hdl:1902.1/12061&version=1.0

//-------------------------------------------------------
// Poole
//-------------------------------------------------------
// Link
http://localhost:8080/dataset.xhtml?id=10844

https://dvn-vm6.hmdc.harvard.edu:8080/dataset.xhtml?id=13412

https://dataverse.harvard.edu/dataset.xhtml?id=3231

// Get datasetversion
select * from datasetversion where dataset_id=10844;

// Pull filemetadata
select * from filemetadata where datasetversion_id = 12401;

// ------------------------------------------------------------------------------------------------------------
// file category table index (NEW)
// ------------------------------------------------------------------------------------------------------------
// 

CREATE INDEX datafile_category_to_file_metadata ON FILEMETADATA_DATAFILECATEGORY (fileMetadatas_ID);
CREATE INDEX datafile_category_to_file_categories ON FILEMETADATA_DATAFILECATEGORY (fileCategories_ID);

CREATE INDEX ingest_request_to_datafile ON INGESTREQUEST (datafile_id);

CREATE INDEX datafile_tag_to_datafile ON DATAFILETAG (datafile_id);


CREATE INDEX datatable_to_datafile ON datatable (datafile_id);

// ------------------------------------------------------------------------------------------------------------
// file tag table index (OLD)
// ------------------------------------------------------------------------------------------------------------
CREATE INDEX file_category_dataset_id ON datafilecategory (dataset_id);
DROP INDEX file_category_dataset_id;

CREATE INDEX file_tag_datafile_id ON datafiletag (datafile_id);
DROP INDEX file_tag_datafile_id;


// ------------------------------------------------------------------------------------------------------------
// 
// ------------------------------------------------------------------------------------------------------------
ELECT t0.ID, t0.DTYPE, t0.CREATEDATE, t0.INDEXTIME, t0.MODIFICATIONTIME, t0.PERMISSIONINDEXTIME, t0.PERMISSIONMODIFICATIONTIME, t0.PUBLICATIONDATE, t0.CREATOR_ID, t0.OWNER_ID, t0.RELEASEUSER_ID, t1.ID, t1.AFFILIATION, t1.ALIAS, t1.DATAVERSETYPE, t1.description, t1.DISPLAYBYTYPE, t1.FACETROOT, t1.GUESTBOOKROOT, t1.METADATABLOCKROOT, t1.NAME, t1.PERMISSIONROOT, t1.TEMPLATEROOT, t1.THEMEROOT, t1.DEFAULTCONTRIBUTORROLE_ID, t1.DEFAULTTEMPLATE_ID FROM DVOBJECT t0, DATAVERSE t1 WHERE ((t0.ID = ?) AND ((t1.ID = t0.ID) AND (t0.DTYPE = ?)))

