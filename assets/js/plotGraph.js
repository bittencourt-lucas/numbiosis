const plotTag = "#show_plots";
let widthX = $(plotTag).width();
let heightY = $(plotTag).height();
  /**
 * Plotage
 */
function createPlotage(fn, points) {
  if(!fn) {
    fn = '0';
  }
  if (!points) {
    points = [[0,0]];
  }
  functionPlot({
    target: plotTag,
    grid: true,
    width: widthX,
    height: heightY,
    data: [
      { fn: fn },
      { points: points, fnType: 'points',  graphType: 'scatter' }
    ]
  })
}

$(window).on('resize', function(){
  widthX = ($(plotTag).width()) - 10;
  heightY = ($(plotTag).height()) - 10;
  createPlotage();
});