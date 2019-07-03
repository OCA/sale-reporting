// This is an hack to get the hover_* options translated on the
// boolean_fa_icon_widget terminology widget. The terms are translated through
// _t(opt_terms.hover_true) or _t(opt_terms.hover_true) which will only work
// if the terms are already present in the translation map.
// This code does nothing but marks the strings as translatable
var _t = function(x) { return x; };

_t("Switch to: details hidden");
_t("Switch to: details shown");
_t("Switch to: subtotal hidden");
_t("Switch to: subtotal shown");
