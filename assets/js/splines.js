
$(function() {
  $( document ).tooltip({ track: true });
  createPlotage();
  $('#calcular').click(function () {
    const csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    const intervalTag = $('#interval');
    const defined_function = $('#defined_function');
    const category = $('#category').val();
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


    createPlotage(plot);
    function generateColor() {
        let color;
        const colorNumber = Math.floor(Math.random() * Math.floor(6));
        switch(colorNumber) {
          case 0:
            color = 'red';
            break;
          case 1:
            color = 'green';
            break;
          case 2:
            color = 'blue';
            break;
          case 3:
            color = 'purple';
            break;
          case 4:
            color = 'black';
            break;
          case 5:
            color = 'yellow';
            break;
          case 6:
            color = 'grey';
            break;
          default:
            color = 'red';
        }
        return color;
    }
    function createAproximation(element, dataType) {
      let vectors;
      element.forEach((value, index) => {
        vectors = {
          vector: value,
          offset: value,
          graphType: category,
          fnType: 'vector',
          color: generateColor(),
        }
        dataType.push(vectors);
      });
      return dataType;
    }
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
        console.log(approximations);
        let dataType = [
          { fn: plot},
          { points: graphic, fnType: 'points',  graphType: 'scatter', color: 'black'},

        ]
        dataType = createAproximation(approximations, dataType);
        console.log(dataType);
        // lastPoint = lastPoint[lastPoint.length - 1];
        createPlotage(undefined, undefined, undefined, dataType);
        $('#interations_value').text(interval);
        // $('#found_y').text(`(${lastPoint[0]},${lastPoint[1]})`);
        $('#function_title').text(plot);
      }
    });
  })
});
