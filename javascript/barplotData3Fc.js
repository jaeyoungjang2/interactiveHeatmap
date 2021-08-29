function bar_Data3paintImage(ids, readJson){
  let bar_x = [];
  let bar_y = [];
  let bar_colors = [];

  for (var key in readJson.data.nodes) {
    geneID = readJson.data.nodes[key].objects;

    if(geneID && geneID == ids[0]){
      for ( var i = 0; i < readJson.data.group_names.length; i++) {
        fc_temp = readJson.data.nodes[key].information[readJson.data.group_names[i].replace("_vs_","/")+".fc"]
        bar_x.push(readJson.data.group_names[i]);
        if (fc_temp > 0) {
          fc = logB(fc_temp,2);
          bar_colors.push(volcanoRed);
        } else {
          fc = -logB(-fc_temp,2);
          bar_colors.push(volcanoBlue);
        }
        bar_y.push(fc)
      }
    }
  }


  barplot_data = [{
    x:bar_x,
    y:bar_y,
    type:'bar',
    textposition: 'outside',
    marker:{color:bar_colors}}]

  layout = {
    title: data3FcBarPlotTitle,
    yaxis: {
      zeroline: true,
      gridwith: 4
    },
    xaxis: {
      tickangle: data3FcBarPlotXaxisTickAngle
    },
    yaxis: {
    title: data3FcBarPlotYaxisTitle
    }
  };

  Plotly.newPlot('barplot_myDiv2', barplot_data, layout);
}


function barplotData3Main() {
  ids = readJson.data.nodes[0].objects;
  let bar_x = [];
  let bar_y = [];
  let bar_colors = [];

  for (var key in readJson.data.nodes) {
    geneID = readJson.data.nodes[key].objects;

    if(geneID && geneID == ids[0]){
      for ( var i = 0; i < readJson.data.group_names.length; i++) {
        fc_temp = readJson.data.nodes[key].information[readJson.data.group_names[i].replace("_vs_","/")+".fc"]
        bar_x.push(readJson.data.group_names[i]);
        if (fc_temp > 0) {
          fc = logB(fc_temp,2);
          bar_colors.push(volcanoRed);
        } else {
          fc = -logB(-fc_temp,2);
          bar_colors.push(volcanoBlue);
        }
        bar_y.push(fc)
      }
    }
  }


  barplot_data = [{
    x:bar_x,
    y:bar_y,
    type:'bar',
    textposition: 'outside',
    marker:{color:bar_colors}}]

  layout = {
    title: data3FcBarPlotTitle,
    width: data3FcBarPlotWidth,
    height: data3FcBarPlotHeight,
    yaxis: {
      zeroline: true,
      gridwith: 4
    },
    xaxis: {
      tickangle: data3FcBarPlotXaxisTickAngle
    },
    yaxis: {
    title: data3FcBarPlotYaxisTitle
    }
  };

  Plotly.newPlot('barplot_myDiv2', barplot_data, layout);
}

function barplotData3Main2(readJson) {

  ids = readJson.data.nodes["inchlib#0"].objects;

  let bar_x = [];
  let bar_y = [];
  let bar_colors = [];

  for (var key in readJson.data.nodes) {
    geneID = readJson.data.nodes[key].objects;

    if(geneID && geneID == ids[0]){
      for ( var i = 0; i < readJson.data.group_names.length; i++) {
        fc_temp = readJson.data.nodes[key].information[readJson.data.group_names[i].replace("_vs_","/")+".fc"]
        bar_x.push(readJson.data.group_names[i]);
        if (fc_temp > 0) {
          fc = logB(fc_temp,2);
          bar_colors.push(volcanoRed);
        } else {
          fc = -logB(-fc_temp,2);
          bar_colors.push(volcanoBlue);
        }
        bar_y.push(fc)
      }
    }
  }


  barplot_data = [{
    x:bar_x,
    y:bar_y,
    type:'bar',
    textposition: 'outside',
    marker:{color:bar_colors}}]

  layout = {
    title: data3FcBarPlotTitle,
    width: data3FcBarPlotWidth,
    height: data3FcBarPlotHeight,
    yaxis: {
      zeroline: true,
      gridwith: 4
    },
    xaxis: {
      tickangle: data3FcBarPlotXaxisTickAngle
    },
    yaxis: {
    title: data3FcBarPlotYaxisTitle
    }
  };

  Plotly.newPlot('barplot_myDiv2', barplot_data, layout);
}