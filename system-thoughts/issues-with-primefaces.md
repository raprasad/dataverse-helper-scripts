(in progress)


## Incompatible with Common Javascript Libraries - Including Bootstrap

Sequence on most Dataverse pages:

1. Page loads.  Custom javascript executes to bind bootstrap components.
2. A Primefaces AJAX function reloads part of the page.
3. **This breaks bootstrap**
4. Custom javascript is called again to rebind bootstrap components.

- Implications: **Every page** implements a major hack to make boostrap work.

## Cannot Use Common Testing Tools

## Primeface Generated HTML Lengthens Developer/Designer Time

Dataverse developer last summer laughing in frustration: *I'm just trying to make a checkbox!  Look at this!*

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
</div>```

## Issues with the Primefaces checkbox:

1.  The ```<input type="checkbox"...>``` element itself is not visible to the user.
1.  The element is not available to standard testing tools or packages which depend on visibility and names.
1.  Designers/Developers need extra work to style this item



## Implications

* Over the course of a large project, the inability to do standard automated testing can minimally lead to tens of thousands of dollars in lost staff time.
* For example:
    - Most tools allow the recording and replaying of a series of actions.  This recording/replaying is based on the use of standard HTML elements with stable ```id``` or ```name``` tags.
    - When code changes, actions may be easily replayed to check for errors.
    - These tests bases grow to handle complex user scenarios
* The current use of PrimeFaces does not allow the use the tools.  


## No Peer Usage, and Little Usage in General

* We do no have any academic partners developing new software using Primefaces



### Another example

Standard HTML text input tag for Dataset Title:  

```html
<input type="text" name="title" tabindex="1" value="File Test 2" placeholder="Enter title...">
```

Primefaces HTML text input tag for Dataset Title:   

```html
<input id="datasetForm:tabView:j_idt706:0:j_idt709:0:j_idt716:0:j_idt718:0:inputText" class="ui-inputfield ui-inputtext ui-widget ui-state-default ui-corner-all form-control" type="text" tabindex="1" value="File Test 2" name="datasetForm:tabView:j_idt706:0:j_idt709:0:j_idt716:0:j_idt718:0:inputText" role="textbox" aria-disabled="false" aria-readonly="false" aria-multiline="false" placeholder="Enter title...">
```

#### Explanation

* Part of the reason for the unusual ```id``` and ```name``` is the underlying metadata schema.
* Primefaces generates unique ```id``` and ```name``` combinations for the form fields.

*Implications:*  Again, this makes styling difficult and does not allow easy use of modern testing tools.





