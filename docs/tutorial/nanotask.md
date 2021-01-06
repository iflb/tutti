# Upload Nanotasks

Now you saw how the templates and the flow you created worked to build up your annotation project.  
*But*, didn't you see some things a bit weird?
You might be thinking something like:
- What's the point of being shown and annotating the same pair of images again and again? (Do I have to make thousands of similar templates for my real annotation tasks?)
- ~~Isn't it annoying for annotators to be asked every time what is in the right card? Can't I just ask that when it is necessary?~~  <span style="color:red">To be addressed soon</span>

Yes, those are certainly reasonable questions! No worries, there are ways to handle them.

## Nanotasks

**Nanotasks** are instances of tasks that is rendered by using the same template, all of which share the same set of parameter fields but each of them can have the different parameter values.  
For instance, `main1`, the task template for image labeling, is not intended for annotating only a certain couple of images.
Rather, it is just a **template**, literally; actual contents to be dynamically rendered on this single template are possessed by nanotasks, and each one of the nanotasks are loaded at the time a worker enters the template according to the flow.

Let's take a look at `Main.vue` for `main1` template. In the HTML part of the code, you can see that the source URLs of the images (i.e., `:src` attribute in `<v-img>`) look like some sort of object variables (e.g., `nano.data.img_url0`)  but not hard-coded URLs.

```main1/Main.vue

<template>
    <v-container pa-10>
        <div class="text-h4">Main-1</div>

        <v-card max-width="1000" class="mx-auto my-6 pa-6">
            <v-row align="center">
                <v-col cols="5">
                    <v-card class="pa-3" color="grey lighten-4">
                    <v-img height="300" :src="nano.data.img_url0" contain>

                        <template v-slot:placeholder>
                            <v-row class="fill-height ma-0" align="center" justify="center">
                                <v-progress-circular indeterminate color="grey lighten-1"></v-progress-circular>
                            </v-row>
                        </template>

                    </v-img>
                   </v-card>
                </v-col>
                <v-col cols="2" align="center" justify="center"><v-icon x-large>mdi-arrow-left-right-bold</v-icon></v-col>
                <v-col cols="5">
                    <v-card class="pa-3" color="grey lighten-4">
                    <v-img height="300" :src="nano.data.img_url1" contain>
                        <template v-slot:placeholder>
                            <v-row class="fill-height ma-0" align="center" justify="center">
                                <v-progress-circular indeterminate color="grey lighten-1"></v-progress-circular>
                            </v-row>
                        </template>
                    </v-img>
                    </v-card>
                </v-col>
            </v-row>
            <v-row class="d-flex" justify="center">
                <v-btn class="ma-3" x-large dark color="green darken-4" @click="nano.ans.choice='Same';  submit()">Same</v-btn>
                <v-btn class="ma-3" x-large dark color="green darken-1" @click="nano.ans.choice='Maybe Same';  submit()">Maybe Same</v-btn>
                <v-btn class="ma-3" x-large dark color="red darken-1"   @click="nano.ans.choice='Maybe Not Same';  submit()">Maybe Not Same</v-btn>
                <v-btn class="ma-3" x-large dark color="red darken-4"   @click="nano.ans.choice='Not Same';  submit()">Not Same</v-btn>
            </v-row>
        </v-card>
    </v-container>
</template>

<script>
import nanoMixIn from "@/mixins/nano";
export default {
    mixins: [nanoMixIn],
    data: () => ({
        defaultNanoProps: {
            "img_url0": "https://images-na.ssl-images-amazon.com/images/I/61qEl7SAq9L._AC_SL1000_.jpg",
            "img_url1": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQJxhbQz2Oy8Dn8ksxkaXPbzMIvhTaGUBH98P5nQ9zIXlQVV5OnWT1ozp9joA&usqp=CAc"
        }
    })
};
</script>
```

