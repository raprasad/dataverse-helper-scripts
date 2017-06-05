
# Using Primefaces components vs. API/JSON/Template

## Use a Primefaces component when:

1. Component matches design or can be tweaked via css, built-in styles
1. Component is performant

## Avoid component when:

1. Changing component design becomes main task.
1. Making component performant adds high overhead/complexity

**Summary**: Do what makes sense in the situation rather than forcing code and design to conform to a component

# Comparison of API/JSON/Template vs. Primefaces Component


|#|Capability/Process|API/JSON/Template (server or browser based)|Primefaces Component|Note|
---|:---:|:---:|:---:|:---:
|1|**Dev Time**|**Medium**|**High**||
|2|**Automated Testing** (Rest Assured)|**Yes**|**No**|
|3|**HTML Customization**|**Easy/Medium** (Many tools available or raw HTML)|**Difficult**|Design limited to Primeface components. (ref: dataset page file listing)|
|4|**Troubleshooting** / Identifying where problems/bugs exist|Business Logic and Design **Separate** ("50% easier")|Business Logic and Design **Intertwined**|Easier to identify issues, especially with automated testing of business logic.|
|5|**Performance Tuning**|More choices/Business logic not in component|Often constrained by component||
|6|**Code reuse**|**High**: API endpoints/templates can be re-used|**Low/Medium**: Components tied to Business Logic|
|7|Javascript Dependent|**Yes** - if browser based|**Yes**|
|8|508 Compliance with Forms|**It depends**|**No**|
|9|Widely used in open source community|**Yes** (more potential contributors, more community, stackoverflow,etc)|**No** (2016 we were believed to be only open source project)||
|10|Widely used paradigm|**Yes**|**No** - Industry shifting away|Industry shift to microservices, other frameworks, Oracle pulling resources, fewer programmers in their 20s, etc.|
|11|Selenium Automated Testing|**Yes**|**No** requires significant programming (time prohibitive)|

# Consistency

There is something to be said for using Primefaces components because they are consistent with other parts of the system.  __However__, that view should be factored in with the points in the chart above and, more importantly, with a longer term strategic view of the system if the goals include:
  - Having more API endpoints
  - Increasing the number of code contributors
  - Improving automated testing
  - Shifting some parts of the system to separate microservices to improve scalability
