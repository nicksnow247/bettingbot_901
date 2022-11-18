<!-- Vue SFC -->
<template>
  <div id="app" class="container">
    <div>
      <h2 style="margin-top:20px">Please select sports, dates, runners that you want BET!</h2>
      <treeselect v-model="value" :multiple="true" :options="options" :max-height="600" />
      <br />
      <button type="button" class="btn btn-dark" v-on:click="delete_item">delete</button>
      <button type="button" class="btn btn-dark" onclick="window.location.reload(true)">refresh</button>
      <button type="button" class="btn btn-dark" v-on:click="load_item">load</button>
    </div>
    <br />
    <br />
    <div id="app2">
      <h2 style="margin-top:20px">Please select sports you are intereted in!</h2>
      <treeselect v-model="value_select" :multiple="true" :options="options_select" :max-height="600" />
      <br />
      <button type="button" class="btn btn-dark" v-on:click="save_item_select">save</button>
    </div>
  </div>

  
</template>

<script>
  // import the component
  import Treeselect from '@riophae/vue-treeselect'
  // import the styles
  import '@riophae/vue-treeselect/dist/vue-treeselect.css'
  import axios from "axios";

  export default {
    // register the component
    middleware: ['auth'],
    components: { Treeselect },
    data() {
      return {
        // define the default value
        value: null,
        value_select: null,
        // define options
        options: [],
        combined: []
      }
    },
    async asyncData ({ app }) {
      try {
        const response_sport = await app.$axios.get("/api/events/loaditem")
        var sports_list = response_sport.data
        var only_sports_list = []
        var sports_length = sports_list.length;
        for(var x=0; x<sports_length; x++){
          only_sports_list.push({id:sports_list[x].id+'@'+sports_list[x].label, label:sports_list[x].label})
        }
        
        const response = await app.$axios.get('/api/events/')
        
        var events_data = response.data.results;
        var events_length = events_data.length;

        for(var x=0; x<events_length; x++){
          var tmp_item = events_data[x];
          var index;
          var filteredObj = sports_list.find(function(item, i){
            if(item.id == tmp_item.sport_id){
              index = i;
              return i;
            }
          });
          // get sport_item
          var tmp_sport = sports_list[index];
          if(tmp_sport.children == null) { // if sport_item doesn't have child
            tmp_sport.children = [
                                  {
                                    id: 'd@'+tmp_sport.id+'@'+tmp_item.start_time,
                                    label : tmp_item.start_time,
                                    children : [
                                      {
                                        id: 'e@'+tmp_item.event_id,
                                        label: tmp_item.event_name
                                      }
                                    ]
                                  }
                                ];
          }
          else { // if sport_item has some children
            index = -1;
            filteredObj = tmp_sport.children.find(function(item, i){
              if(item.id == 'd@'+tmp_sport.id+'@'+tmp_item.start_time){
                index = i;
                return i;
              }
            });
            if(index == -1) { // if sport_item does't have child as date
              tmp_sport.children.push(
                                  {
                                    id: 'd@'+tmp_sport.id+'@'+tmp_item.start_time,
                                    label : tmp_item.start_time,
                                    children : [
                                      {
                                        id: 'e@'+tmp_item.event_id,
                                        label: tmp_item.event_name
                                      }
                                    ]
                                  }
              );
            }
            else {
              tmp_sport.children[index].children.push(
                                  {
                                    id: 'e@'+tmp_item.event_id,
                                    label: tmp_item.event_name
                                  }
              );
            }
          }
        }
        return {
          value: null,
          options: sports_list,
          options_select: only_sports_list,
          error: false
        }
      } catch (e) { 
        console.log('error', e)
        return {
          value: [],
          error: true
        }
      }
    },
    methods: {
      delete_item: function (event) {
        if(this.value == null) return;
        var len = this.value.length;
        var req_key = [];

        for (var x=0; x<len; x++) {
          var str = ''+this.value[x];
          var tmp_arr = str.split('@');
          var sport_key = null;
          var time_key = null;
          var event_key = null;
          switch(tmp_arr.length) {
            case 1:
              sport_key = tmp_arr[0];
              break;
            case 2:
              event_key = tmp_arr[1];
              break;
            case 3:
              time_key = tmp_arr[2];
              sport_key = tmp_arr[1];
              break;
          }
          req_key.push({sport_key:sport_key, event_key:event_key, time_key:time_key});
        }

        this.$axios.post('/api/events/deleteitem/', {
          keys : req_key
        })
        .then(function (response) {
          //currentObj.output = response.data;
        })
        .catch(function (error) {
          //currentObj.output = error;
        });
      },
      load_item: function (event) {
        if(this.value == null) return;
        var len = this.value.length;
        var req_key = [];

        for (var x=0; x<len; x++) {
          var str = ''+this.value[x];
          var tmp_arr = str.split('@');
          var sport_key = null;
          var time_key = null;
          var event_key = null;
          switch(tmp_arr.length) {
            case 1:
              sport_key = tmp_arr[0];
              break;
            case 2:
              event_key = tmp_arr[1];
              break;
            case 3:
              time_key = tmp_arr[2];
              sport_key = tmp_arr[1];
              break;
          }
          req_key.push({sport_key:sport_key, event_key:event_key, time_key:time_key});
        }
        var vobj = this
        this.$axios.post('/api/combined/loaditem/', {
          keys : req_key
        })
        .then(function (response) {
          vobj.$store.dispatch('load_runner', response.data)
          vobj.$router.push('/configuration')
        })
        .catch(function (error) {
          //currentObj.output = error;
          console.log(error)
        });
      },

      save_item_select: function (event) {
        if(this.value_select == null) return;
        var len = this.value_select.length;
        var req_key = [];

        for (var x=0; x<len; x++) {
          var str = ''+this.value_select[x];
          var tmp_arr = str.split('@');
          req_key.push({id:tmp_arr[0], sport_id:tmp_arr[0], sport_name:tmp_arr[1]});
        }
        // var vobj = this
        this.$axios.post('/api/events/savetargetsportitem/', {
          keys : req_key
        })
        .then(function (response) {
          // 
        })
        .catch(function (error) {
          // 
        });
      }

    }
  }
</script>