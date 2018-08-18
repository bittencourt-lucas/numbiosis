const trigonometric = /^(\()?(sin|cos|tan|arcsin|arccos|arctan|hypot|arctan2|degress|radians|unwrap|deg2rad|rad2deg)/;
const hyperbolic = /(sinh|cosh|tang|arcsinh|arcosh|arctang)/
const rouding = /(around|round_|rint|fix|floor|ceil|trunc)/
const sumsProductsDifferences = /(prod|sum|nanprod|nansum|cumprod|cumsum|nancumprod|nancumsum|diff|ediff1d|gradient|cross|trapz)/
const exponentsLogarithms = /(exp|expm1|exp2|log2|log1p|logaddexp|logaddexp2)/

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