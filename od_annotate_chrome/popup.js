$(document).ready(function () {
  $("#loader").fadeOut("slow");
  $(document).ajaxStart(function () {
      $("#loader").fadeIn("slow");
  });

  $(document).ajaxComplete(function () {
      $("#loader").fadeOut("slow");
  });
});
document.getElementById("btnSemtab").addEventListener("click", generate);

function generate(){
  file_link = $("#file_link").val();
  if(file_link == ""){
    alert("Please enter the csv url");
  }else{
    $("#semtab_graph").addClass("hide");
    var $form = $("#form-semtab"),
    url = $form.attr("action");
    mydata = "file_link="+file_link
    //alert(mydata);
    var semtabBtn = $.ajax({
        type: 'POST',
        url: url,
        data: mydata,
        success: function(resultData) {
          if (resultData.success) {
              $("#semtab_table").html(resultData.html);
              console.log(resultData.graph_json);
              subjectColumnId = resultData.subjectColumnId;
              $.getJSON(resultData.graph_json, function( data ) {
                generate_graph(data, subjectColumnId, "#semtab_graph", "Minimal Graph", 750, 600);
                $("#semtab_graph").removeClass("hide");
              });
              $.getJSON(resultData.graph_json_full, function( data ) {
                generate_graph(data, subjectColumnId, "#semtab_fullgraph", "Full Graph", 750, 600);
                $("#semtab_fullgraph").removeClass("hide");
              });
          }else{
            $("#semtab_table").html("<p style='color:red;'>Something went wrong</p>");
            $("#semtab_graph").addClass("hide");
            $("#semtab_fullgraph").addClass("hide");
          }
        },
        error:function(err) {
          $("#semtab_table").html("<p style='color:red;'>Something went wrong</p>");
          $("#semtab_graph").addClass("hide");
          $("#semtab_fullgraph").addClass("hide");
        },
    });
  }
}

function generate_graph(allData, focalNodeID, divID, graphName, width, height){
  nodeSet = allData.nodes
  console.log(nodeSet);
  linkSet = allData.links
  console.log(linkSet);
  drawCluster(graphName, focalNodeID, nodeSet, linkSet, divID, "colorScale20", width, height);
}

