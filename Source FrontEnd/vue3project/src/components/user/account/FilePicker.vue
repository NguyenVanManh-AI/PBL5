<template>
  <div>
    <input multiple type="file" ref="fileInput" @change="uploadFile"/>
  </div>
</template>

<script>
const axios = require('axios');
export default {
  methods: {
    // upload 1 file
    // uploadFile() {
    //   let formData = new FormData();
    //   formData.append('files', this.$refs.fileInput.files); 

    //   axios.post('http://localhost:8000/api/upload-file/', formData, {
    //     headers: {
    //       'Content-Type': 'multipart/form-data'
    //     }
    //   })
    //   .then(response => {
    //     console.log(response.data);
    //   })
    //   .catch(error => {
    //     console.log(error);
    //   });
    // }

    
    // upload nhiều file 
    uploadFile() {
      let formData = new FormData();
      let files = this.$refs.fileInput.files;

      for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
      }

      axios.post('http://localhost:8000/api/upload-file/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.log(error);
      });
    }
  }
}
</script>
