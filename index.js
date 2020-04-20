function create_bar_plot( d3, area, date, pvalue, indices) {

  // Define the div for the tooltip
    var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

    // deminsions
    var margin = {top: 400, right: 30, bottom: 70, left: 400},
    width = 1500 - margin.left - margin.right,
    height = 1000 - margin.top - margin.bottom;

    // set up svg
    var svg = d3.select(area)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g").attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");


    var file = "./r_data/" + date + "_" + pvalue + ".csv"

    var types = ["positive", "negative"]
    var color = d3.scaleOrdinal(types,  ["green", "red"])

    var market_cap_file = "./market_caps/market_caps.csv";
    var market_cap_data;

    // load market cap
    d3.csv( market_cap_file ).then ( market => {
        market_cap_data = market
    }).then( () => {

    // load the datat from q3.csv
        return d3.csv(file)
    })
    .then( info => {

        var data = format_data(info, indices);
        let links = data['data'].links;
        let nodes = data['data'].nodes;


        //console.log("link")
        //console.log(JSON.stringify(links))

        var tone_min = data['tone_min']
        var tone_max = data['tone_max']


        //console.log("here is min_tone: " + tone_min)
        //console.log("here is max_tone: " + tone_max)


        all = add_market_cap( nodes, market_cap_data);

        nodes = all["nodes"]
        min_size = all['min']
        max_size = all['max']

        //console.log("here is min_size: " + min_size)
        //console.log("here is max_size: " + max_size)
        //console.log("here is nodes: " + JSON.stringify(nodes))


        //console.log("nodes")
        //console.log(JSON.stringify(nodes))


        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id( d => {
                //console.log("hey");
                return d.id

            }))
                // add more spacing in line below
                .force("charge", d3.forceManyBody().strength(-800))
              .force("x", d3.forceX())
              .force("y", d3.forceY());


        // Per-type markers, as they don't inherit styles.
        svg.append("defs").selectAll("marker")
            .data(types)
            .join("marker")
              .attr("id", d => {

                  //console.log("here is d: " + JSON.stringify(d));
                  return `arrow-${d}`
              })
              .attr("viewBox", "0 -5 10 10")
              .attr("refX", 15)
              .attr("refY", -0.5)
            .attr("markerWidth", d => {
                //console.log('here is marker width: ' + JSON.stringify(d))
                return 6
            })
              .attr("markerHeight", 6)
              .attr("orient", "auto")
            .append("path")
              .attr("fill", color)
              .attr("d", "M0,-5L10,0L0,5");

        const link = svg.append("g")
              .attr("fill", "none")
              .attr("stroke-width", 1.5)
            .selectAll("path")
            .data(links)
            .join("path")
                .attr("stroke", d => color(d.type))
                .attr("stroke-width", d => {
                    // this effects line thickness
                    //console.log("here is stroke width: " + JSON.stringify(d.width))
                    return d.width
                })
                .attr("marker-end", d => {

                    //console.log("here is d: " + JSON.stringify(d));
                    // not give arrow to everything
                    if (d.source.id != d.target.id)
                        return `url(${new URL(`#arrow-${d.type}`, location)})`
                });

        const node = svg.append("g")
              .attr("fill", "currentColor")
              .attr("stroke-linecap", "round")
              .attr("stroke-linejoin", "round")
            .selectAll("g")
            .data(nodes)
            .join("g")
              .call(drag(simulation))
          //  .on("mouseover", d => {
          //      console.log("you are hovering")
          //      console.log("d = " + JSON.stringify(d));
                // need to add something with tooltip
          //  })
            .on("mouseover", function(d) {
         div.transition()
             .duration(200)
             .style("opacity", .9);
         div.html("Market cap: " + d.size + " billions")
             .style("left", (d3.event.pageX) + "px")
             .style("top", (d3.event.pageY - 28) + "px");
         })
     .on("mouseout", function(d) {
         div.transition()
             .duration(500)
             .style("opacity", 0);
     })

        node.append("circle")
            .attr("stroke", "white")
            .attr("stroke-width", 1.5)
            .attr("r", d => {
                return Math.log2(d.size);
            })
            .style("fill", d =>  {

                //console.log("here is d: " + JSON.stringify(d))
                // look here this needs to be done better more than likley
                var tone = Math.log2(Math.abs(d.tone))

                // took middle point of 50 (1 -100)
                // was 100 but gave grey while colors with log being smaller number
                tone = "" + (50 - tone) + "%";
                if (d.color =="green") {
                    //see http://www.workwithcolor.com/hsl-color-picker-01.html
                    // to understand hsl
                    return "hsl(120, 100%," + tone +" )"
                } else {
                    return "hsl(0, 100%," + tone +" )"
                }
            })
            // look transparent
            .style("opacity", 0.6);

        node.append("text")
              .attr("x", 8)
              .attr("y", "0.31em")
              .text(d => d.id)
            .clone(true).lower()
              .attr("fill", "none")
              .attr("stroke", "white")
              .attr("stroke-width", 3);


        simulation.on("tick", () => {
            link.attr("d", linkArc);
            node.attr("transform", d => `translate(${d.x},${d.y})`);
        });

        //invalidation.then(() => simulation.stop());


        function linkArc(d) {
            const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
            return `
                M${d.source.x},${d.source.y}
                A${r},${r} 0 0,1 ${d.target.x},${d.target.y}`;
        }

        function drag(simulation) {

            function dragstarted(d) {
                if (!d3.event.active) simulation.alphaTarget(0.3).restart();

                 // setting the fx values will "pin" the nodes to this position
                d.fx = d.x;
                d.fx = d.x;
                d.fy = d.y;
            }

            function dragged(d) {
                d.fx = d3.event.x;
                d.fy = d3.event.y;
            }

            function dragended(d) {
                if (!d3.event.active) simulation.alphaTarget(0);

                //commeted out so notes wont reloacte
                //d.fx = null;
                //d.fy = null;
            }

            return d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended);
        }


        //return svg.node();


    }).catch( err => {
        console.log("error = " + JSON.stringify(err))
        console.log(err);
    })
}


