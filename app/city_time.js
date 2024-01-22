const margin = {top: 30, right: 30, bottom: 70, left: 60},
        width = 800 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    const svg = d3.select("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const tooltip = d3.select("#tooltip");

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

    // Update function with sorting logic
    function update(selectedVar, sortAscending) {  // Add sortAscending parameter
        currentSelectedYearVar = selectedVar; // Update the selected year variable

        fetch(`/data2`)
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
                    // Remove only the bars, not the entire SVG
                    svg.selectAll(".bar").remove();

                    // Update to use the correct property based on the selected year
                    x.domain(data.map(d => d.city));
                    xAxis.call(d3.axisBottom(x))
                        .selectAll("text")
                        .style("text-anchor", "end")
                        .attr("dx", "-.8em")
                        .attr("dy", ".15em")
                        .attr("transform", "rotate(-65)");

                    // Use the year-specific property for each city
                    y.domain([0, d3.max(data, d => d[selectedVar])]);
                    yAxis.transition().duration(1000).call(d3.axisLeft(y));

                    const bars = svg.selectAll(".bar")
                        .data(data);

                    bars.enter()
                        .append("rect")
                        .attr("class", "bar")
                        .attr("x", d => x(d.city))
                        .attr("width", x.bandwidth())
                        .attr("y", height)  // Start the bars at the bottom of the chart
                        .attr("height", 0)  // Initial height set to 0
                        .style("fill", d3.select("#barColorPicker").property("value"))
                        .merge(bars)  // Merge with existing bars
                        .transition()  // Apply a transition to animate the bars
                        .duration(1000)  // Duration of the transition in milliseconds
                        .attr("y", d => y(d[currentSelectedYearVar]))  // Animate to the actual y position
                        .attr("height", d => height - y(d[currentSelectedYearVar]));  // Animate to the actual height

                    bars.exit().remove();

                    svg.selectAll(".bar").on("click", function(event, d) {
                        const index = selectedCities.findIndex(city => city.city === d.city);
                        if (index > -1) {
                            selectedCities.splice(index, 1);
                        } else {
                            selectedCities.push(d);
                        }
                        updateComparisonArea();
                    });
                }
            });
    }

    // Comparison Area Update Function
    function updateComparisonArea() {
        const list = d3.select("#comparison-list");
        list.html("");
        selectedCities.forEach(city => {
            list.append("li").text(`City: ${city.city}, COVID Cases: ${city[currentSelectedYearVar].toLocaleString()}`);
        });
    }

    update('covid_cases_2020');

    function downloadSVG() {
        const svg = document.querySelector('svg');
        const svgData = new XMLSerializer().serializeToString(svg);
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        img.onload = () => {
            ctx.drawImage(img, 0, 0);
            const pngFile = canvas.toDataURL("image/png");
            const downloadLink = document.createElement('a');
            downloadLink.download = 'chart.png';
            downloadLink.href = `${pngFile}`;
            downloadLink.click();
        };
        img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
    }

    document.getElementById('downloadButton').addEventListener('click', downloadSVG);


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