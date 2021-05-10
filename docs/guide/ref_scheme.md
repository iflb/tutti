# Project Scheme


## File name and location

- ```tutti/projects/<project_name>/scheme.py```

?> The file is automatically created with `create_project` command.

!> Changes in the project scheme will NOT be reloaded until you run `LoadFlow` DUCTS event or click <svg width="24" height="24" viewBox="0 0 24 24"><path d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z" /></svg> icon in the Task Flow page in the console.

## Classes

<h3 id="class_libs.scheme.ProjectScheme" class="h-class">class libs.scheme.<b>ProjectScheme</b></h3>

Necessary in `scheme.py`.

Within the class, `config_params()` and `define_flow()` also needs to be implemented.




---



<h4 class="h-class">ProjectScheme.<b>config_params</b><span class="args"></span></h4>


Initializes a set of project parameters.

As of now, each parameter is declared as an instance variable in the class, such as:

```python
class ProjectScheme(ProjectSchemeBase):
    def config_params(self):
        self.title = "My test project"
        self.assignment_order = "dfs"
        ...
```

All available parameters are as follows:

#### Required parameters:

- `title` (*string*) -- A project title.

#### Optional parameters:

- `assignment_order` (*string;* default: "bfs") --
    Specified either as **"bfs"** or **"dfs"**.
    Assignment order of nanotasks that were given the same priority upon upload.
    This is commonly applied to those of each template within the project.
    - With **"bfs"**, assignable nanotasks are ordered by the *breadth-first* search where nanotasks with the same priority and the **least** number of collected answers are assigned first.
    - With **"dfs"**, the *depth-first* search is applied where nanotasks with the same priority and the **most** number of collected answers are assigned first.
- `sort_order` (*string;* default: "natural") --
    Specified either as **"natural"** or **"random"**.
    Sorting order of nanotasks with the equivalent assignment order (i.e., with the same top priority AND the same number of collected answers).
    - With **"natural"**, the sorting order follows the ascending order of nanotask upload (or nanotask ID).
    - With **"random"**, the sorting order is randomized.

<div class="warning">
    Below is an example of the order of queued nanotasks for a certain worker in different <code>assignment_order</code> and <code>sort_order</code> settings.
    Let's say there are eight uploaded nanotasks for a certain template, for each of which a few answers were already collected from workers:<br>
    <img src="./_media/assignment_order.png" width="700" /><br>
    In a situation like this, a worker will be assigned nanotasks in the following orders:<br>
    <table>
        <tr><th>assignment_order</th><th>sort_order</th><th>Resulting nanotask assignment order</th></tr>
        <tr><td>bfs</td><td>natural</td><td>NT:005, NT:008, / NT:004, NT:003, / NT:001, NT:007, NT:006     </td></tr>
        <tr><td>dfs</td><td>natural</td><td>NT:005, NT:008, / NT:003, NT:004, / NT:006, NT:001, NT:007     </td></tr>
        <tr><td>bfs</td><td>random </td><td>(NT:008, NT:005,) / NT:004, NT:003, / (NT:007, NT:001,) NT:006 </td></tr>
        <tr><td>dfs</td><td>random </td><td>(NT:008, NT:005,) / NT:003, NT:004, / NT:006, (NT:007, NT:001) </td></tr>
        <tr><td></td><td></td><td>
            / ... Separator between different priorities <br>
            () ... Randomized; order may vary
        </td></tr>
    </table>
</div>

- `show_title` (*boolean;* default: True) -- Whether to show the project title in the project UI.
- `page_navination` (*boolean;* default: False) -- Whether to show Prev and Next buttons in the project UI that allows workers to go back and forth among assigned nanotasks.
- `push_instruction` (*boolean;* default: True) -- Whether to automatically show an instruction pop-up to new workers.
- `instruction_btn` (*boolean;* default: True) -- Whether to show a button for instruction in the project UI.
- `allow_parallel_sessions` (*boolean;* default: True) -- Whether to allow workers to open the same project in multiple tabs/pages.
- `anonymous` (*boolean;* default: False) -- Whether to allow workers to work without worker ID.
- `preview` (*boolean;* default: True) -- Whether to show preview template when no worker ID is found.
- `completion_alert` (*boolean;* default: False) -- Whether to show a pop-up to notify workers the end of the work session.
 



---




<h4 class="h-class">ProjectScheme.<b>define_flow</b><span class="args"></span></h4>


This function is used to define the task flow.
As of now, a single instance of either `TemplateNode` or `BatchNode` needs to be returned from the function.
For example:

