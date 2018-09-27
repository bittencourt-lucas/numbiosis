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

    function createSolutionElement(solution, tagId) {
      const tbody = $(`#${tagId}`);
      const tr = $('<tr></tr');
      let td;
      solution.forEach(element => {
        td = $('<td></td');
        td.text(element);
        tr.append(td);
      });
      tbody.append(tr);
    }

    function extended(solution, tagId) {
      solution.forEach(element => {
        createSolutionElement(element, tagId);
      });
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
        createSolutionElement(response.solution, 'solution');
        extended(response.extended, 'extended-matrix');
      }
    });
  });
});