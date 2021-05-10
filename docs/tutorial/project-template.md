# Create Project & Templates

## Project

In Tutti, a **project** corresponds to a role of human annotators you wish to assign them for your research, your study, or your Human-In-The-Loop AI system. For example:

- Human facial image labeling task
- COVID-19 social-distancing survey
- Wizard-of-OZ engine in a conversational robot

Let's go ahead and create your first project!

### Steps

1. Click the <svg width="24" height="24" viewBox="0 0 24 24"><path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z" /></svg> icon on the top navigation bar.
2. Type `first-project` for the project name and click "CREATE".
   <img src="./_media/create-prj-screenshot.png" />

3. Select the created `first-project` in the projects list on the navigation bar.

## Template

A **template** is one of statically-rendered web page component(s) which are sequentially shown to the user (e.g., annotator) throughout the project. Taking the COVID-19 social-distancing survey as an example, a possible set of templates (i.e., web pages) would be:

- *Preliminary demographic questions* that asks the participant's age, gender, country of citizenship, etc.
- *Main questions* that relate to the participant's symptoms, places which he/she had been to, etc.
- *Post-questions* that asks the participant's experience through the survey

Let's build some templates upon your `first-project`!

### Steps

Hereafter in this tutorial, we assume your `first-project` is a simple *image labeling task*, with tiny pre- and post-surveys attached to it.

1. Go to "Templates" on the left menu.
2. On the right window, click the <svg width="24" height="24" viewBox="0 0 24 24"><path d="M18 11H15V14H13V11H10V9H13V6H15V9H18M20 4V16H8V4H20M20 2H8C6.9 2 6 2.9 6 4V16C6 17.11 6.9 18 8 18H20C21.11 18 22 17.11 22 16V4C22 2.9 21.11 2 20 2M4 6H2V20C2 21.11 2.9 22 4 22H18V20H4V6Z" /></svg> icon.
3. Enter `preliminary` for the **template name** and choose `Vuetify - Survey` for the **preset template**.
4. Create three more templates by repeating 2--3.
<table>
    <tr>
        <th>Template Name</th><th>Preset Template</th>
    </tr>
    <tr>
        <td>main1</td><td>Vuetify - ImageLabeling</td>
    </tr>
    <tr>
        <td>main2</td><td>Vuetify - SimpleSurvey</td>
    </tr>
    <tr>
        <td>post</td><td>Vuetify - SimpleSurvey</td>
    </tr>
</table>
5. Confirm that all the templates which are named `preliminary`, `main1`, `main2`, and `post` (along with `hello-world`, `[Instruction]` and `[Preview]`) are listed in the dropdown menu.

   !> The created templates may not be reflected immediately; to force reloading, execute `./tutti stop` and then `./tutti start`.

6. Select each created template in the menu to see the page is properly displayed. The displayed template also lets you simulate how it records user inputs, as well as how their results will look like when it is submitted.
   <img src="./_media/template-demo.gif" width="600" />

7. Edit the template file for `main2`, and edit lines as follows (**Keep reading down to "Template Editing" to learn how to do this**):

```diff
- <header><b>Q.</b> Copy-and-paste your Worker ID.</header>
+ <header><b>Q.</b> Describe what you saw in the right picture.</header>

- <v-text-field outlined flat v-nano.required v-model="workerId" label="Worker ID" />
+ <v-text-field outlined flat v-nano.required v-model="description" label="Describe..." />

- data: () => ({ workerId: "" })
+ data: () => ({ description: "" })
```


### Template Editing

As just directed in the step 7 above, `main2` needs a slight modification for this tutorial.
Let's go and make the edit to the file -- meanwhile, we would also like to deliver several key points so that you can smoothly make future edits to other files.

#### File location

The template `main2` for the project `first-project`, for instance, can be found at `tutti/projects/first-project/templates/main2/Main.vue`. More generally,
```
tutti/projects/<project-name>/templates/<template-name>/Main.vue
```
is the file path that you want to open to edit a specific template created for a specific project.

#### .vue file format
The file format for templates has `.vue` extension, which indicates a [Single File Component](https://vuejs.org/v2/guide/single-file-components.html) for [Vue.js](https://vuejs.org/).
Putting it simply, it is a file in which you can code HTML tags, CSS, and JavaScript, all-in-one but properly scoped so that it does not affect other web page components without intention.
See the [official documentation](https://vuejs.org/v2/guide/single-file-components.html) for detailed information.

#### Basic coding examples for Tutti

For instance, `Main.vue` for the `main2` template looks like this (note that this template uses [Vuetify](https://vuetifyjs.com/en/), a Vue UI Library for Material Design):

```main2/Main.vue

<!-- Your HTML code here -->
<template>   
    <v-container pa-10>
        <v-card width="600" class="mx-auto my-6 pa-6">
            <v-row>
                <v-col cols="12">
                    <header><b>Q.</b> Describe what you saw in the right picture.</header>
                </v-col>
                <v-col cols="12">
                    <v-text-field outlined flat v-nano.required v-model="description" label="Describe..." />
                </v-col>
            </v-row>
            <v-row class="d-flex" justify="end">
                <v-btn class="mr-3 mb-3" :disabled="!canSubmit" @click="canSubmit ? submit() : false">next</v-btn>
            </v-row>
        </v-card>
    </v-container>
</template>

<!-- Your JavaScript code here -->
<script>   
import nanoMixIn from "@/mixins/nano";
export default {
    mixins: [nanoMixIn],
    data: () => ({ workerId: "" })
};
</script>

<!-- Your CSS here -->
<style scoped>   
</style>
```

In addition to the programming strategies of Vue.js and Vuetify, there are some programming rules for Tutti functions (e.g., pre-defined JavaScript functions and [Vue custom directives](https://vuejs.org/v2/guide/custom-directive.html)). Namely,
- `v-nano`: when this Vue directive is added to an input tag/component, the key specified for `v-model` as well as its value is registered as a member of user inputs which are sent to Tutti server on submission. If `.required` is appended, the key is treated as a required key (cf. `canSubmit`).
- `submit()`: when this function is called, all the user inputs associated with `v-nano` is sent to Tutti server, immediately followed by loading the next template on the interface.
- `canSubmit`: a binary, computed property that indicate whether all the required fields registered with `v-nano.required` has a valid input value. This can be effectively used with a submit button to toggle its disability.
- `nanoMixIn`: a Vue mix-in module that contains the essential data, methods, and hooks used in templates in Tutti projects. This is always necessary to be included and loaded in the file.

For further information and other programming rules, see [Programming Reference>Template](/guide/ref_template).