```python
from libs.scheme import ProjectSchemeBase
from libs.scheme.flow import TemplateNode

class ProjectScheme(ProjectSchemeBase):
    ...
    def define_flow(self):
        return TemplateNode("mytemplate")
```

Or:

```python
from libs.scheme import ProjectSchemeBase
from libs.scheme.flow import BatchNode, TemplateNode, Condition, Statement

class ProjectScheme(ProjectSchemeBase):
    ...
    def define_flow(self):
        tnode1 = TemplateNode("mytemplate1")
        tnode2 = TemplateNode("mytemplate2")
        return BatchNode("mybatch",
                         children=[tnode1, tnode2],
                         condition=Condition(Statement.WHILE,
                                             self.mybatch_while_condition)

    def mybatch_while_condition(self, wkr_context, ws_context):
        return ws_context.cnt("mybatch")<3
```



---




<h3 class="h-class">class libs.scheme.flow.<b>FlowNode</b></h3>

!> Not intended for direct use by developers. Please use `TemplateNode` and `BatchNode` instead.

A superclass of `TemplateNode` and `BatchNode` which can be used to build blocks for the Task Flow.




---



<h3 class="h-class">class libs.scheme.flow.<b>TemplateNode</b><span class="args">name, condition=None, is_skippable=False, on_enter=None, on_exit=None, on_submit=None</span></h4>

A building component of the Task Flow that represents a **template**, which is an actual nanotask visually shown to workers.

Derived from `FlowNode`.

#### Parameters:

- **name** (*str*) -- A name of the template. This value needs to be the same as that registered via `CreateTemplate` Event.
- **condition** (*Condition*) -- A condition for the statement.
- **is_skippable** (*bool*) -- Whether to allow workers to skip the node to the next when the template node cannot be assigned. *If False is set, the project terminates the work session and starts the new one.*
- **on_enter** (*function*) -- A function that is called *before* the Node is visited (regardless of whether it will be executed or not).
It is passed two arguments: instances of `WorkerContext` and `WorkSessionContext`.
- **on_exit** (*function*) -- A function that is called upon leaving the executed Node.
It is passed two arguments: instances of `WorkerContext` and `WorkSessionContext`.
- **on_submit** (*function*) -- A hook function called internally on submission of the template node.  This function can be used mainly for saving custom information to `WorkerContext` or `WorkSessionContext`. Four arguments are passed to the function: i) a `WorkerContext` instance, ii) a `WorkSessionContext` instance, iii) a *dict* of submitted answers, and iv) a *dict* of ground-truths of the nanotask (or **None** if not exists).\
The code below is an example of setting the `on_submit` parameter so that the work session counts the number of nanotasks a worker answered correctly on the template called "mytemplate1", and use the results to calculate the accuracy to allow only workers who had >=70% accuracy to work on the template called "mytemplate2".

```python
class ProjectScheme(ProjectSchemeBase):
    ...
    def define_flow(self):
        tnode1 = TemplateNode("mytemplate1",
                              statement=Statement.WHILE,
                              condition=self.tnode1_cond,
                              on_submit=self.tnode1_on_submit)

        tnode2 = TemplateNode("mytemplate2",
                              statement=Statement.IF,
                              condition=self.tnode2_cond)

        return BatchNode("mybatch", [tnode1, tnode2])

    def tnode1_cond(self, wkr_context, ws_context): 
        return ws_context.cnt("mytemplate1")<8

    def tnode1_on_submit(self, wkr_context, ws_context, ans, gt):
        is_correct = 1 if ans["somequestion"]==gt["somequestion"] else 0
        ws_context.set_attr("is_correct", is_correct)

    def tnode2_cond(self, wkr_context, ws_context): 
        cc = ws_context.get_attr("is_correct")
        return cc.count("1") / len(cc) >= 0.7

```



---




<h3 class="h-class">class libs.scheme.flow.<b>BatchNode</b><span class="args">name, children, condition=None, is_skippable=False, on_enter=None, on_exit=None</span></h3>

A building component of the Task Flow which can create a group of **templates** and/or **batches**.

Derived from `FlowNode`.

#### Parameters (see `TemplateNode` for detailed descriptions):

- **name** (*str*) -- A name of the batch. This can be any string but needs to be unique.
- **children** (*list*) -- A sequence of child nodes (*i.e.,* `TemplateNode`s and/or `BatchNode`s) to create a group with. All the child nodes must be in the order.
- **condition** (*Condition*) -- A condition for the statement.
- **is_skippable** (*bool*) -- Whether to allow workers to skip the node to the next when the template node cannot be assigned.
- **on_enter** (*function*) -- A function that is called *before* the Node is visited.
- **on_exit** (*function*) -- A function that is called upon leaving the executed Node.


