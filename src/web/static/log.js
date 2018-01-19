const socket = io();
const log = document.getElementById('log');

// Scrolling option
const scroll_area = document.getElementById('scroll_area');
var scroll = true;  // scrolling is enabled by default

socket.on('connect', function() {
  var msg = 'WebSocket is connected.';
  console.log(msg);
  log.innerText += msg + '\n';
});

socket.on('disconnect', function(reason) {
  var msg = 'Reconnecting (' + reason + ')... ';
  console.log(msg);
  log.innerText += msg;
});

socket.on('log', function(msg) {
  console.log(msg);
  log.innerText += msg.data + '\n';
  if (scroll) {
    scroll_area.scrollIntoView(false);
  }
});

// Run when a checkbox is clicked.
// Detect changes and sync both top and bottom Scroll checkboxes.
function toggle_scroll(el) {
  console.log('scroll = ' + el.checked);
  scroll = el.checked;
  var els = document.getElementsByClassName('scroll');
  // Update the other checkbox
  for (var el_ of els) {
    if (el_ !== el) {
      el_.checked = el.checked;
    }
  }
}
