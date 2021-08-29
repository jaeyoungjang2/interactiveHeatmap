// login view setting
function boxPlotMain() {
  let box_y0 = [];
  let box_y1 = [];

  testGroupName = readJson.data.group_names.test;
  controlGroupName = readJson.data.group_names.control;
  testGroupSampleList = readJson.data.test;
  controlGroupSampleList = readJson.data.control;

  geneID = readJson.data.nodes[0].objects;

  for (var value in readJson.data.nodes[0].information){
    if(value.startsWith('N_') && testGroupSampleList.includes(value.slice(2))){
      N_expression = readJson.data.nodes[0].information[value];
      box_y0.push(N_expression) ;
    } else if (value.startsWith('N_') && controlGroupSampleList.includes(value.slice(2))) {
      N_expression = readJson.data.nodes[0].information[value];
      box_y1.push(N_expression);
    }
  }

  var trace1 = {
    y: box_y0,
    type: 'box',
    name: testGroupName,
    marker: {
      color: boxPlotRed
    }
  };

  var trace2 = {
    y: box_y1,
    type: 'box',
    name: controlGroupName,
    marker:{
      color: boxPlotGray
    }
  };

  var data = [trace1, trace2];
  layout = {
    title: {
      text: boxPlotTitle,
      font: {size: boxPlotTitleFontSize},
    },
    yaxis: {
      title: boxPlotYaxisTitle
    },
    width: boxPlotWidth,
    height: boxPlotHeight
  };

  Plotly.newPlot('boxplot_myDiv', data, layout);
}

function box_paintImage(ids){
  // console.log("HIddddddddddddddddddddddddd");
  box_y0 = [];
  box_y1 = [];

  for (var key in readJson.data.nodes) {
    geneID = readJson.data.nodes[key].objects;
    if(geneID && geneID == ids[0]){
      for (var value in readJson.data.nodes[key].information){
        if(value.startsWith('N_') && testGroupSampleList.includes(value.slice(2))){
          N_expression = readJson.data.nodes[key].information[value];
          box_y0.push(N_expression) ;
        } else if (value.startsWith('N_') && controlGroupSampleList.includes(value.slice(2))) {
          N_expression = readJson.data.nodes[key].information[value];
          box_y1.push(N_expression);
        }
      }
    }
  }

  var trace1 = {
    y: box_y0,
    type: 'box',
    name: testGroupName,
    marker: {
      color: boxPlotRed
    }
  };

  var trace2 = {
    y: box_y1,
    type: 'box',
    name: controlGroupName,
    marker:{
      color: boxPlotGray
    }
  };

  layout = {
    title: {
      text: boxPlotTitle,
      font: {size: boxPlotTitleFontSize},
    },
    yaxis: {
      title: boxPlotYaxisTitle
    },
    width: boxPlotWidth,
    height: boxPlotHeight
  };

  var data = [trace1, trace2];
  Plotly.newPlot('boxplot_myDiv', data, layout);
}



function boxPlotMain2() {
  let box_y0 = [];
  let box_y1 = [];

  testGroupName = readJson.data.group_names.test;
  controlGroupName = readJson.data.group_names.control;
  testGroupSampleList = readJson.data.test;
  controlGroupSampleList = readJson.data.control;

  geneID = readJson.data.nodes[key].objects;

  for (var value in readJson.data.nodes[key].information){
    if(value.startsWith('N_') && testGroupSampleList.includes(value.slice(2))){
      N_expression = readJson.data.nodes[key].information[value];
      box_y0.push(N_expression) ;
    } else if (value.startsWith('N_') && controlGroupSampleList.includes(value.slice(2))) {
      N_expression = readJson.data.nodes[key].information[value];
      box_y1.push(N_expression);
    }
  }

  var trace1 = {
    y: box_y0,
    type: 'box',
    name: testGroupName,
    marker: {
      color: boxPlotRed
    }
  };

  var trace2 = {
    y: box_y1,
    type: 'box',
    name: controlGroupName,
    marker:{
      color: boxPlotGray
    }
  };

  var data = [trace1, trace2];
  layout = {
    title: {
      text: boxPlotTitle,
      font: {size: boxPlotTitleFontSize},
    },
    yaxis: {
      title: boxPlotYaxisTitle
    },
    width: boxPlotWidth,
    height: boxPlotHeight
  };

  Plotly.newPlot('boxplot_myDiv', data, layout);
}