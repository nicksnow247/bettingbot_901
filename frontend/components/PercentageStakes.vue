<template>
  <div>
    <b-form-select v-model="value"
                   :options="options"
                   v-on:change="$emit('change', $event, item)"
                   style="width:72px"></b-form-select>
  </div>
</template>

<script>
  export default {
    props: ['item', 'value'],
    data() {
      return {
        options: [
          { value: null, text: 'Off' },
          { value: 0.02, text: '2%' },
          { value: 0.03, text: '3%' },
          { value: 0.04, text: '4%' },
          { value: 0.05, text: '5%' },
          { value: 0.06, text: '6%' },
          { value: 0.07, text: '7%' },
          { value: 0.08, text: '8%' },
          { value: 0.09, text: '9%' },
          { value: 0.1, text: '10%' }
        ]
      }
    }
  }
</script>