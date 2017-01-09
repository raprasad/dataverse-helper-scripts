# Post code review checklist

- [ ] For file add/replace remove ability to add DataFile tags
  - Leave "logic" in place to use for in #3422 - changing label, description and tags of an existing file
    - For existing files, we can validate whether the file is tabular and can have a DataFile tag
- [ ] Use native JSON.
  - [ ] Add new attributes to the native JSON, exclude dataset and dataverse information
  - [ ] rework ```okResponseGsonObject``` to use the native JSON object builder.  
    - This is still a new method which take both a ```JsonObjectBuilder``` object _and_ a String ```message```
- [ ] For add file API endpoint, we now have the dataset object--pass directly to AddReplaceHelper instead of the id
- [ ] Tech debt: Update existing ```findDatasetOrDie``` method to use error messages in bundles
  - [ ] Rename existing bundle errors
  - [ ] Update ad/replace business logic use renamed bundle errors  - [ ] Update API tests to use renamed bundle errors
- [ ] Move to ```removeDuplicatesNullsEmptyStrings``` to a utility class
  - _Which one?_
- [ ] For ```OptionalFileParams```, rename **tags** to **categories** in code/methods
  - [ ] Rename business logic methods
  - [ ] Update tests
  - There's an inconsistency where the UI/user facing logic has the word **tags** but internal code uses **categories**
     - Group decision to keep **categories**
- [ ] ```AddReplaceHelper``` logic  
   - Consolidate calls to ```UpdateDatasetCommand``` in ```step_070_run_update_dataset_command``` and ```step_080_run_update_dataset_command_for_replace```

---

## Include in this ticket?

- [ ] Rename the ```ingestService.addFiles(..)``` method to ```ingestService.saveFiles(..)```
  - retest: DatasetPage UI, EditDataFiles UI, and MediaResourceManagerImpl.java

## Important Prov. note related #3238

- The add/replace API endpoints currently have a "pathway" to add additional JSON variables.  e.g. If you're adding string, numeric, boolean or other JSON based data
- However, the API endpoints will need the ability to add a second file--a prov file.
