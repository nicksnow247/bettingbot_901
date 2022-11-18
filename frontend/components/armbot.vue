<template>
  <div>
    <b-form-checkbox v-model="value" style="max-width:40px"
                     v-on:change="$emit('change', $event, item)"
                     ></b-form-checkbox>
  </div>
</template>

<script>
  export default {
    props: ['item', 'value']
  }
</script>