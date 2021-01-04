# Template

## File names and locations

- Preview
    - `tutti/projects/<project_name>/templates/Preview.vue`
- Instruction
    - `tutti/projects/<project_name>/templates/Instruction.vue`
- Main Template
    - `tutti/projects/<project_name>/templates/<template_name>/Main.vue`

?> Preview and instruction files are created with `create_project` command, and the main template file is created with `create_template` command.

## Preview & instruction

The preview and instruction files, with a `.vue` extension, are basically [Vue.js' single file components](https://vuejs.org/v2/guide/single-file-components.html); you can thus not only write HTML collocate CSS and JavaScript in the files.

For those who are not familiar to Vue.js' single file components, here's an example for the minimum code:

```markup
<!-- Works in both Preview.vue and Instruction.vue -->

<template>
    <div>
        This is my test preview/instruction.
    </div>
</template>
```

Note that a whole HTML needs to be wrapped by `<template>`, as well as only one parent tag (*i.e.,* `<div>` in the above example) is allowed in the block.

### Preview.vue

At present, `Preview.vue` is a necessary page component for particularly when the project is deployed as Amazon Mechanical Turk HITs.
A HIT "preview" page is what MTurk workers see when they actually be assigned and start the HIT, thereby better understanding what the HIT would request them to do.
Typical preview pages contain the similar user interface shown during the task or detailed task instruction.
Be sure to design this page component thoughtfully, since it is requesters' responsibility to instruct workers to get better results and for fair work.

<img src="./_media/preview.gif" width="500" />

### Instruction.vue

`Instruction.vue` is another page component that helps workers get better sense of what needs to be done during the task (this is not limited to Amazon Mechanical Turk).
There are two patterns where the instruction page components is shown to workers: i) automatically rendered in a floating dialog for workers who have never visited the project, and ii) rendered in a floating dialog when the worker clicked "See instruction" button in the project interface (the button is only visible when `ProjectScheme.instruction` is set to True).

<img src="./_media/instruction.gif" width="500" />


## Main Template

### Vue Mixin

All nanotask templates are required to import `nanoMixin` in the `<script>` block:

```javascript
import nanoMixIn from "@/mixins/nano";
export default {
    mixins: [nanoMixIn],
    ...
```

This `nanoMixIn` module contains a set of Tutti-defined [Vue's options](https://vuejs.org/v2/api/#Options-Data) to allow requesters to send and receive Tutti-relevant data with the backend server.

#### data

- `nano.ans`
  - A writable object which stores worker's answers sent to Tutti's backend server when `submit()` is called.
    Its format should be like:
    ```json
    {
        "mykey1": "some string",
        "mykey2": 12345,
        ...
    }
    ```
- `nano.props`
  - A readable object which contains "**nano props**", a set of dynamic contents in the template for a loaded nanotask, which is uploaded with `UploadNanotasks` Event.
- `defaultProps`
  - A readable/writable object for placeholder values when no valid value for a child of `nano.props` was found, such as when no assignable nanotask could be loaded or an unknown child key value was specified.
    To initialize the object, just create data in the template file like:
    ```javascript
    <script>
    import nanoMixIn from "@/mixins/nano";
    export default {
        mixins: [nanoMixIn],
        data: () => ({
            defaultNanoProps: {
                "mystring": "my default value",
                "myurl": "https://some.default.url"
            }
        })
    };
    </script>
    ```
    and the values will automatically replace `nano.props.mystring` and `nano.props.myurl` automatically when nano props are not available.

#### computed property

- `canSubmit`
  - A helper property that returns a boolean value whether all required answer fields are filled (*c.f.,* `v-nano`).

#### method

- `submit()`
  - A method to finish the current template and step forward to the next template node.

#### directives

- `v-nano`
  - Adding `v-nano` directive to input components makes its `v-model`-binded data also synchronized to workers' answer data which is to be sent to Tutti's server.
    If data is bound the `v-nano` directive, the string specified for `v-model` is registered as a key of `nano.ans` object.
  - `.required` modifier is allowed for use to make the input to be a required field (this effects the return value of `canSubmit`).