//Function to create graph
//Source: http://bl.ocks.org/Guerino1/2879486
function drawCluster(drawingName, focalNodeID, nodeSet, linkSet, selectString, colors, width, height) {
      // drawingName => A unique drawing identifier that has no spaces, no "." and no "#" characters.
      // focalNode => Primary Node of Context.
      // nodeSet => Set of nodes and their relevant data.
      // linkSet => Set of links and their relevant data.
      // selectString => String that allows you to pass in
      //           a D3 select string.
      // colors => String to set color scale.  Values can be...
      //           => "colorScale10"
      //           => "colorScale20"
      //           => "colorScale20b"
      //           => "colorScale20c"
      // margin => Integer margin offset value.
      // outerRadius => Integer outer radius value.
      // innerRadius => Integer inner radius value.
      // sortArcs => Controls sorting of Arcs by value.
      //              0 = No Sort.  Maintain original order.
      //              1 = Sort by arc value size.

      // Color Scale Handling...
      var colorScale = d3.scale.category20c();
      switch (colors)
      {
        case "colorScale10":
          colorScale = d3.scale.category10();
          break;
        case "colorScale20":
          colorScale = d3.scale.category20();
          break;
        case "colorScale20b":
          colorScale = d3.scale.category20b();
          break;
        case "colorScale20c":
          colorScale = d3.scale.category20c();
          break;
        default:
          colorScale = d3.scale.category20c();
      };


      var centerNodeSize = 50;
      var nodeSize = 10;
      var color_hash = [];

      var typeMouseOver = function() {

        var thisObject = d3.select(this);
        var typeValue = thisObject.attr("type_value");
        var strippedTypeValue = typeValue.replace(/ /g, "_");

        var legendBulletSelector = "." + "legendBullet-" + strippedTypeValue;
        var selectedBullet = d3.selectAll(legendBulletSelector);
        //document.writeln(legendBulletSelector);
        selectedBullet.style("fill", "Maroon");
  selectedBullet.attr("r", 1.2*6);

        var legendTextSelector = "." + "legendText-" + strippedTypeValue;
        var selectedLegendText = d3.selectAll(legendTextSelector);
        //document.writeln(legendBulletSelector);
        selectedLegendText.style("font", "bold 14px Arial")
        selectedLegendText.style("fill", "Maroon");

        var nodeTextSelector = "." + "nodeText-" + strippedTypeValue;
        var selectedNodeText = d3.selectAll(nodeTextSelector);
        //document.writeln(pie3SliceSelector);
        selectedNodeText.style("font", "bold 16px Arial")
        selectedNodeText.style("fill", "Maroon");

        var nodeCircleSelector = "." + "nodeCircle-" + strippedTypeValue;
        var selectedCircle = d3.selectAll(nodeCircleSelector);
        //document.writeln(nodeCircleSelector);
        selectedCircle.style("fill", "Maroon");
        selectedCircle.style("stroke", "Maroon");
  selectedCircle.attr("r", 1.2*nodeSize);

        var focalNodeCircleSelector = "." + "focalNodeCircle";
        var selectedFocalNodeCircle = d3.selectAll(focalNodeCircleSelector);
        //document.writeln(focalNodeCircleSelector);
        var focalNodeType = selectedFocalNodeCircle.attr("type_value");
        if (typeValue == focalNodeType){
          selectedFocalNodeCircle.style("stroke", "Maroon");
          selectedFocalNodeCircle.style("fill", "White");
        };

        var focalNodeTextSelector = "." + "focalNodeText";
        var selectedFocalNodeText = d3.selectAll(focalNodeTextSelector);
        var focalNodeTextType = selectedFocalNodeText.attr("type_value");
        //document.writeln(pie3SliceSelector);
        if (typeValue == focalNodeTextType) {
          selectedFocalNodeText.style("fill", "Maroon");
          selectedFocalNodeText.style("font", "bold 16px Arial")
        };

      };

      var typeMouseOut = function() {

        var thisObject = d3.select(this);
        var typeValue = thisObject.attr("type_value");
        var colorValue = thisObject.attr("color_value");
        var strippedTypeValue = typeValue.replace(/ /g, "_");

        var legendBulletSelector = "." + "legendBullet-" + strippedTypeValue;
        var selectedBullet = d3.selectAll(legendBulletSelector);
        //document.writeln(legendBulletSelector);
        selectedBullet.style("fill", colorValue);
  selectedBullet.attr("r", 6);

        var legendTextSelector = "." + "legendText-" + strippedTypeValue;
        var selectedLegendText = d3.selectAll(legendTextSelector);
        //document.writeln(legendBulletSelector);
        selectedLegendText.style("font", "normal 14px Arial")
        selectedLegendText.style("fill", "Black");

        var nodeTextSelector = "." + "nodeText-" + strippedTypeValue;
        var selectedNodeText = d3.selectAll(nodeTextSelector);
        //document.writeln(pie3SliceSelector);
        selectedNodeText.style("font", "normal 16px Arial")
        selectedNodeText.style("fill", "Blue");

        var nodeCircleSelector = "." + "nodeCircle-" + strippedTypeValue;
        var selectedCircle = d3.selectAll(nodeCircleSelector);
        //document.writeln(nodeCircleSelector);
        selectedCircle.style("fill", "White");
        selectedCircle.style("stroke", colorValue);
  selectedCircle.attr("r", nodeSize);

        var focalNodeCircleSelector = "." + "focalNodeCircle";
        var selectedFocalNodeCircle = d3.selectAll(focalNodeCircleSelector);
        //document.writeln(focalNodeCircleSelector);
        var focalNodeType = selectedFocalNodeCircle.attr("type_value");
        if (typeValue == focalNodeType){
          selectedFocalNodeCircle.style("stroke", colorValue);
          selectedFocalNodeCircle.style("fill", "White");
        };

        var focalNodeTextSelector = "." + "focalNodeText";
        var selectedFocalNodeText = d3.selectAll(focalNodeTextSelector);
        //document.writeln(pie3SliceSelector);
        selectedFocalNodeText.style("fill", "Blue");
        selectedFocalNodeText.style("font", "normal 14px Arial")

      };

      var nodeMouseOver = function() {

        var thisObject = d3.select(this);
        var typeValue = thisObject.attr("type_value");
        var colorValue = thisObject.attr("color_value");
        var strippedTypeValue = typeValue.replace(/ /g, "_");

        d3.select(this).select("circle").transition()
            .duration(250)
      .attr("r", function(d,i) { if(d.id==focalNodeID) {return 65;} else {return 15;} } );
  d3.select(this).select("text").transition()
            .duration(250)
      .style("font", "bold 20px Arial")
      .attr("fill", "Blue");

        var legendBulletSelector = "." + "legendBullet-" + strippedTypeValue;
        var selectedBullet = d3.selectAll(legendBulletSelector);
        //document.writeln(legendBulletSelector);
        selectedBullet.style("fill", "Maroon");
  selectedBullet.attr("r", 1.2*6);

        var legendTextSelector = "." + "legendText-" + strippedTypeValue;
        var selectedLegendText = d3.selectAll(legendTextSelector);
        //document.writeln(legendBulletSelector);
        selectedLegendText.style("font", "bold 14px Arial")
        selectedLegendText.style("fill", "Maroon");

      }

      var nodeMouseOut = function() {

        var thisObject = d3.select(this);
        var typeValue = thisObject.attr("type_value");
        var colorValue = thisObject.attr("color_value");
        var strippedTypeValue = typeValue.replace(/ /g, "_");

        d3.select(this).select("circle").transition()
            .duration(250)
      .attr("r", function(d,i) { if(d.id==focalNodeID) {return centerNodeSize;} else {return nodeSize;} } );
  d3.select(this).select("text").transition()
            .duration(250)
      .style("font", "normal 16px Arial")
      .attr("fill", "Blue");

        var legendBulletSelector = "." + "legendBullet-" + strippedTypeValue;
        var selectedBullet = d3.selectAll(legendBulletSelector);
        //document.writeln(legendBulletSelector);
        selectedBullet.style("fill", colorValue);
  selectedBullet.attr("r", 6);

        var legendTextSelector = "." + "legendText-" + strippedTypeValue;
        var selectedLegendText = d3.selectAll(legendTextSelector);
        //document.writeln(legendBulletSelector);
        selectedLegendText.style("font", "normal 14px Arial")
        selectedLegendText.style("fill", "Black");

      }

      // Create a hash that maps colors to types...
      nodeSet.forEach(function(d, i) {
        color_hash[d.type] = d.type;
        //document.writeln(color_hash[d.type]);
      });

      function keys(obj)
      {
        var keys = [];

        for(var key in obj)
        {
          if(obj.hasOwnProperty(key))
          {
            keys.push(key);
          }
        }
        return keys;
      }

      var sortedKeys = keys(color_hash).sort();

      sortedKeys.forEach(function(d, i) {
        color_hash[d] = colorScale(i);
        //document.writeln(color_hash[d]);
      });

      // Add colors to original node records...
      nodeSet.forEach(function(d,i) {
        d.color = color_hash[d.type];
        //document.writeln(d.type);
      });

// Create a canvas...
      var svgCanvas = d3.select(selectString)
        .append("svg:svg")
          .attr("width", width)
    .attr("height", height)
        .append("svg:g")
          .attr("class", "focalNodeCanvas")
          .attr("transform", "translate(" + width/2 + "," + height/2 + ")")

      var node_hash = [];
      var type_hash = [];

      // Create a hash that allows access to each node by its id
      nodeSet.forEach(function(d, i) {
        node_hash[d.id] = d;
        type_hash[d.type] = d.type;
      });

      // Append the source object node and the target object node to each link records...
      linkSet.forEach(function(d, i) {
        d.source = node_hash[d.sourceId];
        d.target = node_hash[d.targetId];
        if (d.sourceId == focalNodeID)
    { d.direction = "OUT"; }
        else
    { d.direction = "IN"; }
      });

      // Create a force layout and bind Nodes and Links
      var force = d3.layout.force()
          .nodes(nodeSet)
          .links(linkSet)
          .charge(-1000)
    .gravity(.01)
    .friction(.2)
          .linkStrength(9)
          //.size([width/8, height/10])
          .linkDistance( function(d) { if (width < height) { return width*1/3; } else { return height*1/3 } } ) // Controls edge length
          .on("tick", tick)
          .start();

      // Draw lines for Links between Nodes
      var link = svgCanvas.selectAll(".gLink")
          .data(force.links())
        .enter().append("g")
          .attr("class", "gLink")
        .append("line")
          .attr("class", "link")
          .style("stroke", "#ccc")
          .attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

      // Create Nodes
      var node = svgCanvas.selectAll(".node")
          .data(force.nodes())
        .enter().append("g")
          .attr("class", "node")
          .attr("type_value", function(d, i) { return d.type; })
          .attr("color_value", function(d, i) { return color_hash[d.type]; })
//.attr("fixed", function(d) { if (d.id==focalNodeID) { return true; } else { return false; } } )
          .on("mouseover", nodeMouseOver)
          .on("mouseout", nodeMouseOut)
          .call(force.drag)
  .append("a")
    .attr("xlink:href", function(d) {return d.hlink; });

      // Append circles to Nodes
      node.append("circle")
//.attr("x", function(d) { return d.x; })
//.attr("y", function(d) { return d.y; })
          .attr("r", function(d) { if (d.id==focalNodeID) { return centerNodeSize; } else { return nodeSize; } } )
          .style("fill", "White") // Make the nodes hollow looking
          .attr("type_value", function(d, i) { return d.type; })
          .attr("color_value", function(d, i) { return color_hash[d.type]; })
//.attr("fixed", function(d) { if (d.id==focalNodeID) { return true; } else { return false; } } )
//.attr("x", function(d) { if (d.id==focalNodeID) { return width/2; } else { return d.x; } })
//.attr("y", function(d) { if (d.id==focalNodeID) { return height/2; } else { return d.y; } })
          .attr("class", function(d, i) {
            var str = d.type;
            var strippedString = str.replace(/ /g, "_")
            //return "nodeCircle-" + strippedString; })
      if (d.id==focalNodeID) { return "focalNodeCircle"; }
      else { return "nodeCircle-" + strippedString; }
          })
          .style("stroke-width", 5) // Give the node strokes some thickness
          .style("stroke", function(d, i) { return color_hash[d.type]; } ) // Node stroke colors
    .call(force.drag);

      // Append text to Nodes
      node.append("text")
          .attr("x", function(d) { if (d.id==focalNodeID) { return 0; } else {return 20;} } )
          .attr("y", function(d) { if (d.id==focalNodeID) { return 0; } else {return -10;} } )
    .attr("text-anchor", function(d) { if (d.id==focalNodeID) {return "middle";} else {return "start";} })
    .attr("font-family", "Arial, Helvetica, sans-serif")
          .style("font", "normal 16px Arial")
          .attr("fill", "Blue")
          .style("fill", function(d, i) { return color_hash[d]; })
          .attr("type_value", function(d, i) { return d.type; })
          .attr("color_value", function(d, i) { return color_hash[d.type]; })
          .attr("class", function(d, i) {
            var str = d.type;
            var strippedString = str.replace(/ /g, "_");
            //return "nodeText-" + strippedString; })
      if (d.id==focalNodeID) { return "focalNodeText"; }
      else { return "nodeText-" + strippedString; }
          })
          .attr("dy", ".35em")
          .text(function(d) { return d.name; });

      // Append text to Link edges
      var linkText = svgCanvas.selectAll(".gLink")
          .data(force.links())
        .append("text")
    .attr("font-family", "Arial, Helvetica, sans-serif")
    .attr("x", function(d) {
        if (d.target.x > d.source.x) { return (d.source.x + (d.target.x - d.source.x)/2); }
        else { return (d.target.x + (d.source.x - d.target.x)/2); }
    })
          .attr("y", function(d) {
        if (d.target.y > d.source.y) { return (d.source.y + (d.target.y - d.source.y)/2); }
        else { return (d.target.y + (d.source.y - d.target.y)/2); }
    })
    .attr("fill", "Black")
          .style("font", "normal 12px Arial")
          .attr("dy", ".35em")
          .text(function(d) { return d.linkName; });


      function tick() {
        link
          .attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

        node
          .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

        linkText
    .attr("x", function(d) {
        if (d.target.x > d.source.x) { return (d.source.x + (d.target.x - d.source.x)/2); }
        else { return (d.target.x + (d.source.x - d.target.x)/2); }
    })
    .attr("y", function(d) {
        if (d.target.y > d.source.y) { return (d.source.y + (d.target.y - d.source.y)/2); }
        else { return (d.target.y + (d.source.y - d.target.y)/2); }
    });
      }


      // Print Legend Title...
      svgCanvas.append("text").attr("class","region")
          .text("Legend")
          .attr("x", -1*(width/2 - 10))
          .attr("y", (-height/7*3))
          .style("fill", "Black")
          .style("font", "bold 16px Arial")
          .attr("text-anchor","start");

      // Plot the bullet circles...
      svgCanvas.selectAll("focalNodeCanvas")
          .data(sortedKeys).enter().append("svg:circle") // Append circle elements
          .attr("cx", -1*(width/2 - 25))
          .attr("cy", function(d, i) { return (i*20-height/7*3 + 20); } )
          .attr("stroke-width", ".5")
          .style("fill", function(d, i) { return color_hash[d]; })
          .attr("r", 6)
          .attr("color_value", function(d, i) { return color_hash[d]; })
          .attr("type_value", function(d, i) { return d; })
          .attr("index_value", function(d, i) { return "index-" + i; })
          .attr("class", function(d) {
              var str = d;
              var strippedString = str.replace(/ /g, "_")
	return "legendBullet-" + strippedString; })
          .on('mouseover', typeMouseOver)
          .on("mouseout", typeMouseOut);

      // Create legend text that acts as label keys...
      svgCanvas.selectAll("a.legend_link")
          .data(sortedKeys) // Instruct to bind dataSet to text elements
        .enter().append("svg:a") // Append legend elements
          .append("text")
            .attr("text-anchor", "center")
            .attr("x", -1*(width/2 - 40))
            .attr("y", function(d, i) { return (i*20-height/7*3 + 20); } )
            .attr("dx", 0)
            .attr("dy", "4px") // Controls padding to place text in alignment with bullets
            .text(function(d) { return d;})
            .attr("color_value", function(d, i) { return color_hash[d]; })
            .attr("type_value", function(d, i) { return d; })
            .attr("index_value", function(d, i) { return "index-" + i; })
            .attr("class", function(d) {
              var str = d;
              var strippedString = str.replace(/ /g, "_")
              return "legendText-" + strippedString; })
            .style("fill", "Black")
            .style("font", "normal 14px Arial")
            .on('mouseover', typeMouseOver)
            .on("mouseout", typeMouseOut);

}