function add_market_cap(nodes, market_cap_data) {

    var min = null
    var max = null

    //console.log("here is market cap data: " + JSON.stringify( market_cap_data));
    //console.log("here is nodes: " + JSON.stringify(nodes));
    for ( var x in  market_cap_data) {
        //console.log("here is maket[x]: " + JSON.stringify(market_cap_data[x])
        for (var y in nodes) {
            if ( market_cap_data[x][''] ===  nodes[y]['id'] ) {
                //console.log("we have a match of: " + nodes[y]['id'])
                nodes[y]['size'] =  parseInt(market_cap_data[x]['Market Cap in Billion'])
                if  (min === null &&  max === null) {
                    min = nodes[y]['size']
                    max = nodes[y]['size']
                } else {

                    if ( nodes[y]['size'] < min) {
                        min = nodes[y]['size']
                    }

                    if ( nodes[y]['size'] > max) {
                        max = nodes[y]['size']
                    }
                }
            }
        }
    }
    //console.log("here is nodes: " + JSON.stringify(nodes));
    return {'nodes': nodes, 'min': min, "max": max}
}


function format_data( info, indices) {

    //console.log("here is info: " + JSON.stringify(info))

    //var info = [{"":"AEX","AEX":"9.3","ATX":"0","BEL_20":"0","Bovespa":"0","BSE_Sensex":"0","CAC40":"0","CSE":"0","DAX_PERFORMANCE.INDEX":"0","Dow_30":"0","EURONEXT_100":"0","HANG_SENG_INDEX":"0","IBEX_35":"0","IDX_Composite":"0","KOSPI_Composite_Index":"0","MOEX_Russia_Index":"0","Nasdaq":"0","Nifty_50":"0","IPC_MEXICO":"0","MERVAL":"0","Nikkei_225":"0","Russell_2000":"0","SP_500":"0","SP_NZX_50_INDEX_GROSS":"0","SP_TSX_Composite_index":"0","SMI":"0"}]

    var tone_min = null
    var tone_max = null

    var data = { nodes: [], links: []}

    for( let x in info) {
        let hold;
        if (indices.includes(info[x][""])) {
            for( let y in info[x]) {
                let index = y
                let value = parseFloat(info[x][y])
                if ( index == '') {
                    hold = {'id': info[x]['']}
                } else if (value != 0 && indices.includes(y)){
                    let color;
                    if( value > 0) color = 'green'
                    else color = "red"
                    hold['color'] = color
                    hold['tone'] =  value

                    if (tone_min === null && tone_max === null) {
                        tone_min = value
                        tone_max = value
                    } else {

                        if (tone_min >  value){
                            tone_min = value
                        }

                        if (tone_max < value){
                            tone_max = value
                        }

                    }

                    let type;
                    if(value > 0) type = 'positive'
                    else type = "negative"
                    data.links.push({
                        'source': info[x][''],
                        'target': index,
                        'width': Math.abs(value),
                        'type': type
                    });
                }
            }
            data.nodes.push( hold);
        } else {
            //console.log("this is not included " + info[x][''])
        }
    }
    return {'data': data, 'tone_min': tone_min, 'tone_max': tone_max};
}
