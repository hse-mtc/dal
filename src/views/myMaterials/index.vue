<template>
<!--  <div class="dashboard-container">-->
<!--    <div class="dashboard-text">{{ name }}, добро пожаловать на сайт.</div>-->
<!--    <div>Страница сейчас находится на стадии разработки, по всем вопросам: <a href="mailto:vmloskutov@edu.hse.ru">vmloskutov@edu.hse.ru</a></div>-->
<!--  </div>-->
<!--  <div class="container">-->
<!--    <div class="large-12 medium-12 small-12 cell">-->
<!--      <label>Files-->
<!--        <input type="file" id="files" ref="files" multiple v-on:change="handleFilesUpload()"/>-->
<!--      </label>-->
<!--    </div>-->
<!--    <div class="large-12 medium-12 small-12 cell">-->
<!--      <div v-for="(file, key) in files" class="file-listing">{{ file.name }} <span class="remove-file" v-on:click="removeFile( key )">Remove</span></div>-->
<!--    </div>-->
<!--    <br>-->
<!--    <div class="large-12 medium-12 small-12 cell">-->
<!--      <button v-on:click="addFiles()">Add Files</button>-->
<!--    </div>-->
<!--    <br>-->
<!--    <div class="large-12 medium-12 small-12 cell">-->
<!--      <button v-on:click="submitFiles()">Submit</button>-->
<!--    </div>-->
<!--  </div>-->
</template>

<script>
import { mapGetters } from 'vuex'
import axios from 'axios'
export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  data(){
    return {
      files: []
    }
  },
  methods: {
    submitUpload() {
      console.log(this.$refs.upload)
      // this.$refs.upload.submit();
    },
    addFiles(){
      this.$refs.files.click();
    },
    submitFiles(){

      let formData = new FormData();
      for( var i = 0; i < this.files.length; i++ ){
        let file = this.files[i];
        formData.append('files[' + i + ']', file);
      }
      formData.append('first_name', 'Dan');
      formData.append('last_name', 'Pastori');
      console.log(formData)
      axios.post( 'http://172.20.10.3:8000/api/XEP',
              formData,
              {
                headers: {
                  'Content-Type': 'multipart/form-data'
                }
              }
      ).then(function(){
        console.log('SUCCESS!!');
      })
              .catch(function(){
                console.log('FAILURE!!');
              });
    },
    handleFilesUpload(){
      let uploadedFiles = this.$refs.files.files;
      for( var i = 0; i < uploadedFiles.length; i++ ){
        this.files.push( uploadedFiles[i] );
      }
    },
    removeFile( key ){
      this.files.splice( key, 1 );
    }
  }
}
</script>

<!--<style lang="scss" scoped>-->
<!--.dashboard {-->
<!--  &-container {-->
<!--    margin: 30px;-->
<!--  }-->
<!--  &-text {-->
<!--    font-size: 30px;-->
<!--    line-height: 46px;-->
<!--  }-->
<!--}-->
<!--</style>-->

<style>
  input[type="file"]{
    position: absolute;
    top: -500px;
  }
  div.file-listing{
    width: 200px;
  }
  span.remove-file{
    color: red;
    cursor: pointer;
    float: right;
  }
</style>
