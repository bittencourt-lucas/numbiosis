
$(function() {
  $( document ).tooltip({ track: true });
  createPlotage();
  $('#calcular').click(function () {
    const csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    const intervalTag = $('#interval');
    const defined_function = $('#defined_function');

    var f = defined_function.val();
    var interval = intervalTag.val();

    if(isNaN(interval)) {
      alert('Foi digitado um tipo não aceito. Verifique novamente os campos.');
      return;
    }

    if(!f) { f = defined_function.attr('placeholder'); }
    if(!interval) { interval = intervalTag.attr('placeholder'); }
    var plot = fixGraph(f);
    f = fixPython(f);


    // createPlotage(plot, [[0,0]],'linear');
    $.ajax({
      type:"POST",
      url:"/modulo2/processingSpline",
      data: {
        "f": f,
        "interval": interval,
        "csrfmiddlewaretoken": csrftoken
      },
      success: function(response){
        console.log(response);
        var graphic = response.graphic;
        var approximations = response.aproximations;
        // lastPoint = lastPoint[lastPoint.length - 1];

        createPlotage(plot, approximations, 'linear');
        $('#interations_value').text(interval);
        // $('#found_y').text(`(${lastPoint[0]},${lastPoint[1]})`);
        $('#function_title').text(plot);
      }
    });
  })
});
