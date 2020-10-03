var app = new Vue({
  el: "#app",
  data: {
    tod: "time of day",
    readings : "readings"
  },
  methods: {
    handlerSystem: function(event) {
      data = JSON.parse(event['data']);
      if (data.tod) {
        this.tod = data.tod;
      }
      if (data.event) {
        this.readings = JSON.parse(data.event).reading;
      }
    }
  }
});

var e = new EventSource('/stream');
e.addEventListener('system', app.handlerSystem);
e.onerror = function() { console.log('onclose') };
