include "globals.mzn";

int: WTab = 700;
int: HTab = 400;
int: WMin = 140;
int: NTypes = 2;
array[1..NTypes] of int: _NFix = [5, 5];
int: NFix = sum(_NFix);
array[0..NTypes] of int: WFix = array1d(0..NTypes, [0, 145, 145]);
array[0..NTypes] of int: HFix = array1d(0..NTypes, [0, 145,  55]);

int: minFix = 2; % min no. of fixtures.
int: maxFix = 4; % max no. of fixtures.

array [1..NFix] of var 0..WTab: x;
array [1..NFix] of var 0..HTab: y;
array [1..NFix] of var 0..NTypes: t;

array [1..NTypes] of var 0..NFix: _n;
var minFix..maxFix: n;

function var int:
xc(var 0..NFix: i) ::promise_total = (x[i] + (WFix[t[i]] div 2));
function var int:
yc(var 0..NFix: i) ::promise_total = (y[i] + (HFix[t[i]] div 2));

constraint n = sum(_n);

constraint _n = [count(t,i) | i in 1..NTypes] /\ count(t,0) = NFix - n;

constraint forall(i in 1..NTypes)(_n[i] <= _NFix[i]);

constraint lex_chain(array2d(1..2, 1..NFix, x ++ y));

constraint forall (i in 1..NFix) (
  (i > n) <-> (x[i] = WTab /\ y[i] = HTab /\ t[i] = 0)
);

constraint diffn_nonstrict(
  x, y, [WFix[t[i]] | i in 1..NFix], [HFix[t[i]] | i in 1..NFix]
);

constraint forall (i in 2..n where x[i-1] != x[i]) (
  x[i-1] + WFix[t[i]] + WMin <= x[i]
);

% Geometric constraints
constraint forall (i in 1..n)(
let {
  var int: x1 = x[i] + WFix[t[i]];
  var int: y1 = y[i] + HFix[t[i]];
} in
  x[i] >= 20                       /\
  -20*x[i] + 100*y1 - 25791 <= 0   /\
  58*x1 + 100*y1 - 78192 <= 0      /\
  x1 - 689 <= 0                    /\
  54*x1 - 100*y[i] - 35621 <= 0    /\
  -20*x[i] - 100*y[i] + 13906 <= 0
);

% Maximize distance between pairs of centroids plus sum widths + heights
% for each fixture.
solve maximize
sum(i, j in 1..n where i < j)(
  abs(xc(i) - xc(j)) + abs(yc(i) - yc(j))
) +
sum(i in 1..n)(WFix[t[i]] + HFix[t[i]]);

output [
  "{\n",
  "\"x\": ", show(x), ",\n",
  "\"y\": ", show(y), ",\n",
  "\"fixtures_center_x\": ", show([(x[i] + (WFix[t[i]] / 2)) | i in 1..n]), ",\n",
  "\"fixtures_center_y\": ", show([(y[i] + (HFix[t[i]] / 2)) | i in 1..n]), ",\n",
  "\"selected_fixture\": ", show([1 * (t[i] != 0) | i in 1..NFix]), ",\n",
  "\"fixture_type\": ", show(t), ",\n",
  "\"objective_value\": ", show(_objective), "\n",
  "}\n"
];