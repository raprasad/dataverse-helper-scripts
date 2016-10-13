Notes for https://github.com/IQSS/dataverse/issues/2290

# File Replace

## A. Remaining API tasks

#### 1. Include ability to add a file description

- In another release: add categories, tags, and/or restrictions

---

## B. Tasks for both API and UI

#### 1. Create new notifications for Replacing or Adding files to a Dataset.

- Add enum to UserNotification.java
- Add 4 bundle properties
    - Add File - Email message
    - Add File - Web page notification
    - Replace File - Email message
    - Replace File - Web page notification

#### 2. Ingest  (API and UI)

- Make call to ingest process asynchronous

#### 3. Tests

- Use RestAssured to create tests for new API endpoints
  - See https://github.com/IQSS/dataverse/issues/3387
- The same code/scenarios will be run for the UI

---

## C. UI Tasks for Replacing a File (not viewing replacement history)

### New Backing Bean and .xhtml file for Single File Replacement

Working name for the new backing bean: ```SingleFileReplacePage.java```

### Some justification for a separate bean

In a meeting organized by @mheppler we tentatively agreed to a new .xhtml file and to use the ```EditDatafilesPage.java``` backing bean.  After looking at this in more detail, I think a new backing bean also makes sense.

The main reasons to make a separate backing bean are clarity and maintenance.  The new page will work on a single file, not a dataset version. The main differences between a proposed ```SingleFileReplacePage.java``` and the existing ```EditDatafilesPage.java```  will be:

- [ ] ```init()```  - this method will be much different between pages due to the new page working on a single file
- [ ] As soon as a single file is uploaded, the "add files" functionality via drag/drop or selection should disappear
    - e.g. The UI behavior for file upload is much different
- [ ] In the near-future we will need to add additional upload support for single prov. "metadata" files
    - See balsamiq mock-up
- [ ] Need to new methods for handleDropboxUpload and handleFileUpload
    - The current page allows these methods to be called multiple times
    - Again, the operations differs for a single file.
- [ ] No need to select multiple files.
- [ ] No need for delete functionality
- [ ] No need to use the multi-file save command or related error messages
- [ ] Don't want to a add a 3rd "mode" to the existing back bean (currently handles upload multiple files and create)


### Variables for new ```SingleFileReplacePage.java``` backing bean

note: ```*``` - ids or other identifiers of these objects will be specified in the url for the page

- [ ] ```dataset```* - selected Dataset
- [ ] ```datafile```* - selected DataFile
- [ ] ```datasetVersion``` - selected DatasetVersion
    - DRAFT if it exists, or create an "edit version"
- [ ] ```fileMetadata``` - of the DataFile to replace
- [ ] ```addReplaceFileHelper``` - instance of AddReplaceFileHelper to track the "state" of the replacement
    - Used for the replace API endpoint
    - Tracks/contains the dataset working version
    - Kicks off ingest
    - Contains status error messages
    - Phase I: Instantiated upon file upload
        - File checked along with possible error conditions
    - Phase II: Save
        - Runs commands to save this new draft and notify the user


### General Workflow for new ```SingleFileReplacePage.java``` backing bean

Basic workflow--note, the user may cancel at any time and return to the File landing page.

- User uploads a replacement file
- User may add a description and/or tags
- User may choose to restrict the file
- User either saves the result or cancels the operation
    - User brought back to File landing page with appropriate messaging
