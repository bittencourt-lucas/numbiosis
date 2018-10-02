const plotTag = "#show_plots";
let widthX = $(plotTag).width();
let heightY = $(plotTag).height();
  /**
 * Plotage
 */
function createPlotage(fn, points, fnTypes, dataType, graph) {
  if(!fn) {
    fn = '0';
  }
  if (!points) {
    points = [[0,0]];
  }

  if(!fnTypes) {
    fnTypes = 'points'
  }

  if(!graph) {
    graph = 'scatter';
  }

  if(!dataType) {
    dataType =
    [
      { fn: fn },
      { points: points, fnType: fnTypes,  graphType: graph }
    ]
  }
  functionPlot({
    target: plotTag,
    grid: true,
    width: widthX,
    height: heightY,
    data: dataType,
  })
}

$(window).on('resize', function(){
  widthX = ($(plotTag).width()) - 10;
  heightY = ($(plotTag).height()) - 10;
  createPlotage();
});