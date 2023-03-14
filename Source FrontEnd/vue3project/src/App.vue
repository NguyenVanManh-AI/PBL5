<template>
  <div class="p-6">
    <router-view></router-view>
  </div>
</template>

<script>


export default {
  name: 'App',
  components:{

  },
  data(){
    return {

    }
  },
  mounted(){

  }
}
</script>

<style >
.modal-header .close {
    padding-right: 40px !important;
    padding-top: 20px !important;
}
.blue,label {
    color: #0085FF;
}
::-webkit-scrollbar {
  width: 13px;
}

::-webkit-scrollbar-track { 
  background: white; 
}
 
::-webkit-scrollbar-thumb {
    background: #888;  
    border-radius: 10px;
    border: 3px solid transparent;
    background-clip: content-box;
}

::-webkit-scrollbar-thumb:hover {
    background: #0085FF; 
    border-radius: 10px;
    border: 3px solid transparent;
    background-clip: content-box;
}

#view{
  display: grid;
  width: 100%;
  overflow-y: scroll;
}
#view::-webkit-scrollbar {
    display: none;
}
/* Hide scrollbar for IE, Edge and Firefox */
#view {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
</style>
