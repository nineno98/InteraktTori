const quiz_id = document.getElementById("quiz_id").value;

async function fetchData(apiUrl) {
    try {
        const response = await fetch(apiUrl);
        return await response.json();
    } catch (error) {
        console.error("Hiba az adatlekéréskor:", error);
        return [];
    }
}
function createChart(data, containerId, BubbleColor){
    if(data.length == 0 || data.every(d => d.scoreRatio ==0)){
        const container = document.getElementById('chart-container');
        while(container.hasChildNodes()){
            container.removeChild(container.firstChild);
        }
        const message = document.createElement('p');
        message.setAttribute('id','no-chart-message');
        message.textContent = "Nincs megjeleníthető adat a buborékdiagram rajzolásához!";
        container.appendChild(message);
        
    }else{
        const formattedData = { "name": "root", "children": data.map(d => ({ name: d.text, value: d.scoreRatio })) };

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
                .attr("fill", BubbleColor)
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
        
        }
    
};

function createDataTable(data){
    const tableRoot = document.getElementById('table-root');
    const tHead = document.createElement("thead");
    tHead.setAttribute('class','sajat-head');
    tHead.innerHTML = `
        <tr>
            <th>#</th>
            <th>Kérdés</th>
            <th>Arány</th>
        </tr>
    `;
    tableRoot.appendChild(tHead);
    const tBody = document.createElement("tbody");
    data.forEach((item, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${item.text}</td>
            <td>${(item.scoreRatio * 100).toFixed(2)}%</td>
        `;
        tBody.appendChild(row);
    })
    tableRoot.appendChild(tBody);

};

function calculateScoreRatio(data){
    return data.map(d => {
        const fullPoint = d.points * d.total_answers;
        const scoreRatio = fullPoint > 0 ? d.total_awarded_points / fullPoint : 0;
        return {...d, scoreRatio:scoreRatio}
    });
}

async function initComponents() {
    const QuestionsAPIData = await fetchData(`http://127.0.0.1:8000/api/test-questions/${quiz_id}/`);
    const calculatedData = calculateScoreRatio(QuestionsAPIData);
    console.log(calculatedData);
    const topQuestionsData = calculatedData
        .filter(d => d.scoreRatio > 0)
        .sort((a, b) => a.scoreRatio - b.scoreRatio)
        .slice(0, 10);
    
    const worstQuestionsData = calculatedData
        .filter(d => d.scoreRatio > 0)
        .sort((a, b) => a.scoreRatio - b.scoreRatio)
        .slice(0, 10);
    
    const maxScoreRatio = Math.max(...worstQuestionsData.map(q => q.scoreRatio));
    const invertedWorstQuestions = worstQuestionsData.map(q => ({
        ...q,
        inverted_score_ratio: maxScoreRatio - q.scoreRatio + 0.01
    }));

    //createDataTable(topQuestionsData);
    createChart(topQuestionsData, "#top-score",  "#90EE90");
    createChart(worstQuestionsData, "#wrost-score",  "#FF4C4C");

    createDataTable(calculatedData);
}

initComponents();

