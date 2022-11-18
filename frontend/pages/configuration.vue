<template>
  <div class="course-list-row">
    <table>
      <thead>
        <th scope="col"> Start date </th>
        <th scope="col"> Event name</th>
        <th scope="col">Market</th>
        <th scope="col">Status</th>
        <th scope="col">Inplay</th>
        <th scope="col">Position</th>
        <th scope="col">Runner</th>
        <th scope="col">Back Odds</th>
        <th scope="col">Lay Odds</th>
        <th scope="col">Trade type</th>
        <th scope="col">B1 trigger</th>
        <th scope="col">L2 trgger</th>
        <th scope="col">L1 trigger</th>
        <th scope="col">B2 trgger</th>
        <th scope="col">Auto Stake</th>
        <th scope="col">Back Stake</th>
        <th scope="col">Lay Stake</th>
        <th scope="col">Arm bot</th>
      </thead>
      <tbody v-if="combined.length==0" >
        <tr>
          <td colspan=10>There are no data</td>
        </tr>
      </tbody>
      <tbody v-if="combined.length>0" >
        <tr v-for="row in combined" :key="row.runner_id" >

          <td>{{ row.event.start_time }}</td>
          <td>{{ row.event.event_name }}</td>
          <td>{{ row.market.market_name }}</td>
          <td>{{ row.market.status }}</td>
          <td>{{ row.market.is_ip }}</td>
          <td>{{ row.order.rem_pot_pro }}</td>
          <td>{{ row.name }}</td>
          <td>{{ row.back_odds }}</td>
          <td>{{ row.lay_odds }}</td>

          <td>
            <b-form-select v-model="row.bettriggers.tigger_mode"
                          v-on:change="selectBackOrLay($event, row.runner_id)"
                          :options="optionlay" style="width:100px"></b-form-select>
          </td>
          <td>
            <b-form-input type="text"
                          v-model="row.bettriggers.b1_trig"
                          v-show="row.bettriggers.show1"
                          v-on:change="changeB1Trig($event, row.runner_id)"
                          style="width:64px"></b-form-input>
          </td>
          <td>
            <b-form-input type="text"
                          v-model="row.bettriggers.l2_trig"
                          v-show="row.bettriggers.show1"
                          v-on:change="changeL2Trig($event, row.runner_id)"
                          style="width:64px"></b-form-input>
          </td>
          <td>
            <b-form-input type="text"
                          v-model="row.bettriggers.l1_trig"
                          v-show="row.bettriggers.show2"
                          v-on:change="changeL1Trig($event, row.runner_id)"
                          style="width:64px"></b-form-input>
          </td>
          <td>
            <b-form-input type="text"
                          v-model="row.bettriggers.b2_trig"
                          v-show="row.bettriggers.show2"
                          v-on:change="changeB2Trig($event, row.runner_id)"
                          style="width:64px"></b-form-input>
          </td>
          <td>
            <b-form-select v-model="row.stakes.round_bal"
                          :options="options"
                          v-on:change="selectAutoStakes($event, row.runner_id)"
                          style="width:72px"></b-form-select>
          </td>
          <td>
            <b-form-input type="text"
                          v-model="row.userstakes.back_stake"
                          v-show="row.userstakes.show"
                          v-on:change="changeBackStake($event, row.runner_id)"
                          style="width:64px"></b-form-input>
          </td>
          <td>
            <b-form-input type="text"
                          v-model="row.userstakes.lay_stake"
                          v-show="row.userstakes.show"
                          v-on:change="changeLayStake($event, row.runner_id)"
                          style="width:64px"></b-form-input>
          </td>
          <td>
            <b-form-checkbox v-model="row.bettriggers.armbot" style="max-width:40px"
                            v-on:change="selectArmBot($event, row.runner_id)"
                            ></b-form-checkbox>
          </td>

        </tr>
      </tbody>
      
    </table>
    <button type="button" class="btn btn-dark" v-on:click="save_config">Save</button>
  </div>
</template>

<script>
import BacklayStakes from '~/components/BacklayStakes.vue';
import PriceTriggers from '~/components/PriceTriggers.vue';
import PercentageStakes from '~/components/PercentageStakes.vue';
import UserStakes from '~/components/UserStakes.vue';
import armbot from '~/components/armbot.vue';

//import axios from "axios";

