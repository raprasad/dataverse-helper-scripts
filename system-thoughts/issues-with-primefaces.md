(reference by creator of primefaces/angular: http://www.beyondjava.net/blog/angularfaces-jsf-beyond-ajax/)

# Thoughts on Primefaces

In general, the advertised benefits of using Primefaces include:

- Hiding complexity but keeping flexibility
- Reducing development time  
- Shielding developers from having to write Javascript

However, for *highly customized user interfaces*, Primefaces may have the opposite effect.  For the Dataverse project in particular, the benefits have not been as promised.  

The remainder of this page details three ways in which Primefaces has a negative effect on the development process:

1. [Primefaces is Incompatible with Bootstrap (and other JS libraries)](#1-primefaces-is-incompatible-with-bootstrap-and-other-js-libraries)
    -  *Every dataverse page* implements a major hack to make boostrap work.
2. [Primefaces Creates Non-Standard HTML: Lengthening Development and Testing Time](#2-primefaces-creates-non-standard-html-lengthening-development-and-testing-time)
    - More difficult to customize HTML/JS/CSS
    - Cannot use standard automated testing tools
    - **More money spent on development and bug testing**
3. [No Peer Usage, Cut off from the rest of the web community](#3-no-peer-usage-cut-off-from-the-rest-of-the-web-community)
    - There are very few academic/peer users of Primefaces.  
    - This leads to less information/documentation.  e.g. sparse/outdated StackOverflow compared to other software
    - Bad Open Source: Using older/harder to use software means fewer collaborators 
    - click to enlarge: <a href="https://github.com/IQSS/dataverse-helper-scripts/blob/master/system-thoughts/primefaces-jobs.png?raw=true"><img src="https://github.com/IQSS/dataverse-helper-scripts/blob/master/system-thoughts/primefaces-jobs.png?raw=true" width="200" /></a>

The document ends with a note a on examining technology to *incrementally* explore Primefaces alternatives. 

## (1) Primefaces is Incompatible with Bootstrap (and other JS libraries)

Sequence of events on most Dataverse pages:

1. Page loads.  Custom javascript executes to bind bootstrap components.
2. User action triggers Primefaces AJAX to reload part of the page.
3. **This breaks bootstrap**
4. Custom javascript is called again to rebind bootstrap components.

Primefaces does have a "Twitter Boostrap" theme--meaning that Primefaces adds an extra layer of complexity by wrapping Bootstrap's functionality.  This extra layer means that any Bootstrap upgrades need to be "re-wrapped"/integrated into the Primefaces theme before being made available.  (We do not use this theme.)

**Bottom Line**: *Every  dataverse page* implements a major hack to make native boostrap work.


## (2) Primefaces Creates Non-Standard HTML: Lengthening Development and Testing Time

- Dataverse developer (PhD candidate) laughing in disbelief/frustration: *I'm just trying to make a checkbox!  Look at this!*

#### Primefaces auto-generates HTML that lengthens the development cycle. Specifically:
 1. Cannot Use Common Testing Tools
 2. Hard to Develop/Design Pages -- hackish css/js
 3. Difficult to write pages that pass W3C Validation (Dataverse currently does not pass)
 
### Example 1: Primefaces checkbox

Standard HTML checkbox:  

```html
<input type="checkbox" name="versionsTab" value="version1">
```

Primefaces checkbox: 

```html
<div class="ui-chkbox ui-widget">
    <div class="ui-helper-hidden-accessible">
        <input type="checkbox" name="datasetForm:tabView:versionsTable_checkbox">
    </div>
    <div class="ui-chkbox-box ui-widget ui-corner-all ui-state-default">
    <span class="ui-chkbox-icon ui-c"></span>
    </div>
</div>
```

#### Issues with the Primefaces checkbox:

1.  The ```<input type="checkbox"...>``` element itself is not visible to the user.
1.  In addition, the element is not available to standard testing tools or packages which depend on visibility and ```name``` and/or ```id``` attributes.
1.  Designers/Developers need extra work to access this item via css or javascript. For example, to apply a style or access data via jquery, considerable extra time is spent creating relative selectors that can navigate the Primefaces HTML.

#### Implications

* **Money and Bugs.**  In the course of a large project, the inability to do standard automated testing can minimally lead to tens of thousands of dollars in lost staff time.
* For example:
    - Most tools allow the recording and replaying of a series of actions.  This recording/replaying is based on the use of standard HTML elements with stable ```id``` or ```name``` tags.
    - When code changes, actions may be easily replayed to check for errors.
    - These tests bases grow to handle complex user scenarios
* The current use of PrimeFaces does not allow the use of modern testing tools without considerable custom programming.  

### Example 2: Primefaces input boxes for Metadata

Standard HTML text input tag for Dataset Title:  

```html
<input type="text" name="title" tabindex="1" value="File Test 2" placeholder="Enter title...">
```

Primefaces HTML text input tag for Dataset Title:   

```html
<input id="datasetForm:tabView:j_idt706:0:j_idt709:0:j_idt716:0:j_idt718:0:inputText" 
class="ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all form-control" 
type="text" tabindex="1" value="File Test 2" 
name="datasetForm:tabView:j_idt706:0:j_idt709:0:j_idt716:0:j_idt718:0:inputText" 
role="textbox" aria-disabled="false" aria-readonly="false" aria-multiline="false" 
placeholder="Enter title...">
```

#### Explanation 
- What is ```datasetForm:tabView:j_idt706:0:j_idt709:0:j_idt716:0:j_idt718:0:inputText```?
* Part of the reason for the unusual ```id``` and ```name``` attributes is the dynamic nature of the underlying metadata data model.
* Primefaces generates unique/incomprehensible ```id``` and ```name``` combinations for the form fields.

#### Implications
- Again, this makes custom css/js more difficult and does not allow easy use of modern testing tools.

**Bottom Line**: 
  1. Cannot use standard automated testing tools without considerable extra programming
    - Kevin and Elda had to abandon use of Sauce Labs last summer because of this
  2. More difficult to develop (and debug) HTML/JS/CSS
  3. **More money spent on development and bug testing**
  4. **Unusual constraints/stress placed on Designers and QA**

## (3) No Peer Usage, Cut off from the rest of the web community

* We do not have any academic partners developing new software using Primefaces
* Job site indeed.com only lists 147 Primefaces jobs in the country.
   * The combined total for MA, CA, and NY is 24
   * For Java Server Faces, the total for MA, CA, and NY is 200 to 400
      * Depending on whether the search is for "Java Server Faces" or "Java JSF"
   * Compared to 147 national Primefaces listings on indeed.com, there are:
      - 6,000+ for angular (started 2009)
      - 5,000+ for backbone (started 2010)
      - 2,000+ for ember (started 2011)
      - 1,700+ for knockout (started 2010)
   * Chart: ![Primefaces Job Chart](https://github.com/IQSS/dataverse-helper-scripts/blob/master/system-thoughts/primefaces-jobs.png?raw=true)
* The expertise in these "newer" frameworks is quite heavy in academia as well as industry.  (Angular was
* Developers with expertise in modern javascript frameworks are right next store: HWP project (adapting angular), HarvardX, Museums, etc

**Bottom Line**: 
  1. There are very few academic/peer users of Primefaces.  In addition, the total number of Primefaces users *appears* to be dwindling.
  1. This leads to less information/documentation.  e.g. sparse/outdated StackOverflow compared to other software
  1. **Bad Open Source**: Using older/harder to use software means fewer potential collaborators 

## Future Use of Primefaces

* To keep the Dataverse platform current, we should explore the use of alternative, well-known javascript libraries.
* **Other teams/partners are significantly more productive** simply because they take advantage of more widely-used open source tools that offer strong user communities and the ability to accomplish world class work.
* The continued use of Primefaces is detrimental to the team's ability to productively add new functionality.  




