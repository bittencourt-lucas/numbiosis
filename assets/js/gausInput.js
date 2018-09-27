$(function() {
  /**
   * @param {object} columnElement element from DOM which have a list of input values.
   */
  function loadElement(columnElement) {
    const columnArray = [];
    columnElement.each(function(index) {
      element = $(this);
      if (element.val() === '' || element.val() === undefined) {
        element = element.attr('placeholder');
        columnArray.push(element);
      }
    });
    return columnArray;
  }

  $('#calcule').click(function() {
    const firstColumn = $('.first-column');
    const middleColumn = $('.middle-column');
    const lastColumn = $('.last-column');
    const vectorColumn = $('.vector-column');
    const matrix = [];
    const vector =  JSON.stringify(loadElement(vectorColumn));
    const csrftoken = $('input[name=csrfmiddlewaretoken]').val();
    const resultTable = $('#result_table');

    matrix.push(loadElement(firstColumn));
    matrix.push(loadElement(middleColumn));
    matrix.push(loadElement(lastColumn));

    function createSolutionElement(solution) {
      const solutionTag = $('#solution');
      let concatString;
      solution.forEach(element => {
       solutionTag.text(solutionTag.text() + ', ' + element);
      });
      solutionTag.text('[' + (solutionTag.text()).substr(1) + ' ]');
    }

    $.ajax({
      type:"POST",
      url:"/modulo2/calculaGaussJordan",
      data: {
        "matrizA":  JSON.stringify(matrix),
        "vectorB": vector,
        "csrfmiddlewaretoken": csrftoken,
      },
      success: function(response){
        createSolutionElement(response.solution);
      }
    });
  });
});