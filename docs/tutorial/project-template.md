# Create Project & Templates

## Create Project

In Tutti, a **project** corresponds to a role of human annotators you wish to assign them for your research, your study, or your Human-In-The-Loop AI system. For example:

- Human facial image labeling task
- COVID-19 social-distancing survey
- Wizard-of-OZ engine in a conversational robot

Let's go ahead and create your first project!

### Steps

1. Click the <svg width="24" height="24" viewBox="0 0 24 24"><path d="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z" /></svg> icon on the top navigation bar and select "Create Project..."
2. Type `first-project` for the project name and click "CREATE".
   <img src="./_media/create-prj-screenshot.png" />

3. Select the created `first-project` in the projects list on the navigation bar.

## Create Template

A **template** is one of statically-rendered web page component(s) which are sequentially shown to the user (e.g., annotator) throughout the project. Taking the COVID-19 social-distancing survey as an example, a possible set of templates (i.e., web pages) would be:

- *Preliminary demographic questions* that asks the participant's age, gender, country of citizenship, etc.
- *Main questions* that relate to the participant's symptoms, places which he/she had been to, etc.
- *Post-questions* that asks the participant's experience through the survey

Let's build some templates upon your `first-project`!

### Steps

Hereafter in this tutorial, we assume your `first-project` is a simple *image labeling task*, with tiny pre- and post-surveys attached to it.

1. Go to "Templates" on the left menu.
2. On the right window, click the <svg width="24" height="24" viewBox="0 0 24 24"><path d="M18 11H15V14H13V11H10V9H13V6H15V9H18M20 4V16H8V4H20M20 2H8C6.9 2 6 2.9 6 4V16C6 17.11 6.9 18 8 18H20C21.11 18 22 17.11 22 16V4C22 2.9 21.11 2 20 2M4 6H2V20C2 21.11 2.9 22 4 22H18V20H4V6Z" /></svg> icon.
3. Enter `preliminary` for the template name and choose `Vuetify - Survey` for the preset template.
4. Repeat two more times through 2. and 3. with the template name and preset template, respectively, as follows:
  - `main`, `Vuetify - ImageLabeling`
  - `post`, `Vuetify - SimpleSurvey`
5. Confirm that all the templates which are named `preliminary`, `main`, and `post` are listed in the dropdown menu.

   !> The created templates may not be reflected immediately; to force reloading, stop the docker application by hitting Ctrl-C in the terminal and run it again.

6. Select each created template in the menu to see the page is properly displayed. The displayed template also lets you simulate how it records user inputs, as well as how their results will look like when it is submitted.
   <img src="./_media/template-demo.gif" width="600" />

Now that you've created templates for this tutorial, you can proceed to [2. Design Flow](/tutorial/flow.md) -- however, the followings are a few extra steps to **edit their codes** if you are already interested.


### Template Editing

Your template `pre` for the project `first-project`, for instance, can be found at `tutti/projects/first-project/templates/pre/Main.vue`. More generally,
```
tutti/projects/<project-name>/templates/<template-name>/Main.vue
```
is the file path that you want to open to edit a specific template created for a specific project.

The file format for templates has `.vue` extension, which indicates a [Single File Component](https://vuejs.org/v2/guide/single-file-components.html) for [Vue.js](https://vuejs.org/).
Putting it simply, it is a file in which you can code HTML tags, CSS, and JavaScript, all-in-one but properly scoped so that it does not affect other web page components without intention.
See the [official documentation](https://vuejs.org/v2/guide/single-file-components.html) for detailed information.

For instance, `Main.vue` for the `post` template looks like this (note that this template uses [Vuetify](https://vuetifyjs.com/en/), a Vue UI Library for Material Design):

```vue
<!-- post/Main.vue -->

<template>   <!-- Your HTML code here -->
    <v-container pa-10>
        <v-card width="600" class="mx-auto my-6 pa-6">
            <v-row>
                <v-col cols="12">
                    <header><b>Q.</b> Copy-and-paste your Worker ID.</header>
                </v-col>
                <v-col cols="12">
                    <v-text-field outlined flat v-nano.required v-model="workerId" label="Worker ID" />
                </v-col>
            </v-row>
            <v-row class="d-flex" justify="end">
                <v-btn class="mr-3 mb-3" :disabled="!canSubmit" @click="canSubmit ? submit() : false">next</v-btn>
            </v-row>
        </v-card>
    </v-container>
</template>

<script>   <!-- Your JavaScript code here -->
import nanoMixIn from "@/mixins/nano";
export default {
    mixins: [nanoMixIn],
    data: () => ({
        workerId: ""
    })
};
</script>

<style scoped>   <!-- Your CSS here -->
</style>
```

In addition to Vue.js and Vuetify strategies, there are some programming rules for Tutti functions (e.g., pre-defined JavaScript functions and [Vue custom directives](https://vuejs.org/v2/guide/custom-directive.html)). Namely,
- `v-nano`: when this Vue directive is added to an input tag/component, the key specified for `v-model` as well as its value is registered as a member of user inputs which are sent to Tutti server on submission. If `.required` is appended, the key is treated as a required key (cf. `canSubmit`).
- `submit()`: when this function is called, all the user inputs associated with `v-nano` is sent to Tutti server, immediately followed by loading the next template on the interface.
- `canSubmit`: a binary, computed property that indicate whether all the required fields registered with `v-nano.required` has a valid input value. This can be effectively used with a submit button to toggle its disability.
- `nanoMixIn`: a Vue mix-in module that contains the essential data, methods, and hooks used in templates in Tutti projects. This is always necessary to be included and loaded in the file.

For further information and other programming rules, see [Programming Reference](/guide/ref).

?> Since Tutti runs Vue CLI dev server for the frontend, your edit in the code will be instantly reloaded and reflected without refreshing the browser ("[Hot-Module-Replacement](https://cli.vuejs.org/guide/cli-service.html#vue-cli-service-serve)").
