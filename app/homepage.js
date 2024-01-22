// Function to create the bubble chart
function createBubbleChart() {
    fetch('/data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (Array.isArray(data)) {
                // Initialize SVG and scales
                var svgWidth = 1000, svgHeight = 600;
                var margin = { top: 50, right: 50, bottom: 50, left: 50 };
                var width = svgWidth - margin.left - margin.right;
                var height = svgHeight - margin.top - margin.bottom;

                var svg = d3.select('#bubbleChart')
                    .attr('width', svgWidth)
                    .attr('height', svgHeight);

                var chartArea = svg.append('g')
                    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

                // Create scale for bubble size
                var radiusScale = d3.scaleSqrt()
                    .domain([0, d3.max(data, function(d) { return d.population; })])
                    .range([0, 50]);

                // Force simulation
                var simulation = d3.forceSimulation(data)
                    .force("charge", d3.forceManyBody().strength(5))
                    .force("center", d3.forceCenter(width / 2, height / 2))
                    .force("collision", d3.forceCollide().radius(function(d) {
                        return radiusScale(d.population);
                    }))
                    .on("tick", ticked);

                function ticked() {
                    bubbles
                        .attr("cx", function(d) { return d.x; })
                        .attr("cy", function(d) { return d.y; });
                }

                // Create bubbles
                var bubbles = chartArea.selectAll('.bubble')
                    .data(data)
                    .enter().append('circle')
                    .attr('class', 'bubble')
                    .attr('r', function(d) { return radiusScale(d.population); }) // Set initial radius
                    .style('fill', function(d) { return d3.interpolateRainbow(Math.random()); }) // Random color
                    .style('opacity', 0.7);

                // Hover effect to increase size and change opacity
                bubbles.on('mouseenter', function (event, d) {
                    d3.select(this)
                        .transition()
                        .duration(300) // Duration of the grow/shrink animation
                        .attr('r', radiusScale(d.population) * 1.2) // Increase size by 20%
                        .style('opacity', 1); // Increase opacity

                    // Show tooltip
                    d3.select('#tooltip')
                        .style('opacity', 1)
                        .html('<b>Population: </b>' + d.population.toLocaleString())
                        .style('left', (event.pageX + 10) + 'px')
                        .style('top', (event.pageY - 28) + 'px');
                })
                    .on('mouseleave', function (event, d) {
                        d3.select(this)
                            .transition()
                            .duration(500) // Duration of the grow/shrink animation
                            .attr('r', radiusScale(d.population)) // Return to original size
                            .style('opacity', 0.7); // Return to original opacity

                        // Hide tooltip
                        d3.select('#tooltip').style('opacity', 0);
                    });

                bubbles.on('click', function(event, d) {
                    document.getElementById('infoBox').style.display = 'block';
                    document.getElementById('infoText').innerHTML =
                        'City: ' + d.city.toLocaleString() + '<br>' +
                        'Deaths: ' + d['deaths'].toLocaleString();
                });

                svg.append("text")
                    .attr("x", (svgWidth / 2))
                    .attr("y", margin.top / 2)
                    .attr("text-anchor", "middle")
                    .style("font-size", "20px")
                    .style("text-decoration", "underline")
                    .text("COVID-19 Deaths across German Cities");
            } else {
                console.error('Data is not an array:', data);
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            // Handle the error appropriately
        });
}

// Function to create the scatter plot
function createScatterPlot() {
    fetch('/data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (Array.isArray(data)) {
                console.log('Data received:', data);

                data.forEach(function(d) {
                    d.population = +d.population;
                    d.covid_cases = +d.covid_cases;
                    d.cityAbbreviation = d.city.substring(0, 2); // Abbreviate city name
                });

                // Initialize SVG and scales
                var svgWidth = 1000, svgHeight = 600;
                var margin = { top: 20, right: 20, bottom: 60, left: 70 };
                var width = svgWidth - margin.left - margin.right;
                var height = svgHeight - margin.top - margin.bottom;

                var svg = d3.select("#scatterPlot")
                    .attr("width", svgWidth)
                    .attr("height", svgHeight)
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

                // Create an ordinal scale for x-axis using abbreviated city names
                var x = d3.scaleBand()
                    .domain(data.map(function(d) { return d.cityAbbreviation; }))
                    .range([0, width])
                    .padding(0.1);

                svg.append("g")
                    .attr("class", "myXaxis")
                    .attr("transform", "translate(0," + height + ")")
                    .call(d3.axisBottom(x).tickSize(0)); // Remove x-axis ticks

                var y = d3.scaleLinear()
                    .domain([0, d3.max(data, function(d) { return d.covid_cases; })])
                    .range([height, 0]);
                svg.append("g").call(d3.axisLeft(y));

                // Color scale - you can choose a different scale if you prefer
                var colorScale = d3.scaleOrdinal(d3.schemeCategory10);

                // Add dots
                var points = svg.append('g')
                    .selectAll("dot")
                    .data(data)
                    .enter()
                    .append("circle")
                    .attr("cx", function (d) { return x(d.cityAbbreviation); }) // Use abbreviated city name for x-coordinate
                    .attr("cy", function (d) { return y(d.covid_cases); })
                    .attr("r", 15)
                    .style("fill", function(d, i) { return colorScale(i); });


                // Tooltip and hover effects
                points.on("mouseenter", function(event, d) {
                    d3.select("#tooltip")
                        .style("opacity", 1)
                        .html("City: " + d.city + "<br>Population: " + d.population.toLocaleString() + "<br>COVID-19 Cases: " + d.covid_cases.toLocaleString())
                        .style("left", (event.pageX + 10) + "px")
                        .style("top", (event.pageY - 28) + "px");
                }).on("mouseleave", function() {
                    d3.select("#tooltip").style("opacity", 0);
                });
            } else {
                console.error('Data is not an array:', data);
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            // Handle the error appropriately
        });
}

// Function to show the selected graph
function showGraph() {
    var selectedGraph = document.getElementById('graphSelect').value;
    var bubbleChart = document.getElementById('bubbleChart');
    var scatterPlot = document.getElementById('scatterPlot');
    var bubbleColorPicker = document.getElementById('bubbleCustomizationForm');
    var infoBox = document.getElementById('infoBox');
    var infoTextBubble = document.getElementById('infoTextBubble')

    bubbleChart.style.display = 'none';
    scatterPlot.style.display = 'none';
    bubbleColorPicker.style.display = 'none';
    infoBox.style.display = 'none';
    infoTextBubble.style.display = 'none';

    if (selectedGraph === 'bubbleChart') {
        bubbleChart.style.display = 'block';
        bubbleColorPicker.style.display = 'block';
        infoTextBubble.style.display = 'block';
        createBubbleChart();
    } else if (selectedGraph === 'scatterPlot') {
        scatterPlot.style.display = 'block';
        createScatterPlot();
    } else if (selectedGraph === 'city_timedata') {
        window.location.href = 'city_timedata.html'; // Redirect to timedata.html
    }
}

// Add event listener to the bubble color picker
document.getElementById('bubbleColor').addEventListener('input', function(event) {
    d3.selectAll('#bubbleChart .bubble').style('fill', event.target.value);
});

// Initial calls to create charts
createBubbleChart();