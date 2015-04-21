
function load_js(target) {
 var head = document.getElementsByTagName('HEAD').item(0);
 var script = document.createElement("script");
 script.type = 'text/javascript';
 script.src = target;
 head.appendChild(script);
}

load_js('http://ajax.googleapis.com/ajax/libs/jquery/1.3.1/jquery.min.js');

function addLoadEvent(f) {
  $(document).ready(function(){f();});
}