Strictly speaking, the string value `nano.data.img_url0` and `nano.data.img_url1` actually works as javascript object variables, when the attribute name of their tags has a colon prefix (i.e., `:src`).
This is a part of Vue.js' template syntax -- [a shorthand of `v-bind` directive](https://vuejs.org/v2/guide/syntax.html#v-bind-Shorthand) which interpolates the value of the specified variable in HTML attributes.
`nano.data` is also a reserved structure for Tutti's functionality, which means the values for the fields `img_url0` and `img_url1` is loaded from one of the registered nanotasks and interpolated to the `src` attributes.
In Tutti, we call these fields for nanotasks **nano-props**.

#### Default values

So where did the cute teddy bear images that you just saw during the test run come from?
They are defined as the placeholder values in the JavaScript code as the members of `defaultNanoProps`.
The placeholder values are used when no nanotask is registered to the template or when you test the template in the browser console's Template page.
In the practical usage as an annotation system, you need to register nanotasks before you run the project so that dynamic image pairs are loaded.

!> `defaultProps` is a key of Vue's `data` object reserved for Tutti's functionality, defined in the `nanoMixIn` module.

In below, we explain how to upload nanotask data for `main1` template.

### Steps

1. From the side bar menu of the browser console, go to Task Flow page.

2. Click the <svg width="24" height="24" viewBox="0 0 24 24"><path d="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z" /></svg> icon of the card for `main1` temlate to choose "Import Nanotasks..."

3. Choose `sample-nanotasks.json` stored in `tutti/projects/first-project/templates/main1/`. ~~In the preview, you will see a list of image URLs for each nanotask (represented as a row) to be imported.~~ Then click "IMPORT".

4. If you see an outlined button that says "Nanotasks (15)", it means the nanotasks were successfully imported. You can see the list of the imported nanotasks by clicking the button.

  <img src="./_media/imported-nanotasks.png" width="500" />

5. Restart Tutti service (or restart Tutti's backend service with `docker-compose restart backend`), refresh the browser console, and select **first-project** as the project name in the top navigation bar.

6. Go to "Launch in Production Mode (Private)" again and start the annotation tasks. You will see the images for `main1` template are now of URLs used in the registered nanotasks.

### Understanding nanotask JSON

Currently, the only way we prepared for uploading nanotasks is via JSON file.
`sample-nanotasks.json` contains information in the following format:
```json
{
    "Settings": {
        "TagName": "mytagname",
        "NumAssignable": 3,
        "Priority": 1
    },
    "Nanotasks": [
        {
            "NumAssignable": 2,      // <--- this overrides global value (3)
            "Priority": 3,           // <--- this overrides global value (1)
            "Props": {
                "img_url0": "/static/trump-left.jpg",
                "img_url1": "/static/trump-right-1.jpg"
            },
            "GroundTruths": {
                "choice": "Same"
            }
        },
        ...
    ]
}
```

The top member named "Settings" specifies parameters for global settings across all nanotasks defined in the file.

`TagName` is useful for creating a user-defined group of nanotasks, as Events for nanotask manipulation (*e.g.,* `UploadNanotasks` or `DeleteNanotasks`) can be queried for the group; it can be any string, but is recommended to be unique from that of any other nanotask group uploaded previously for more easily keeping track of all uploaded nanotasks.

`NumAssignable` refers to the number of workers who can be assigned to the nanotask(s).
`Priority` is an integer value for sorting assignment order of nanotasks; the **smaller** the number is set, the **more importantly** the nanotask(s) is/are treated.
`NumAssignable` and `Priority` set as `Settings`' children are applied globally to all nanotasks listed in the file; however, the global values are overridden for nanotask items of which members are set individually as their children members in the `Nanotasks` list.

`Props` specifies, as key-value data, contents you want to be dynamically rendered in the template as nanotasks are loaded one by one.
Each key needs to correspond with what appears in the template, and its value can only accept a string.

`GroundTruths` specifies, also as key-value data, ground-truth answers you wish to use to check workers' answers with in `FlowNode`'s conditional statements (see [Project Scheme](guide/ref_scheme.md)) or manually after workers' answers are collected.
