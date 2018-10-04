
$(function() {
  $( document ).tooltip({ track: true });
  createPlotage();

  $('#calcular').click(function () {
    var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    var botton_estimate = $('#botton_estimate');
    var top_estimate = $('#top_estimate');
    var function_calculate = $('#function_calculate');
    var function_calculate2 = $('#function_calculate2');
    var tolerance = $('#tolerance');
    var maximum_interations = $('#maximum_interations');

    var xl = botton_estimate.val();
    var xu = top_estimate.val();
    var f = function_calculate.val();
    var f2 = function_calculate2.val();
    var tol = tolerance.val();
    var maxi = maximum_interations.val();
    // if(isNaN(xl) || isNaN(xu) || isNaN(tol) || isNaN(maxi)) {
    //   alert('Foi digitado um tipo não aceito. Verifique novamente os campos.');
    //   return;
    // }

    if(!xl) { xl = botton_estimate.attr('placeholder'); }
    if(!xu) { xu = top_estimate.attr('placeholder'); }
    if(!f) { f = function_calculate.attr('placeholder'); }
    if(!f2) { f2 = function_calculate2.attr('placeholder'); }
    if(!tol) { tol = tolerance.attr('placeholder'); }
    if(!maxi) { maxi = maximum_interations.attr('placeholder'); }
    console.log('Inside calcular newton')
    const plot = fixGraph(f);
    const plot2 = fixGraph(f2);
    f = fixPython(f);
    f2 = fixPython(f2);

    console.log(plot)
    console.log(plot2)
    const data = [
      { fn: plot, fnType: 'implicit', color: 'blue' },
      { fn: plot2, fnType: 'implicit', color: 'green' },
      { points: [[0,0]], fnType: 'points', graphType: 'scatter' }
    ];

    createPlotage(undefined, undefined, undefined, data);
    $.ajax({
      type:"POST",
      url:"/modulo2/calculaNewton",
      data: {
        "xl": xl,
        "xu": xu,
        "func1": f,
        "func2": f2,
        "tol": tol,
        "maxi": maxi,
        "csrfmiddlewaretoken": csrftoken
      },
      success: function(response){
        const points = response.points;
        const lastPoint = points[points.length - 1]
        console.log(response)
        const data = [
          { fn: plot, fnType: 'implicit' },
          { fn: plot2, fnType: 'implicit', color: 'green' },
          { points: points, fnType: 'points',  graphType: 'scatter', color: 'red' },
        ];
        createPlotage(undefined,undefined, undefined, data);
        $('#interations_value').text(maxi);
        $('#found_y').text(`(${lastPoint[0]},${lastPoint[1]})`);
        $('#function_title').text(plot);
      }
    });
  })
});
