var app = new Vue({
  el: "#app",
  data: {
    t: "hey",
    tod: "time of day",
    values: []
  },
  methods: {
    handlerSystem: function(event) {
      data = JSON.parse(event['data']);
      this.tod = data.tod;
      this.values = data.values; 
    }
  }
});

var e = new EventSource('/stream');
e.addEventListener('system', app.handlerSystem);
e.onerror = function() { console.log('onclose') };
