const quiz_id = document.getElementById("quiz_id").value;
console.log(quiz_id);


function createBubleChart(apiUrl, containerId, color){
    let color_ = color;
    
    fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        const formattedData = { "name": "root", "children": data.map(d => ({ name: d.text, value: d.score_ratio })) };

        const width = 800, height = 600;
        const color = d3.scaleOrdinal(d3.schemeCategory10);
        const pack = d3.pack().size([width, height]).padding(5);

        const root = d3.hierarchy(formattedData).sum(d => d.value);
        const nodes = pack(root).leaves();

        const svg = d3.select(containerId);

        const bubbles = svg.selectAll(".bubble")
            .data(nodes)
            .enter()
            .append("g")
            .attr("class", "bubble")
            .attr("transform", d => `translate(${d.x}, ${d.y})`);
        
        bubbles.append("circle")
            .attr("r", d => d.r)
            .attr("fill", color_)
            .attr("stroke", "#333")
            .attr("stroke-width", 2);

        bubbles.append("text")
            .attr("dy", "-0.1em")
            
            .attr("font-size", d => Math.min(d.r / 3, 16))
            .attr("fill", "white")
            .each(function (d) {
                const words = d.data.name.match(/.{1,18}(\s|$)/g);
                if (words) {
                    words.forEach((word, i) => {
                        d3.select(this).append("tspan")
                            .attr("x", 0)
                            .attr("dy", i === 0 ? "-5" : "1.2em")
                            .text(word.trim());
                    });
                }
            });
    })
    .catch(error => {
        console.log(error);
    });
};




createBubleChart(`http://127.0.0.1:8000/top-questions/${quiz_id}/`, "#top-score" , "#90EE90")
createBubleChart(`http://127.0.0.1:8000/top-wrost-questions/${quiz_id}/`, "#wrost-score" , "#FF4C4C")
