var clock = document.getElementById("countdown")  
  , targetDate = new Date(2014, 03, 11);

clock.innerHTML = countdown(targetDate, null, countdown.WEEKS | countdown.DAYS | countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3).toString();
setInterval(function(){  
  clock.innerHTML = countdown(targetDate, null, countdown.WEEKS | countdown.DAYS | countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3).toString();
}, 1000);

var templates, templateStatsClient, templateStatsEquipe;

$.get('templates/templates.mustache.html', function(data) {
  templates = $(data);
  templateStatsClient = templates.filter('#templateStatsClient').html();
  templateStatsSysFera = templates.filter('#templateStatsSysFera').html();
  templateStatsEquipe = templates.filter('#templateStatsEquipe').html();
});

// Query the project data JSON, render it against the Mustache template, and insert it in the project body tables
setInterval(function(){
  $.getJSON('data/dataProjects.json', function(dataProjects) {
    dataProjects["projetsClient"].forEach(function(it){
      if (it.deadline < 24) {
        it.deadlineStatus = "success"
      } else if (it.deadline < 48) {
        it.deadlineStatus = "warning"
      } else {
        it.deadlineStatus = "danger"
      }
      it.deadline = it.deadline.toLocaleString()
    });
    $('#statsClient').html(Mustache.render(templateStatsClient, dataProjects))
    $('#statsSysFera').html(Mustache.render(templateStatsSysFera, dataProjects))
  });
}, 1000);

// Query the team data JSON, render it against the Mustache template, and insert it in the Team body table
setInterval(function(){
  $.getJSON('data/dataTeam.json', function(dataTeam) {
    dataTeam["members"].forEach(function(member){
      if (member.issues.open < 3) {
        member.wipStatus = "success"
      } else {
        member.wipStatus = "danger"
      }
    });
    $('#statsEquipe').html(Mustache.render(templateStatsEquipe, dataTeam))
  });
}, 1000);