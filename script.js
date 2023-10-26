"use strict";

// Sample Data Munging, see PY equivalent in index.py

let student_data = [
  { 'name': 'Bob', 'id': 0, 'scores': [68, 75, 56, 81] },
  { 'name': 'Alice', 'id': 1, 'scores': [75, 90, 64, 88] },
  { 'name': 'Carol', 'id': 2, 'scores': [59, 74, 71, 68] },
  { 'name': 'Dan', 'id': 3, 'scores': [64, 58, 53, 62] },
];

function processStudentData(data, passThreshold = 60, meritThreshold = 75) {
  data.forEach((sdata) => {
    let av = sdata.scores.reduce((a, b) => a + b, 0) / sdata.scores.length;

    if (av > meritThreshold) {
      sdata.assessment = "passed with merit";
    } else if (av > passThreshold) {
      sdata.assessment = "passed";
    } else {
      sdata.assessment = "failed";
    }

    console.log(`${sdata.name}'s (id: ${sdata.id})
      final assessment is: ${sdata.assessment.toUpperCase()}`);
  });
}

// let sel = d3.select('#viz')
//   .attr('width', '600px')
//   .attr('height', '400px')
//   .style('background', 'lightgray');

let chartCircles = (data) => {
  let chart = d3.select("#chart-h");
  chart
    .attr('height', data.height)
    .attr('width', data.width);
  chart
    .selectAll('circle')
    .data(data.circles)
    .enter()
    .append('circle')
    .attr('cx', (d) => d.x)
    .attr('cy', (d) => d.y)
    .attr('r', (d) => d.r)
    .attr('fill', 'red');
};

let data = {
  width: 300, height: 150,
  circles: [
    { 'x': 50, 'y': 30, 'r': 20 },
    { 'x': 70, 'y': 80, 'r': 10 },
    { 'x': 160, 'y': 60, 'r': 10 },
    { 'x': 200, 'y': 100, 'r': 5 },
  ]
};

chartCircles(data)