export default {
  
  middleware: ['auth'],

  components:{
    BacklayStakes,
    PriceTriggers,
    PercentageStakes,
    UserStakes,
    armbot
  },
  data() {
    var combined = this.$store.state.runner
    var tmp_len = 0
    if(combined) {
      tmp_len = combined.length
    }
    else {
      combined = []
    }
    for (var tmp_index = 0; tmp_index < tmp_len; tmp_index ++ ) {
      if(combined[tmp_index].bettriggers == null) {
        combined[tmp_index].bettriggers = {
          b1_trig : null,
          b2_trig : null,
          l1_trig : null,
          l2_trig : null,
          tigger_mode : null,
          armbot : false
        }
      }
      combined[tmp_index].bettriggers.show1 = (combined[tmp_index].bettriggers.tigger_mode==0)?true:false
      combined[tmp_index].bettriggers.show2 = (combined[tmp_index].bettriggers.tigger_mode==1)?true:false
      if(combined[tmp_index].stakes == null) {
        combined[tmp_index].stakes = {
          percent_1 : 0,
          percent_2 : 0,
          percent_3 : 0,
          percent_4 : 0,
          percent_5 : 0,
          percent_6 : 0,
          percent_7 : 0,
          percent_8 : 0,
          percent_9 : 0,
          percent_10 : 0,
          round_bal : null
        }
      }
      if(combined[tmp_index].userstakes == null) {
        combined[tmp_index].userstakes = {
          back_stake : null,
          lay_stake : null
        }
      }
      combined[tmp_index].userstakes.show = combined[tmp_index].stakes.round_bal==null?true:false

      if(combined[tmp_index].order == null) {
        combined[tmp_index].order = {
          market_id : null,
          temp_id :null,
          event_name : '',
          time_stamp : '',
          event_id : null,
          market_name : '',
          market_type : '',
          runner_id : null,
          runner_name : '',
          side : '',
          odds : 0,
          odds_type : '',
          stake : 0,
          remaining : 0,
          pot_pro : 0,
          rem_pot_pro : 0,
          pot_lib : 0,
          created_at : null,
          status : '',
          inplay : ''
        }
      }
      combined[tmp_index].order.show = (combined[tmp_index].order.pot_pro != 0)?combined[tmp_index].order.pot_pro:combined[tmp_index].order.pot_lib
    }

    return {
      events: [],
      markets: [],
      combined: combined,
      changed: [],
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
      ],
      optionlay: [
        { value: null, text: '' },
        { value: 0, text: 'Back first' },
        { value: 1, text: 'Lay first' }
      ]
    }
  },
  async asyncData ({ app }) {
    try {
      const events = await app.$axios.get('/api/events/')
      const markets = await app.$axios.get('/api/markets/')

      return {
        events: events.data.results,
        markets: markets.data.results,
        // combined: response.data.results,
        error: false
      }
    } catch (e) {
      console.log('error', e)
      return {
        events: [],
        markets:[],
        // combined: [],
        error: true
      }
    }
  },
  methods: {
    selectBackOrLay: function(value, runner_id) {
      var filteredObj = this.findRow(runner_id)
      filteredObj.bettriggers.tigger_mode = value
      filteredObj.bettriggers.show1 = (filteredObj.bettriggers.tigger_mode==0)?true:false
      filteredObj.bettriggers.show2 = (filteredObj.bettriggers.tigger_mode==1)?true:false
      this.saveChange(runner_id)
    },
    changeB1Trig: function(value, runner_id) {
      var filteredObj = this.findRow(runner_id)
      filteredObj.bettriggers.b1_trig = value
      this.saveChange(runner_id)
    },
    changeL2Trig: function(value, runner_id) {
      var filteredObj = this.findRow(runner_id)
      filteredObj.bettriggers.l2_trig = value
      this.saveChange(runner_id)
    },
    changeL1Trig: function(value, runner_id) {
      var filteredObj = this.findRow(runner_id)
      filteredObj.bettriggers.l1_trig = value
      this.saveChange(runner_id)
    },
    changeB2Trig: function(value, runner_id) {
      var filteredObj = this.findRow(runner_id)
      filteredObj.bettriggers.b2_trig = value
      this.saveChange(runner_id)
    },
    selectAutoStakes: function(value, runner_id) {
      var filteredObj = this.findRow(runner_id)
      filteredObj.stakes.round_bal = value
      filteredObj.userstakes.show = (filteredObj.stakes.round_bal==null)?true:false
      this.saveChange(runner_id)
    },
    changeBackStake: function(value, runner_id) {
      var filteredObj = this.findRow(runner_id)
      filteredObj.userstakes.back_stake = value
      this.saveChange(runner_id)
    },
    changeLayStake: function(value, runner_id) {
      var filteredObj = this.findRow(runner_id)
      filteredObj.userstakes.lay_stake = value
      this.saveChange(runner_id)
    },
    selectArmBot: function(value, runner_id) {
      var filteredObj = this.findRow(runner_id)
      filteredObj.bettriggers.armbot = value
      this.saveChange(runner_id)
    },
    findRow: function(runner_id){
      var index;
      var filteredObj = this.combined.find(function(item, i){
        if(item.runner_id == runner_id){
          index = i
          return i;
        }
      });
      return this.combined[index]
    },
    saveChange: function(runner_id) {
      //
      var index = -1;
      var tmp_obj = this.findRow(runner_id)
      var filteredObj = this.changed.find(function(item, i){
        if(item.runner_id == runner_id){
          index = i
          return i;
        }
      });
      if(index >= 0){
        this.changed[index] = tmp_obj
      }
      else {
        this.changed.push(tmp_obj)
      }
    },
    save_config: function(){
      console.log(this.changed)
      this.$axios.post('/api/combined/saveitem/', {
        keys : this.changed
      })
      .then(function (response) {
        console.log(response)
      })
      .catch(function (error) {
        console.log(error)
      });
    }
  }
};




</script>


<style>

th, td {
font-family: ‘Lato’, sans-serif;
font-size: 12px;
font-weight: 400;
padding: 10px;
text-align: left;
width: 0%;
}


</style>
