// Bar chart
// let data = [23,34, 54, 56, 57]

// let power_num = d3.scaleLinear()
//     .domain([0, d3.max(data)])
//     .range([0,570]);

// d3.select(".chart")
//     .selectAll("div")
//     .data(data)
//         .enter()
//         .append("div")
//         .style("width", function(d){return power_num(d) + "px";})
//         .text(function(d) { return d;} );

// Line Chart Example

// Define dataset
dataset = [
  {
    'date': '2011-07-01T19:14:34.000Z',
    'value': 58.13
  },
  {
    'date': '2011-07-01T19:13:34.000Z',
    'value': 53.98
  },
  {
    'date': '2011-07-01T19:12:34.000Z',
    'value': 67.00
  },
  {
    'date': '2011-07-01T19:11:34.000Z',
    'value': 89.70
  },
  {
    'date': '2011-07-01T19:10:34.000Z',
    'value': 99.00
  }
]

margin = {
  'top': 20,
  'right': 20,
  'bo'
}

parseDate = d3.timeFormat("%Y-%m-%dT%H:%M:%S.%LZ").parse;

dataset.forEach(element => {
    element.date = d3.timeParse(element.date);
    element.value += element.value
    return 
});

svg = d3.select('main')
    .append('svg')
    .attr('width', '100px')
    .attr('height', '100px')
    .append('g')

x = d3.timeScale()
    .domain(d3.extent(dataset, d => {
        d.date
    })).range([0, width])

y = d3.scaleLinear()
    .domain([0, 1.05*d3.max(dataset, element =>{ Math.max(element.value)})])
    .range([height, 0])

xAxis = d3.svg.axis()


