const margin = { top: 30, right: 60, bottom: 70, left: 60 },
      width = 800 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

const svg = d3.select("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

const tooltip = d3.select("#tooltip");
const tooltip2 = d3.select("#tooltip2")

const x = d3.scaleBand()
    .range([0, width])
    .padding(0.2);

// Define x-axis
const xAxis = svg.append("g")
    .attr("transform", `translate(0,${height})`);

const y = d3.scaleLinear()
    .range([height, 0]);

// Define y-axis
const yAxis = svg.append("g")
    .attr("class", "myYaxis");

const y1 = d3.scaleLinear()
    .range([height, 0]);

// Define second y-axis (right side for population)
const yAxisRight = svg.append("g")
    .attr("class", "myYaxis")
    .attr("transform", `translate(${width}, 0)`);

let selectedCities = [];
let currentSelectedYearVar = 'covid_cases_2020'; // Default year

// Add listener for the color picker
d3.select("#barColorPicker").on("input", function() {
    svg.selectAll(".bar")
        .style("fill", this.value);
});

// Sorting function
function sortData(data, ascending = true) {
    return data.sort((a, b) => ascending ?
        a[currentSelectedYearVar] - b[currentSelectedYearVar] :
        b[currentSelectedYearVar] - a[currentSelectedYearVar]);
}

// Add an option for total COVID cases
document.getElementById('year').innerHTML += '<option value="covid_cases">All Years (Total Cases)</option>';

// Update function with sorting logic
function update(selectedVar, sortAscending) { 
    currentSelectedYearVar = selectedVar;

    fetch(`/data`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (Array.isArray(data)) {
            if (sortAscending !== undefined) {
                data = sortData(data, sortAscending);
            }
            svg.selectAll(".bar").remove();

            x.domain(data.map(d => d.city));
            xAxis.call(d3.axisBottom(x))
                .selectAll("text")
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-65)");

            // Set the domains for both y-axes
            y.domain([0, d3.max(data, d => d[selectedVar])]); // For COVID cases
            y1.domain([0, d3.max(data, d => d.population)]);  // For population

            // Update the axes
            yAxis.transition().duration(1000).call(d3.axisLeft(y));
            yAxisRight.transition().duration(1000).call(d3.axisRight(y1));

            const bars = svg.selectAll(".bar")
                .data(data);

            bars.enter()
                .append("rect")
                .attr("class", "bar")
                .attr("x", d => x(d.city))
                .attr("width", x.bandwidth())
                .attr("y", height)
                .attr("height", 0)
                .style("fill", "green")
                .merge(bars)
                .transition()
                .duration(1000)
                .attr("y", d => y(d[currentSelectedYearVar]))
                .attr("height", d => height - y(d[currentSelectedYearVar]));

            bars.exit().remove();

            svg.selectAll(".bar").on("click", function(event, d) {
                console.log("Clicked bar:", d.city);
                const index = selectedCities.findIndex(city => city.city === d.city);
                if (index > -1) {
                    selectedCities.splice(index, 1);
                    // Remove the highlight class
                    d3.select(this).classed("highlighted-bar", false);
                } else {
                    selectedCities.push(d);
                    // Add the highlight class
                    d3.select(this).classed("highlighted-bar", true);
                }
                updateComparisonArea();
            });

            // Create elements for population data
            svg.selectAll(".populationCircle").remove();
            svg.selectAll(".populationCircle")
                .data(data)
                .enter()
                .append("circle")
                .attr("class", "populationCircle")
                .attr("cx", d => x(d.city) + x.bandwidth() / 2) // Center in the band
                .attr("cy", d => y1(d.population))
                .attr("r", 5) // Radius of circles
                .style("fill", "blue") // Example color for population data
                .style("opacity", 0.7)
                .on("mouseenter", function(event, d) {
                    tooltip2.style("display", "block")
                           .html(`Population: ${d.population.toLocaleString()}`)
                           .style("left", (event.pageX + 10) + "px")
                           .style("top", (event.pageY - 28) + "px");
                })
                .on("mouseleave", function() {
                    tooltip2.style("display", "none");
                });
        }
    });
}

function updateComparisonArea() {
    const list = d3.select("#comparison-list");
    list.html("");
    selectedCities.forEach(city => {
        list.append("li").html(`City: ${city.city}<br>COVID Cases: ${city.covid_cases_2020.toLocaleString()}<br>Deaths: ${city.deaths.toLocaleString()}`);
        // Apply the highlight class to the corresponding bars in the chart
        svg.selectAll(".bar")
            .filter(d => d.city === city.city)
            .classed("highlighted-bar", true);
    });
}


update('covid_cases_2020');

// Event listener for year change
d3.select("#year").on("change", function(event) {
    const selectedOption = d3.select(this).property("value");
    update(selectedOption);
});

// Event listeners for sorting
d3.select("#sortAscending").on("click", function() {
    update(d3.select("#year").property("value"), true);
});

d3.select("#sortDescending").on("click", function() {
    update(d3.select("#year").property("value"), false);
});

d3.select("#clear-comparison").on("click", function() {
    selectedCities = []; // Clear the selectCities array
    updateComparisonArea();   // Update the comparison area to reflect the cleared array
});