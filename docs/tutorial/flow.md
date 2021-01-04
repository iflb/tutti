# Design Flow

## Flow

Now that you've created projects and templates -- but how would you define their order of which template comes first, next, and last?
Here we introduce **flow**.

Flow allows you to:
- define an ordered sequence of multiple templates to be displayed to users
- group multiple templates and manage them as a batch
- apply rules to skip, iterate, or interrupt a specific batch/template

We are exploring various types of system interactions where Human-In-The-Loop AI engineers, researchers, or individual in-house annotators would want their annotation systems to behave, in order to achieve their own goals.
Tutti's **flow**-designing strategy enables you to build as complex and detailed flows as you wish, yet only requiring you to get the minimal knowledge.

### Steps

1. On the left menu of your Tutti browser console, click "Task Flow". At this point you should only see the boxes named "Start" and "End" with a couple of down-arrows.
2. Open the scheme configuration file for your project `first-project`, which is located at `tutti/projects/first-project/scheme.py`.

3. Edit & save `scheme.py` as follows:

```python
from libs.scheme import ProjectSchemeBase
from libs.scheme.flow import BatchNode, TemplateNode, Statement

class ProjectScheme(ProjectSchemeBase):

    ...

    def define_flow(self):
        t_pre = TemplateNode("preliminary")

        t_main1 = TemplateNode("main1")
        t_main2 = TemplateNode("main2")
        b_main = BatchNode("main",
                           [t_main1, t_main2],
                           statement=Statement.WHILE,
                           condition=self.b_main_cond)

        t_post = TemplateNode("post")

        return BatchNode("all", children=[t_pre, b_main, t_post])

    def b_main_cond(self, wkr_client, ws_client): 
        return ws_client.cnt("main")<5
  ```

4. Go back to the browser console and click <svg width="24" height="24" viewBox="0 0 24 24"><path d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z" /></svg> to reload the flow.
  You're all set if a flow chart like below is rendered in the page.

  !> If the flow chart is not loaded, there might be some syntax or variable error in the `scheme.py` file.

  <img src="./_media/flow.png" width="500" />

Congrats on the successful flow configuration! :tada:
Now, technically, you can already publish your annotation project -- **surprisingly easy, isn't it?**  
Yes, let's go and see what it's like; but before that, please give us a second to recap what just happened.

### Understanding the flow

Looking into the rendered flow chart, we assume it wouldn't be hard for you to understand what the chart means.
The gray rectangle cards represent **batches**, or task groups to which certain functions are applied, and the blue shaped cards represent **templates**, which are actual tasks rendered for users to give their inputs on.

Once the annotation task is started by a user, `preliminary` task is shown to the user.
After submitting the task, the batch of the main tasks starts; `main1` is shown first, followed by `main2` when `main1` is submitted.
What happens after that?
As the "**LOOP condition**" indicates in the chart, the user returns to `main1` and then to `main2` -- and this will be continued for a total of five times.
Lastly, `post` task is assigned; when it is submitted, the user ends the task session.

### Flow configuration API

`scheme.py` just expresses the same flow structure described above, just like building blocks of `TemplateNode` and `BatchNode`.
The both types of nodes generally takes the same set of arguments, such as their names and if/while statement and conditions, while `BatchNode` particularly takes multiple `TemplateNode`s as its children.  
Note that the whole flow also needs to be wrapped by a largest batch and then return it from `define_flow()`.

For further details of the flow configuration API, see [Programming Reference>Project Scheme](./guide/ref_scheme).

## Test run with static templates

### Steps

1. In the browser console, make sure that **first-project** is selected in the top dropdown menu, and click the <svg width="24" height="24" viewBox="0 0 24 24"><path d="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z" /></svg> icon to select "**Launch in Production Mode (Private)**".

2. A new page tab appears, enter "**testworker**" as a worker name and click "LOGIN".

3. Now you are a worker of the task you created, and you should be seeing `preliminary` task first. Start filling the form and proceed by clicking "NEXT", and continue until you see `post` task.

  <img src="./_media/task-sample.gif" width="600" />

  ?> Task templates can go back-and-forth with their answers saved. Try clicking <svg width="24" height="24" viewBox="0 0 24 24"><path d="M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z" /></svg> and <svg width="24" height="24" viewBox="0 0 24 24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg> buttons at the top.

4. Fill the `post` task's form and click "NEXT". Make sure that the page is reloaded (which means the whole flow is completed,) and `preliminary` task appears again.
