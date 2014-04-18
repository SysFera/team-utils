// Variables
var clock = $("#countdown")
  , statsClient = $('#statsClient')
  , statsSysFera = $('#statsSysFera')
  , statsEquipe = $('#statsEquipe')
  , jenkinsBuilds = $('#jenkinsBuilds')
  , github = $('#github')
  , deployments = $('#deployments')
  , templates, templateStatsSysFera, templateStatsClient, templateStatsEquipe, templateJenkins, templateGithub, templateDeployments;

$.ajaxSetup({ cache: false });

// Initial templates gathering. Done only once.
$.get('templates/templates.mustache.html', function(data) {
  templates = $(data);
  templateStatsClient = templates.filter('#templateStatsClient').html();
  templateStatsSysFera = templates.filter('#templateStatsSysFera').html();
  templateStatsEquipe = templates.filter('#templateStatsEquipe').html();
  templateJenkins = templates.filter('#templateJenkins').html();
  templateDeployments = templates.filter('#templateDeployments').html();
  templateGithub = templates.filter('#templateGithub').html();
});

// main refreshDisplay function
function refreshDisplay() {

  // Query the config file and create a display using the end date
  $.getJSON('data/config.json', function(data) {

    // sets the page's refresh time
    var refreshTime = data['global']['refreshtime'];
    setInterval(function(){  
      location.reload();
    }, refreshTime);

    // sets the date of the sprint's end
    var nextSprint = new Date(
      data['sprint']['end']['year'],
      // months in JS are an index, so e.g., April is 3 and not 4
      data['sprint']['end']['month'] - 1,
      data['sprint']['end']['day'],
      18, 0, 0);
    var sprintEnd = countdown(nextSprint, null, countdown.WEEKS | countdown.DAYS | countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3);
    clock.html(sprintEnd.toString());
    var sprintDanger = (sprintEnd.value + 432000000) > 0;
    $("#sprintEnd").toggleClass( "sprintDanger", sprintDanger );
  });

  // Query the project data JSON, render it against the Mustache template, and insert it in the project body tables
  $.getJSON('data/dataProjects.json', function(dataProjects) {
    dataProjects["customers"].forEach(function(it){
      if (it.deadline < 24) {
        it.deadlineStatus = "success"
      } else if (it.deadline < 48) {
        it.deadlineStatus = "warning"
      } else {
        it.deadlineStatus = "danger"
      }
      it.deadline = it.deadline.toLocaleString()
    });
    statsClient.html(Mustache.render(templateStatsClient, dataProjects));
    statsSysFera.html(Mustache.render(templateStatsSysFera, dataProjects));
  })
    .fail(function() {
      statsClient.html(Mustache.render(templateStatsClient, []));
      statsSysFera.html(Mustache.render(templateStatsSysFera, []));
    });

  // Query the team data JSON, render it against the Mustache template, and insert it in the Team body table
  $.getJSON('data/dataTeam.json', function(dataTeam) {
    dataTeam["users"].forEach(function(member){
      if (member.issues.open == 0) {
        member.wipStatus = "danger"
      } else if (member.issues.open > 3) {
        member.wipStatus = "danger"
      } else if (member.issues.open > 2) {
        member.wipStatus = "warning"
      } else {
        member.wipStatus = "success"
      }
    });
    statsEquipe.html(Mustache.render(templateStatsEquipe, dataTeam));
  })
    .fail(function() {
      statsEquipe.html(Mustache.render(templateStatsEquipe, []));
    });

  // Query the Jenkins data JSON, render it against the Mustache template, and insert it in the Jenkins builds table
  $.getJSON('data/dataJenkins.json', function(dataJenkins) {
    jenkinsBuilds.html(Mustache.render(templateJenkins, dataJenkins));
  })
    .fail(function() {
      jenkinsBuilds.html(Mustache.render(templateJenkins, []));
    });

  // Query the Changelogs JSON, render it against the Mustache template, and insert it in the Changelogs div  
  $.getJSON('data/dataGithub.json', function(dataGithub) {
    github.html(Mustache.render(templateGithub, dataGithub))
  })
    .fail(function() {
      github.html(Mustache.render(templateGithub, []));
    });

  // Query the deployment monitoring JSON, render it against the Mustache template, and insert it in the deployments div
  $.getJSON('data/dataDeployments.json', function(dataDeployments) {
      dataDeployments["clients"].forEach(function(client){
        if (client.overall == "OK") {
          client.status = "success"
        } else if (client.overall == "NOK") {
          client.status = "danger"
        } else {
          client.status = "warning"
        }
        if (client.failed > 0) {
          client.errors = "true"
        }
      });
      deployments.html(Mustache.render(templateDeployments, dataDeployments));
  })
    .fail(function() {
      deployments.html(Mustache.render(templateDeployments, []));
    });
}

refreshDisplay();