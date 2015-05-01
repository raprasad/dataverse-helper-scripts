(notes in progress)
# Thoughts on Primefaces

## (1) Primefaces is Incompatible with Bootstrap (and other JS libraries)

Sequence on most Dataverse pages:

1. Page loads.  Custom javascript executes to bind bootstrap components.
2. User action triggers Primefaces AJAX to reload part of the page.
3. **This breaks bootstrap**
4. Custom javascript is called again to rebind bootstrap components.

**Bottom Line**: *Every page* implements a major hack to make boostrap work.


## (2) Primefaces HTML: Lengthens Development and Testing Time

- Dataverse developer last summer laughing in frustration: *I'm just trying to make a checkbox!  Look at this!*

Main Points:
 1. Cannot Use Common Testing Tools
 2. Hard to Develop/Design Pages -- start using hackish css/js
 

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
1.  The element is not available to standard testing tools or packages which depend on visibility and ```name``` and/or ```id``` attributes.
1.  Designers/Developers need extra work to access this item via css or javascript

#### Implications

* **Money and Bugs.**  In the course of a large project, the inability to do standard automated testing can minimally lead to tens of thousands of dollars in lost staff time.
* For example:
    - Most tools allow the recording and replaying of a series of actions.  This recording/replaying is based on the use of standard HTML elements with stable ```id``` or ```name``` tags.
    - When code changes, actions may be easily replayed to check for errors.
    - These tests bases grow to handle complex user scenarios
* The current use of PrimeFaces does not allow the use of modern testing tools.  

### Example 1: Primefaces input boxes for Metadata

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
* Part of the reason for the unusual ```id``` and ```name``` attributes is dynamic nature of the underlying metadata data model.
* Primefaces generates unique/incomprehensible ```id``` and ```name``` combinations for the form fields.

#### Implications
- Again, this makes styling difficult and does not allow easy use of modern testing tools.

**Bottom Line**: 
  1. Cannot use standard automated testing tools
    - Kevin and Elda had to abandon use of Sauce Labs last summer because of this
  2. More difficult to develop HTML/JS/CSS
  3. **More money spent on development and bug testing**
  4. **Unusual constraints/stress placed on Designers and QA staff**

## (3) No Peer Usage, and Little Usage in General

* We do no have any academic partners developing new software using Primefaces
* Job sites such as indeed.com only list 147 Primefaces jobs in the country.
   * The combined total for MA, CA, and NY is 24
   * Compared to 147 national Primefaces listings on indeed.com, there are:
      - 6,000+ for angular
      - 5,000+ for backbone
      - 2,000+ for ember
      - 1,700+ for knockout
* The expertise in these frameworks is quite heavy in academia as well as industry, including adaption by Harvard/MIT projects such as EdX and IQSS's HWP project

**Bottom Line**: 
  1. There are very few industry or academic users of Primefaces
  1. This leads to less information documentation.  e.g. StackOverflow
  2. It deters collaborators 
  
