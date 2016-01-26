function makePlot(data, selector){

  //var data = [4, 8, 15, 16, 23, 42];

  var dataset = data //[

  var x = d3.scale.linear()
      .domain([0, d3.max(data)])
      .range([0, 200]);

  d3.select(selector)
    .selectAll("div")
      .data(data)
    .enter().append("div")
      .style("width", function(d) { return x(d) + "px"; })
      .text(function(d) { return Math.round(d * 100) / 100 + '%'; });
}