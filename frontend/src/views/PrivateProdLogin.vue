<template>
  <v-app id="inspire">
    <v-main>
      <v-container class="fill-height" fluid >
        <v-row align="center" justify="center" >
          <v-col cols="12" sm="8" md="4" >
            <v-card class="elevation-12">
              <v-toolbar color="indigo" dark flat >
                <v-toolbar-title>Enter your worker ID</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form ref="form" @submit.prevent="mySubmit">
                  <v-text-field label="Worker ID" v-model="workerId" prepend-icon="mdi-account" type="text" :rules="workerIdRules" ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="mySubmit">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>

export default {
    data: () => ({
        workerId: "",
        projectName: "",
        workerIdRules: [
            v => !!v || "worker ID is required"
        ],
        projectRules: [
            v => !!v || "project name is required"
        ]
    }),
    created() {
        if(this.$route.query.project) this.projectName = this.$route.query.project;
    },
    props: {
      source: String,
    },
    methods: {
        mySubmit() {
            if(this.$refs.form.validate()){
                localStorage.setItem("workerId", this.workerId);
                window.location.href = `./private-prod/${this.projectName}`;
            }
        }
    }
}
</script>
