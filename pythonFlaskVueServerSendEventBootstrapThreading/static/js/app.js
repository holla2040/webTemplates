var app = new Vue({
  el: "#app",
  data: {
    t: "hey",
    tod: "time of day"
  },
  methods: {
    handlerSystem: function(event) {
      data = JSON.parse(event['data']);
      console.log(data);
      this.tod = data.tod;
      this.t = data.t;
    }
  }
});

var e = new EventSource('/stream');
e.addEventListener('system', app.handlerSystem);
e.onerror = function() { console.log('onclose') };
