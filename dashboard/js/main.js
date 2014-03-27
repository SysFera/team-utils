var clock = document.getElementById("countdown")  
  , targetDate = new Date(2014, 03, 11);

clock.innerHTML = countdown(targetDate, null, countdown.WEEKS | countdown.DAYS | countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3).toString();
setInterval(function(){  
  clock.innerHTML = countdown(targetDate, null, countdown.WEEKS | countdown.DAYS | countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3).toString();
}, 1000);


var templateStats;

$.get('templates/projects.mustache.html', function(template) {
  templateStats = $(template).filter('#template-stats').html();
});

setInterval(function(){
  $.getJSON('data/data.json', function(data) {
    data["projects"].forEach(function(it){
      if (it.deadline < 24) {
        it.deadlineStatus = "status"
      } else if (it.deadline < 48) {
        it.deadlineStatus = "warning"
      } else {
        it.deadlineStatus = "danger"
      }
      it.deadline = it.deadline.toLocaleString()
    });
    $('#stats').html(Mustache.render(templateStats, data))
  });
}, 1000);