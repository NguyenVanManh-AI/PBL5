<template>
  <div>
    <input multiple type="file" ref="fileInput" @change="uploadFile"/>
  </div>
</template>

<script>
const axios = require('axios');
export default {
  methods: {
    uploadFile() {
      let formData = new FormData();
      formData.append('file', this.$refs.fileInput.files[0]);

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
