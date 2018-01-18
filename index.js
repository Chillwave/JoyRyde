var OBDReader = require('serial-obd');
var options = {};
options.baudrate = 115200;
var serialOBDReader = new OBDReader("/dev/rfcomm0", options);
var dataReceivedMarker = {};

serialOBDReader.on('dataReceived', function (data) {
    console.log(data);
    dataReceivedMarker = data;
});

serialOBDReader.on('connected', function (data) {
    this.addPoller("vss");
    this.addPoller("rpm");
    this.addPoller("temp");
    this.addPoller("load_pct");
    this.addPoller("map");
    this.addPoller("frp");

    this.startPolling(2000); //Polls all added pollers each 2000 ms.
});

serialOBDReader.connect();
