<template>
  <div>
    <b-form-select v-model="value"
                   v-on:change="$emit('change', $event, item)"
                   :options="options" style="width:100px"></b-form-select>
  </div>
</template>

<script>
  export default {
    props: ['item', 'value'],
    data() {
      return {
        options: [
          { value: null, text: '' },
          { value: 0, text: 'Back first' },
          { value: 1, text: 'Lay first' },
        ]

      }
    }
  }
</script>
