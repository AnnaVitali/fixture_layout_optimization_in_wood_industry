include "globals.mzn";

% Data are expressed in dm to avoid overflow.

float: WTab = 7.00;
float: HTab = 4.00;
float: WMin = 1.40;
int: NTypes = 2;
array[1..NTypes] of int: _NFix = [5, 5];
int: NFix = sum(_NFix);
array[0..NTypes] of float: WFix = array1d(0..NTypes, [0, 1.45, 1.45]);
array[0..NTypes] of float: HFix = array1d(0..NTypes, [0, 1.45,  0.55]);

int: minFix = 2; % min no. of fixtures.
int: maxFix = 4; % max no. of fixtures.

array [1..NFix] of var 0..WTab: x;
array [1..NFix] of var 0..HTab: y;
array [1..NFix] of var 0..NTypes: t;

array [1..NTypes] of var 0..NFix: _n;
var minFix..maxFix: n;

var 0..WTab: x_g;
var 0..HTab: y_g;

float: maxJxFix = 159238584.33333334;
array [1..maxFix] of var 0..maxJxFix: jx_fix;

float: maxJyFix = 169353335.48583332;
array [1..maxFix] of var 0..maxJxFix: jy_fix;

float: maxJxyFix = 127358033.42500001;
array [1..maxFix] of var 0..maxJxFix: jxy_fix;

% Total moments
var 0..maxJxFix*maxFix: jx;
var 0..maxJyFix*maxFix: jy;
var 0..maxJxyFix*maxFix: jxy;

% Result of inertia expression
float: maxRoot = 1019667262.6100001;
var 0..maxRoot: root;


function var float: xc(var 0..NFix: i):: promise_total = x[i] + (WFix[t[i]] / 2);
function var float: yc(var 0..NFix: i)::promise_total = y[i] + (HFix[t[i]] / 2);
function var float: xw(var 0..NFix: i)::promise_total = x[i] + WFix[t[i]];
function var float: yh(var 0..NFix: i)::promise_total = y[i] + HFix[t[i]];

function var float: area(var 0..NFix: i)::promise_total = WFix[t[i]] * HFix[t[i]];

% common terms (edge-wise oriented area contributions)
function var float: ct_v1_v2(var 0..NFix: i)::promise_total = x[i] * yh(i) - x[i] * y[i];
function var float: ct_v2_v3(var 0..NFix: i)::promise_total = x[i] * yh(i) - xw(i) * yh(i);
function var float: ct_v3_v4(var 0..NFix: i)::promise_total = xw(i) * y[i] - xw(i) * yh(i);
function var float: ct_v4_v1(var 0..NFix: i)::promise_total = xw(i) * y[i] - x[i] * y[i];

constraint n = sum(_n);
constraint _n = [count(t,i) | i in 1..NTypes] /\ count(t,0) = NFix - n;


constraint forall(i in 1..NTypes)(_n[i] <= _NFix[i]);

constraint forall(i, j in 1..n where i < j)
(
  t[i] = t[j] -> lex_greater([x[j], y[j]], [x[i], y[i]])
);

constraint forall (i in 1..NFix) (
  (i > n) <-> (x[i] = WTab /\ y[i] = HTab /\ t[i] = 0)
);

% non-overlapping
constraint forall(i, j in 1..n where i < j)(
  xw(i) <= x[j] \/
  xw(j) <= x[i] \/
  yh(i) <= y[j] \/
  yh(j) <= y[i]
);

constraint forall (i in 1..n)(
  x[i] >= 0.2                       /\
  -0.2*x[i] + yh(i) - 2.5791 <= 0   /\
  0.58*xw(i) + yh(i) - 7.8192 <= 0  /\
  xw(i) - 6.89 <= 0                 /\
  0.54*xw(i) - y[i] - 3.5621 <= 0   /\
  -0.2*x[i] - y[i] + 1.3906 <= 0
);


constraint forall (i in 2..n where x[i-1] != x[i]) (
  x[i-1] + WFix[t[i]] + WMin <= x[i]
);

constraint x_g * sum([area(i) | i in 1..NFix]) = sum([area(i) * xc(i) | i in 1..NFix]);

constraint y_g * sum([area(i) | i in 1..NFix]) = sum([area(i) * yc(i) | i in 1..NFix]);

constraint forall(i in 1..maxFix)(
  jx_fix[i] = abs((
    (y[i]*y[i] + y[i]*yh(i) + yh(i)*yh(i)) * ct_v1_v2(i) +
    (3 * yh(i)*yh(i)) * ct_v2_v3(i) +
    (yh(i)*yh(i) + yh(i)*y[i] + y[i]*y[i]) * ct_v3_v4(i) +
    (3 * y[i]*y[i]) * ct_v4_v1(i)
  ) / 12)
  /\
  jy_fix[i] = abs((
    (3 * x[i]*x[i]) * ct_v1_v2(i) +
    (x[i]*x[i] + x[i]*xw(i) + xw(i)*xw(i)) * ct_v2_v3(i) +
    (3 * xw(i)*xw(i)) * ct_v3_v4(i) +
    (xw(i)*xw(i) + xw(i)*x[i] + x[i]*x[i]) * ct_v4_v1(i)
  ) / 12)
  /\
  jxy_fix[i] = abs(3 * (
    x[i] * (y[i] + yh(i)) * ct_v1_v2(i) +
    (x[i] + xw(i)) * yh(i) * ct_v2_v3(i) +
    xw(i) * (y[i] + yh(i)) * ct_v3_v4(i) +
    (x[i] + xw(i)) * y[i] * ct_v4_v1(i)
  ) / 24)
);

constraint jx = sum(jx_fix) - sum([area(i) | i in 1..NFix]) * y_g * y_g;

constraint jy = sum(jy_fix) - sum([area(i) | i in 1..NFix]) * x_g * x_g;

constraint jxy = sum(jxy_fix) - sum([area(i) | i in 1..NFix]) * x_g * y_g;

constraint (root * root) = (jx - jy) * (jx - jy) + 4 * (jxy * jxy);

% Maximize the sum of the Principal Moments of Inertia
solve maximize (0.5 * (jx + jy) - 0.5 * root) + (0.5 * (jx + jy) + 0.5 * root);

output [
  "{\n",
  "\"x\": ", show([i * 100.0 | i in x]), ",\n",
  "\"y\": ", show([i * 100.0 | i in y]), ",\n",
  "\"fixtures_center_x\": ", show([(x[i] + (WFix[t[i]] / 2)) * 100.0 | i in 1..n]), ",\n",
  "\"fixtures_center_y\": ", show([(y[i] + (HFix[t[i]] / 2)) * 100.0 | i in 1..n]), ",\n",
  "\"selected_fixture\": ", show([1 * (t[i] != 0) | i in 1..NFix]), ",\n",
  "\"fixture_type\": ", show(t), ",\n",
  "\"x_g\": ", show(x_g * 100.0), ",\n",
  "\"y_g\": ", show(y_g * 100.0), ",\n",
  "\"objective_value\": ", show(_objective), "\n",
  "}\n"
];

