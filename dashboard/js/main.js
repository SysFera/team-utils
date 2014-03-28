// Variables
var clock = $("#countdown")
  , sprintEnd, sprintDanger
  , statsClient = $('#statsClient')
  , statsSysFera = $('#statsSysFera')
  , statsEquipe = $('#statsEquipe')
  , jenkinsBuilds = $('#jenkinsBuilds')
  , nextSprint = new Date(2014, 03, 11, 18)
  , refreshTime = 10000
  , templates, templateStatsClient, templateStatsEquipe;

// Initial templates gathering. Done only once.
$.get('templates/templates.mustache.html', function(data) {
  templates = $(data);
  templateStatsClient = templates.filter('#templateStatsClient').html();
  templateStatsSysFera = templates.filter('#templateStatsSysFera').html();
  templateStatsEquipe = templates.filter('#templateStatsEquipe').html();
  templateJenkins = templates.filter('#templateJenkins').html();
});

// main refreshDisplay function
function refreshDisplay() {
  // Create and display the the countdown
  sprintEnd = countdown(nextSprint, null, countdown.WEEKS | countdown.DAYS | countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3);
  clock.html(sprintEnd.toString());
  sprintDanger = (sprintEnd.value + 432000000) > 0
  $("#sprintEnd").toggleClass( "sprintDanger", sprintDanger );
  // Query the project data JSON, render it against the Mustache template, and insert it in the project body tables
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
    statsClient.html(Mustache.render(templateStatsClient, dataProjects))
    statsSysFera.html(Mustache.render(templateStatsSysFera, dataProjects))
  });
  // Query the team data JSON, render it against the Mustache template, and insert it in the Team body table
  $.getJSON('data/dataTeam.json', function(dataTeam) {
    dataTeam["members"].forEach(function(member){
      if (member.issues.open < 3) {
        member.wipStatus = "success"
      } else {
        member.wipStatus = "danger"
      }
    });
    statsEquipe.html(Mustache.render(templateStatsEquipe, dataTeam))
  });
  // Query the team data JSON, render it against the Mustache template, and insert it in the Team body table
  $.getJSON('data/dataJenkins.json', function(dataJenkins) {
    jenkinsBuilds.html(Mustache.render(templateJenkins, dataJenkins))
  });
}

refreshDisplay();

setInterval(function(){  
  refreshDisplay();
}, refreshTime);