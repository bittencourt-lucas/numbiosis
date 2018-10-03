const trigonometric = /^(\()?(sin|cos|tan|arcsin|arccos|arctan|hypot|arctan2|degress|radians|unwrap|deg2rad|rad2deg)/;
const hyperbolic = /(sinh|cosh|tang|arcsinh|arcosh|arctang)/
const rouding = /(around|round_|rint|fix|floor|ceil|trunc)/
const sumsProductsDifferences = /(prod|sum|nanprod|nansum|cumprod|cumsum|nancumprod|nancumsum|diff|ediff1d|gradient|cross|trapz)/
const exponentsLogarithms = /(exp|expm1|exp2|log2|log1p|logaddexp|logaddexp2)/

const multiplyRegex = /\d+(?=([a-z|A-Z]))/

function preProcess(func) {
  var processed = '';
  var index
  func = 'cos(tg(sin))';
  while(func.length > 0) {
    if(trigonometric.test(func)) {
      index = trigonometric.exec(func);
      var val = (index['index'] + index[0].length);
      processed = func.substring(0, val);
      func = func.slice(val);
      processed = func.replace(trigonometric.exec(func)[0], `np.${trigonometric.exec(func)[0]}`);
    }
  }
  console.log(func);
}

function fixGraph(func) {
  var plot = func.replace("np.", "");
  if (plot.indexOf("**") !== -1) {
    plot = plot.replace("**", "^");
  }
  if (plot.indexOf("=")) {
    plot = plot.substring(0, s.indexOf('='));
  }
  return plot;
}

function fixPython(func) {
  let plot = func;
  while(plot.indexOf("^") !== -1) {
    plot = plot.replace("^", "**")
  }
  let fix;
  while(multiplyRegex.test(plot)) {
    fix = multiplyRegex.exec(plot);
    plot = plot.replace(`${fix[0]}${fix[1]}`, `${fix[0]}*${fix[1]}`)
  }
  return plot;
}