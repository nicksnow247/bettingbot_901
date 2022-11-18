<template>
  <div>
    <b-form-input type="text"
                  v-model="value"
                  v-show="checked"
                  style="width:64px"></b-form-input>
  </div>
</template>

<script>
  export default {
    props: ['checked', 'value']
  }
</script>