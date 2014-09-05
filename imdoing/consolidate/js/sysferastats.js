var containerChart, containerRange
    , rackCharts = {}
    , ndx, all, domainDate, currentFilter = dc.filterAll()
    , dateDimension, dateDimensionPowerSum
    , d3locale, formatScientific, formatNumber, formatDate, formatFilterDate
    , serverMetrics = ["cpu", "ram", "hdd"]
    , rackList = ["A", "B", "C", "D"];

function a15MinutesRound(date) {
  var minutes = 15;
  var timezone = date.getTimezoneOffset();
  return new Date((Math.floor(date / 6e4 / minutes - timezone) + timezone) * 6e4 * minutes);
}

// d3 localization
if ((locale == "fr") || (locale == "fr_FR")) {
  d3locale = d3.locale({
    "decimal": ",",
    "thousands": ".",
    "grouping": [3],
    "currency": ["", " €"],
    "dateTime": "%a %e %b %Y %X (GMT%Z)",
    "date": "%d/%m/%Y",
    "time": "%H:%M:%S",
    "periods": ["", ""],
    "days": ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"],
    "shortDays": ["dim.", "lun.", "mar.", "mer.", "jeu.", "ven.", "sam."],
    "months": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
    "shortMonths": ["janv.", "févr.", "mars", "avril", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
  });
  formatDate = d3locale.timeFormat.multi([
    ["%H:%M", function(d) { return d.getMinutes(); }],
    ["%Hh", function(d) { return d.getHours(); }],
    ["%a %e", function(d) { return d.getDay() && d.getDate() != 1; }],
    ["%a %e", function(d) { return d.getDate() != 1; }],
    ["%a %e %B", function(d) { return d.getMonth(); }],
    ["%Y", function() { return true; }]
  ]);
  formatFilterDate = d3locale.timeFormat("%A %e %b, %H:%M");
  formatScientific = d3locale.numberFormat("^,.1s");
  formatNumber = d3locale.numberFormat("f");
} else {
  formatDate = d3.time.format.multi([
    ["%I:%M %p", function(d) { return d.getMinutes(); }],
    ["%I %p", function(d) { return d.getHours(); }],
    ["%a %e", function(d) { return d.getDay() && d.getDate() != 1; }],
    ["%a %e", function(d) { return d.getDate() != 1; }],
    ["%a, %B %e", function(d) { return d.getMonth(); }],
    ["%Y", function() { return true; }]
  ]);
  formatFilterDate = d3.time.format("%A, %B %e, %H:%M");
  formatScientific = d3.format("^,.2s");
  formatNumber = d3.format("f");
}
// end d3 localization

function createServerCharts() {
  $("div[id^='server-cpu-']").each(function (idx, el) {
    createServerChart(el);
  });
}

function createServerChart(el) {
  // let's get the server's id
  var id = el.id.replace('server-cpu-','');
  // let's get the rack's position
  var pos = $(el).parents(".rackTab").attr('id').replace("rack","");

  rackCharts[pos].servers[id] = {};

  // now we can create the charts for each metric (except power)
  $.each(serverMetrics, function(idx, metric) {
    rackCharts[pos].servers[id][metric] = {};

    rackCharts[pos].servers[id][metric].group = dateDimension.group().reduceSum(function (d) {
      if ((d.s == id) && (d.ty == metric)) {
        return d.v;
      } else {
        return 0;
      }
    });

    rackCharts[pos].servers[id][metric].chart = dc.lineChart("#server-"+metric+"-"+id, "rack" + pos)
        .width(220)
        .height(100)
        .yAxisPadding("10%")
        .transitionDuration(750)
        .dimension(dateDimension)
        .group(rackCharts[pos].servers[id][metric].group)
        .x(d3.time.scale().domain(domainDate))
        .round(d3.time.hour)
        .xUnits(d3.time.hours)
        .brushOn(false)
        .renderHorizontalGridLines(true)
        .title(function(d){
          var value = d.data.value;
          if(isNaN(value)) value = 0;
          return formatNumber(value) + "% " + metric.toUpperCase() + " - " + formatDate(d.data.key);
        })
        .renderArea(true);
    rackCharts[pos].servers[id][metric].chart.yAxis().tickValues([0, 20, 40, 60, 80, 100]);
    rackCharts[pos].servers[id][metric].chart.xAxis().ticks(3);
    rackCharts[pos].servers[id][metric].chart.xAxis().tickFormat(function (d) {
      return formatDate(d);
    });

  });
}

function createRackCharts() {
  $.each(rackList, function(idx, pos) {
    createRackChart(pos);
  });
}

function createRackChart(pos) {
  rackCharts[pos] = {};
  rackCharts[pos].rendered = false;
  rackCharts[pos].servers = {};

  rackCharts[pos].dimension = dateDimension.group().reduceSum(function (d) {
    if ((d.r == pos) && d.ty == "power" ) {
      return d.v;
    } else {
      return 0;
    }
  });

  rackCharts[pos].range = dc.lineChart("#rack"+pos+"Range", "rack"+pos)
      .width(700)
      .height(100)
      .yAxisPadding("10%")
      .transitionDuration(750)
      .dimension(dateDimension)
      .group(rackCharts[pos].dimension)
      .elasticY(true)
      .renderArea(true)
      .x(d3.time.scale().domain(domainDate))
      .round(d3.time.hour)
      .xUnits(d3.time.hours)
      .brushOn(true)
      .filterPrinter(function (filters) {
        var filter = filters[0], s = "";
        s += formatFilterDate(filter[0]) + " -> " + formatFilterDate(filter[1]);
        return s;
      });
  rackCharts[pos].range.yAxis().ticks(2);
  rackCharts[pos].range.yAxis().tickFormat(function (d) {
    return formatScientific(d);
  });
  rackCharts[pos].range.xAxis().tickFormat(function (d) {
    return formatDate(d);
  });

  rackCharts[pos].chart = dc.lineChart("#rack"+pos+"Chart", "rack"+pos)
      .width(700)
      .height(200)
      .yAxisPadding("10%")
      .transitionDuration(750)
      .dimension(dateDimension)
      .group(rackCharts[pos].dimension)
      .x(d3.time.scale().domain(domainDate))
      .rangeChart(rackCharts[pos].range)
      .round(d3.time.hour)
      .xUnits(d3.time.hours)
      .renderArea(true)
      .brushOn(false)
      .renderHorizontalGridLines(true)
      .title(function(d){
        var value = d.data.value;
        if(isNaN(value)) value = 0;
        return formatNumber(value) + "W - " + formatDate(d.data.key);
      })
      .elasticY(true);
  rackCharts[pos].chart.yAxis().ticks(5);
  rackCharts[pos].chart.yAxis().tickFormat(function (d) {
    return formatScientific(d);
  });
  rackCharts[pos].chart.xAxis().tickFormat(function (d) {
    return formatDate(d);
  });
}

function computeDomainDate(dateDimension) {
  var startCalculated = dateDimension.bottom(1)[0]["d"];
  var endCalculated = dateDimension.top(1)[0]["d"];

  return [startCalculated, endCalculated];
}

function preprocess(row) {
  row.d = new Date(row.ts);
  return row;
}

function process(d) {
  // d.s = the server's id
  // d.r = the rack's position (A, B, C, D)
  // d.ts = the measure's timestamp
  // d.ty = the metric's type
  // d.v = the measure's value

  d.forEach(function (row) {
    return preprocess(row)
  });
  ndx = crossfilter(d);
  all = ndx.groupAll();

  dateDimension = ndx.dimension(function (d) {
    return a15MinutesRound(d.d);
    return d3.time.hour(d.d);
  });
  dateDimensionPowerSum = dateDimension.group().reduceSum(function (d) {
    if (d.ty == "power") {
      return d.v;
    } else {
      return 0;
    }
  });

  domainDate = computeDomainDate(dateDimension);

  containerRange = dc.lineChart("#containerRange")
      .width(700)
      .height(100)
      .yAxisPadding("10%")
      .transitionDuration(750)
      .dimension(dateDimension)
      .group(dateDimensionPowerSum)
      .elasticY(true)
      .renderArea(true)
      .x(d3.time.scale().domain(domainDate))
      .round(d3.time.hour)
      .filterPrinter(function (filters) {
        var filter = filters[0], s = "";
        s += formatFilterDate(filter[0]) + " -> " + formatFilterDate(filter[1]);
        return s;
      });
  containerRange.yAxis().ticks(2);
  containerRange.yAxis().tickFormat(function (d) {
    return formatScientific(d);
  });
  containerRange.xAxis().tickFormat(function (d) {
    return formatDate(d);
  });

  containerChart = dc.lineChart("#containerChart")
      .width(700)
      .height(200)
      .yAxisPadding("10%")
      .transitionDuration(750)
      .dimension(dateDimension)
      .group(dateDimensionPowerSum)
      .x(d3.time.scale().domain(domainDate))
      .rangeChart(containerRange)
      .round(d3.time.hour)
      .xUnits(d3.time.hours)
      .renderArea(true)
      .brushOn(false)
      .turnOnControls(true)
      .title(function(d){
        var value = d.data.value;
        if(isNaN(value)) value = 0;
        return formatNumber(value) + "W " + " - " + formatDate(d.data.key);
      })
      .renderHorizontalGridLines(true)
      .elasticY(true);
  containerChart.yAxis().ticks(5);
  containerChart.yAxis().tickFormat(function (d) {
    return formatScientific(d);
  });
  containerChart.xAxis().tickFormat(function (d) {
    return formatDate(d);
  });

  createRackCharts();
  createServerCharts();

  containerRange.on("filtered", function (chart) {
    var filters = chart.filters();
    if (filters.length > 0) {
      currentFilter = [filters[0][0], filters[0][1]];
    } else {
      currentFilter = chart.filter();
    }
    $("#global .pleasewait").hide();

    dc.events.trigger(function () {
      containerChart.focus(currentFilter);
      dc.redrawAll();
    }, 500);
  });

  $.each(rackList, function(idx, pos) {
    rackCharts[pos].range.on("filtered", function (chart) {
      var filters = chart.filters();
      if (filters.length > 0) {
        currentFilter = [filters[0][0], filters[0][1]];
      } else {
        currentFilter = chart.filter();
      }

      dc.events.trigger(function () {
        rackCharts[pos].chart.focus(currentFilter);
        $.each(rackCharts[pos].servers, function(index, server) {
          $.each(serverMetrics, function(idx, metric){
            server[metric].chart.focus(currentFilter);
          });
        });
        dc.redrawAll("rack"+pos);
      }, 300);

    });
  });

  $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    setTimeout(function() {
      var current = e.target.hash;
      var targetRange, pos;

      if (current == "#global" ) {
        targetRange = containerRange;
      } else {
        pos = current.replace("#rack","");
        // check if that particular rackChart group has already been rendered; if not, do it.
        if (!rackCharts[pos].rendered) {
          $("#rack" + pos + " .pleasewait").hide();
          dc.renderAll("rack" + pos);
          rackCharts[pos].rendered = true;
        }
        targetRange = rackCharts[pos].range;
      }

      if (currentFilter) {
        var backup = currentFilter;
        targetRange.filterAll();
        currentFilter = backup;
        targetRange.filter(currentFilter);
      } else {
        targetRange.filterAll();
      }
    }, 200);
  });

  dc.renderAll();

  // filter by default on the last 12 hours, unless the data we have covers a shorter span
  var diff = (domainDate[1].getTime() - domainDate[0].getTime()) / (1000*3600); // difference in hours
  if (diff > 12) {
    var newStart = new Date(domainDate[1].getTime() - 12*60*60*1000);
    containerRange.filter([newStart, domainDate[1]]);
  }
}
function dataEmpty() {
  var html = '<div class="pleasewait lead alert alert-danger text-center">';
  html += '<i class="fa fa-warning"></i>&nbsp;';
  html += DATAERROR;
  html += '</div>';

  updatePW(html);
}
function updatePW(html) {
  $(".pleasewait").replaceWith(html);
}

function loadData(dataSource) {
  d3.json(dataSource,
      function(error, json) {
        if (json.length <= 0) { dataEmpty(); }
        else { process(json); }
      }
  );
}