---


<h3 class="h-class">class libs.scheme.flow.<b>Condition</b><span class="args">statement, func, **kwargs</span></h3>

A class that specifies the rule for `FlowNode` to be executed/skipped or looped with a conditional statement(s).

#### Parameters:

- **statement** (*Statement*) -- A type of statement (*i.e.,* IF or WHILE).
- **func** (*function*) -- The function passed here is called internally before the system tries to load the node.
The function is passed at least two arguments: **instances of `WorkerContext` and `WorkSessionContext`**.
The node is loaded if the function returns True, otherwise the node will not be loaded.
The code below is an example of initializing the Condition object and passing it as a `FlowNode`'s parameter, so that a work session repeats assigning a template named "mytemplate" for three times before submission:

```python
class ProjectScheme(ProjectSchemeBase):
    ...
    def define_flow(self):
        return TemplateNode("mytemplate",
                            condition=Condition(Statement.WHILE, self.tnode_cond))

    def tnode_cond(self, wkr_context, ws_context): 
        return ws_context.cnt("mytemplate")<3
```

- **kwargs** -- A set of arbitrary keyword arguments are allowed to be passed to the object, for the reusability of the passed function.
The above example can be further written as follows (note that `tmpl_name` is now passed as the third argument of the `Condition` object):

```python
class ProjectScheme(ProjectSchemeBase):
    ...
    def define_flow(self):
        tmpls = [TemplateNode(name, condition=Condition(Statement.WHILE, self.count_cond, tmpl_name=name)) for name in ["mytemplate", "mytemplate2"]]
        return BatchNode("mybatch", tmpls)

    def count_cond(self, wkr_context, ws_context, tmpl_name): 
        return ws_context.cnt(tmpl_name)<3
```

Now the project iterates "mytemplate" `TemplateNode` three times, and then "mytemplate2" `TemplateNode` three other times.


---


<h3 class="h-class">class libs.scheme.flow.<b>Statement</b></h3>

An `enum.Enum` subclass of available conditional statements for the task flow.

- **NONE** -- No statement (the node is always executed once)
- **IF** -- IF statement (the node is executed once when the node's `condition` returns True)
- **WHILE** -- WHILE statement (the node is iteratively executed as long as the node's `condition` returns True)


---


<h3 class="h-class">class libs.scheme.context.<b>ContextBase</b></h3>

At present, this class is a superclass of `WorkerContext` and `WorkSessionContext` which provides developers with data memory used in evaluating conditional statements set to `TemplateNode` and `BatchNode`.


---


<h4 class="h-class">ContextBase.<b>set_attr</b><span class="args">name, value</span></h4>

Stores a primitive value (*i.e.,* bool, int, float, list, and dict) for the specified attribute key.
To store an object instance of any Python class, use `set_attr_obj()` instead.

#### Parameters:

- **name** (*str*) -- An attribute key name.
- **value** (*primitive type*) -- A stored value for the attribute key.


---


<h4 class="h-class">ContextBase.<b>set_attr_obj</b><span class="args">name, value</span></h4>

Stores an object of any Python class for the specified attribute key.

#### Parameters:

- **name** (*str*) -- An attribute key name.
- **value** (*object*) -- A stored value for the attribute key.


---


<h4 class="h-class">ContextBase.<b>get_attr</b><span class="args">name</span></h4>

Gets a value for the specified attribute key which was set with `set_attr`.
To get values set with `set_attr_obj`, use `get_attr_obj` instead.

#### Parameters:

- **name** (*str*) -- An attribute name.

##### Return value:

- The stored value.


---


<h4 class="h-class">ContextBase.<b>get_attr_obj</b><span class="args">name</span></h4>

Gets a value for the specified attribute key which was set with `set_attr_obj`.

#### Parameters:

- **name** (*str*) -- An attribute name.

##### Return value:

- The stored value.


---


<h4 class="h-class">ContextBase.<b>cnt</b><span class="args">node_name</span></h4>

Returns a number of times the node is visited previously.

#### Parameters:

- **node_name** (*str*) -- A name of `TemplateNode` or `BatchNode`.

##### Return value:

An *integer* value.


---


<h3 class="h-class">class libs.scheme.context.<b>WorkerContext</b></h3>

A `ContextBase` subclass with a scope for a worker ID.


---


<h3 class="h-class">class libs.scheme.context.<b>WorkSessionContext</b></h3>

A `ContextBase` subclass with a scope for a work session.
