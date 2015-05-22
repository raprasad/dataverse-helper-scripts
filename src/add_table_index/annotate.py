from msg_util import *

xindex_list = """Object|Cols to Index
FileMetadata|datafile_id,datasetversion_id
DatasetVersion|dataset_id
Dataset|guestbook_id,thumbnailfile_id
DataFileCategory|dataset_id
DataFileTag|datafile_id
DataverseTheme|dataverse_id
DataTable|datafile_id
DataVariable|datatable_id
IngestReport|datafile_id
IngestRequest|datafile_id
VariableCategory|datavariable_id
VariableRange|datavariable_id
VariableRangeItem|datavariable_id
UserNotification|user_id
SummaryStatistic|datavariable_id
#MetadataBlock|dataverse_id
#ControlledVocabularyValue|datasetfieldtype_id""".split('\n')


index_list = """Object|Cols to Index
ActionLogRecord|useridentifier,actiontype,starttime
AuthenticationProviderRow|enabled
ControlledVocabAlternate|controlledvocabularyvalue_id,datasetfieldtype_id
ControlledVocabularyValue|datasetfieldtype_id,displayorder
CustomFieldMap|sourcedatasetfield,sourcetemplate
DatasetFieldDefaultValue|datasetfield_id,defaultvalueset_id,parentdatasetfielddefaultvalue_id,displayorder
DatasetLock|user_id,dataset_id
DatasetVersionUser|authenticateduser_id,datasetversion_id
Dataverse|fk_dataverse_id,defaultcontributorrole_id,defaulttemplate_id,alias,affiliation,dataversetype,facetroot,guestbookroot,metadatablockroot,templateroot,permissionroot,themeroot
DvObject|dtype,owner_id,creator_id,releaseuser_id
DataverseContact|dataverse_id,contactemail,displayorder
DataverseFacet|dataverse_id,datasetfieldtype_id,displayorder
DataverseFeaturedDataverse|dataverse_id,featureddataverse_id,displayorder
DataverseFieldTypeInputLevel|dataverse_id,datasetfieldtype_id,required
DataverseRole|owner_id,name,alias
ExplicitGroup|owner_id,groupalias,groupaliasinowner
DataFile|ingeststatus,md5,contenttype,restricted
BuiltInUser|lastName
HarvestingDataverseConfig|dataverse_id,harvesttype,harveststyle,harvestingurl
PersistedGlobalGroup|persistedgroupalias,dtype
RoleAssignment|assigneeidentifier,definitionpoint_id,role_id
ForeignMetadataFieldMapping|foreignmetadataformatmapping_id,foreignfieldxpath,parentfieldmapping_id
""".split('\n')


#@JoinTable(indexes = {@Index(columnList="filecategories_id"),@Index(columnList="filemetadatas_id")})

ALL_CREATE_STMTS = []
def show_annotate(**kwargs):
    global index_list
    
    show_annotate = kwargs.get('show_annotate', False)
    show_annotate_with_indent = kwargs.get('with_indent', True)
    show_direct_sql = kwargs.get('show_direct_sql', False)
    show_drop_sql = kwargs.get('show_drop_sql', False)
    show_drop_table = kwargs.get('show_drop_table', False)
    show_git_commands = kwargs.get('show_git_commands', False)
    
    index_list = [x.strip() for x in index_list if len(x.strip()) > 0 and not x[0] == '#']
    print index_list
    for cnt, line in enumerate(index_list, 0):
        if cnt == 0: continue
        msgt('(%s) %s' % (cnt, line))
        
        obj_name, attrs = line.split('|')
        print obj_name, attrs
        col_names = attrs.split(',')
        col_names = [ c.strip() for c in col_names ]
    
        tbl_name = obj_name.lower()
        
        # Create annotation
        if show_annotate:
            msgd('> annotate')
            idx_list = [ '@Index(columnList="%s")' % x for x in col_names]
            if show_annotate_with_indent:
                join_delim = '\n\t\t, '            
            else:
                join_delim = ', '
            
            print '@Table(indexes = {%s})' % (join_delim.join(idx_list))
    
        # Create direct index line
        # example index name: index_datasetfieldvalue_datasetfield_id
        #
        if show_direct_sql:
            msgd('> create sql')                
            
            ALL_CREATE_STMTS.append('/* %s' % ('-' * 40 ))
            if len(col_names) == 1:                    
                ALL_CREATE_STMTS.append('    %s index (%s.java)' % (tbl_name, obj_name))
            else:
                ALL_CREATE_STMTS.append('   %s indices (%s.java)' % (tbl_name, obj_name))
            ALL_CREATE_STMTS.append('*/ %s' % ('-' * 40 ))
            
            for c in col_names:
                index_name = 'index_%s_%s' % (tbl_name, c.lower())
                create_stmt = 'CREATE INDEX %s ON %s (%s);'\
                        % (index_name, tbl_name, c.lower())
                ALL_CREATE_STMTS.append(create_stmt)
                print create_stmt
        if show_drop_sql:
            msgd('> drop index sql')            
            
            for c in col_names:
                index_name = 'index_%s_%s' % (tbl_name, c.lower())
                print 'DROP INDEX %s;' % (index_name)

        if show_drop_table:
            msgd('> drop table sql')                        
            print 'DROP TABLE %s CASCADE;' % tbl_name
        
            print "SELECT * FROM pg_indexes WHERE tablename = '%s';" % tbl_name
            
        if show_git_commands:
            msgd('> git commands')                                    
            print 'git add */%s.java' % obj_name
            print 'git commit -m "#1880, Add index for %s.java"' % obj_name
            print 'git pull origin 4.0.1'
# @JoinTable(indexes = {@Index(columnList="filecategories_id"),@Index(columnList="filemetadatas_id")})
            
                        
if __name__=='__main__':
    show_annotate(show_annotate=True,
                show_direct_sql=True, 
                show_drop_sql=False, 
                show_drop_table=True,
                show_git_commands=True)
                
#print '\n'.join(ALL_CREATE_STMTS)