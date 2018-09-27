
$(function() {
  $( document ).tooltip({ track: true });
  createPlotage();
  $('#calcular').click(function () {
    var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    var botton_estimate = $('#botton_estimate');
    var top_estimate = $('#top_estimate');
    var function_calculate = $('#function_calculate');
    var tolerance = $('#tolerance');
    var maximum_interations = $('#maximum_interations');

    var xl = botton_estimate.val();
    var xu = top_estimate.val();
    var f = function_calculate.val();
    var tol = tolerance.val();
    var maxi = maximum_interations.val();
    if(isNaN(xl) || isNaN(xu) || isNaN(tol) || isNaN(maxi)) {
      alert('Foi digitado um tipo não aceito. Verifique novamente os campos.');
      return;
    }

    if(!xl) { xl = botton_estimate.attr('placeholder'); }
    if(!xu) { xu = top_estimate.attr('placeholder'); }
    if(!f) { f = function_calculate.attr('placeholder'); }
    if(!tol) { tol = tolerance.attr('placeholder'); }
    if(!maxi) { maxi = maximum_interations.attr('placeholder'); }
    var plot = fixGraph(f);
    f = fixPython(f);

    createPlotage(plot);
    $.ajax({
      type:"POST",
      url:"/modulo1/calculafp",
      data: {
        "xl": xl,
        "xu": xu,
        "f": f,
        "tol": tol,
        "maxi": maxi,
        "csrfmiddlewaretoken": csrftoken
      },
      success: function(response){
        var lastPoint = response.points;
        lastPoint = lastPoint[lastPoint.length - 1];
        createPlotage(plot, response.points);
        $('#interations_value').text(maxi);
        $('#found_y').text(`(${lastPoint[0]},${lastPoint[1]})`);
        $('#function_title').text(plot);
      }
    });
  })
});
