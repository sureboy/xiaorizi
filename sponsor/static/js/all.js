!function (a, b, c) {
    var d = function (d, e) {
        var f = !!b.getComputedStyle;
        f || (b.getComputedStyle = function (a) {
            return this.el = a, this.getPropertyValue = function (b) {
                var c = /(\-([a-z]){1})/g;
                return "float" === b && (b = "styleFloat"), c.test(b) && (b = b.replace(c, function () {
                    return arguments[2].toUpperCase()
                })), a.currentStyle[b] ? a.currentStyle[b] : null
            }, this
        });
        var g, h, i, j, k, l, m = function (a, b, c, d) {
            if ("addEventListener"in a) {
                try {
                    a.addEventListener(b, c, d)
                } catch (e) {
                    if ("object" != typeof c || !c.handleEvent) {
                        throw e
                    }
                    a.addEventListener(b, function (a) {
                        c.handleEvent.call(c, a)
                    }, d)
                }
            } else {
                "attachEvent"in a && ("object" == typeof c && c.handleEvent ? a.attachEvent("on" + b, function () {
                    c.handleEvent.call(c)
                }) : a.attachEvent("on" + b, c))
            }
        }, n = function (a, b, c, d) {
            if ("removeEventListener"in a) {
                try {
                    a.removeEventListener(b, c, d)
                } catch (e) {
                    if ("object" != typeof c || !c.handleEvent) {
                        throw e
                    }
                    a.removeEventListener(b, function (a) {
                        c.handleEvent.call(c, a)
                    }, d)
                }
            } else {
                "detachEvent"in a && ("object" == typeof c && c.handleEvent ? a.detachEvent("on" + b, function () {
                    c.handleEvent.call(c)
                }) : a.detachEvent("on" + b, c))
            }
        }, o = function (a) {
            if (a.children.length < 1) {
                throw new Error("The Nav container has no containing elements")
            }
            for (var b = [], c = 0; c < a.children.length; c++) {
                1 === a.children[c].nodeType && b.push(a.children[c])
            }
            return b
        }, p = function (a, b) {
            for (var c in b) {
                a.setAttribute(c, b[c])
            }
        }, q = function (a, b) {
            0 !== a.className.indexOf(b) && (a.className += " " + b, a.className = a.className.replace(/(^\s*)|(\s*$)/g, ""))
        }, r = function (a, b) {
            var c = new RegExp("(\\s|^)" + b + "(\\s|$)");
            a.className = a.className.replace(c, " ").replace(/(^\s*)|(\s*$)/g, "")
        }, s = function (a, b, c) {
            for (var d = 0; d < a.length; d++) {
                b.call(c, d, a[d])
            }
        }, t = a.createElement("style"), u = a.documentElement, v = function (b, c) {
            var d;
            this.options = {
                animate: !0,
                transition: 284,
                label: "Menu",
                insert: "before",
                customToggle: "",
                closeOnNavClick: !1,
                openPos: "relative",
                navClass: "nav-collapse",
                navActiveClass: "js-nav-active",
                jsClass: "js",
                init: function () {
                },
                open: function () {
                },
                close: function () {
                }
            };
            for (d in c) {
                this.options[d] = c[d]
            }
            if (q(u, this.options.jsClass), this.wrapperEl = b.replace("#", ""), a.getElementById(this.wrapperEl)) {
                this.wrapper = a.getElementById(this.wrapperEl)
            } else {
                if (!a.querySelector(this.wrapperEl)) {
                    throw new Error("The nav element you are trying to select doesn't exist")
                }
                this.wrapper = a.querySelector(this.wrapperEl)
            }
            this.wrapper.inner = o(this.wrapper), h = this.options, g = this.wrapper, this._init(this)
        };
        return v.prototype = {
            destroy: function () {
                this._removeStyles(), r(g, "closed"), r(g, "opened"), r(g, h.navClass), r(g, h.navClass + "-" + this.index), r(u, h.navActiveClass), g.removeAttribute("style"), g.removeAttribute("aria-hidden"), n(b, "resize", this, !1), n(a.body, "touchmove", this, !1), n(i, "touchstart", this, !1), n(i, "touchend", this, !1), n(i, "mouseup", this, !1), n(i, "keyup", this, !1), n(i, "click", this, !1), h.customToggle ? i.removeAttribute("aria-hidden") : i.parentNode.removeChild(i)
            }, toggle: function () {
                j === !0 && (l ? this.close() : this.open())
            }, open: function () {
                l || (r(g, "closed"), q(g, "opened"), q(u, h.navActiveClass), q(i, "active"), g.style.position = h.openPos, p(g, {"aria-hidden": "false"}), l = !0, h.open())
            }, close: function () {
                l && (q(g, "closed"), r(g, "opened"), r(u, h.navActiveClass), r(i, "active"), p(g, {"aria-hidden": "true"}), h.animate ? (j = !1, setTimeout(function () {
                    g.style.position = "absolute", j = !0
                }, h.transition + 10)) : g.style.position = "absolute", l = !1, h.close())
            }, resize: function () {
                "none" !== b.getComputedStyle(i, null).getPropertyValue("display") ? (k = !0, p(i, {"aria-hidden": "false"}), g.className.match(/(^|\s)closed(\s|$)/) && (p(g, {"aria-hidden": "true"}), g.style.position = "absolute"), this._createStyles(), this._calcHeight()) : (k = !1, p(i, {"aria-hidden": "true"}), p(g, {"aria-hidden": "false"}), g.style.position = h.openPos, this._removeStyles())
            }, handleEvent: function (a) {
                var c = a || b.event;
                switch (c.type) {
                    case"touchstart":
                        this._onTouchStart(c);
                        break;
                    case"touchmove":
                        this._onTouchMove(c);
                        break;
                    case"touchend":
                    case"mouseup":
                        this._onTouchEnd(c);
                        break;
                    case"click":
                        this._preventDefault(c);
                        break;
                    case"keyup":
                        this._onKeyUp(c);
                        break;
                    case"resize":
                        this.resize(c)
                }
            }, _init: function () {
                this.index = c++, q(g, h.navClass), q(g, h.navClass + "-" + this.index), q(g, "closed"), j = !0, l = !1, this._closeOnNavClick(), this._createToggle(), this._transitions(), this.resize();
                var d = this;
                setTimeout(function () {
                    d.resize()
                }, 20), m(b, "resize", this, !1), m(a.body, "touchmove", this, !1), m(i, "touchstart", this, !1), m(i, "touchend", this, !1), m(i, "mouseup", this, !1), m(i, "keyup", this, !1), m(i, "click", this, !1), h.init()
            }, _createStyles: function () {
                t.parentNode || (t.type = "text/css", a.getElementsByTagName("head")[0].appendChild(t))
            }, _removeStyles: function () {
                t.parentNode && t.parentNode.removeChild(t)
            }, _createToggle: function () {
                if (h.customToggle) {
                    var b = h.customToggle.replace("#", "");
                    if (a.getElementById(b)) {
                        i = a.getElementById(b)
                    } else {
                        if (!a.querySelector(b)) {
                            throw new Error("The custom nav toggle you are trying to select doesn't exist")
                        }
                        i = a.querySelector(b)
                    }
                } else {
                    var c = a.createElement("a");
                    c.innerHTML = h.label, p(c, {
                        href: "#",
                        "class": "nav-toggle"
                    }), "after" === h.insert ? g.parentNode.insertBefore(c, g.nextSibling) : g.parentNode.insertBefore(c, g), i = c
                }
            }, _closeOnNavClick: function () {
                if (h.closeOnNavClick && "querySelectorAll"in a) {
                    var b = g.querySelectorAll("a"), c = this;
                    s(b, function (a) {
                        m(b[a], "click", function () {
                            k && c.toggle()
                        }, !1)
                    })
                }
            }, _preventDefault: function (a) {
                a.preventDefault ? (a.preventDefault(), a.stopPropagation()) : a.returnValue = !1
            }, _onTouchStart: function (b) {
                b.stopPropagation(), "after" === h.insert && q(a.body, "disable-pointer-events"), this.startX = b.touches[0].clientX, this.startY = b.touches[0].clientY, this.touchHasMoved = !1, n(i, "mouseup", this, !1)
            }, _onTouchMove: function (a) {
                (Math.abs(a.touches[0].clientX - this.startX) > 10 || Math.abs(a.touches[0].clientY - this.startY) > 10) && (this.touchHasMoved = !0)
            }, _onTouchEnd: function (c) {
                if (this._preventDefault(c), !this.touchHasMoved) {
                    if ("touchend" === c.type) {
                        return this.toggle(), "after" === h.insert && setTimeout(function () {
                            r(a.body, "disable-pointer-events")
                        }, h.transition + 300), void 0
                    }
                    var d = c || b.event;
                    3 !== d.which && 2 !== d.button && this.toggle()
                }
            }, _onKeyUp: function (a) {
                var c = a || b.event;
                13 === c.keyCode && this.toggle()
            }, _transitions: function () {
                if (h.animate) {
                    var a = g.style, b = "max-height " + h.transition + "ms";
                    a.WebkitTransition = b, a.MozTransition = b, a.OTransition = b, a.transition = b
                }
            }, _calcHeight: function () {
                for (var a = 0, b = 0; b < g.inner.length; b++) {
                    a += g.inner[b].offsetHeight
                }
                var c = "." + h.jsClass + " ." + h.navClass + "-" + this.index + ".opened{max-height:" + a + "px !important}";
                t.styleSheet ? t.styleSheet.cssText = c : t.innerHTML = c, c = ""
            }
        }, new v(d, e)
    };
    b.responsiveNav = d
}(document, window, 0);
(function (e, t) {
    function _(e) {
        var t = M[e] = {};
        return v.each(e.split(y), function (e, n) {
            t[n] = !0
        }), t
    }

    function H(e, n, r) {
        if (r === t && e.nodeType === 1) {
            var i = "data-" + n.replace(P, "-$1").toLowerCase();
            r = e.getAttribute(i);
            if (typeof r == "string") {
                try {
                    r = r === "true" ? !0 : r === "false" ? !1 : r === "null" ? null : +r + "" === r ? +r : D.test(r) ? v.parseJSON(r) : r
                } catch (s) {
                }
                v.data(e, n, r)
            } else {
                r = t
            }
        }
        return r
    }

    function B(e) {
        var t;
        for (t in e) {
            if (t === "data" && v.isEmptyObject(e[t])) {
                continue
            }
            if (t !== "toJSON") {
                return !1
            }
        }
        return !0
    }

    function et() {
        return !1
    }

    function tt() {
        return !0
    }

    function ut(e) {
        return !e || !e.parentNode || e.parentNode.nodeType === 11
    }

    function at(e, t) {
        do {
            e = e[t]
        } while (e && e.nodeType !== 1);
        return e
    }

    function ft(e, t, n) {
        t = t || 0;
        if (v.isFunction(t)) {
            return v.grep(e, function (e, r) {
                var i = !!t.call(e, r, e);
                return i === n
            })
        }
        if (t.nodeType) {
            return v.grep(e, function (e, r) {
                return e === t === n
            })
        }
        if (typeof t == "string") {
            var r = v.grep(e, function (e) {
                return e.nodeType === 1
            });
            if (it.test(t)) {
                return v.filter(t, r, !n)
            }
            t = v.filter(t, r)
        }
        return v.grep(e, function (e, r) {
            return v.inArray(e, t) >= 0 === n
        })
    }

    function lt(e) {
        var t = ct.split("|"), n = e.createDocumentFragment();
        if (n.createElement) {
            while (t.length) {
                n.createElement(t.pop())
            }
        }
        return n
    }

    function Lt(e, t) {
        return e.getElementsByTagName(t)[0] || e.appendChild(e.ownerDocument.createElement(t))
    }

    function At(e, t) {
        if (t.nodeType !== 1 || !v.hasData(e)) {
            return
        }
        var n, r, i, s = v._data(e), o = v._data(t, s), u = s.events;
        if (u) {
            delete o.handle, o.events = {};
            for (n in u) {
                for (r = 0, i = u[n].length; r < i; r++) {
                    v.event.add(t, n, u[n][r])
                }
            }
        }
        o.data && (o.data = v.extend({}, o.data))
    }

    function Ot(e, t) {
        var n;
        if (t.nodeType !== 1) {
            return
        }
        t.clearAttributes && t.clearAttributes(), t.mergeAttributes && t.mergeAttributes(e), n = t.nodeName.toLowerCase(), n === "object" ? (t.parentNode && (t.outerHTML = e.outerHTML), v.support.html5Clone && e.innerHTML && !v.trim(t.innerHTML) && (t.innerHTML = e.innerHTML)) : n === "input" && Et.test(e.type) ? (t.defaultChecked = t.checked = e.checked, t.value !== e.value && (t.value = e.value)) : n === "option" ? t.selected = e.defaultSelected : n === "input" || n === "textarea" ? t.defaultValue = e.defaultValue : n === "script" && t.text !== e.text && (t.text = e.text), t.removeAttribute(v.expando)
    }

    function Mt(e) {
        return typeof e.getElementsByTagName != "undefined" ? e.getElementsByTagName("*") : typeof e.querySelectorAll != "undefined" ? e.querySelectorAll("*") : []
    }

    function _t(e) {
        Et.test(e.type) && (e.defaultChecked = e.checked)
    }

    function Qt(e, t) {
        if (t in e) {
            return t
        }
        var n = t.charAt(0).toUpperCase() + t.slice(1), r = t, i = Jt.length;
        while (i--) {
            t = Jt[i] + n;
            if (t in e) {
                return t
            }
        }
        return r
    }

    function Gt(e, t) {
        return e = t || e, v.css(e, "display") === "none" || !v.contains(e.ownerDocument, e)
    }

    function Yt(e, t) {
        var n, r, i = [], s = 0, o = e.length;
        for (; s < o; s++) {
            n = e[s];
            if (!n.style) {
                continue
            }
            i[s] = v._data(n, "olddisplay"), t ? (!i[s] && n.style.display === "none" && (n.style.display = ""), n.style.display === "" && Gt(n) && (i[s] = v._data(n, "olddisplay", nn(n.nodeName)))) : (r = Dt(n, "display"), !i[s] && r !== "none" && v._data(n, "olddisplay", r))
        }
        for (s = 0; s < o; s++) {
            n = e[s];
            if (!n.style) {
                continue
            }
            if (!t || n.style.display === "none" || n.style.display === "") {
                n.style.display = t ? i[s] || "" : "none"
            }
        }
        return e
    }

    function Zt(e, t, n) {
        var r = Rt.exec(t);
        return r ? Math.max(0, r[1] - (n || 0)) + (r[2] || "px") : t
    }

    function en(e, t, n, r) {
        var i = n === (r ? "border" : "content") ? 4 : t === "width" ? 1 : 0, s = 0;
        for (; i < 4; i += 2) {
            n === "margin" && (s += v.css(e, n + $t[i], !0)), r ? (n === "content" && (s -= parseFloat(Dt(e, "padding" + $t[i])) || 0), n !== "margin" && (s -= parseFloat(Dt(e, "border" + $t[i] + "Width")) || 0)) : (s += parseFloat(Dt(e, "padding" + $t[i])) || 0, n !== "padding" && (s += parseFloat(Dt(e, "border" + $t[i] + "Width")) || 0))
        }
        return s
    }

    function tn(e, t, n) {
        var r = t === "width" ? e.offsetWidth : e.offsetHeight, i = !0, s = v.support.boxSizing && v.css(e, "boxSizing") === "border-box";
        if (r <= 0 || r == null) {
            r = Dt(e, t);
            if (r < 0 || r == null) {
                r = e.style[t]
            }
            if (Ut.test(r)) {
                return r
            }
            i = s && (v.support.boxSizingReliable || r === e.style[t]), r = parseFloat(r) || 0
        }
        return r + en(e, t, n || (s ? "border" : "content"), i) + "px"
    }

    function nn(e) {
        if (Wt[e]) {
            return Wt[e]
        }
        var t = v("<" + e + ">").appendTo(i.body), n = t.css("display");
        t.remove();
        if (n === "none" || n === "") {
            Pt = i.body.appendChild(Pt || v.extend(i.createElement("iframe"), {frameBorder: 0, width: 0, height: 0}));
            if (!Ht || !Pt.createElement) {
                Ht = (Pt.contentWindow || Pt.contentDocument).document, Ht.write("<!doctype html><html><body>"), Ht.close()
            }
            t = Ht.body.appendChild(Ht.createElement(e)), n = Dt(t, "display"), i.body.removeChild(Pt)
        }
        return Wt[e] = n, n
    }

    function fn(e, t, n, r) {
        var i;
        if (v.isArray(t)) {
            v.each(t, function (t, i) {
                n || sn.test(e) ? r(e, i) : fn(e + "[" + (typeof i == "object" ? t : "") + "]", i, n, r)
            })
        } else {
            if (!n && v.type(t) === "object") {
                for (i in t) {
                    fn(e + "[" + i + "]", t[i], n, r)
                }
            } else {
                r(e, t)
            }
        }
    }

    function Cn(e) {
        return function (t, n) {
            typeof t != "string" && (n = t, t = "*");
            var r, i, s, o = t.toLowerCase().split(y), u = 0, a = o.length;
            if (v.isFunction(n)) {
                for (; u < a; u++) {
                    r = o[u], s = /^\+/.test(r), s && (r = r.substr(1) || "*"), i = e[r] = e[r] || [], i[s ? "unshift" : "push"](n)
                }
            }
        }
    }

    function kn(e, n, r, i, s, o) {
        s = s || n.dataTypes[0], o = o || {}, o[s] = !0;
        var u, a = e[s], f = 0, l = a ? a.length : 0, c = e === Sn;
        for (; f < l && (c || !u); f++) {
            u = a[f](n, r, i), typeof u == "string" && (!c || o[u] ? u = t : (n.dataTypes.unshift(u), u = kn(e, n, r, i, u, o)))
        }
        return (c || !u) && !o["*"] && (u = kn(e, n, r, i, "*", o)), u
    }

    function Ln(e, n) {
        var r, i, s = v.ajaxSettings.flatOptions || {};
        for (r in n) {
            n[r] !== t && ((s[r] ? e : i || (i = {}))[r] = n[r])
        }
        i && v.extend(!0, e, i)
    }

    function An(e, n, r) {
        var i, s, o, u, a = e.contents, f = e.dataTypes, l = e.responseFields;
        for (s in l) {
            s in r && (n[l[s]] = r[s])
        }
        while (f[0] === "*") {
            f.shift(), i === t && (i = e.mimeType || n.getResponseHeader("content-type"))
        }
        if (i) {
            for (s in a) {
                if (a[s] && a[s].test(i)) {
                    f.unshift(s);
                    break
                }
            }
        }
        if (f[0]in r) {
            o = f[0]
        } else {
            for (s in r) {
                if (!f[0] || e.converters[s + " " + f[0]]) {
                    o = s;
                    break
                }
                u || (u = s)
            }
            o = o || u
        }
        if (o) {
            return o !== f[0] && f.unshift(o), r[o]
        }
    }

    function On(e, t) {
        var n, r, i, s, o = e.dataTypes.slice(), u = o[0], a = {}, f = 0;
        e.dataFilter && (t = e.dataFilter(t, e.dataType));
        if (o[1]) {
            for (n in e.converters) {
                a[n.toLowerCase()] = e.converters[n]
            }
        }
        for (; i = o[++f];) {
            if (i !== "*") {
                if (u !== "*" && u !== i) {
                    n = a[u + " " + i] || a["* " + i];
                    if (!n) {
                        for (r in a) {
                            s = r.split(" ");
                            if (s[1] === i) {
                                n = a[u + " " + s[0]] || a["* " + s[0]];
                                if (n) {
                                    n === !0 ? n = a[r] : a[r] !== !0 && (i = s[0], o.splice(f--, 0, i));
                                    break
                                }
                            }
                        }
                    }
                    if (n !== !0) {
                        if (n && e["throws"]) {
                            t = n(t)
                        } else {
                            try {
                                t = n(t)
                            } catch (l) {
                                return {state: "parsererror", error: n ? l : "No conversion from " + u + " to " + i}
                            }
                        }
                    }
                }
                u = i
            }
        }
        return {state: "success", data: t}
    }

    function Fn() {
        try {
            return new e.XMLHttpRequest
        } catch (t) {
        }
    }

    function In() {
        try {
            return new e.ActiveXObject("Microsoft.XMLHTTP")
        } catch (t) {
        }
    }

    function $n() {
        return setTimeout(function () {
            qn = t
        }, 0), qn = v.now()
    }

    function Jn(e, t) {
        v.each(t, function (t, n) {
            var r = (Vn[t] || []).concat(Vn["*"]), i = 0, s = r.length;
            for (; i < s; i++) {
                if (r[i].call(e, t, n)) {
                    return
                }
            }
        })
    }

    function Kn(e, t, n) {
        var r, i = 0, s = 0, o = Xn.length, u = v.Deferred().always(function () {
            delete a.elem
        }), a = function () {
            var t = qn || $n(), n = Math.max(0, f.startTime + f.duration - t), r = n / f.duration || 0, i = 1 - r, s = 0, o = f.tweens.length;
            for (; s < o; s++) {
                f.tweens[s].run(i)
            }
            return u.notifyWith(e, [f, i, n]), i < 1 && o ? n : (u.resolveWith(e, [f]), !1)
        }, f = u.promise({
            elem: e,
            props: v.extend({}, t),
            opts: v.extend(!0, {specialEasing: {}}, n),
            originalProperties: t,
            originalOptions: n,
            startTime: qn || $n(),
            duration: n.duration,
            tweens: [],
            createTween: function (t, n, r) {
                var i = v.Tween(e, f.opts, t, n, f.opts.specialEasing[t] || f.opts.easing);
                return f.tweens.push(i), i
            },
            stop: function (t) {
                var n = 0, r = t ? f.tweens.length : 0;
                for (; n < r; n++) {
                    f.tweens[n].run(1)
                }
                return t ? u.resolveWith(e, [f, t]) : u.rejectWith(e, [f, t]), this
            }
        }), l = f.props;
        Qn(l, f.opts.specialEasing);
        for (; i < o; i++) {
            r = Xn[i].call(f, e, l, f.opts);
            if (r) {
                return r
            }
        }
        return Jn(f, l), v.isFunction(f.opts.start) && f.opts.start.call(e, f), v.fx.timer(v.extend(a, {
            anim: f,
            queue: f.opts.queue,
            elem: e
        })), f.progress(f.opts.progress).done(f.opts.done, f.opts.complete).fail(f.opts.fail).always(f.opts.always)
    }

    function Qn(e, t) {
        var n, r, i, s, o;
        for (n in e) {
            r = v.camelCase(n), i = t[r], s = e[n], v.isArray(s) && (i = s[1], s = e[n] = s[0]), n !== r && (e[r] = s, delete e[n]), o = v.cssHooks[r];
            if (o && "expand"in o) {
                s = o.expand(s), delete e[r];
                for (n in s) {
                    n in e || (e[n] = s[n], t[n] = i)
                }
            } else {
                t[r] = i
            }
        }
    }

    function Gn(e, t, n) {
        var r, i, s, o, u, a, f, l, c, h = this, p = e.style, d = {}, m = [], g = e.nodeType && Gt(e);
        n.queue || (l = v._queueHooks(e, "fx"), l.unqueued == null && (l.unqueued = 0, c = l.empty.fire, l.empty.fire = function () {
            l.unqueued || c()
        }), l.unqueued++, h.always(function () {
            h.always(function () {
                l.unqueued--, v.queue(e, "fx").length || l.empty.fire()
            })
        })), e.nodeType === 1 && ("height"in t || "width"in t) && (n.overflow = [p.overflow, p.overflowX, p.overflowY], v.css(e, "display") === "inline" && v.css(e, "float") === "none" && (!v.support.inlineBlockNeedsLayout || nn(e.nodeName) === "inline" ? p.display = "inline-block" : p.zoom = 1)), n.overflow && (p.overflow = "none", v.support.shrinkWrapBlocks || h.done(function () {
            p.overflow = n.overflow[0], p.overflowX = n.overflow[1], p.overflowY = n.overflow[2]
        }));
        for (r in t) {
            s = t[r];
            if (Un.exec(s)) {
                delete t[r], a = a || s === "toggle";
                if (s === (g ? "hide" : "show")) {
                    continue
                }
                m.push(r)
            }
        }
        o = m.length;
        if (o) {
            u = v._data(e, "fxshow") || v._data(e, "fxshow", {}), "hidden"in u && (g = u.hidden), a && (u.hidden = !g), g ? v(e).show() : h.done(function () {
                v(e).hide()
            }), h.done(function () {
                var t;
                v.removeData(e, "fxshow", !0);
                for (t in d) {
                    v.style(e, t, d[t])
                }
            });
            for (r = 0; r < o; r++) {
                i = m[r], f = h.createTween(i, g ? u[i] : 0), d[i] = u[i] || v.style(e, i), i in u || (u[i] = f.start, g && (f.end = f.start, f.start = i === "width" || i === "height" ? 1 : 0))
            }
        }
    }

    function Yn(e, t, n, r, i) {
        return new Yn.prototype.init(e, t, n, r, i)
    }

    function Zn(e, t) {
        var n, r = {height: e}, i = 0;
        t = t ? 1 : 0;
        for (; i < 4; i += 2 - t) {
            n = $t[i], r["margin" + n] = r["padding" + n] = e
        }
        return t && (r.opacity = r.width = e), r
    }

    function tr(e) {
        return v.isWindow(e) ? e : e.nodeType === 9 ? e.defaultView || e.parentWindow : !1
    }

    var n, r, i = e.document, s = e.location, o = e.navigator, u = e.jQuery, a = e.$, f = Array.prototype.push, l = Array.prototype.slice, c = Array.prototype.indexOf, h = Object.prototype.toString, p = Object.prototype.hasOwnProperty, d = String.prototype.trim, v = function (e, t) {
        return new v.fn.init(e, t, n)
    }, m = /[\-+]?(?:\d*\.|)\d+(?:[eE][\-+]?\d+|)/.source, g = /\S/, y = /\s+/, b = /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, w = /^(?:[^#<]*(<[\w\W]+>)[^>]*$|#([\w\-]*)$)/, E = /^<(\w+)\s*\/?>(?:<\/\1>|)$/, S = /^[\],:{}\s]*$/, x = /(?:^|:|,)(?:\s*\[)+/g, T = /\\(?:["\\\/bfnrt]|u[\da-fA-F]{4})/g, N = /"[^"\\\r\n]*"|true|false|null|-?(?:\d\d*\.|)\d+(?:[eE][\-+]?\d+|)/g, C = /^-ms-/, k = /-([\da-z])/gi, L = function (e, t) {
        return (t + "").toUpperCase()
    }, A = function () {
        i.addEventListener ? (i.removeEventListener("DOMContentLoaded", A, !1), v.ready()) : i.readyState === "complete" && (i.detachEvent("onreadystatechange", A), v.ready())
    }, O = {};
    v.fn = v.prototype = {
        constructor: v, init: function (e, n, r) {
            var s, o, u, a;
            if (!e) {
                return this
            }
            if (e.nodeType) {
                return this.context = this[0] = e, this.length = 1, this
            }
            if (typeof e == "string") {
                e.charAt(0) === "<" && e.charAt(e.length - 1) === ">" && e.length >= 3 ? s = [null, e, null] : s = w.exec(e);
                if (s && (s[1] || !n)) {
                    if (s[1]) {
                        return n = n instanceof v ? n[0] : n, a = n && n.nodeType ? n.ownerDocument || n : i, e = v.parseHTML(s[1], a, !0), E.test(s[1]) && v.isPlainObject(n) && this.attr.call(e, n, !0), v.merge(this, e)
                    }
                    o = i.getElementById(s[2]);
                    if (o && o.parentNode) {
                        if (o.id !== s[2]) {
                            return r.find(e)
                        }
                        this.length = 1, this[0] = o
                    }
                    return this.context = i, this.selector = e, this
                }
                return !n || n.jquery ? (n || r).find(e) : this.constructor(n).find(e)
            }
            return v.isFunction(e) ? r.ready(e) : (e.selector !== t && (this.selector = e.selector, this.context = e.context), v.makeArray(e, this))
        }, selector: "", jquery: "1.8.3", length: 0, size: function () {
            return this.length
        }, toArray: function () {
            return l.call(this)
        }, get: function (e) {
            return e == null ? this.toArray() : e < 0 ? this[this.length + e] : this[e]
        }, pushStack: function (e, t, n) {
            var r = v.merge(this.constructor(), e);
            return r.prevObject = this, r.context = this.context, t === "find" ? r.selector = this.selector + (this.selector ? " " : "") + n : t && (r.selector = this.selector + "." + t + "(" + n + ")"), r
        }, each: function (e, t) {
            return v.each(this, e, t)
        }, ready: function (e) {
            return v.ready.promise().done(e), this
        }, eq: function (e) {
            return e = +e, e === -1 ? this.slice(e) : this.slice(e, e + 1)
        }, first: function () {
            return this.eq(0)
        }, last: function () {
            return this.eq(-1)
        }, slice: function () {
            return this.pushStack(l.apply(this, arguments), "slice", l.call(arguments).join(","))
        }, map: function (e) {
            return this.pushStack(v.map(this, function (t, n) {
                return e.call(t, n, t)
            }))
        }, end: function () {
            return this.prevObject || this.constructor(null)
        }, push: f, sort: [].sort, splice: [].splice
    }, v.fn.init.prototype = v.fn, v.extend = v.fn.extend = function () {
        var e, n, r, i, s, o, u = arguments[0] || {}, a = 1, f = arguments.length, l = !1;
        typeof u == "boolean" && (l = u, u = arguments[1] || {}, a = 2), typeof u != "object" && !v.isFunction(u) && (u = {}), f === a && (u = this, --a);
        for (; a < f; a++) {
            if ((e = arguments[a]) != null) {
                for (n in e) {
                    r = u[n], i = e[n];
                    if (u === i) {
                        continue
                    }
                    l && i && (v.isPlainObject(i) || (s = v.isArray(i))) ? (s ? (s = !1, o = r && v.isArray(r) ? r : []) : o = r && v.isPlainObject(r) ? r : {}, u[n] = v.extend(l, o, i)) : i !== t && (u[n] = i)
                }
            }
        }
        return u
    }, v.extend({
        noConflict: function (t) {
            return e.$ === v && (e.$ = a), t && e.jQuery === v && (e.jQuery = u), v
        }, isReady: !1, readyWait: 1, holdReady: function (e) {
            e ? v.readyWait++ : v.ready(!0)
        }, ready: function (e) {
            if (e === !0 ? --v.readyWait : v.isReady) {
                return
            }
            if (!i.body) {
                return setTimeout(v.ready, 1)
            }
            v.isReady = !0;
            if (e !== !0 && --v.readyWait > 0) {
                return
            }
            r.resolveWith(i, [v]), v.fn.trigger && v(i).trigger("ready").off("ready")
        }, isFunction: function (e) {
            return v.type(e) === "function"
        }, isArray: Array.isArray || function (e) {
            return v.type(e) === "array"
        }, isWindow: function (e) {
            return e != null && e == e.window
        }, isNumeric: function (e) {
            return !isNaN(parseFloat(e)) && isFinite(e)
        }, type: function (e) {
            return e == null ? String(e) : O[h.call(e)] || "object"
        }, isPlainObject: function (e) {
            if (!e || v.type(e) !== "object" || e.nodeType || v.isWindow(e)) {
                return !1
            }
            try {
                if (e.constructor && !p.call(e, "constructor") && !p.call(e.constructor.prototype, "isPrototypeOf")) {
                    return !1
                }
            } catch (n) {
                return !1
            }
            var r;
            for (r in e) {
            }
            return r === t || p.call(e, r)
        }, isEmptyObject: function (e) {
            var t;
            for (t in e) {
                return !1
            }
            return !0
        }, error: function (e) {
            throw new Error(e)
        }, parseHTML: function (e, t, n) {
            var r;
            return !e || typeof e != "string" ? null : (typeof t == "boolean" && (n = t, t = 0), t = t || i, (r = E.exec(e)) ? [t.createElement(r[1])] : (r = v.buildFragment([e], t, n ? null : []), v.merge([], (r.cacheable ? v.clone(r.fragment) : r.fragment).childNodes)))
        }, parseJSON: function (t) {
            if (!t || typeof t != "string") {
                return null
            }
            t = v.trim(t);
            if (e.JSON && e.JSON.parse) {
                return e.JSON.parse(t)
            }
            if (S.test(t.replace(T, "@").replace(N, "]").replace(x, ""))) {
                return (new Function("return " + t))()
            }
            v.error("Invalid JSON: " + t)
        }, parseXML: function (n) {
            var r, i;
            if (!n || typeof n != "string") {
                return null
            }
            try {
                e.DOMParser ? (i = new DOMParser, r = i.parseFromString(n, "text/xml")) : (r = new ActiveXObject("Microsoft.XMLDOM"), r.async = "false", r.loadXML(n))
            } catch (s) {
                r = t
            }
            return (!r || !r.documentElement || r.getElementsByTagName("parsererror").length) && v.error("Invalid XML: " + n), r
        }, noop: function () {
        }, globalEval: function (t) {
            t && g.test(t) && (e.execScript || function (t) {
                e.eval.call(e, t)
            })(t)
        }, camelCase: function (e) {
            return e.replace(C, "ms-").replace(k, L)
        }, nodeName: function (e, t) {
            return e.nodeName && e.nodeName.toLowerCase() === t.toLowerCase()
        }, each: function (e, n, r) {
            var i, s = 0, o = e.length, u = o === t || v.isFunction(e);
            if (r) {
                if (u) {
                    for (i in e) {
                        if (n.apply(e[i], r) === !1) {
                            break
                        }
                    }
                } else {
                    for (; s < o;) {
                        if (n.apply(e[s++], r) === !1) {
                            break
                        }
                    }
                }
            } else {
                if (u) {
                    for (i in e) {
                        if (n.call(e[i], i, e[i]) === !1) {
                            break
                        }
                    }
                } else {
                    for (; s < o;) {
                        if (n.call(e[s], s, e[s++]) === !1) {
                            break
                        }
                    }
                }
            }
            return e
        }, trim: d && !d.call("\ufeff\u00a0") ? function (e) {
            return e == null ? "" : d.call(e)
        } : function (e) {
            return e == null ? "" : (e + "").replace(b, "")
        }, makeArray: function (e, t) {
            var n, r = t || [];
            return e != null && (n = v.type(e), e.length == null || n === "string" || n === "function" || n === "regexp" || v.isWindow(e) ? f.call(r, e) : v.merge(r, e)), r
        }, inArray: function (e, t, n) {
            var r;
            if (t) {
                if (c) {
                    return c.call(t, e, n)
                }
                r = t.length, n = n ? n < 0 ? Math.max(0, r + n) : n : 0;
                for (; n < r; n++) {
                    if (n in t && t[n] === e) {
                        return n
                    }
                }
            }
            return -1
        }, merge: function (e, n) {
            var r = n.length, i = e.length, s = 0;
            if (typeof r == "number") {
                for (; s < r; s++) {
                    e[i++] = n[s]
                }
            } else {
                while (n[s] !== t) {
                    e[i++] = n[s++]
                }
            }
            return e.length = i, e
        }, grep: function (e, t, n) {
            var r, i = [], s = 0, o = e.length;
            n = !!n;
            for (; s < o; s++) {
                r = !!t(e[s], s), n !== r && i.push(e[s])
            }
            return i
        }, map: function (e, n, r) {
            var i, s, o = [], u = 0, a = e.length, f = e instanceof v || a !== t && typeof a == "number" && (a > 0 && e[0] && e[a - 1] || a === 0 || v.isArray(e));
            if (f) {
                for (; u < a; u++) {
                    i = n(e[u], u, r), i != null && (o[o.length] = i)
                }
            } else {
                for (s in e) {
                    i = n(e[s], s, r), i != null && (o[o.length] = i)
                }
            }
            return o.concat.apply([], o)
        }, guid: 1, proxy: function (e, n) {
            var r, i, s;
            return typeof n == "string" && (r = e[n], n = e, e = r), v.isFunction(e) ? (i = l.call(arguments, 2), s = function () {
                return e.apply(n, i.concat(l.call(arguments)))
            }, s.guid = e.guid = e.guid || v.guid++, s) : t
        }, access: function (e, n, r, i, s, o, u) {
            var a, f = r == null, l = 0, c = e.length;
            if (r && typeof r == "object") {
                for (l in r) {
                    v.access(e, n, l, r[l], 1, o, i)
                }
                s = 1
            } else {
                if (i !== t) {
                    a = u === t && v.isFunction(i), f && (a ? (a = n, n = function (e, t, n) {
                        return a.call(v(e), n)
                    }) : (n.call(e, i), n = null));
                    if (n) {
                        for (; l < c; l++) {
                            n(e[l], r, a ? i.call(e[l], l, n(e[l], r)) : i, u)
                        }
                    }
                    s = 1
                }
            }
            return s ? e : f ? n.call(e) : c ? n(e[0], r) : o
        }, now: function () {
            return (new Date).getTime()
        }
    }), v.ready.promise = function (t) {
        if (!r) {
            r = v.Deferred();
            if (i.readyState === "complete") {
                setTimeout(v.ready, 1)
            } else {
                if (i.addEventListener) {
                    i.addEventListener("DOMContentLoaded", A, !1), e.addEventListener("load", v.ready, !1)
                } else {
                    i.attachEvent("onreadystatechange", A), e.attachEvent("onload", v.ready);
                    var n = !1;
                    try {
                        n = e.frameElement == null && i.documentElement
                    } catch (s) {
                    }
                    n && n.doScroll && function o() {
                        if (!v.isReady) {
                            try {
                                n.doScroll("left")
                            } catch (e) {
                                return setTimeout(o, 50)
                            }
                            v.ready()
                        }
                    }()
                }
            }
        }
        return r.promise(t)
    }, v.each("Boolean Number String Function Array Date RegExp Object".split(" "), function (e, t) {
        O["[object " + t + "]"] = t.toLowerCase()
    }), n = v(i);
    var M = {};
    v.Callbacks = function (e) {
        e = typeof e == "string" ? M[e] || _(e) : v.extend({}, e);
        var n, r, i, s, o, u, a = [], f = !e.once && [], l = function (t) {
            n = e.memory && t, r = !0, u = s || 0, s = 0, o = a.length, i = !0;
            for (; a && u < o; u++) {
                if (a[u].apply(t[0], t[1]) === !1 && e.stopOnFalse) {
                    n = !1;
                    break
                }
            }
            i = !1, a && (f ? f.length && l(f.shift()) : n ? a = [] : c.disable())
        }, c = {
            add: function () {
                if (a) {
                    var t = a.length;
                    (function r(t) {
                        v.each(t, function (t, n) {
                            var i = v.type(n);
                            i === "function" ? (!e.unique || !c.has(n)) && a.push(n) : n && n.length && i !== "string" && r(n)
                        })
                    })(arguments), i ? o = a.length : n && (s = t, l(n))
                }
                return this
            }, remove: function () {
                return a && v.each(arguments, function (e, t) {
                    var n;
                    while ((n = v.inArray(t, a, n)) > -1) {
                        a.splice(n, 1), i && (n <= o && o--, n <= u && u--)
                    }
                }), this
            }, has: function (e) {
                return v.inArray(e, a) > -1
            }, empty: function () {
                return a = [], this
            }, disable: function () {
                return a = f = n = t, this
            }, disabled: function () {
                return !a
            }, lock: function () {
                return f = t, n || c.disable(), this
            }, locked: function () {
                return !f
            }, fireWith: function (e, t) {
                return t = t || [], t = [e, t.slice ? t.slice() : t], a && (!r || f) && (i ? f.push(t) : l(t)), this
            }, fire: function () {
                return c.fireWith(this, arguments), this
            }, fired: function () {
                return !!r
            }
        };
        return c
    }, v.extend({
        Deferred: function (e) {
            var t = [["resolve", "done", v.Callbacks("once memory"), "resolved"], ["reject", "fail", v.Callbacks("once memory"), "rejected"], ["notify", "progress", v.Callbacks("memory")]], n = "pending", r = {
                state: function () {
                    return n
                }, always: function () {
                    return i.done(arguments).fail(arguments), this
                }, then: function () {
                    var e = arguments;
                    return v.Deferred(function (n) {
                        v.each(t, function (t, r) {
                            var s = r[0], o = e[t];
                            i[r[1]](v.isFunction(o) ? function () {
                                var e = o.apply(this, arguments);
                                e && v.isFunction(e.promise) ? e.promise().done(n.resolve).fail(n.reject).progress(n.notify) : n[s + "With"](this === i ? n : this, [e])
                            } : n[s])
                        }), e = null
                    }).promise()
                }, promise: function (e) {
                    return e != null ? v.extend(e, r) : r
                }
            }, i = {};
            return r.pipe = r.then, v.each(t, function (e, s) {
                var o = s[2], u = s[3];
                r[s[1]] = o.add, u && o.add(function () {
                    n = u
                }, t[e ^ 1][2].disable, t[2][2].lock), i[s[0]] = o.fire, i[s[0] + "With"] = o.fireWith
            }), r.promise(i), e && e.call(i, i), i
        }, when: function (e) {
            var t = 0, n = l.call(arguments), r = n.length, i = r !== 1 || e && v.isFunction(e.promise) ? r : 0, s = i === 1 ? e : v.Deferred(), o = function (e, t, n) {
                return function (r) {
                    t[e] = this, n[e] = arguments.length > 1 ? l.call(arguments) : r, n === u ? s.notifyWith(t, n) : --i || s.resolveWith(t, n)
                }
            }, u, a, f;
            if (r > 1) {
                u = new Array(r), a = new Array(r), f = new Array(r);
                for (; t < r; t++) {
                    n[t] && v.isFunction(n[t].promise) ? n[t].promise().done(o(t, f, n)).fail(s.reject).progress(o(t, a, u)) : --i
                }
            }
            return i || s.resolveWith(f, n), s.promise()
        }
    }), v.support = function () {
        var t, n, r, s, o, u, a, f, l, c, h, p = i.createElement("div");
        p.setAttribute("className", "t"), p.innerHTML = "  <link/><table></table><a href='/a'>a</a><input type='checkbox'/>", n = p.getElementsByTagName("*"), r = p.getElementsByTagName("a")[0];
        if (!n || !r || !n.length) {
            return {}
        }
        s = i.createElement("select"), o = s.appendChild(i.createElement("option")), u = p.getElementsByTagName("input")[0], r.style.cssText = "top:1px;float:left;opacity:.5", t = {
            leadingWhitespace: p.firstChild.nodeType === 3,
            tbody: !p.getElementsByTagName("tbody").length,
            htmlSerialize: !!p.getElementsByTagName("link").length,
            style: /top/.test(r.getAttribute("style")),
            hrefNormalized: r.getAttribute("href") === "/a",
            opacity: /^0.5/.test(r.style.opacity),
            cssFloat: !!r.style.cssFloat,
            checkOn: u.value === "on",
            optSelected: o.selected,
            getSetAttribute: p.className !== "t",
            enctype: !!i.createElement("form").enctype,
            html5Clone: i.createElement("nav").cloneNode(!0).outerHTML !== "<:nav></:nav>",
            boxModel: i.compatMode === "CSS1Compat",
            submitBubbles: !0,
            changeBubbles: !0,
            focusinBubbles: !1,
            deleteExpando: !0,
            noCloneEvent: !0,
            inlineBlockNeedsLayout: !1,
            shrinkWrapBlocks: !1,
            reliableMarginRight: !0,
            boxSizingReliable: !0,
            pixelPosition: !1
        }, u.checked = !0, t.noCloneChecked = u.cloneNode(!0).checked, s.disabled = !0, t.optDisabled = !o.disabled;
        try {
            delete p.test
        } catch (d) {
            t.deleteExpando = !1
        }
        !p.addEventListener && p.attachEvent && p.fireEvent && (p.attachEvent("onclick", h = function () {
            t.noCloneEvent = !1
        }), p.cloneNode(!0).fireEvent("onclick"), p.detachEvent("onclick", h)), u = i.createElement("input"), u.value = "t", u.setAttribute("type", "radio"), t.radioValue = u.value === "t", u.setAttribute("checked", "checked"), u.setAttribute("name", "t"), p.appendChild(u), a = i.createDocumentFragment(), a.appendChild(p.lastChild), t.checkClone = a.cloneNode(!0).cloneNode(!0).lastChild.checked, t.appendChecked = u.checked, a.removeChild(u), a.appendChild(p);
        if (p.attachEvent) {
            for (l in{submit: !0, change: !0, focusin: !0}) {
                f = "on" + l, c = f in p, c || (p.setAttribute(f, "return;"), c = typeof p[f] == "function"), t[l + "Bubbles"] = c
            }
        }
        return v(function () {
            var n, r, s, o, u = "padding:0;margin:0;border:0;display:block;", a = i.getElementsByTagName("body")[0];
            if (!a) {
                return
            }
            n = i.createElement("div"), n.style.cssText = "visibility:hidden;border:0;width:0;height:0;position:static;top:0;margin-top:1px", a.insertBefore(n, a.firstChild), r = i.createElement("div"), n.appendChild(r), r.innerHTML = "<table><tr><td></td><td>t</td></tr></table>", s = r.getElementsByTagName("td"), s[0].style.cssText = "padding:0;margin:0;border:0;display:none", c = s[0].offsetHeight === 0, s[0].style.display = "", s[1].style.display = "none", t.reliableHiddenOffsets = c && s[0].offsetHeight === 0, r.innerHTML = "", r.style.cssText = "box-sizing:border-box;-moz-box-sizing:border-box;-webkit-box-sizing:border-box;padding:1px;border:1px;display:block;width:4px;margin-top:1%;position:absolute;top:1%;", t.boxSizing = r.offsetWidth === 4, t.doesNotIncludeMarginInBodyOffset = a.offsetTop !== 1, e.getComputedStyle && (t.pixelPosition = (e.getComputedStyle(r, null) || {}).top !== "1%", t.boxSizingReliable = (e.getComputedStyle(r, null) || {width: "4px"}).width === "4px", o = i.createElement("div"), o.style.cssText = r.style.cssText = u, o.style.marginRight = o.style.width = "0", r.style.width = "1px", r.appendChild(o), t.reliableMarginRight = !parseFloat((e.getComputedStyle(o, null) || {}).marginRight)), typeof r.style.zoom != "undefined" && (r.innerHTML = "", r.style.cssText = u + "width:1px;padding:1px;display:inline;zoom:1", t.inlineBlockNeedsLayout = r.offsetWidth === 3, r.style.display = "block", r.style.overflow = "visible", r.innerHTML = "<div></div>", r.firstChild.style.width = "5px", t.shrinkWrapBlocks = r.offsetWidth !== 3, n.style.zoom = 1), a.removeChild(n), n = r = s = o = null
        }), a.removeChild(p), n = r = s = o = u = a = p = null, t
    }();
    var D = /(?:\{[\s\S]*\}|\[[\s\S]*\])$/, P = /([A-Z])/g;
    v.extend({
        cache: {},
        deletedIds: [],
        uuid: 0,
        expando: "jQuery" + (v.fn.jquery + Math.random()).replace(/\D/g, ""),
        noData: {embed: !0, object: "clsid:D27CDB6E-AE6D-11cf-96B8-444553540000", applet: !0},
        hasData: function (e) {
            return e = e.nodeType ? v.cache[e[v.expando]] : e[v.expando], !!e && !B(e)
        },
        data: function (e, n, r, i) {
            if (!v.acceptData(e)) {
                return
            }
            var s, o, u = v.expando, a = typeof n == "string", f = e.nodeType, l = f ? v.cache : e, c = f ? e[u] : e[u] && u;
            if ((!c || !l[c] || !i && !l[c].data) && a && r === t) {
                return
            }
            c || (f ? e[u] = c = v.deletedIds.pop() || v.guid++ : c = u), l[c] || (l[c] = {}, f || (l[c].toJSON = v.noop));
            if (typeof n == "object" || typeof n == "function") {
                i ? l[c] = v.extend(l[c], n) : l[c].data = v.extend(l[c].data, n)
            }
            return s = l[c], i || (s.data || (s.data = {}), s = s.data), r !== t && (s[v.camelCase(n)] = r), a ? (o = s[n], o == null && (o = s[v.camelCase(n)])) : o = s, o
        },
        removeData: function (e, t, n) {
            if (!v.acceptData(e)) {
                return
            }
            var r, i, s, o = e.nodeType, u = o ? v.cache : e, a = o ? e[v.expando] : v.expando;
            if (!u[a]) {
                return
            }
            if (t) {
                r = n ? u[a] : u[a].data;
                if (r) {
                    v.isArray(t) || (t in r ? t = [t] : (t = v.camelCase(t), t in r ? t = [t] : t = t.split(" ")));
                    for (i = 0, s = t.length; i < s; i++) {
                        delete r[t[i]]
                    }
                    if (!(n ? B : v.isEmptyObject)(r)) {
                        return
                    }
                }
            }
            if (!n) {
                delete u[a].data;
                if (!B(u[a])) {
                    return
                }
            }
            o ? v.cleanData([e], !0) : v.support.deleteExpando || u != u.window ? delete u[a] : u[a] = null
        },
        _data: function (e, t, n) {
            return v.data(e, t, n, !0)
        },
        acceptData: function (e) {
            var t = e.nodeName && v.noData[e.nodeName.toLowerCase()];
            return !t || t !== !0 && e.getAttribute("classid") === t
        }
    }), v.fn.extend({
        data: function (e, n) {
            var r, i, s, o, u, a = this[0], f = 0, l = null;
            if (e === t) {
                if (this.length) {
                    l = v.data(a);
                    if (a.nodeType === 1 && !v._data(a, "parsedAttrs")) {
                        s = a.attributes;
                        for (u = s.length; f < u; f++) {
                            o = s[f].name, o.indexOf("data-") || (o = v.camelCase(o.substring(5)), H(a, o, l[o]))
                        }
                        v._data(a, "parsedAttrs", !0)
                    }
                }
                return l
            }
            return typeof e == "object" ? this.each(function () {
                v.data(this, e)
            }) : (r = e.split(".", 2), r[1] = r[1] ? "." + r[1] : "", i = r[1] + "!", v.access(this, function (n) {
                if (n === t) {
                    return l = this.triggerHandler("getData" + i, [r[0]]), l === t && a && (l = v.data(a, e), l = H(a, e, l)), l === t && r[1] ? this.data(r[0]) : l
                }
                r[1] = n, this.each(function () {
                    var t = v(this);
                    t.triggerHandler("setData" + i, r), v.data(this, e, n), t.triggerHandler("changeData" + i, r)
                })
            }, null, n, arguments.length > 1, null, !1))
        }, removeData: function (e) {
            return this.each(function () {
                v.removeData(this, e)
            })
        }
    }), v.extend({
        queue: function (e, t, n) {
            var r;
            if (e) {
                return t = (t || "fx") + "queue", r = v._data(e, t), n && (!r || v.isArray(n) ? r = v._data(e, t, v.makeArray(n)) : r.push(n)), r || []
            }
        }, dequeue: function (e, t) {
            t = t || "fx";
            var n = v.queue(e, t), r = n.length, i = n.shift(), s = v._queueHooks(e, t), o = function () {
                v.dequeue(e, t)
            };
            i === "inprogress" && (i = n.shift(), r--), i && (t === "fx" && n.unshift("inprogress"), delete s.stop, i.call(e, o, s)), !r && s && s.empty.fire()
        }, _queueHooks: function (e, t) {
            var n = t + "queueHooks";
            return v._data(e, n) || v._data(e, n, {
                    empty: v.Callbacks("once memory").add(function () {
                        v.removeData(e, t + "queue", !0), v.removeData(e, n, !0)
                    })
                })
        }
    }), v.fn.extend({
        queue: function (e, n) {
            var r = 2;
            return typeof e != "string" && (n = e, e = "fx", r--), arguments.length < r ? v.queue(this[0], e) : n === t ? this : this.each(function () {
                var t = v.queue(this, e, n);
                v._queueHooks(this, e), e === "fx" && t[0] !== "inprogress" && v.dequeue(this, e)
            })
        }, dequeue: function (e) {
            return this.each(function () {
                v.dequeue(this, e)
            })
        }, delay: function (e, t) {
            return e = v.fx ? v.fx.speeds[e] || e : e, t = t || "fx", this.queue(t, function (t, n) {
                var r = setTimeout(t, e);
                n.stop = function () {
                    clearTimeout(r)
                }
            })
        }, clearQueue: function (e) {
            return this.queue(e || "fx", [])
        }, promise: function (e, n) {
            var r, i = 1, s = v.Deferred(), o = this, u = this.length, a = function () {
                --i || s.resolveWith(o, [o])
            };
            typeof e != "string" && (n = e, e = t), e = e || "fx";
            while (u--) {
                r = v._data(o[u], e + "queueHooks"), r && r.empty && (i++, r.empty.add(a))
            }
            return a(), s.promise(n)
        }
    });
    var j, F, I, q = /[\t\r\n]/g, R = /\r/g, U = /^(?:button|input)$/i, z = /^(?:button|input|object|select|textarea)$/i, W = /^a(?:rea|)$/i, X = /^(?:autofocus|autoplay|async|checked|controls|defer|disabled|hidden|loop|multiple|open|readonly|required|scoped|selected)$/i, V = v.support.getSetAttribute;
    v.fn.extend({
        attr: function (e, t) {
            return v.access(this, v.attr, e, t, arguments.length > 1)
        }, removeAttr: function (e) {
            return this.each(function () {
                v.removeAttr(this, e)
            })
        }, prop: function (e, t) {
            return v.access(this, v.prop, e, t, arguments.length > 1)
        }, removeProp: function (e) {
            return e = v.propFix[e] || e, this.each(function () {
                try {
                    this[e] = t, delete this[e]
                } catch (n) {
                }
            })
        }, addClass: function (e) {
            var t, n, r, i, s, o, u;
            if (v.isFunction(e)) {
                return this.each(function (t) {
                    v(this).addClass(e.call(this, t, this.className))
                })
            }
            if (e && typeof e == "string") {
                t = e.split(y);
                for (n = 0, r = this.length; n < r; n++) {
                    i = this[n];
                    if (i.nodeType === 1) {
                        if (!i.className && t.length === 1) {
                            i.className = e
                        } else {
                            s = " " + i.className + " ";
                            for (o = 0, u = t.length; o < u; o++) {
                                s.indexOf(" " + t[o] + " ") < 0 && (s += t[o] + " ")
                            }
                            i.className = v.trim(s)
                        }
                    }
                }
            }
            return this
        }, removeClass: function (e) {
            var n, r, i, s, o, u, a;
            if (v.isFunction(e)) {
                return this.each(function (t) {
                    v(this).removeClass(e.call(this, t, this.className))
                })
            }
            if (e && typeof e == "string" || e === t) {
                n = (e || "").split(y);
                for (u = 0, a = this.length; u < a; u++) {
                    i = this[u];
                    if (i.nodeType === 1 && i.className) {
                        r = (" " + i.className + " ").replace(q, " ");
                        for (s = 0, o = n.length; s < o; s++) {
                            while (r.indexOf(" " + n[s] + " ") >= 0) {
                                r = r.replace(" " + n[s] + " ", " ")
                            }
                        }
                        i.className = e ? v.trim(r) : ""
                    }
                }
            }
            return this
        }, toggleClass: function (e, t) {
            var n = typeof e, r = typeof t == "boolean";
            return v.isFunction(e) ? this.each(function (n) {
                v(this).toggleClass(e.call(this, n, this.className, t), t)
            }) : this.each(function () {
                if (n === "string") {
                    var i, s = 0, o = v(this), u = t, a = e.split(y);
                    while (i = a[s++]) {
                        u = r ? u : !o.hasClass(i), o[u ? "addClass" : "removeClass"](i)
                    }
                } else {
                    if (n === "undefined" || n === "boolean") {
                        this.className && v._data(this, "__className__", this.className), this.className = this.className || e === !1 ? "" : v._data(this, "__className__") || ""
                    }
                }
            })
        }, hasClass: function (e) {
            var t = " " + e + " ", n = 0, r = this.length;
            for (; n < r; n++) {
                if (this[n].nodeType === 1 && (" " + this[n].className + " ").replace(q, " ").indexOf(t) >= 0) {
                    return !0
                }
            }
            return !1
        }, val: function (e) {
            var n, r, i, s = this[0];
            if (!arguments.length) {
                if (s) {
                    return n = v.valHooks[s.type] || v.valHooks[s.nodeName.toLowerCase()], n && "get"in n && (r = n.get(s, "value")) !== t ? r : (r = s.value, typeof r == "string" ? r.replace(R, "") : r == null ? "" : r)
                }
                return
            }
            return i = v.isFunction(e), this.each(function (r) {
                var s, o = v(this);
                if (this.nodeType !== 1) {
                    return
                }
                i ? s = e.call(this, r, o.val()) : s = e, s == null ? s = "" : typeof s == "number" ? s += "" : v.isArray(s) && (s = v.map(s, function (e) {
                    return e == null ? "" : e + ""
                })), n = v.valHooks[this.type] || v.valHooks[this.nodeName.toLowerCase()];
                if (!n || !("set"in n) || n.set(this, s, "value") === t) {
                    this.value = s
                }
            })
        }
    }), v.extend({
        valHooks: {
            option: {
                get: function (e) {
                    var t = e.attributes.value;
                    return !t || t.specified ? e.value : e.text
                }
            }, select: {
                get: function (e) {
                    var t, n, r = e.options, i = e.selectedIndex, s = e.type === "select-one" || i < 0, o = s ? null : [], u = s ? i + 1 : r.length, a = i < 0 ? u : s ? i : 0;
                    for (; a < u; a++) {
                        n = r[a];
                        if ((n.selected || a === i) && (v.support.optDisabled ? !n.disabled : n.getAttribute("disabled") === null) && (!n.parentNode.disabled || !v.nodeName(n.parentNode, "optgroup"))) {
                            t = v(n).val();
                            if (s) {
                                return t
                            }
                            o.push(t)
                        }
                    }
                    return o
                }, set: function (e, t) {
                    var n = v.makeArray(t);
                    return v(e).find("option").each(function () {
                        this.selected = v.inArray(v(this).val(), n) >= 0
                    }), n.length || (e.selectedIndex = -1), n
                }
            }
        },
        attrFn: {},
        attr: function (e, n, r, i) {
            var s, o, u, a = e.nodeType;
            if (!e || a === 3 || a === 8 || a === 2) {
                return
            }
            if (i && v.isFunction(v.fn[n])) {
                return v(e)[n](r)
            }
            if (typeof e.getAttribute == "undefined") {
                return v.prop(e, n, r)
            }
            u = a !== 1 || !v.isXMLDoc(e), u && (n = n.toLowerCase(), o = v.attrHooks[n] || (X.test(n) ? F : j));
            if (r !== t) {
                if (r === null) {
                    v.removeAttr(e, n);
                    return
                }
                return o && "set"in o && u && (s = o.set(e, r, n)) !== t ? s : (e.setAttribute(n, r + ""), r)
            }
            return o && "get"in o && u && (s = o.get(e, n)) !== null ? s : (s = e.getAttribute(n), s === null ? t : s)
        },
        removeAttr: function (e, t) {
            var n, r, i, s, o = 0;
            if (t && e.nodeType === 1) {
                r = t.split(y);
                for (; o < r.length; o++) {
                    i = r[o], i && (n = v.propFix[i] || i, s = X.test(i), s || v.attr(e, i, ""), e.removeAttribute(V ? i : n), s && n in e && (e[n] = !1))
                }
            }
        },
        attrHooks: {
            type: {
                set: function (e, t) {
                    if (U.test(e.nodeName) && e.parentNode) {
                        v.error("type property can't be changed")
                    } else {
                        if (!v.support.radioValue && t === "radio" && v.nodeName(e, "input")) {
                            var n = e.value;
                            return e.setAttribute("type", t), n && (e.value = n), t
                        }
                    }
                }
            }, value: {
                get: function (e, t) {
                    return j && v.nodeName(e, "button") ? j.get(e, t) : t in e ? e.value : null
                }, set: function (e, t, n) {
                    if (j && v.nodeName(e, "button")) {
                        return j.set(e, t, n)
                    }
                    e.value = t
                }
            }
        },
        propFix: {
            tabindex: "tabIndex",
            readonly: "readOnly",
            "for": "htmlFor",
            "class": "className",
            maxlength: "maxLength",
            cellspacing: "cellSpacing",
            cellpadding: "cellPadding",
            rowspan: "rowSpan",
            colspan: "colSpan",
            usemap: "useMap",
            frameborder: "frameBorder",
            contenteditable: "contentEditable"
        },
        prop: function (e, n, r) {
            var i, s, o, u = e.nodeType;
            if (!e || u === 3 || u === 8 || u === 2) {
                return
            }
            return o = u !== 1 || !v.isXMLDoc(e), o && (n = v.propFix[n] || n, s = v.propHooks[n]), r !== t ? s && "set"in s && (i = s.set(e, r, n)) !== t ? i : e[n] = r : s && "get"in s && (i = s.get(e, n)) !== null ? i : e[n]
        },
        propHooks: {
            tabIndex: {
                get: function (e) {
                    var n = e.getAttributeNode("tabindex");
                    return n && n.specified ? parseInt(n.value, 10) : z.test(e.nodeName) || W.test(e.nodeName) && e.href ? 0 : t
                }
            }
        }
    }), F = {
        get: function (e, n) {
            var r, i = v.prop(e, n);
            return i === !0 || typeof i != "boolean" && (r = e.getAttributeNode(n)) && r.nodeValue !== !1 ? n.toLowerCase() : t
        }, set: function (e, t, n) {
            var r;
            return t === !1 ? v.removeAttr(e, n) : (r = v.propFix[n] || n, r in e && (e[r] = !0), e.setAttribute(n, n.toLowerCase())), n
        }
    }, V || (I = {name: !0, id: !0, coords: !0}, j = v.valHooks.button = {
        get: function (e, n) {
            var r;
            return r = e.getAttributeNode(n), r && (I[n] ? r.value !== "" : r.specified) ? r.value : t
        }, set: function (e, t, n) {
            var r = e.getAttributeNode(n);
            return r || (r = i.createAttribute(n), e.setAttributeNode(r)), r.value = t + ""
        }
    }, v.each(["width", "height"], function (e, t) {
        v.attrHooks[t] = v.extend(v.attrHooks[t], {
            set: function (e, n) {
                if (n === "") {
                    return e.setAttribute(t, "auto"), n
                }
            }
        })
    }), v.attrHooks.contenteditable = {
        get: j.get, set: function (e, t, n) {
            t === "" && (t = "false"), j.set(e, t, n)
        }
    }), v.support.hrefNormalized || v.each(["href", "src", "width", "height"], function (e, n) {
        v.attrHooks[n] = v.extend(v.attrHooks[n], {
            get: function (e) {
                var r = e.getAttribute(n, 2);
                return r === null ? t : r
            }
        })
    }), v.support.style || (v.attrHooks.style = {
        get: function (e) {
            return e.style.cssText.toLowerCase() || t
        }, set: function (e, t) {
            return e.style.cssText = t + ""
        }
    }), v.support.optSelected || (v.propHooks.selected = v.extend(v.propHooks.selected, {
        get: function (e) {
            var t = e.parentNode;
            return t && (t.selectedIndex, t.parentNode && t.parentNode.selectedIndex), null
        }
    })), v.support.enctype || (v.propFix.enctype = "encoding"), v.support.checkOn || v.each(["radio", "checkbox"], function () {
        v.valHooks[this] = {
            get: function (e) {
                return e.getAttribute("value") === null ? "on" : e.value
            }
        }
    }), v.each(["radio", "checkbox"], function () {
        v.valHooks[this] = v.extend(v.valHooks[this], {
            set: function (e, t) {
                if (v.isArray(t)) {
                    return e.checked = v.inArray(v(e).val(), t) >= 0
                }
            }
        })
    });
    var $ = /^(?:textarea|input|select)$/i, J = /^([^\.]*|)(?:\.(.+)|)$/, K = /(?:^|\s)hover(\.\S+|)\b/, Q = /^key/, G = /^(?:mouse|contextmenu)|click/, Y = /^(?:focusinfocus|focusoutblur)$/, Z = function (e) {
        return v.event.special.hover ? e : e.replace(K, "mouseenter$1 mouseleave$1")
    };
    v.event = {
        add: function (e, n, r, i, s) {
            var o, u, a, f, l, c, h, p, d, m, g;
            if (e.nodeType === 3 || e.nodeType === 8 || !n || !r || !(o = v._data(e))) {
                return
            }
            r.handler && (d = r, r = d.handler, s = d.selector), r.guid || (r.guid = v.guid++), a = o.events, a || (o.events = a = {}), u = o.handle, u || (o.handle = u = function (e) {
                return typeof v == "undefined" || !!e && v.event.triggered === e.type ? t : v.event.dispatch.apply(u.elem, arguments)
            }, u.elem = e), n = v.trim(Z(n)).split(" ");
            for (f = 0; f < n.length; f++) {
                l = J.exec(n[f]) || [], c = l[1], h = (l[2] || "").split(".").sort(), g = v.event.special[c] || {}, c = (s ? g.delegateType : g.bindType) || c, g = v.event.special[c] || {}, p = v.extend({
                    type: c,
                    origType: l[1],
                    data: i,
                    handler: r,
                    guid: r.guid,
                    selector: s,
                    needsContext: s && v.expr.match.needsContext.test(s),
                    namespace: h.join(".")
                }, d), m = a[c];
                if (!m) {
                    m = a[c] = [], m.delegateCount = 0;
                    if (!g.setup || g.setup.call(e, i, h, u) === !1) {
                        e.addEventListener ? e.addEventListener(c, u, !1) : e.attachEvent && e.attachEvent("on" + c, u)
                    }
                }
                g.add && (g.add.call(e, p), p.handler.guid || (p.handler.guid = r.guid)), s ? m.splice(m.delegateCount++, 0, p) : m.push(p), v.event.global[c] = !0
            }
            e = null
        },
        global: {},
        remove: function (e, t, n, r, i) {
            var s, o, u, a, f, l, c, h, p, d, m, g = v.hasData(e) && v._data(e);
            if (!g || !(h = g.events)) {
                return
            }
            t = v.trim(Z(t || "")).split(" ");
            for (s = 0; s < t.length; s++) {
                o = J.exec(t[s]) || [], u = a = o[1], f = o[2];
                if (!u) {
                    for (u in h) {
                        v.event.remove(e, u + t[s], n, r, !0)
                    }
                    continue
                }
                p = v.event.special[u] || {}, u = (r ? p.delegateType : p.bindType) || u, d = h[u] || [], l = d.length, f = f ? new RegExp("(^|\\.)" + f.split(".").sort().join("\\.(?:.*\\.|)") + "(\\.|$)") : null;
                for (c = 0; c < d.length; c++) {
                    m = d[c], (i || a === m.origType) && (!n || n.guid === m.guid) && (!f || f.test(m.namespace)) && (!r || r === m.selector || r === "**" && m.selector) && (d.splice(c--, 1), m.selector && d.delegateCount--, p.remove && p.remove.call(e, m))
                }
                d.length === 0 && l !== d.length && ((!p.teardown || p.teardown.call(e, f, g.handle) === !1) && v.removeEvent(e, u, g.handle), delete h[u])
            }
            v.isEmptyObject(h) && (delete g.handle, v.removeData(e, "events", !0))
        },
        customEvent: {getData: !0, setData: !0, changeData: !0},
        trigger: function (n, r, s, o) {
            if (!s || s.nodeType !== 3 && s.nodeType !== 8) {
                var u, a, f, l, c, h, p, d, m, g, y = n.type || n, b = [];
                if (Y.test(y + v.event.triggered)) {
                    return
                }
                y.indexOf("!") >= 0 && (y = y.slice(0, -1), a = !0), y.indexOf(".") >= 0 && (b = y.split("."), y = b.shift(), b.sort());
                if ((!s || v.event.customEvent[y]) && !v.event.global[y]) {
                    return
                }
                n = typeof n == "object" ? n[v.expando] ? n : new v.Event(y, n) : new v.Event(y), n.type = y, n.isTrigger = !0, n.exclusive = a, n.namespace = b.join("."), n.namespace_re = n.namespace ? new RegExp("(^|\\.)" + b.join("\\.(?:.*\\.|)") + "(\\.|$)") : null, h = y.indexOf(":") < 0 ? "on" + y : "";
                if (!s) {
                    u = v.cache;
                    for (f in u) {
                        u[f].events && u[f].events[y] && v.event.trigger(n, r, u[f].handle.elem, !0)
                    }
                    return
                }
                n.result = t, n.target || (n.target = s), r = r != null ? v.makeArray(r) : [], r.unshift(n), p = v.event.special[y] || {};
                if (p.trigger && p.trigger.apply(s, r) === !1) {
                    return
                }
                m = [[s, p.bindType || y]];
                if (!o && !p.noBubble && !v.isWindow(s)) {
                    g = p.delegateType || y, l = Y.test(g + y) ? s : s.parentNode;
                    for (c = s; l; l = l.parentNode) {
                        m.push([l, g]), c = l
                    }
                    c === (s.ownerDocument || i) && m.push([c.defaultView || c.parentWindow || e, g])
                }
                for (f = 0; f < m.length && !n.isPropagationStopped(); f++) {
                    l = m[f][0], n.type = m[f][1], d = (v._data(l, "events") || {})[n.type] && v._data(l, "handle"), d && d.apply(l, r), d = h && l[h], d && v.acceptData(l) && d.apply && d.apply(l, r) === !1 && n.preventDefault()
                }
                return n.type = y, !o && !n.isDefaultPrevented() && (!p._default || p._default.apply(s.ownerDocument, r) === !1) && (y !== "click" || !v.nodeName(s, "a")) && v.acceptData(s) && h && s[y] && (y !== "focus" && y !== "blur" || n.target.offsetWidth !== 0) && !v.isWindow(s) && (c = s[h], c && (s[h] = null), v.event.triggered = y, s[y](), v.event.triggered = t, c && (s[h] = c)), n.result
            }
            return
        },
        dispatch: function (n) {
            n = v.event.fix(n || e.event);
            var r, i, s, o, u, a, f, c, h, p, d = (v._data(this, "events") || {})[n.type] || [], m = d.delegateCount, g = l.call(arguments), y = !n.exclusive && !n.namespace, b = v.event.special[n.type] || {}, w = [];
            g[0] = n, n.delegateTarget = this;
            if (b.preDispatch && b.preDispatch.call(this, n) === !1) {
                return
            }
            if (m && (!n.button || n.type !== "click")) {
                for (s = n.target; s != this; s = s.parentNode || this) {
                    if (s.disabled !== !0 || n.type !== "click") {
                        u = {}, f = [];
                        for (r = 0; r < m; r++) {
                            c = d[r], h = c.selector, u[h] === t && (u[h] = c.needsContext ? v(h, this).index(s) >= 0 : v.find(h, this, null, [s]).length), u[h] && f.push(c)
                        }
                        f.length && w.push({elem: s, matches: f})
                    }
                }
            }
            d.length > m && w.push({elem: this, matches: d.slice(m)});
            for (r = 0; r < w.length && !n.isPropagationStopped(); r++) {
                a = w[r], n.currentTarget = a.elem;
                for (i = 0; i < a.matches.length && !n.isImmediatePropagationStopped(); i++) {
                    c = a.matches[i];
                    if (y || !n.namespace && !c.namespace || n.namespace_re && n.namespace_re.test(c.namespace)) {
                        n.data = c.data, n.handleObj = c, o = ((v.event.special[c.origType] || {}).handle || c.handler).apply(a.elem, g), o !== t && (n.result = o, o === !1 && (n.preventDefault(), n.stopPropagation()))
                    }
                }
            }
            return b.postDispatch && b.postDispatch.call(this, n), n.result
        },
        props: "attrChange attrName relatedNode srcElement altKey bubbles cancelable ctrlKey currentTarget eventPhase metaKey relatedTarget shiftKey target timeStamp view which".split(" "),
        fixHooks: {},
        keyHooks: {
            props: "char charCode key keyCode".split(" "), filter: function (e, t) {
                return e.which == null && (e.which = t.charCode != null ? t.charCode : t.keyCode), e
            }
        },
        mouseHooks: {
            props: "button buttons clientX clientY fromElement offsetX offsetY pageX pageY screenX screenY toElement".split(" "),
            filter: function (e, n) {
                var r, s, o, u = n.button, a = n.fromElement;
                return e.pageX == null && n.clientX != null && (r = e.target.ownerDocument || i, s = r.documentElement, o = r.body, e.pageX = n.clientX + (s && s.scrollLeft || o && o.scrollLeft || 0) - (s && s.clientLeft || o && o.clientLeft || 0), e.pageY = n.clientY + (s && s.scrollTop || o && o.scrollTop || 0) - (s && s.clientTop || o && o.clientTop || 0)), !e.relatedTarget && a && (e.relatedTarget = a === e.target ? n.toElement : a), !e.which && u !== t && (e.which = u & 1 ? 1 : u & 2 ? 3 : u & 4 ? 2 : 0), e
            }
        },
        fix: function (e) {
            if (e[v.expando]) {
                return e
            }
            var t, n, r = e, s = v.event.fixHooks[e.type] || {}, o = s.props ? this.props.concat(s.props) : this.props;
            e = v.Event(r);
            for (t = o.length; t;) {
                n = o[--t], e[n] = r[n]
            }
            return e.target || (e.target = r.srcElement || i), e.target.nodeType === 3 && (e.target = e.target.parentNode), e.metaKey = !!e.metaKey, s.filter ? s.filter(e, r) : e
        },
        special: {
            load: {noBubble: !0},
            focus: {delegateType: "focusin"},
            blur: {delegateType: "focusout"},
            beforeunload: {
                setup: function (e, t, n) {
                    v.isWindow(this) && (this.onbeforeunload = n)
                }, teardown: function (e, t) {
                    this.onbeforeunload === t && (this.onbeforeunload = null)
                }
            }
        },
        simulate: function (e, t, n, r) {
            var i = v.extend(new v.Event, n, {type: e, isSimulated: !0, originalEvent: {}});
            r ? v.event.trigger(i, null, t) : v.event.dispatch.call(t, i), i.isDefaultPrevented() && n.preventDefault()
        }
    }, v.event.handle = v.event.dispatch, v.removeEvent = i.removeEventListener ? function (e, t, n) {
        e.removeEventListener && e.removeEventListener(t, n, !1)
    } : function (e, t, n) {
        var r = "on" + t;
        e.detachEvent && (typeof e[r] == "undefined" && (e[r] = null), e.detachEvent(r, n))
    }, v.Event = function (e, t) {
        if (!(this instanceof v.Event)) {
            return new v.Event(e, t)
        }
        e && e.type ? (this.originalEvent = e, this.type = e.type, this.isDefaultPrevented = e.defaultPrevented || e.returnValue === !1 || e.getPreventDefault && e.getPreventDefault() ? tt : et) : this.type = e, t && v.extend(this, t), this.timeStamp = e && e.timeStamp || v.now(), this[v.expando] = !0
    }, v.Event.prototype = {
        preventDefault: function () {
            this.isDefaultPrevented = tt;
            var e = this.originalEvent;
            if (!e) {
                return
            }
            e.preventDefault ? e.preventDefault() : e.returnValue = !1
        }, stopPropagation: function () {
            this.isPropagationStopped = tt;
            var e = this.originalEvent;
            if (!e) {
                return
            }
            e.stopPropagation && e.stopPropagation(), e.cancelBubble = !0
        }, stopImmediatePropagation: function () {
            this.isImmediatePropagationStopped = tt, this.stopPropagation()
        }, isDefaultPrevented: et, isPropagationStopped: et, isImmediatePropagationStopped: et
    }, v.each({mouseenter: "mouseover", mouseleave: "mouseout"}, function (e, t) {
        v.event.special[e] = {
            delegateType: t, bindType: t, handle: function (e) {
                var n, r = this, i = e.relatedTarget, s = e.handleObj, o = s.selector;
                if (!i || i !== r && !v.contains(r, i)) {
                    e.type = s.origType, n = s.handler.apply(this, arguments), e.type = t
                }
                return n
            }
        }
    }), v.support.submitBubbles || (v.event.special.submit = {
        setup: function () {
            if (v.nodeName(this, "form")) {
                return !1
            }
            v.event.add(this, "click._submit keypress._submit", function (e) {
                var n = e.target, r = v.nodeName(n, "input") || v.nodeName(n, "button") ? n.form : t;
                r && !v._data(r, "_submit_attached") && (v.event.add(r, "submit._submit", function (e) {
                    e._submit_bubble = !0
                }), v._data(r, "_submit_attached", !0))
            })
        }, postDispatch: function (e) {
            e._submit_bubble && (delete e._submit_bubble, this.parentNode && !e.isTrigger && v.event.simulate("submit", this.parentNode, e, !0))
        }, teardown: function () {
            if (v.nodeName(this, "form")) {
                return !1
            }
            v.event.remove(this, "._submit")
        }
    }), v.support.changeBubbles || (v.event.special.change = {
        setup: function () {
            if ($.test(this.nodeName)) {
                if (this.type === "checkbox" || this.type === "radio") {
                    v.event.add(this, "propertychange._change", function (e) {
                        e.originalEvent.propertyName === "checked" && (this._just_changed = !0)
                    }), v.event.add(this, "click._change", function (e) {
                        this._just_changed && !e.isTrigger && (this._just_changed = !1), v.event.simulate("change", this, e, !0)
                    })
                }
                return !1
            }
            v.event.add(this, "beforeactivate._change", function (e) {
                var t = e.target;
                $.test(t.nodeName) && !v._data(t, "_change_attached") && (v.event.add(t, "change._change", function (e) {
                    this.parentNode && !e.isSimulated && !e.isTrigger && v.event.simulate("change", this.parentNode, e, !0)
                }), v._data(t, "_change_attached", !0))
            })
        }, handle: function (e) {
            var t = e.target;
            if (this !== t || e.isSimulated || e.isTrigger || t.type !== "radio" && t.type !== "checkbox") {
                return e.handleObj.handler.apply(this, arguments)
            }
        }, teardown: function () {
            return v.event.remove(this, "._change"), !$.test(this.nodeName)
        }
    }), v.support.focusinBubbles || v.each({focus: "focusin", blur: "focusout"}, function (e, t) {
        var n = 0, r = function (e) {
            v.event.simulate(t, e.target, v.event.fix(e), !0)
        };
        v.event.special[t] = {
            setup: function () {
                n++ === 0 && i.addEventListener(e, r, !0)
            }, teardown: function () {
                --n === 0 && i.removeEventListener(e, r, !0)
            }
        }
    }), v.fn.extend({
        on: function (e, n, r, i, s) {
            var o, u;
            if (typeof e == "object") {
                typeof n != "string" && (r = r || n, n = t);
                for (u in e) {
                    this.on(u, n, r, e[u], s)
                }
                return this
            }
            r == null && i == null ? (i = n, r = n = t) : i == null && (typeof n == "string" ? (i = r, r = t) : (i = r, r = n, n = t));
            if (i === !1) {
                i = et
            } else {
                if (!i) {
                    return this
                }
            }
            return s === 1 && (o = i, i = function (e) {
                return v().off(e), o.apply(this, arguments)
            }, i.guid = o.guid || (o.guid = v.guid++)), this.each(function () {
                v.event.add(this, e, i, r, n)
            })
        }, one: function (e, t, n, r) {
            return this.on(e, t, n, r, 1)
        }, off: function (e, n, r) {
            var i, s;
            if (e && e.preventDefault && e.handleObj) {
                return i = e.handleObj, v(e.delegateTarget).off(i.namespace ? i.origType + "." + i.namespace : i.origType, i.selector, i.handler), this
            }
            if (typeof e == "object") {
                for (s in e) {
                    this.off(s, n, e[s])
                }
                return this
            }
            if (n === !1 || typeof n == "function") {
                r = n, n = t
            }
            return r === !1 && (r = et), this.each(function () {
                v.event.remove(this, e, r, n)
            })
        }, bind: function (e, t, n) {
            return this.on(e, null, t, n)
        }, unbind: function (e, t) {
            return this.off(e, null, t)
        }, live: function (e, t, n) {
            return v(this.context).on(e, this.selector, t, n), this
        }, die: function (e, t) {
            return v(this.context).off(e, this.selector || "**", t), this
        }, delegate: function (e, t, n, r) {
            return this.on(t, e, n, r)
        }, undelegate: function (e, t, n) {
            return arguments.length === 1 ? this.off(e, "**") : this.off(t, e || "**", n)
        }, trigger: function (e, t) {
            return this.each(function () {
                v.event.trigger(e, t, this)
            })
        }, triggerHandler: function (e, t) {
            if (this[0]) {
                return v.event.trigger(e, t, this[0], !0)
            }
        }, toggle: function (e) {
            var t = arguments, n = e.guid || v.guid++, r = 0, i = function (n) {
                var i = (v._data(this, "lastToggle" + e.guid) || 0) % r;
                return v._data(this, "lastToggle" + e.guid, i + 1), n.preventDefault(), t[i].apply(this, arguments) || !1
            };
            i.guid = n;
            while (r < t.length) {
                t[r++].guid = n
            }
            return this.click(i)
        }, hover: function (e, t) {
            return this.mouseenter(e).mouseleave(t || e)
        }
    }), v.each("blur focus focusin focusout load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup error contextmenu".split(" "), function (e, t) {
        v.fn[t] = function (e, n) {
            return n == null && (n = e, e = null), arguments.length > 0 ? this.on(t, null, e, n) : this.trigger(t)
        }, Q.test(t) && (v.event.fixHooks[t] = v.event.keyHooks), G.test(t) && (v.event.fixHooks[t] = v.event.mouseHooks)
    }), function (e, t) {
        function nt(e, t, n, r) {
            n = n || [], t = t || g;
            var i, s, a, f, l = t.nodeType;
            if (!e || typeof e != "string") {
                return n
            }
            if (l !== 1 && l !== 9) {
                return []
            }
            a = o(t);
            if (!a && !r) {
                if (i = R.exec(e)) {
                    if (f = i[1]) {
                        if (l === 9) {
                            s = t.getElementById(f);
                            if (!s || !s.parentNode) {
                                return n
                            }
                            if (s.id === f) {
                                return n.push(s), n
                            }
                        } else {
                            if (t.ownerDocument && (s = t.ownerDocument.getElementById(f)) && u(t, s) && s.id === f) {
                                return n.push(s), n
                            }
                        }
                    } else {
                        if (i[2]) {
                            return S.apply(n, x.call(t.getElementsByTagName(e), 0)), n
                        }
                        if ((f = i[3]) && Z && t.getElementsByClassName) {
                            return S.apply(n, x.call(t.getElementsByClassName(f), 0)), n
                        }
                    }
                }
            }
            return vt(e.replace(j, "$1"), t, n, r, a)
        }

        function rt(e) {
            return function (t) {
                var n = t.nodeName.toLowerCase();
                return n === "input" && t.type === e
            }
        }

        function it(e) {
            return function (t) {
                var n = t.nodeName.toLowerCase();
                return (n === "input" || n === "button") && t.type === e
            }
        }

        function st(e) {
            return N(function (t) {
                return t = +t, N(function (n, r) {
                    var i, s = e([], n.length, t), o = s.length;
                    while (o--) {
                        n[i = s[o]] && (n[i] = !(r[i] = n[i]))
                    }
                })
            })
        }

        function ot(e, t, n) {
            if (e === t) {
                return n
            }
            var r = e.nextSibling;
            while (r) {
                if (r === t) {
                    return -1
                }
                r = r.nextSibling
            }
            return 1
        }

        function ut(e, t) {
            var n, r, s, o, u, a, f, l = L[d][e + " "];
            if (l) {
                return t ? 0 : l.slice(0)
            }
            u = e, a = [], f = i.preFilter;
            while (u) {
                if (!n || (r = F.exec(u))) {
                    r && (u = u.slice(r[0].length) || u), a.push(s = [])
                }
                n = !1;
                if (r = I.exec(u)) {
                    s.push(n = new m(r.shift())), u = u.slice(n.length), n.type = r[0].replace(j, " ")
                }
                for (o in i.filter) {
                    (r = J[o].exec(u)) && (!f[o] || (r = f[o](r))) && (s.push(n = new m(r.shift())), u = u.slice(n.length), n.type = o, n.matches = r)
                }
                if (!n) {
                    break
                }
            }
            return t ? u.length : u ? nt.error(e) : L(e, a).slice(0)
        }

        function at(e, t, r) {
            var i = t.dir, s = r && t.dir === "parentNode", o = w++;
            return t.first ? function (t, n, r) {
                while (t = t[i]) {
                    if (s || t.nodeType === 1) {
                        return e(t, n, r)
                    }
                }
            } : function (t, r, u) {
                if (!u) {
                    var a, f = b + " " + o + " ", l = f + n;
                    while (t = t[i]) {
                        if (s || t.nodeType === 1) {
                            if ((a = t[d]) === l) {
                                return t.sizset
                            }
                            if (typeof a == "string" && a.indexOf(f) === 0) {
                                if (t.sizset) {
                                    return t
                                }
                            } else {
                                t[d] = l;
                                if (e(t, r, u)) {
                                    return t.sizset = !0, t
                                }
                                t.sizset = !1
                            }
                        }
                    }
                } else {
                    while (t = t[i]) {
                        if (s || t.nodeType === 1) {
                            if (e(t, r, u)) {
                                return t
                            }
                        }
                    }
                }
            }
        }

        function ft(e) {
            return e.length > 1 ? function (t, n, r) {
                var i = e.length;
                while (i--) {
                    if (!e[i](t, n, r)) {
                        return !1
                    }
                }
                return !0
            } : e[0]
        }

        function lt(e, t, n, r, i) {
            var s, o = [], u = 0, a = e.length, f = t != null;
            for (; u < a; u++) {
                if (s = e[u]) {
                    if (!n || n(s, r, i)) {
                        o.push(s), f && t.push(u)
                    }
                }
            }
            return o
        }

        function ct(e, t, n, r, i, s) {
            return r && !r[d] && (r = ct(r)), i && !i[d] && (i = ct(i, s)), N(function (s, o, u, a) {
                var f, l, c, h = [], p = [], d = o.length, v = s || dt(t || "*", u.nodeType ? [u] : u, []), m = e && (s || !t) ? lt(v, h, e, u, a) : v, g = n ? i || (s ? e : d || r) ? [] : o : m;
                n && n(m, g, u, a);
                if (r) {
                    f = lt(g, p), r(f, [], u, a), l = f.length;
                    while (l--) {
                        if (c = f[l]) {
                            g[p[l]] = !(m[p[l]] = c)
                        }
                    }
                }
                if (s) {
                    if (i || e) {
                        if (i) {
                            f = [], l = g.length;
                            while (l--) {
                                (c = g[l]) && f.push(m[l] = c)
                            }
                            i(null, g = [], f, a)
                        }
                        l = g.length;
                        while (l--) {
                            (c = g[l]) && (f = i ? T.call(s, c) : h[l]) > -1 && (s[f] = !(o[f] = c))
                        }
                    }
                } else {
                    g = lt(g === o ? g.splice(d, g.length) : g), i ? i(null, o, g, a) : S.apply(o, g)
                }
            })
        }

        function ht(e) {
            var t, n, r, s = e.length, o = i.relative[e[0].type], u = o || i.relative[" "], a = o ? 1 : 0, f = at(function (e) {
                return e === t
            }, u, !0), l = at(function (e) {
                return T.call(t, e) > -1
            }, u, !0), h = [function (e, n, r) {
                return !o && (r || n !== c) || ((t = n).nodeType ? f(e, n, r) : l(e, n, r))
            }];
            for (; a < s; a++) {
                if (n = i.relative[e[a].type]) {
                    h = [at(ft(h), n)]
                } else {
                    n = i.filter[e[a].type].apply(null, e[a].matches);
                    if (n[d]) {
                        r = ++a;
                        for (; r < s; r++) {
                            if (i.relative[e[r].type]) {
                                break
                            }
                        }
                        return ct(a > 1 && ft(h), a > 1 && e.slice(0, a - 1).join("").replace(j, "$1"), n, a < r && ht(e.slice(a, r)), r < s && ht(e = e.slice(r)), r < s && e.join(""))
                    }
                    h.push(n)
                }
            }
            return ft(h)
        }

        function pt(e, t) {
            var r = t.length > 0, s = e.length > 0, o = function (u, a, f, l, h) {
                var p, d, v, m = [], y = 0, w = "0", x = u && [], T = h != null, N = c, C = u || s && i.find.TAG("*", h && a.parentNode || a), k = b += N == null ? 1 : Math.E;
                T && (c = a !== g && a, n = o.el);
                for (; (p = C[w]) != null; w++) {
                    if (s && p) {
                        for (d = 0; v = e[d]; d++) {
                            if (v(p, a, f)) {
                                l.push(p);
                                break
                            }
                        }
                        T && (b = k, n = ++o.el)
                    }
                    r && ((p = !v && p) && y--, u && x.push(p))
                }
                y += w;
                if (r && w !== y) {
                    for (d = 0; v = t[d]; d++) {
                        v(x, m, a, f)
                    }
                    if (u) {
                        if (y > 0) {
                            while (w--) {
                                !x[w] && !m[w] && (m[w] = E.call(l))
                            }
                        }
                        m = lt(m)
                    }
                    S.apply(l, m), T && !u && m.length > 0 && y + t.length > 1 && nt.uniqueSort(l)
                }
                return T && (b = k, c = N), x
            };
            return o.el = 0, r ? N(o) : o
        }

        function dt(e, t, n) {
            var r = 0, i = t.length;
            for (; r < i; r++) {
                nt(e, t[r], n)
            }
            return n
        }

        function vt(e, t, n, r, s) {
            var o, u, f, l, c, h = ut(e), p = h.length;
            if (!r && h.length === 1) {
                u = h[0] = h[0].slice(0);
                if (u.length > 2 && (f = u[0]).type === "ID" && t.nodeType === 9 && !s && i.relative[u[1].type]) {
                    t = i.find.ID(f.matches[0].replace($, ""), t, s)[0];
                    if (!t) {
                        return n
                    }
                    e = e.slice(u.shift().length)
                }
                for (o = J.POS.test(e) ? -1 : u.length - 1; o >= 0; o--) {
                    f = u[o];
                    if (i.relative[l = f.type]) {
                        break
                    }
                    if (c = i.find[l]) {
                        if (r = c(f.matches[0].replace($, ""), z.test(u[0].type) && t.parentNode || t, s)) {
                            u.splice(o, 1), e = r.length && u.join("");
                            if (!e) {
                                return S.apply(n, x.call(r, 0)), n
                            }
                            break
                        }
                    }
                }
            }
            return a(e, h)(r, t, s, n, z.test(e)), n
        }

        function mt() {
        }

        var n, r, i, s, o, u, a, f, l, c, h = !0, p = "undefined", d = ("sizcache" + Math.random()).replace(".", ""), m = String, g = e.document, y = g.documentElement, b = 0, w = 0, E = [].pop, S = [].push, x = [].slice, T = [].indexOf || function (e) {
                var t = 0, n = this.length;
                for (; t < n; t++) {
                    if (this[t] === e) {
                        return t
                    }
                }
                return -1
            }, N = function (e, t) {
            return e[d] = t == null || t, e
        }, C = function () {
            var e = {}, t = [];
            return N(function (n, r) {
                return t.push(n) > i.cacheLength && delete e[t.shift()], e[n + " "] = r
            }, e)
        }, k = C(), L = C(), A = C(), O = "[\\x20\\t\\r\\n\\f]", M = "(?:\\\\.|[-\\w]|[^\\x00-\\xa0])+", _ = M.replace("w", "w#"), D = "([*^$|!~]?=)", P = "\\[" + O + "*(" + M + ")" + O + "*(?:" + D + O + "*(?:(['\"])((?:\\\\.|[^\\\\])*?)\\3|(" + _ + ")|)|)" + O + "*\\]", H = ":(" + M + ")(?:\\((?:(['\"])((?:\\\\.|[^\\\\])*?)\\2|([^()[\\]]*|(?:(?:" + P + ")|[^:]|\\\\.)*|.*))\\)|)", B = ":(even|odd|eq|gt|lt|nth|first|last)(?:\\(" + O + "*((?:-\\d)?\\d*)" + O + "*\\)|)(?=[^-]|$)", j = new RegExp("^" + O + "+|((?:^|[^\\\\])(?:\\\\.)*)" + O + "+$", "g"), F = new RegExp("^" + O + "*," + O + "*"), I = new RegExp("^" + O + "*([\\x20\\t\\r\\n\\f>+~])" + O + "*"), q = new RegExp(H), R = /^(?:#([\w\-]+)|(\w+)|\.([\w\-]+))$/, U = /^:not/, z = /[\x20\t\r\n\f]*[+~]/, W = /:not\($/, X = /h\d/i, V = /input|select|textarea|button/i, $ = /\\(?!\\)/g, J = {
            ID: new RegExp("^#(" + M + ")"),
            CLASS: new RegExp("^\\.(" + M + ")"),
            NAME: new RegExp("^\\[name=['\"]?(" + M + ")['\"]?\\]"),
            TAG: new RegExp("^(" + M.replace("w", "w*") + ")"),
            ATTR: new RegExp("^" + P),
            PSEUDO: new RegExp("^" + H),
            POS: new RegExp(B, "i"),
            CHILD: new RegExp("^:(only|nth|first|last)-child(?:\\(" + O + "*(even|odd|(([+-]|)(\\d*)n|)" + O + "*(?:([+-]|)" + O + "*(\\d+)|))" + O + "*\\)|)", "i"),
            needsContext: new RegExp("^" + O + "*[>+~]|" + B, "i")
        }, K = function (e) {
            var t = g.createElement("div");
            try {
                return e(t)
            } catch (n) {
                return !1
            } finally {
                t = null
            }
        }, Q = K(function (e) {
            return e.appendChild(g.createComment("")), !e.getElementsByTagName("*").length
        }), G = K(function (e) {
            return e.innerHTML = "<a href='#'></a>", e.firstChild && typeof e.firstChild.getAttribute !== p && e.firstChild.getAttribute("href") === "#"
        }), Y = K(function (e) {
            e.innerHTML = "<select></select>";
            var t = typeof e.lastChild.getAttribute("multiple");
            return t !== "boolean" && t !== "string"
        }), Z = K(function (e) {
            return e.innerHTML = "<div class='hidden e'></div><div class='hidden'></div>", !e.getElementsByClassName || !e.getElementsByClassName("e").length ? !1 : (e.lastChild.className = "e", e.getElementsByClassName("e").length === 2)
        }), et = K(function (e) {
            e.id = d + 0, e.innerHTML = "<a name='" + d + "'></a><div name='" + d + "'></div>", y.insertBefore(e, y.firstChild);
            var t = g.getElementsByName && g.getElementsByName(d).length === 2 + g.getElementsByName(d + 0).length;
            return r = !g.getElementById(d), y.removeChild(e), t
        });
        try {
            x.call(y.childNodes, 0)[0].nodeType
        } catch (tt) {
            x = function (e) {
                var t, n = [];
                for (; t = this[e]; e++) {
                    n.push(t)
                }
                return n
            }
        }
        nt.matches = function (e, t) {
            return nt(e, null, null, t)
        }, nt.matchesSelector = function (e, t) {
            return nt(t, null, null, [e]).length > 0
        }, s = nt.getText = function (e) {
            var t, n = "", r = 0, i = e.nodeType;
            if (i) {
                if (i === 1 || i === 9 || i === 11) {
                    if (typeof e.textContent == "string") {
                        return e.textContent
                    }
                    for (e = e.firstChild; e; e = e.nextSibling) {
                        n += s(e)
                    }
                } else {
                    if (i === 3 || i === 4) {
                        return e.nodeValue
                    }
                }
            } else {
                for (; t = e[r]; r++) {
                    n += s(t)
                }
            }
            return n
        }, o = nt.isXML = function (e) {
            var t = e && (e.ownerDocument || e).documentElement;
            return t ? t.nodeName !== "HTML" : !1
        }, u = nt.contains = y.contains ? function (e, t) {
            var n = e.nodeType === 9 ? e.documentElement : e, r = t && t.parentNode;
            return e === r || !!(r && r.nodeType === 1 && n.contains && n.contains(r))
        } : y.compareDocumentPosition ? function (e, t) {
            return t && !!(e.compareDocumentPosition(t) & 16)
        } : function (e, t) {
            while (t = t.parentNode) {
                if (t === e) {
                    return !0
                }
            }
            return !1
        }, nt.attr = function (e, t) {
            var n, r = o(e);
            return r || (t = t.toLowerCase()), (n = i.attrHandle[t]) ? n(e) : r || Y ? e.getAttribute(t) : (n = e.getAttributeNode(t), n ? typeof e[t] == "boolean" ? e[t] ? t : null : n.specified ? n.value : null : null)
        }, i = nt.selectors = {
            cacheLength: 50,
            createPseudo: N,
            match: J,
            attrHandle: G ? {} : {
                href: function (e) {
                    return e.getAttribute("href", 2)
                }, type: function (e) {
                    return e.getAttribute("type")
                }
            },
            find: {
                ID: r ? function (e, t, n) {
                    if (typeof t.getElementById !== p && !n) {
                        var r = t.getElementById(e);
                        return r && r.parentNode ? [r] : []
                    }
                } : function (e, n, r) {
                    if (typeof n.getElementById !== p && !r) {
                        var i = n.getElementById(e);
                        return i ? i.id === e || typeof i.getAttributeNode !== p && i.getAttributeNode("id").value === e ? [i] : t : []
                    }
                }, TAG: Q ? function (e, t) {
                    if (typeof t.getElementsByTagName !== p) {
                        return t.getElementsByTagName(e)
                    }
                } : function (e, t) {
                    var n = t.getElementsByTagName(e);
                    if (e === "*") {
                        var r, i = [], s = 0;
                        for (; r = n[s]; s++) {
                            r.nodeType === 1 && i.push(r)
                        }
                        return i
                    }
                    return n
                }, NAME: et && function (e, t) {
                    if (typeof t.getElementsByName !== p) {
                        return t.getElementsByName(name)
                    }
                }, CLASS: Z && function (e, t, n) {
                    if (typeof t.getElementsByClassName !== p && !n) {
                        return t.getElementsByClassName(e)
                    }
                }
            },
            relative: {
                ">": {dir: "parentNode", first: !0},
                " ": {dir: "parentNode"},
                "+": {dir: "previousSibling", first: !0},
                "~": {dir: "previousSibling"}
            },
            preFilter: {
                ATTR: function (e) {
                    return e[1] = e[1].replace($, ""), e[3] = (e[4] || e[5] || "").replace($, ""), e[2] === "~=" && (e[3] = " " + e[3] + " "), e.slice(0, 4)
                }, CHILD: function (e) {
                    return e[1] = e[1].toLowerCase(), e[1] === "nth" ? (e[2] || nt.error(e[0]), e[3] = +(e[3] ? e[4] + (e[5] || 1) : 2 * (e[2] === "even" || e[2] === "odd")), e[4] = +(e[6] + e[7] || e[2] === "odd")) : e[2] && nt.error(e[0]), e
                }, PSEUDO: function (e) {
                    var t, n;
                    if (J.CHILD.test(e[0])) {
                        return null
                    }
                    if (e[3]) {
                        e[2] = e[3]
                    } else {
                        if (t = e[4]) {
                            q.test(t) && (n = ut(t, !0)) && (n = t.indexOf(")", t.length - n) - t.length) && (t = t.slice(0, n), e[0] = e[0].slice(0, n)), e[2] = t
                        }
                    }
                    return e.slice(0, 3)
                }
            },
            filter: {
                ID: r ? function (e) {
                    return e = e.replace($, ""), function (t) {
                        return t.getAttribute("id") === e
                    }
                } : function (e) {
                    return e = e.replace($, ""), function (t) {
                        var n = typeof t.getAttributeNode !== p && t.getAttributeNode("id");
                        return n && n.value === e
                    }
                }, TAG: function (e) {
                    return e === "*" ? function () {
                        return !0
                    } : (e = e.replace($, "").toLowerCase(), function (t) {
                        return t.nodeName && t.nodeName.toLowerCase() === e
                    })
                }, CLASS: function (e) {
                    var t = k[d][e + " "];
                    return t || (t = new RegExp("(^|" + O + ")" + e + "(" + O + "|$)")) && k(e, function (e) {
                            return t.test(e.className || typeof e.getAttribute !== p && e.getAttribute("class") || "")
                        })
                }, ATTR: function (e, t, n) {
                    return function (r, i) {
                        var s = nt.attr(r, e);
                        return s == null ? t === "!=" : t ? (s += "", t === "=" ? s === n : t === "!=" ? s !== n : t === "^=" ? n && s.indexOf(n) === 0 : t === "*=" ? n && s.indexOf(n) > -1 : t === "$=" ? n && s.substr(s.length - n.length) === n : t === "~=" ? (" " + s + " ").indexOf(n) > -1 : t === "|=" ? s === n || s.substr(0, n.length + 1) === n + "-" : !1) : !0
                    }
                }, CHILD: function (e, t, n, r) {
                    return e === "nth" ? function (e) {
                        var t, i, s = e.parentNode;
                        if (n === 1 && r === 0) {
                            return !0
                        }
                        if (s) {
                            i = 0;
                            for (t = s.firstChild; t; t = t.nextSibling) {
                                if (t.nodeType === 1) {
                                    i++;
                                    if (e === t) {
                                        break
                                    }
                                }
                            }
                        }
                        return i -= r, i === n || i % n === 0 && i / n >= 0
                    } : function (t) {
                        var n = t;
                        switch (e) {
                            case"only":
                            case"first":
                                while (n = n.previousSibling) {
                                    if (n.nodeType === 1) {
                                        return !1
                                    }
                                }
                                if (e === "first") {
                                    return !0
                                }
                                n = t;
                            case"last":
                                while (n = n.nextSibling) {
                                    if (n.nodeType === 1) {
                                        return !1
                                    }
                                }
                                return !0
                        }
                    }
                }, PSEUDO: function (e, t) {
                    var n, r = i.pseudos[e] || i.setFilters[e.toLowerCase()] || nt.error("unsupported pseudo: " + e);
                    return r[d] ? r(t) : r.length > 1 ? (n = [e, e, "", t], i.setFilters.hasOwnProperty(e.toLowerCase()) ? N(function (e, n) {
                        var i, s = r(e, t), o = s.length;
                        while (o--) {
                            i = T.call(e, s[o]), e[i] = !(n[i] = s[o])
                        }
                    }) : function (e) {
                        return r(e, 0, n)
                    }) : r
                }
            },
            pseudos: {
                not: N(function (e) {
                    var t = [], n = [], r = a(e.replace(j, "$1"));
                    return r[d] ? N(function (e, t, n, i) {
                        var s, o = r(e, null, i, []), u = e.length;
                        while (u--) {
                            if (s = o[u]) {
                                e[u] = !(t[u] = s)
                            }
                        }
                    }) : function (e, i, s) {
                        return t[0] = e, r(t, null, s, n), !n.pop()
                    }
                }),
                has: N(function (e) {
                    return function (t) {
                        return nt(e, t).length > 0
                    }
                }),
                contains: N(function (e) {
                    return function (t) {
                        return (t.textContent || t.innerText || s(t)).indexOf(e) > -1
                    }
                }),
                enabled: function (e) {
                    return e.disabled === !1
                },
                disabled: function (e) {
                    return e.disabled === !0
                },
                checked: function (e) {
                    var t = e.nodeName.toLowerCase();
                    return t === "input" && !!e.checked || t === "option" && !!e.selected
                },
                selected: function (e) {
                    return e.parentNode && e.parentNode.selectedIndex, e.selected === !0
                },
                parent: function (e) {
                    return !i.pseudos.empty(e)
                },
                empty: function (e) {
                    var t;
                    e = e.firstChild;
                    while (e) {
                        if (e.nodeName > "@" || (t = e.nodeType) === 3 || t === 4) {
                            return !1
                        }
                        e = e.nextSibling
                    }
                    return !0
                },
                header: function (e) {
                    return X.test(e.nodeName)
                },
                text: function (e) {
                    var t, n;
                    return e.nodeName.toLowerCase() === "input" && (t = e.type) === "text" && ((n = e.getAttribute("type")) == null || n.toLowerCase() === t)
                },
                radio: rt("radio"),
                checkbox: rt("checkbox"),
                file: rt("file"),
                password: rt("password"),
                image: rt("image"),
                submit: it("submit"),
                reset: it("reset"),
                button: function (e) {
                    var t = e.nodeName.toLowerCase();
                    return t === "input" && e.type === "button" || t === "button"
                },
                input: function (e) {
                    return V.test(e.nodeName)
                },
                focus: function (e) {
                    var t = e.ownerDocument;
                    return e === t.activeElement && (!t.hasFocus || t.hasFocus()) && !!(e.type || e.href || ~e.tabIndex)
                },
                active: function (e) {
                    return e === e.ownerDocument.activeElement
                },
                first: st(function () {
                    return [0]
                }),
                last: st(function (e, t) {
                    return [t - 1]
                }),
                eq: st(function (e, t, n) {
                    return [n < 0 ? n + t : n]
                }),
                even: st(function (e, t) {
                    for (var n = 0; n < t; n += 2) {
                        e.push(n)
                    }
                    return e
                }),
                odd: st(function (e, t) {
                    for (var n = 1; n < t; n += 2) {
                        e.push(n)
                    }
                    return e
                }),
                lt: st(function (e, t, n) {
                    for (var r = n < 0 ? n + t : n; --r >= 0;) {
                        e.push(r)
                    }
                    return e
                }),
                gt: st(function (e, t, n) {
                    for (var r = n < 0 ? n + t : n; ++r < t;) {
                        e.push(r)
                    }
                    return e
                })
            }
        }, f = y.compareDocumentPosition ? function (e, t) {
            return e === t ? (l = !0, 0) : (!e.compareDocumentPosition || !t.compareDocumentPosition ? e.compareDocumentPosition : e.compareDocumentPosition(t) & 4) ? -1 : 1
        } : function (e, t) {
            if (e === t) {
                return l = !0, 0
            }
            if (e.sourceIndex && t.sourceIndex) {
                return e.sourceIndex - t.sourceIndex
            }
            var n, r, i = [], s = [], o = e.parentNode, u = t.parentNode, a = o;
            if (o === u) {
                return ot(e, t)
            }
            if (!o) {
                return -1
            }
            if (!u) {
                return 1
            }
            while (a) {
                i.unshift(a), a = a.parentNode
            }
            a = u;
            while (a) {
                s.unshift(a), a = a.parentNode
            }
            n = i.length, r = s.length;
            for (var f = 0; f < n && f < r; f++) {
                if (i[f] !== s[f]) {
                    return ot(i[f], s[f])
                }
            }
            return f === n ? ot(e, s[f], -1) : ot(i[f], t, 1)
        }, [0, 0].sort(f), h = !l, nt.uniqueSort = function (e) {
            var t, n = [], r = 1, i = 0;
            l = h, e.sort(f);
            if (l) {
                for (; t = e[r]; r++) {
                    t === e[r - 1] && (i = n.push(r))
                }
                while (i--) {
                    e.splice(n[i], 1)
                }
            }
            return e
        }, nt.error = function (e) {
            throw new Error("Syntax error, unrecognized expression: " + e)
        }, a = nt.compile = function (e, t) {
            var n, r = [], i = [], s = A[d][e + " "];
            if (!s) {
                t || (t = ut(e)), n = t.length;
                while (n--) {
                    s = ht(t[n]), s[d] ? r.push(s) : i.push(s)
                }
                s = A(e, pt(i, r))
            }
            return s
        }, g.querySelectorAll && function () {
            var e, t = vt, n = /'|\\/g, r = /\=[\x20\t\r\n\f]*([^'"\]]*)[\x20\t\r\n\f]*\]/g, i = [":focus"], s = [":active"], u = y.matchesSelector || y.mozMatchesSelector || y.webkitMatchesSelector || y.oMatchesSelector || y.msMatchesSelector;
            K(function (e) {
                e.innerHTML = "<select><option selected=''></option></select>", e.querySelectorAll("[selected]").length || i.push("\\[" + O + "*(?:checked|disabled|ismap|multiple|readonly|selected|value)"), e.querySelectorAll(":checked").length || i.push(":checked")
            }), K(function (e) {
                e.innerHTML = "<p test=''></p>", e.querySelectorAll("[test^='']").length && i.push("[*^$]=" + O + "*(?:\"\"|'')"), e.innerHTML = "<input type='hidden'/>", e.querySelectorAll(":enabled").length || i.push(":enabled", ":disabled")
            }), i = new RegExp(i.join("|")), vt = function (e, r, s, o, u) {
                if (!o && !u && !i.test(e)) {
                    var a, f, l = !0, c = d, h = r, p = r.nodeType === 9 && e;
                    if (r.nodeType === 1 && r.nodeName.toLowerCase() !== "object") {
                        a = ut(e), (l = r.getAttribute("id")) ? c = l.replace(n, "\\$&") : r.setAttribute("id", c), c = "[id='" + c + "'] ", f = a.length;
                        while (f--) {
                            a[f] = c + a[f].join("")
                        }
                        h = z.test(e) && r.parentNode || r, p = a.join(",")
                    }
                    if (p) {
                        try {
                            return S.apply(s, x.call(h.querySelectorAll(p), 0)), s
                        } catch (v) {
                        } finally {
                            l || r.removeAttribute("id")
                        }
                    }
                }
                return t(e, r, s, o, u)
            }, u && (K(function (t) {
                e = u.call(t, "div");
                try {
                    u.call(t, "[test!='']:sizzle"), s.push("!=", H)
                } catch (n) {
                }
            }), s = new RegExp(s.join("|")), nt.matchesSelector = function (t, n) {
                n = n.replace(r, "='$1']");
                if (!o(t) && !s.test(n) && !i.test(n)) {
                    try {
                        var a = u.call(t, n);
                        if (a || e || t.document && t.document.nodeType !== 11) {
                            return a
                        }
                    } catch (f) {
                    }
                }
                return nt(n, null, null, [t]).length > 0
            })
        }(), i.pseudos.nth = i.pseudos.eq, i.filters = mt.prototype = i.pseudos, i.setFilters = new mt, nt.attr = v.attr, v.find = nt, v.expr = nt.selectors, v.expr[":"] = v.expr.pseudos, v.unique = nt.uniqueSort, v.text = nt.getText, v.isXMLDoc = nt.isXML, v.contains = nt.contains
    }(e);
    var nt = /Until$/, rt = /^(?:parents|prev(?:Until|All))/, it = /^.[^:#\[\.,]*$/, st = v.expr.match.needsContext, ot = {
        children: !0,
        contents: !0,
        next: !0,
        prev: !0
    };
    v.fn.extend({
        find: function (e) {
            var t, n, r, i, s, o, u = this;
            if (typeof e != "string") {
                return v(e).filter(function () {
                    for (t = 0, n = u.length; t < n; t++) {
                        if (v.contains(u[t], this)) {
                            return !0
                        }
                    }
                })
            }
            o = this.pushStack("", "find", e);
            for (t = 0, n = this.length; t < n; t++) {
                r = o.length, v.find(e, this[t], o);
                if (t > 0) {
                    for (i = r; i < o.length; i++) {
                        for (s = 0; s < r; s++) {
                            if (o[s] === o[i]) {
                                o.splice(i--, 1);
                                break
                            }
                        }
                    }
                }
            }
            return o
        }, has: function (e) {
            var t, n = v(e, this), r = n.length;
            return this.filter(function () {
                for (t = 0; t < r; t++) {
                    if (v.contains(this, n[t])) {
                        return !0
                    }
                }
            })
        }, not: function (e) {
            return this.pushStack(ft(this, e, !1), "not", e)
        }, filter: function (e) {
            return this.pushStack(ft(this, e, !0), "filter", e)
        }, is: function (e) {
            return !!e && (typeof e == "string" ? st.test(e) ? v(e, this.context).index(this[0]) >= 0 : v.filter(e, this).length > 0 : this.filter(e).length > 0)
        }, closest: function (e, t) {
            var n, r = 0, i = this.length, s = [], o = st.test(e) || typeof e != "string" ? v(e, t || this.context) : 0;
            for (; r < i; r++) {
                n = this[r];
                while (n && n.ownerDocument && n !== t && n.nodeType !== 11) {
                    if (o ? o.index(n) > -1 : v.find.matchesSelector(n, e)) {
                        s.push(n);
                        break
                    }
                    n = n.parentNode
                }
            }
            return s = s.length > 1 ? v.unique(s) : s, this.pushStack(s, "closest", e)
        }, index: function (e) {
            return e ? typeof e == "string" ? v.inArray(this[0], v(e)) : v.inArray(e.jquery ? e[0] : e, this) : this[0] && this[0].parentNode ? this.prevAll().length : -1
        }, add: function (e, t) {
            var n = typeof e == "string" ? v(e, t) : v.makeArray(e && e.nodeType ? [e] : e), r = v.merge(this.get(), n);
            return this.pushStack(ut(n[0]) || ut(r[0]) ? r : v.unique(r))
        }, addBack: function (e) {
            return this.add(e == null ? this.prevObject : this.prevObject.filter(e))
        }
    }), v.fn.andSelf = v.fn.addBack, v.each({
        parent: function (e) {
            var t = e.parentNode;
            return t && t.nodeType !== 11 ? t : null
        }, parents: function (e) {
            return v.dir(e, "parentNode")
        }, parentsUntil: function (e, t, n) {
            return v.dir(e, "parentNode", n)
        }, next: function (e) {
            return at(e, "nextSibling")
        }, prev: function (e) {
            return at(e, "previousSibling")
        }, nextAll: function (e) {
            return v.dir(e, "nextSibling")
        }, prevAll: function (e) {
            return v.dir(e, "previousSibling")
        }, nextUntil: function (e, t, n) {
            return v.dir(e, "nextSibling", n)
        }, prevUntil: function (e, t, n) {
            return v.dir(e, "previousSibling", n)
        }, siblings: function (e) {
            return v.sibling((e.parentNode || {}).firstChild, e)
        }, children: function (e) {
            return v.sibling(e.firstChild)
        }, contents: function (e) {
            return v.nodeName(e, "iframe") ? e.contentDocument || e.contentWindow.document : v.merge([], e.childNodes)
        }
    }, function (e, t) {
        v.fn[e] = function (n, r) {
            var i = v.map(this, t, n);
            return nt.test(e) || (r = n), r && typeof r == "string" && (i = v.filter(r, i)), i = this.length > 1 && !ot[e] ? v.unique(i) : i, this.length > 1 && rt.test(e) && (i = i.reverse()), this.pushStack(i, e, l.call(arguments).join(","))
        }
    }), v.extend({
        filter: function (e, t, n) {
            return n && (e = ":not(" + e + ")"), t.length === 1 ? v.find.matchesSelector(t[0], e) ? [t[0]] : [] : v.find.matches(e, t)
        }, dir: function (e, n, r) {
            var i = [], s = e[n];
            while (s && s.nodeType !== 9 && (r === t || s.nodeType !== 1 || !v(s).is(r))) {
                s.nodeType === 1 && i.push(s), s = s[n]
            }
            return i
        }, sibling: function (e, t) {
            var n = [];
            for (; e; e = e.nextSibling) {
                e.nodeType === 1 && e !== t && n.push(e)
            }
            return n
        }
    });
    var ct = "abbr|article|aside|audio|bdi|canvas|data|datalist|details|figcaption|figure|footer|header|hgroup|mark|meter|nav|output|progress|section|summary|time|video", ht = / jQuery\d+="(?:null|\d+)"/g, pt = /^\s+/, dt = /<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/gi, vt = /<([\w:]+)/, mt = /<tbody/i, gt = /<|&#?\w+;/, yt = /<(?:script|style|link)/i, bt = /<(?:script|object|embed|option|style)/i, wt = new RegExp("<(?:" + ct + ")[\\s/>]", "i"), Et = /^(?:checkbox|radio)$/, St = /checked\s*(?:[^=]|=\s*.checked.)/i, xt = /\/(java|ecma)script/i, Tt = /^\s*<!(?:\[CDATA\[|\-\-)|[\]\-]{2}>\s*$/g, Nt = {
        option: [1, "<select multiple='multiple'>", "</select>"],
        legend: [1, "<fieldset>", "</fieldset>"],
        thead: [1, "<table>", "</table>"],
        tr: [2, "<table><tbody>", "</tbody></table>"],
        td: [3, "<table><tbody><tr>", "</tr></tbody></table>"],
        col: [2, "<table><tbody></tbody><colgroup>", "</colgroup></table>"],
        area: [1, "<map>", "</map>"],
        _default: [0, "", ""]
    }, Ct = lt(i), kt = Ct.appendChild(i.createElement("div"));
    Nt.optgroup = Nt.option, Nt.tbody = Nt.tfoot = Nt.colgroup = Nt.caption = Nt.thead, Nt.th = Nt.td, v.support.htmlSerialize || (Nt._default = [1, "X<div>", "</div>"]), v.fn.extend({
        text: function (e) {
            return v.access(this, function (e) {
                return e === t ? v.text(this) : this.empty().append((this[0] && this[0].ownerDocument || i).createTextNode(e))
            }, null, e, arguments.length)
        }, wrapAll: function (e) {
            if (v.isFunction(e)) {
                return this.each(function (t) {
                    v(this).wrapAll(e.call(this, t))
                })
            }
            if (this[0]) {
                var t = v(e, this[0].ownerDocument).eq(0).clone(!0);
                this[0].parentNode && t.insertBefore(this[0]), t.map(function () {
                    var e = this;
                    while (e.firstChild && e.firstChild.nodeType === 1) {
                        e = e.firstChild
                    }
                    return e
                }).append(this)
            }
            return this
        }, wrapInner: function (e) {
            return v.isFunction(e) ? this.each(function (t) {
                v(this).wrapInner(e.call(this, t))
            }) : this.each(function () {
                var t = v(this), n = t.contents();
                n.length ? n.wrapAll(e) : t.append(e)
            })
        }, wrap: function (e) {
            var t = v.isFunction(e);
            return this.each(function (n) {
                v(this).wrapAll(t ? e.call(this, n) : e)
            })
        }, unwrap: function () {
            return this.parent().each(function () {
                v.nodeName(this, "body") || v(this).replaceWith(this.childNodes)
            }).end()
        }, append: function () {
            return this.domManip(arguments, !0, function (e) {
                (this.nodeType === 1 || this.nodeType === 11) && this.appendChild(e)
            })
        }, prepend: function () {
            return this.domManip(arguments, !0, function (e) {
                (this.nodeType === 1 || this.nodeType === 11) && this.insertBefore(e, this.firstChild)
            })
        }, before: function () {
            if (!ut(this[0])) {
                return this.domManip(arguments, !1, function (e) {
                    this.parentNode.insertBefore(e, this)
                })
            }
            if (arguments.length) {
                var e = v.clean(arguments);
                return this.pushStack(v.merge(e, this), "before", this.selector)
            }
        }, after: function () {
            if (!ut(this[0])) {
                return this.domManip(arguments, !1, function (e) {
                    this.parentNode.insertBefore(e, this.nextSibling)
                })
            }
            if (arguments.length) {
                var e = v.clean(arguments);
                return this.pushStack(v.merge(this, e), "after", this.selector)
            }
        }, remove: function (e, t) {
            var n, r = 0;
            for (; (n = this[r]) != null; r++) {
                if (!e || v.filter(e, [n]).length) {
                    !t && n.nodeType === 1 && (v.cleanData(n.getElementsByTagName("*")), v.cleanData([n])), n.parentNode && n.parentNode.removeChild(n)
                }
            }
            return this
        }, empty: function () {
            var e, t = 0;
            for (; (e = this[t]) != null; t++) {
                e.nodeType === 1 && v.cleanData(e.getElementsByTagName("*"));
                while (e.firstChild) {
                    e.removeChild(e.firstChild)
                }
            }
            return this
        }, clone: function (e, t) {
            return e = e == null ? !1 : e, t = t == null ? e : t, this.map(function () {
                return v.clone(this, e, t)
            })
        }, html: function (e) {
            return v.access(this, function (e) {
                var n = this[0] || {}, r = 0, i = this.length;
                if (e === t) {
                    return n.nodeType === 1 ? n.innerHTML.replace(ht, "") : t
                }
                if (typeof e == "string" && !yt.test(e) && (v.support.htmlSerialize || !wt.test(e)) && (v.support.leadingWhitespace || !pt.test(e)) && !Nt[(vt.exec(e) || ["", ""])[1].toLowerCase()]) {
                    e = e.replace(dt, "<$1></$2>");
                    try {
                        for (; r < i; r++) {
                            n = this[r] || {}, n.nodeType === 1 && (v.cleanData(n.getElementsByTagName("*")), n.innerHTML = e)
                        }
                        n = 0
                    } catch (s) {
                    }
                }
                n && this.empty().append(e)
            }, null, e, arguments.length)
        }, replaceWith: function (e) {
            return ut(this[0]) ? this.length ? this.pushStack(v(v.isFunction(e) ? e() : e), "replaceWith", e) : this : v.isFunction(e) ? this.each(function (t) {
                var n = v(this), r = n.html();
                n.replaceWith(e.call(this, t, r))
            }) : (typeof e != "string" && (e = v(e).detach()), this.each(function () {
                var t = this.nextSibling, n = this.parentNode;
                v(this).remove(), t ? v(t).before(e) : v(n).append(e)
            }))
        }, detach: function (e) {
            return this.remove(e, !0)
        }, domManip: function (e, n, r) {
            e = [].concat.apply([], e);
            var i, s, o, u, a = 0, f = e[0], l = [], c = this.length;
            if (!v.support.checkClone && c > 1 && typeof f == "string" && St.test(f)) {
                return this.each(function () {
                    v(this).domManip(e, n, r)
                })
            }
            if (v.isFunction(f)) {
                return this.each(function (i) {
                    var s = v(this);
                    e[0] = f.call(this, i, n ? s.html() : t), s.domManip(e, n, r)
                })
            }
            if (this[0]) {
                i = v.buildFragment(e, this, l), o = i.fragment, s = o.firstChild, o.childNodes.length === 1 && (o = s);
                if (s) {
                    n = n && v.nodeName(s, "tr");
                    for (u = i.cacheable || c - 1; a < c; a++) {
                        r.call(n && v.nodeName(this[a], "table") ? Lt(this[a], "tbody") : this[a], a === u ? o : v.clone(o, !0, !0))
                    }
                }
                o = s = null, l.length && v.each(l, function (e, t) {
                    t.src ? v.ajax ? v.ajax({
                        url: t.src,
                        type: "GET",
                        dataType: "script",
                        async: !1,
                        global: !1,
                        "throws": !0
                    }) : v.error("no ajax") : v.globalEval((t.text || t.textContent || t.innerHTML || "").replace(Tt, "")), t.parentNode && t.parentNode.removeChild(t)
                })
            }
            return this
        }
    }), v.buildFragment = function (e, n, r) {
        var s, o, u, a = e[0];
        return n = n || i, n = !n.nodeType && n[0] || n, n = n.ownerDocument || n, e.length === 1 && typeof a == "string" && a.length < 512 && n === i && a.charAt(0) === "<" && !bt.test(a) && (v.support.checkClone || !St.test(a)) && (v.support.html5Clone || !wt.test(a)) && (o = !0, s = v.fragments[a], u = s !== t), s || (s = n.createDocumentFragment(), v.clean(e, n, s, r), o && (v.fragments[a] = u && s)), {
            fragment: s,
            cacheable: o
        }
    }, v.fragments = {}, v.each({
        appendTo: "append",
        prependTo: "prepend",
        insertBefore: "before",
        insertAfter: "after",
        replaceAll: "replaceWith"
    }, function (e, t) {
        v.fn[e] = function (n) {
            var r, i = 0, s = [], o = v(n), u = o.length, a = this.length === 1 && this[0].parentNode;
            if ((a == null || a && a.nodeType === 11 && a.childNodes.length === 1) && u === 1) {
                return o[t](this[0]), this
            }
            for (; i < u; i++) {
                r = (i > 0 ? this.clone(!0) : this).get(), v(o[i])[t](r), s = s.concat(r)
            }
            return this.pushStack(s, e, o.selector)
        }
    }), v.extend({
        clone: function (e, t, n) {
            var r, i, s, o;
            v.support.html5Clone || v.isXMLDoc(e) || !wt.test("<" + e.nodeName + ">") ? o = e.cloneNode(!0) : (kt.innerHTML = e.outerHTML, kt.removeChild(o = kt.firstChild));
            if ((!v.support.noCloneEvent || !v.support.noCloneChecked) && (e.nodeType === 1 || e.nodeType === 11) && !v.isXMLDoc(e)) {
                Ot(e, o), r = Mt(e), i = Mt(o);
                for (s = 0; r[s]; ++s) {
                    i[s] && Ot(r[s], i[s])
                }
            }
            if (t) {
                At(e, o);
                if (n) {
                    r = Mt(e), i = Mt(o);
                    for (s = 0; r[s]; ++s) {
                        At(r[s], i[s])
                    }
                }
            }
            return r = i = null, o
        }, clean: function (e, t, n, r) {
            var s, o, u, a, f, l, c, h, p, d, m, g, y = t === i && Ct, b = [];
            if (!t || typeof t.createDocumentFragment == "undefined") {
                t = i
            }
            for (s = 0; (u = e[s]) != null; s++) {
                typeof u == "number" && (u += "");
                if (!u) {
                    continue
                }
                if (typeof u == "string") {
                    if (!gt.test(u)) {
                        u = t.createTextNode(u)
                    } else {
                        y = y || lt(t), c = t.createElement("div"), y.appendChild(c), u = u.replace(dt, "<$1></$2>"), a = (vt.exec(u) || ["", ""])[1].toLowerCase(), f = Nt[a] || Nt._default, l = f[0], c.innerHTML = f[1] + u + f[2];
                        while (l--) {
                            c = c.lastChild
                        }
                        if (!v.support.tbody) {
                            h = mt.test(u), p = a === "table" && !h ? c.firstChild && c.firstChild.childNodes : f[1] === "<table>" && !h ? c.childNodes : [];
                            for (o = p.length - 1; o >= 0; --o) {
                                v.nodeName(p[o], "tbody") && !p[o].childNodes.length && p[o].parentNode.removeChild(p[o])
                            }
                        }
                        !v.support.leadingWhitespace && pt.test(u) && c.insertBefore(t.createTextNode(pt.exec(u)[0]), c.firstChild), u = c.childNodes, c.parentNode.removeChild(c)
                    }
                }
                u.nodeType ? b.push(u) : v.merge(b, u)
            }
            c && (u = c = y = null);
            if (!v.support.appendChecked) {
                for (s = 0; (u = b[s]) != null; s++) {
                    v.nodeName(u, "input") ? _t(u) : typeof u.getElementsByTagName != "undefined" && v.grep(u.getElementsByTagName("input"), _t)
                }
            }
            if (n) {
                m = function (e) {
                    if (!e.type || xt.test(e.type)) {
                        return r ? r.push(e.parentNode ? e.parentNode.removeChild(e) : e) : n.appendChild(e)
                    }
                };
                for (s = 0; (u = b[s]) != null; s++) {
                    if (!v.nodeName(u, "script") || !m(u)) {
                        n.appendChild(u), typeof u.getElementsByTagName != "undefined" && (g = v.grep(v.merge([], u.getElementsByTagName("script")), m), b.splice.apply(b, [s + 1, 0].concat(g)), s += g.length)
                    }
                }
            }
            return b
        }, cleanData: function (e, t) {
            var n, r, i, s, o = 0, u = v.expando, a = v.cache, f = v.support.deleteExpando, l = v.event.special;
            for (; (i = e[o]) != null; o++) {
                if (t || v.acceptData(i)) {
                    r = i[u], n = r && a[r];
                    if (n) {
                        if (n.events) {
                            for (s in n.events) {
                                l[s] ? v.event.remove(i, s) : v.removeEvent(i, s, n.handle)
                            }
                        }
                        a[r] && (delete a[r], f ? delete i[u] : i.removeAttribute ? i.removeAttribute(u) : i[u] = null, v.deletedIds.push(r))
                    }
                }
            }
        }
    }), function () {
        var e, t;
        v.uaMatch = function (e) {
            e = e.toLowerCase();
            var t = /(chrome)[ \/]([\w.]+)/.exec(e) || /(webkit)[ \/]([\w.]+)/.exec(e) || /(opera)(?:.*version|)[ \/]([\w.]+)/.exec(e) || /(msie) ([\w.]+)/.exec(e) || e.indexOf("compatible") < 0 && /(mozilla)(?:.*? rv:([\w.]+)|)/.exec(e) || [];
            return {browser: t[1] || "", version: t[2] || "0"}
        }, e = v.uaMatch(o.userAgent), t = {}, e.browser && (t[e.browser] = !0, t.version = e.version), t.chrome ? t.webkit = !0 : t.webkit && (t.safari = !0), v.browser = t, v.sub = function () {
            function e(t, n) {
                return new e.fn.init(t, n)
            }

            v.extend(!0, e, this), e.superclass = this, e.fn = e.prototype = this(), e.fn.constructor = e, e.sub = this.sub, e.fn.init = function (r, i) {
                return i && i instanceof v && !(i instanceof e) && (i = e(i)), v.fn.init.call(this, r, i, t)
            }, e.fn.init.prototype = e.fn;
            var t = e(i);
            return e
        }
    }();
    var Dt, Pt, Ht, Bt = /alpha\([^)]*\)/i, jt = /opacity=([^)]*)/, Ft = /^(top|right|bottom|left)$/, It = /^(none|table(?!-c[ea]).+)/, qt = /^margin/, Rt = new RegExp("^(" + m + ")(.*)$", "i"), Ut = new RegExp("^(" + m + ")(?!px)[a-z%]+$", "i"), zt = new RegExp("^([-+])=(" + m + ")", "i"), Wt = {BODY: "block"}, Xt = {
        position: "absolute",
        visibility: "hidden",
        display: "block"
    }, Vt = {
        letterSpacing: 0,
        fontWeight: 400
    }, $t = ["Top", "Right", "Bottom", "Left"], Jt = ["Webkit", "O", "Moz", "ms"], Kt = v.fn.toggle;
    v.fn.extend({
        css: function (e, n) {
            return v.access(this, function (e, n, r) {
                return r !== t ? v.style(e, n, r) : v.css(e, n)
            }, e, n, arguments.length > 1)
        }, show: function () {
            return Yt(this, !0)
        }, hide: function () {
            return Yt(this)
        }, toggle: function (e, t) {
            var n = typeof e == "boolean";
            return v.isFunction(e) && v.isFunction(t) ? Kt.apply(this, arguments) : this.each(function () {
                (n ? e : Gt(this)) ? v(this).show() : v(this).hide()
            })
        }
    }), v.extend({
        cssHooks: {
            opacity: {
                get: function (e, t) {
                    if (t) {
                        var n = Dt(e, "opacity");
                        return n === "" ? "1" : n
                    }
                }
            }
        },
        cssNumber: {
            fillOpacity: !0,
            fontWeight: !0,
            lineHeight: !0,
            opacity: !0,
            orphans: !0,
            widows: !0,
            zIndex: !0,
            zoom: !0
        },
        cssProps: {"float": v.support.cssFloat ? "cssFloat" : "styleFloat"},
        style: function (e, n, r, i) {
            if (!e || e.nodeType === 3 || e.nodeType === 8 || !e.style) {
                return
            }
            var s, o, u, a = v.camelCase(n), f = e.style;
            n = v.cssProps[a] || (v.cssProps[a] = Qt(f, a)), u = v.cssHooks[n] || v.cssHooks[a];
            if (r === t) {
                return u && "get"in u && (s = u.get(e, !1, i)) !== t ? s : f[n]
            }
            o = typeof r, o === "string" && (s = zt.exec(r)) && (r = (s[1] + 1) * s[2] + parseFloat(v.css(e, n)), o = "number");
            if (r == null || o === "number" && isNaN(r)) {
                return
            }
            o === "number" && !v.cssNumber[a] && (r += "px");
            if (!u || !("set"in u) || (r = u.set(e, r, i)) !== t) {
                try {
                    f[n] = r
                } catch (l) {
                }
            }
        },
        css: function (e, n, r, i) {
            var s, o, u, a = v.camelCase(n);
            return n = v.cssProps[a] || (v.cssProps[a] = Qt(e.style, a)), u = v.cssHooks[n] || v.cssHooks[a], u && "get"in u && (s = u.get(e, !0, i)), s === t && (s = Dt(e, n)), s === "normal" && n in Vt && (s = Vt[n]), r || i !== t ? (o = parseFloat(s), r || v.isNumeric(o) ? o || 0 : s) : s
        },
        swap: function (e, t, n) {
            var r, i, s = {};
            for (i in t) {
                s[i] = e.style[i], e.style[i] = t[i]
            }
            r = n.call(e);
            for (i in t) {
                e.style[i] = s[i]
            }
            return r
        }
    }), e.getComputedStyle ? Dt = function (t, n) {
        var r, i, s, o, u = e.getComputedStyle(t, null), a = t.style;
        return u && (r = u.getPropertyValue(n) || u[n], r === "" && !v.contains(t.ownerDocument, t) && (r = v.style(t, n)), Ut.test(r) && qt.test(n) && (i = a.width, s = a.minWidth, o = a.maxWidth, a.minWidth = a.maxWidth = a.width = r, r = u.width, a.width = i, a.minWidth = s, a.maxWidth = o)), r
    } : i.documentElement.currentStyle && (Dt = function (e, t) {
        var n, r, i = e.currentStyle && e.currentStyle[t], s = e.style;
        return i == null && s && s[t] && (i = s[t]), Ut.test(i) && !Ft.test(t) && (n = s.left, r = e.runtimeStyle && e.runtimeStyle.left, r && (e.runtimeStyle.left = e.currentStyle.left), s.left = t === "fontSize" ? "1em" : i, i = s.pixelLeft + "px", s.left = n, r && (e.runtimeStyle.left = r)), i === "" ? "auto" : i
    }), v.each(["height", "width"], function (e, t) {
        v.cssHooks[t] = {
            get: function (e, n, r) {
                if (n) {
                    return e.offsetWidth === 0 && It.test(Dt(e, "display")) ? v.swap(e, Xt, function () {
                        return tn(e, t, r)
                    }) : tn(e, t, r)
                }
            }, set: function (e, n, r) {
                return Zt(e, n, r ? en(e, t, r, v.support.boxSizing && v.css(e, "boxSizing") === "border-box") : 0)
            }
        }
    }), v.support.opacity || (v.cssHooks.opacity = {
        get: function (e, t) {
            return jt.test((t && e.currentStyle ? e.currentStyle.filter : e.style.filter) || "") ? 0.01 * parseFloat(RegExp.$1) + "" : t ? "1" : ""
        }, set: function (e, t) {
            var n = e.style, r = e.currentStyle, i = v.isNumeric(t) ? "alpha(opacity=" + t * 100 + ")" : "", s = r && r.filter || n.filter || "";
            n.zoom = 1;
            if (t >= 1 && v.trim(s.replace(Bt, "")) === "" && n.removeAttribute) {
                n.removeAttribute("filter");
                if (r && !r.filter) {
                    return
                }
            }
            n.filter = Bt.test(s) ? s.replace(Bt, i) : s + " " + i
        }
    }), v(function () {
        v.support.reliableMarginRight || (v.cssHooks.marginRight = {
            get: function (e, t) {
                return v.swap(e, {display: "inline-block"}, function () {
                    if (t) {
                        return Dt(e, "marginRight")
                    }
                })
            }
        }), !v.support.pixelPosition && v.fn.position && v.each(["top", "left"], function (e, t) {
            v.cssHooks[t] = {
                get: function (e, n) {
                    if (n) {
                        var r = Dt(e, t);
                        return Ut.test(r) ? v(e).position()[t] + "px" : r
                    }
                }
            }
        })
    }), v.expr && v.expr.filters && (v.expr.filters.hidden = function (e) {
        return e.offsetWidth === 0 && e.offsetHeight === 0 || !v.support.reliableHiddenOffsets && (e.style && e.style.display || Dt(e, "display")) === "none"
    }, v.expr.filters.visible = function (e) {
        return !v.expr.filters.hidden(e)
    }), v.each({margin: "", padding: "", border: "Width"}, function (e, t) {
        v.cssHooks[e + t] = {
            expand: function (n) {
                var r, i = typeof n == "string" ? n.split(" ") : [n], s = {};
                for (r = 0; r < 4; r++) {
                    s[e + $t[r] + t] = i[r] || i[r - 2] || i[0]
                }
                return s
            }
        }, qt.test(e) || (v.cssHooks[e + t].set = Zt)
    });
    var rn = /%20/g, sn = /\[\]$/, on = /\r?\n/g, un = /^(?:color|date|datetime|datetime-local|email|hidden|month|number|password|range|search|tel|text|time|url|week)$/i, an = /^(?:select|textarea)/i;
    v.fn.extend({
        serialize: function () {
            return v.param(this.serializeArray())
        }, serializeArray: function () {
            return this.map(function () {
                return this.elements ? v.makeArray(this.elements) : this
            }).filter(function () {
                return this.name && !this.disabled && (this.checked || an.test(this.nodeName) || un.test(this.type))
            }).map(function (e, t) {
                var n = v(this).val();
                return n == null ? null : v.isArray(n) ? v.map(n, function (e, n) {
                    return {name: t.name, value: e.replace(on, "\r\n")}
                }) : {name: t.name, value: n.replace(on, "\r\n")}
            }).get()
        }
    }), v.param = function (e, n) {
        var r, i = [], s = function (e, t) {
            t = v.isFunction(t) ? t() : t == null ? "" : t, i[i.length] = encodeURIComponent(e) + "=" + encodeURIComponent(t)
        };
        n === t && (n = v.ajaxSettings && v.ajaxSettings.traditional);
        if (v.isArray(e) || e.jquery && !v.isPlainObject(e)) {
            v.each(e, function () {
                s(this.name, this.value)
            })
        } else {
            for (r in e) {
                fn(r, e[r], n, s)
            }
        }
        return i.join("&").replace(rn, "+")
    };
    var ln, cn, hn = /#.*$/, pn = /^(.*?):[ \t]*([^\r\n]*)\r?$/mg, dn = /^(?:about|app|app\-storage|.+\-extension|file|res|widget):$/, vn = /^(?:GET|HEAD)$/, mn = /^\/\//, gn = /\?/, yn = /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, bn = /([?&])_=[^&]*/, wn = /^([\w\+\.\-]+:)(?:\/\/([^\/?#:]*)(?::(\d+)|)|)/, En = v.fn.load, Sn = {}, xn = {}, Tn = ["*/"] + ["*"];
    try {
        cn = s.href
    } catch (Nn) {
        cn = i.createElement("a"), cn.href = "", cn = cn.href
    }
    ln = wn.exec(cn.toLowerCase()) || [], v.fn.load = function (e, n, r) {
        if (typeof e != "string" && En) {
            return En.apply(this, arguments)
        }
        if (!this.length) {
            return this
        }
        var i, s, o, u = this, a = e.indexOf(" ");
        return a >= 0 && (i = e.slice(a, e.length), e = e.slice(0, a)), v.isFunction(n) ? (r = n, n = t) : n && typeof n == "object" && (s = "POST"), v.ajax({
            url: e,
            type: s,
            dataType: "html",
            data: n,
            complete: function (e, t) {
                r && u.each(r, o || [e.responseText, t, e])
            }
        }).done(function (e) {
            o = arguments, u.html(i ? v("<div>").append(e.replace(yn, "")).find(i) : e)
        }), this
    }, v.each("ajaxStart ajaxStop ajaxComplete ajaxError ajaxSuccess ajaxSend".split(" "), function (e, t) {
        v.fn[t] = function (e) {
            return this.on(t, e)
        }
    }), v.each(["get", "post"], function (e, n) {
        v[n] = function (e, r, i, s) {
            return v.isFunction(r) && (s = s || i, i = r, r = t), v.ajax({
                type: n,
                url: e,
                data: r,
                success: i,
                dataType: s
            })
        }
    }), v.extend({
        getScript: function (e, n) {
            return v.get(e, t, n, "script")
        },
        getJSON: function (e, t, n) {
            return v.get(e, t, n, "json")
        },
        ajaxSetup: function (e, t) {
            return t ? Ln(e, v.ajaxSettings) : (t = e, e = v.ajaxSettings), Ln(e, t), e
        },
        ajaxSettings: {
            url: cn,
            isLocal: dn.test(ln[1]),
            global: !0,
            type: "GET",
            contentType: "application/x-www-form-urlencoded; charset=UTF-8",
            processData: !0,
            async: !0,
            accepts: {
                xml: "application/xml, text/xml",
                html: "text/html",
                text: "text/plain",
                json: "application/json, text/javascript",
                "*": Tn
            },
            contents: {xml: /xml/, html: /html/, json: /json/},
            responseFields: {xml: "responseXML", text: "responseText"},
            converters: {"* text": e.String, "text html": !0, "text json": v.parseJSON, "text xml": v.parseXML},
            flatOptions: {context: !0, url: !0}
        },
        ajaxPrefilter: Cn(Sn),
        ajaxTransport: Cn(xn),
        ajax: function (e, n) {
            function T(e, n, s, a) {
                var l, y, b, w, S, T = n;
                if (E === 2) {
                    return
                }
                E = 2, u && clearTimeout(u), o = t, i = a || "", x.readyState = e > 0 ? 4 : 0, s && (w = An(c, x, s));
                if (e >= 200 && e < 300 || e === 304) {
                    c.ifModified && (S = x.getResponseHeader("Last-Modified"), S && (v.lastModified[r] = S), S = x.getResponseHeader("Etag"), S && (v.etag[r] = S)), e === 304 ? (T = "notmodified", l = !0) : (l = On(c, w), T = l.state, y = l.data, b = l.error, l = !b)
                } else {
                    b = T;
                    if (!T || e) {
                        T = "error", e < 0 && (e = 0)
                    }
                }
                x.status = e, x.statusText = (n || T) + "", l ? d.resolveWith(h, [y, T, x]) : d.rejectWith(h, [x, T, b]), x.statusCode(g), g = t, f && p.trigger("ajax" + (l ? "Success" : "Error"), [x, c, l ? y : b]), m.fireWith(h, [x, T]), f && (p.trigger("ajaxComplete", [x, c]), --v.active || v.event.trigger("ajaxStop"))
            }

            typeof e == "object" && (n = e, e = t), n = n || {};
            var r, i, s, o, u, a, f, l, c = v.ajaxSetup({}, n), h = c.context || c, p = h !== c && (h.nodeType || h instanceof v) ? v(h) : v.event, d = v.Deferred(), m = v.Callbacks("once memory"), g = c.statusCode || {}, b = {}, w = {}, E = 0, S = "canceled", x = {
                readyState: 0, setRequestHeader: function (e, t) {
                    if (!E) {
                        var n = e.toLowerCase();
                        e = w[n] = w[n] || e, b[e] = t
                    }
                    return this
                }, getAllResponseHeaders: function () {
                    return E === 2 ? i : null
                }, getResponseHeader: function (e) {
                    var n;
                    if (E === 2) {
                        if (!s) {
                            s = {};
                            while (n = pn.exec(i)) {
                                s[n[1].toLowerCase()] = n[2]
                            }
                        }
                        n = s[e.toLowerCase()]
                    }
                    return n === t ? null : n
                }, overrideMimeType: function (e) {
                    return E || (c.mimeType = e), this
                }, abort: function (e) {
                    return e = e || S, o && o.abort(e), T(0, e), this
                }
            };
            d.promise(x), x.success = x.done, x.error = x.fail, x.complete = m.add, x.statusCode = function (e) {
                if (e) {
                    var t;
                    if (E < 2) {
                        for (t in e) {
                            g[t] = [g[t], e[t]]
                        }
                    } else {
                        t = e[x.status], x.always(t)
                    }
                }
                return this
            }, c.url = ((e || c.url) + "").replace(hn, "").replace(mn, ln[1] + "//"), c.dataTypes = v.trim(c.dataType || "*").toLowerCase().split(y), c.crossDomain == null && (a = wn.exec(c.url.toLowerCase()), c.crossDomain = !(!a || a[1] === ln[1] && a[2] === ln[2] && (a[3] || (a[1] === "http:" ? 80 : 443)) == (ln[3] || (ln[1] === "http:" ? 80 : 443)))), c.data && c.processData && typeof c.data != "string" && (c.data = v.param(c.data, c.traditional)), kn(Sn, c, n, x);
            if (E === 2) {
                return x
            }
            f = c.global, c.type = c.type.toUpperCase(), c.hasContent = !vn.test(c.type), f && v.active++ === 0 && v.event.trigger("ajaxStart");
            if (!c.hasContent) {
                c.data && (c.url += (gn.test(c.url) ? "&" : "?") + c.data, delete c.data), r = c.url;
                if (c.cache === !1) {
                    var N = v.now(), C = c.url.replace(bn, "$1_=" + N);
                    c.url = C + (C === c.url ? (gn.test(c.url) ? "&" : "?") + "_=" + N : "")
                }
            }
            (c.data && c.hasContent && c.contentType !== !1 || n.contentType) && x.setRequestHeader("Content-Type", c.contentType), c.ifModified && (r = r || c.url, v.lastModified[r] && x.setRequestHeader("If-Modified-Since", v.lastModified[r]), v.etag[r] && x.setRequestHeader("If-None-Match", v.etag[r])), x.setRequestHeader("Accept", c.dataTypes[0] && c.accepts[c.dataTypes[0]] ? c.accepts[c.dataTypes[0]] + (c.dataTypes[0] !== "*" ? ", " + Tn + "; q=0.01" : "") : c.accepts["*"]);
            for (l in c.headers) {
                x.setRequestHeader(l, c.headers[l])
            }
            if (!c.beforeSend || c.beforeSend.call(h, x, c) !== !1 && E !== 2) {
                S = "abort";
                for (l in{success: 1, error: 1, complete: 1}) {
                    x[l](c[l])
                }
                o = kn(xn, c, n, x);
                if (!o) {
                    T(-1, "No Transport")
                } else {
                    x.readyState = 1, f && p.trigger("ajaxSend", [x, c]), c.async && c.timeout > 0 && (u = setTimeout(function () {
                        x.abort("timeout")
                    }, c.timeout));
                    try {
                        E = 1, o.send(b, T)
                    } catch (k) {
                        if (!(E < 2)) {
                            throw k
                        }
                        T(-1, k)
                    }
                }
                return x
            }
            return x.abort()
        },
        active: 0,
        lastModified: {},
        etag: {}
    });
    var Mn = [], _n = /\?/, Dn = /(=)\?(?=&|$)|\?\?/, Pn = v.now();
    v.ajaxSetup({
        jsonp: "callback", jsonpCallback: function () {
            var e = Mn.pop() || v.expando + "_" + Pn++;
            return this[e] = !0, e
        }
    }), v.ajaxPrefilter("json jsonp", function (n, r, i) {
        var s, o, u, a = n.data, f = n.url, l = n.jsonp !== !1, c = l && Dn.test(f), h = l && !c && typeof a == "string" && !(n.contentType || "").indexOf("application/x-www-form-urlencoded") && Dn.test(a);
        if (n.dataTypes[0] === "jsonp" || c || h) {
            return s = n.jsonpCallback = v.isFunction(n.jsonpCallback) ? n.jsonpCallback() : n.jsonpCallback, o = e[s], c ? n.url = f.replace(Dn, "$1" + s) : h ? n.data = a.replace(Dn, "$1" + s) : l && (n.url += (_n.test(f) ? "&" : "?") + n.jsonp + "=" + s), n.converters["script json"] = function () {
                return u || v.error(s + " was not called"), u[0]
            }, n.dataTypes[0] = "json", e[s] = function () {
                u = arguments
            }, i.always(function () {
                e[s] = o, n[s] && (n.jsonpCallback = r.jsonpCallback, Mn.push(s)), u && v.isFunction(o) && o(u[0]), u = o = t
            }), "script"
        }
    }), v.ajaxSetup({
        accepts: {script: "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"},
        contents: {script: /javascript|ecmascript/},
        converters: {
            "text script": function (e) {
                return v.globalEval(e), e
            }
        }
    }), v.ajaxPrefilter("script", function (e) {
        e.cache === t && (e.cache = !1), e.crossDomain && (e.type = "GET", e.global = !1)
    }), v.ajaxTransport("script", function (e) {
        if (e.crossDomain) {
            var n, r = i.head || i.getElementsByTagName("head")[0] || i.documentElement;
            return {
                send: function (s, o) {
                    n = i.createElement("script"), n.async = "async", e.scriptCharset && (n.charset = e.scriptCharset), n.src = e.url, n.onload = n.onreadystatechange = function (e, i) {
                        if (i || !n.readyState || /loaded|complete/.test(n.readyState)) {
                            n.onload = n.onreadystatechange = null, r && n.parentNode && r.removeChild(n), n = t, i || o(200, "success")
                        }
                    }, r.insertBefore(n, r.firstChild)
                }, abort: function () {
                    n && n.onload(0, 1)
                }
            }
        }
    });
    var Hn, Bn = e.ActiveXObject ? function () {
        for (var e in Hn) {
            Hn[e](0, 1)
        }
    } : !1, jn = 0;
    v.ajaxSettings.xhr = e.ActiveXObject ? function () {
        return !this.isLocal && Fn() || In()
    } : Fn, function (e) {
        v.extend(v.support, {ajax: !!e, cors: !!e && "withCredentials"in e})
    }(v.ajaxSettings.xhr()), v.support.ajax && v.ajaxTransport(function (n) {
        if (!n.crossDomain || v.support.cors) {
            var r;
            return {
                send: function (i, s) {
                    var o, u, a = n.xhr();
                    n.username ? a.open(n.type, n.url, n.async, n.username, n.password) : a.open(n.type, n.url, n.async);
                    if (n.xhrFields) {
                        for (u in n.xhrFields) {
                            a[u] = n.xhrFields[u]
                        }
                    }
                    n.mimeType && a.overrideMimeType && a.overrideMimeType(n.mimeType), !n.crossDomain && !i["X-Requested-With"] && (i["X-Requested-With"] = "XMLHttpRequest");
                    try {
                        for (u in i) {
                            a.setRequestHeader(u, i[u])
                        }
                    } catch (f) {
                    }
                    a.send(n.hasContent && n.data || null), r = function (e, i) {
                        var u, f, l, c, h;
                        try {
                            if (r && (i || a.readyState === 4)) {
                                r = t, o && (a.onreadystatechange = v.noop, Bn && delete Hn[o]);
                                if (i) {
                                    a.readyState !== 4 && a.abort()
                                } else {
                                    u = a.status, l = a.getAllResponseHeaders(), c = {}, h = a.responseXML, h && h.documentElement && (c.xml = h);
                                    try {
                                        c.text = a.responseText
                                    } catch (p) {
                                    }
                                    try {
                                        f = a.statusText
                                    } catch (p) {
                                        f = ""
                                    }
                                    !u && n.isLocal && !n.crossDomain ? u = c.text ? 200 : 404 : u === 1223 && (u = 204)
                                }
                            }
                        } catch (d) {
                            i || s(-1, d)
                        }
                        c && s(u, f, c, l)
                    }, n.async ? a.readyState === 4 ? setTimeout(r, 0) : (o = ++jn, Bn && (Hn || (Hn = {}, v(e).unload(Bn)), Hn[o] = r), a.onreadystatechange = r) : r()
                }, abort: function () {
                    r && r(0, 1)
                }
            }
        }
    });
    var qn, Rn, Un = /^(?:toggle|show|hide)$/, zn = new RegExp("^(?:([-+])=|)(" + m + ")([a-z%]*)$", "i"), Wn = /queueHooks$/, Xn = [Gn], Vn = {
        "*": [function (e, t) {
            var n, r, i = this.createTween(e, t), s = zn.exec(t), o = i.cur(), u = +o || 0, a = 1, f = 20;
            if (s) {
                n = +s[2], r = s[3] || (v.cssNumber[e] ? "" : "px");
                if (r !== "px" && u) {
                    u = v.css(i.elem, e, !0) || n || 1;
                    do {
                        a = a || ".5", u /= a, v.style(i.elem, e, u + r)
                    } while (a !== (a = i.cur() / o) && a !== 1 && --f)
                }
                i.unit = r, i.start = u, i.end = s[1] ? u + (s[1] + 1) * n : n
            }
            return i
        }]
    };
    v.Animation = v.extend(Kn, {
        tweener: function (e, t) {
            v.isFunction(e) ? (t = e, e = ["*"]) : e = e.split(" ");
            var n, r = 0, i = e.length;
            for (; r < i; r++) {
                n = e[r], Vn[n] = Vn[n] || [], Vn[n].unshift(t)
            }
        }, prefilter: function (e, t) {
            t ? Xn.unshift(e) : Xn.push(e)
        }
    }), v.Tween = Yn, Yn.prototype = {
        constructor: Yn, init: function (e, t, n, r, i, s) {
            this.elem = e, this.prop = n, this.easing = i || "swing", this.options = t, this.start = this.now = this.cur(), this.end = r, this.unit = s || (v.cssNumber[n] ? "" : "px")
        }, cur: function () {
            var e = Yn.propHooks[this.prop];
            return e && e.get ? e.get(this) : Yn.propHooks._default.get(this)
        }, run: function (e) {
            var t, n = Yn.propHooks[this.prop];
            return this.options.duration ? this.pos = t = v.easing[this.easing](e, this.options.duration * e, 0, 1, this.options.duration) : this.pos = t = e, this.now = (this.end - this.start) * t + this.start, this.options.step && this.options.step.call(this.elem, this.now, this), n && n.set ? n.set(this) : Yn.propHooks._default.set(this), this
        }
    }, Yn.prototype.init.prototype = Yn.prototype, Yn.propHooks = {
        _default: {
            get: function (e) {
                var t;
                return e.elem[e.prop] == null || !!e.elem.style && e.elem.style[e.prop] != null ? (t = v.css(e.elem, e.prop, !1, ""), !t || t === "auto" ? 0 : t) : e.elem[e.prop]
            }, set: function (e) {
                v.fx.step[e.prop] ? v.fx.step[e.prop](e) : e.elem.style && (e.elem.style[v.cssProps[e.prop]] != null || v.cssHooks[e.prop]) ? v.style(e.elem, e.prop, e.now + e.unit) : e.elem[e.prop] = e.now
            }
        }
    }, Yn.propHooks.scrollTop = Yn.propHooks.scrollLeft = {
        set: function (e) {
            e.elem.nodeType && e.elem.parentNode && (e.elem[e.prop] = e.now)
        }
    }, v.each(["toggle", "show", "hide"], function (e, t) {
        var n = v.fn[t];
        v.fn[t] = function (r, i, s) {
            return r == null || typeof r == "boolean" || !e && v.isFunction(r) && v.isFunction(i) ? n.apply(this, arguments) : this.animate(Zn(t, !0), r, i, s)
        }
    }), v.fn.extend({
        fadeTo: function (e, t, n, r) {
            return this.filter(Gt).css("opacity", 0).show().end().animate({opacity: t}, e, n, r)
        }, animate: function (e, t, n, r) {
            var i = v.isEmptyObject(e), s = v.speed(t, n, r), o = function () {
                var t = Kn(this, v.extend({}, e), s);
                i && t.stop(!0)
            };
            return i || s.queue === !1 ? this.each(o) : this.queue(s.queue, o)
        }, stop: function (e, n, r) {
            var i = function (e) {
                var t = e.stop;
                delete e.stop, t(r)
            };
            return typeof e != "string" && (r = n, n = e, e = t), n && e !== !1 && this.queue(e || "fx", []), this.each(function () {
                var t = !0, n = e != null && e + "queueHooks", s = v.timers, o = v._data(this);
                if (n) {
                    o[n] && o[n].stop && i(o[n])
                } else {
                    for (n in o) {
                        o[n] && o[n].stop && Wn.test(n) && i(o[n])
                    }
                }
                for (n = s.length; n--;) {
                    s[n].elem === this && (e == null || s[n].queue === e) && (s[n].anim.stop(r), t = !1, s.splice(n, 1))
                }
                (t || !r) && v.dequeue(this, e)
            })
        }
    }), v.each({
        slideDown: Zn("show"),
        slideUp: Zn("hide"),
        slideToggle: Zn("toggle"),
        fadeIn: {opacity: "show"},
        fadeOut: {opacity: "hide"},
        fadeToggle: {opacity: "toggle"}
    }, function (e, t) {
        v.fn[e] = function (e, n, r) {
            return this.animate(t, e, n, r)
        }
    }), v.speed = function (e, t, n) {
        var r = e && typeof e == "object" ? v.extend({}, e) : {
            complete: n || !n && t || v.isFunction(e) && e,
            duration: e,
            easing: n && t || t && !v.isFunction(t) && t
        };
        r.duration = v.fx.off ? 0 : typeof r.duration == "number" ? r.duration : r.duration in v.fx.speeds ? v.fx.speeds[r.duration] : v.fx.speeds._default;
        if (r.queue == null || r.queue === !0) {
            r.queue = "fx"
        }
        return r.old = r.complete, r.complete = function () {
            v.isFunction(r.old) && r.old.call(this), r.queue && v.dequeue(this, r.queue)
        }, r
    }, v.easing = {
        linear: function (e) {
            return e
        }, swing: function (e) {
            return 0.5 - Math.cos(e * Math.PI) / 2
        }
    }, v.timers = [], v.fx = Yn.prototype.init, v.fx.tick = function () {
        var e, n = v.timers, r = 0;
        qn = v.now();
        for (; r < n.length; r++) {
            e = n[r], !e() && n[r] === e && n.splice(r--, 1)
        }
        n.length || v.fx.stop(), qn = t
    }, v.fx.timer = function (e) {
        e() && v.timers.push(e) && !Rn && (Rn = setInterval(v.fx.tick, v.fx.interval))
    }, v.fx.interval = 13, v.fx.stop = function () {
        clearInterval(Rn), Rn = null
    }, v.fx.speeds = {
        slow: 600,
        fast: 200,
        _default: 400
    }, v.fx.step = {}, v.expr && v.expr.filters && (v.expr.filters.animated = function (e) {
        return v.grep(v.timers, function (t) {
            return e === t.elem
        }).length
    });
    var er = /^(?:body|html)$/i;
    v.fn.offset = function (e) {
        if (arguments.length) {
            return e === t ? this : this.each(function (t) {
                v.offset.setOffset(this, e, t)
            })
        }
        var n, r, i, s, o, u, a, f = {top: 0, left: 0}, l = this[0], c = l && l.ownerDocument;
        if (!c) {
            return
        }
        return (r = c.body) === l ? v.offset.bodyOffset(l) : (n = c.documentElement, v.contains(n, l) ? (typeof l.getBoundingClientRect != "undefined" && (f = l.getBoundingClientRect()), i = tr(c), s = n.clientTop || r.clientTop || 0, o = n.clientLeft || r.clientLeft || 0, u = i.pageYOffset || n.scrollTop, a = i.pageXOffset || n.scrollLeft, {
            top: f.top + u - s,
            left: f.left + a - o
        }) : f)
    }, v.offset = {
        bodyOffset: function (e) {
            var t = e.offsetTop, n = e.offsetLeft;
            return v.support.doesNotIncludeMarginInBodyOffset && (t += parseFloat(v.css(e, "marginTop")) || 0, n += parseFloat(v.css(e, "marginLeft")) || 0), {
                top: t,
                left: n
            }
        }, setOffset: function (e, t, n) {
            var r = v.css(e, "position");
            r === "static" && (e.style.position = "relative");
            var i = v(e), s = i.offset(), o = v.css(e, "top"), u = v.css(e, "left"), a = (r === "absolute" || r === "fixed") && v.inArray("auto", [o, u]) > -1, f = {}, l = {}, c, h;
            a ? (l = i.position(), c = l.top, h = l.left) : (c = parseFloat(o) || 0, h = parseFloat(u) || 0), v.isFunction(t) && (t = t.call(e, n, s)), t.top != null && (f.top = t.top - s.top + c), t.left != null && (f.left = t.left - s.left + h), "using"in t ? t.using.call(e, f) : i.css(f)
        }
    }, v.fn.extend({
        position: function () {
            if (!this[0]) {
                return
            }
            var e = this[0], t = this.offsetParent(), n = this.offset(), r = er.test(t[0].nodeName) ? {
                top: 0,
                left: 0
            } : t.offset();
            return n.top -= parseFloat(v.css(e, "marginTop")) || 0, n.left -= parseFloat(v.css(e, "marginLeft")) || 0, r.top += parseFloat(v.css(t[0], "borderTopWidth")) || 0, r.left += parseFloat(v.css(t[0], "borderLeftWidth")) || 0, {
                top: n.top - r.top,
                left: n.left - r.left
            }
        }, offsetParent: function () {
            return this.map(function () {
                var e = this.offsetParent || i.body;
                while (e && !er.test(e.nodeName) && v.css(e, "position") === "static") {
                    e = e.offsetParent
                }
                return e || i.body
            })
        }
    }), v.each({scrollLeft: "pageXOffset", scrollTop: "pageYOffset"}, function (e, n) {
        var r = /Y/.test(n);
        v.fn[e] = function (i) {
            return v.access(this, function (e, i, s) {
                var o = tr(e);
                if (s === t) {
                    return o ? n in o ? o[n] : o.document.documentElement[i] : e[i]
                }
                o ? o.scrollTo(r ? v(o).scrollLeft() : s, r ? s : v(o).scrollTop()) : e[i] = s
            }, e, i, arguments.length, null)
        }
    }), v.each({Height: "height", Width: "width"}, function (e, n) {
        v.each({padding: "inner" + e, content: n, "": "outer" + e}, function (r, i) {
            v.fn[i] = function (i, s) {
                var o = arguments.length && (r || typeof i != "boolean"), u = r || (i === !0 || s === !0 ? "margin" : "border");
                return v.access(this, function (n, r, i) {
                    var s;
                    return v.isWindow(n) ? n.document.documentElement["client" + e] : n.nodeType === 9 ? (s = n.documentElement, Math.max(n.body["scroll" + e], s["scroll" + e], n.body["offset" + e], s["offset" + e], s["client" + e])) : i === t ? v.css(n, r, i, u) : v.style(n, r, i, u)
                }, n, o ? i : t, o, null)
            }
        })
    }), e.jQuery = e.$ = v, typeof define == "function" && define.amd && define.amd.jQuery && define("jquery", [], function () {
        return v
    })
})(window);
function color() {
    if ($("#colorColumn").length <= 0) {
        return false
    } else {
        var colorColumn = $("#colorColumn");
        var rows = colorColumn.find(".inner_wrapper");
        var first = $(rows[0]).find("div.service");
        var serviceTmp = null;
        if (first) {
            for (var i = 0; i < first.length; i++) {
                serviceTmp = $(first[i]);
                if (i <= 1) {
                    serviceTmp.addClass("color_1")
                } else {
                    serviceTmp.addClass("gray");
                    if (serviceTmp.find("span.glyphicon-tag").length >= 0) {
                        serviceTmp.find("span.glyphicon-tag").addClass("color_11")
                    }
                }
            }
        }
        var second = $(rows[1]).find("div.service");
        if (second) {
            for (var j = 0; j < second.length; j++) {
                serviceTmp = $(second[j]);
                if (j <= 1) {
                    serviceTmp.addClass("color_2")
                } else {
                    serviceTmp.addClass("gray");
                    if (serviceTmp.find("span.glyphicon-tag").length >= 0) {
                        serviceTmp.find("span.glyphicon-tag").addClass("color_22")
                    }
                }
            }
        }
        var third = $(rows[2]).find("div.service");
        if (third) {
            for (var k = 0; k < third.length; k++) {
                serviceTmp = $(third[k]);
                if (k <= 1) {
                    serviceTmp.addClass("color_3")
                } else {
                    serviceTmp.addClass("gray");
                    if (serviceTmp.find("span.glyphicon-tag").length >= 0) {
                        serviceTmp.find("span.glyphicon-tag").addClass("color_33")
                    }
                }
            }
        }
    }
}
function disabledBtn() {
    if ($("#priceList").attr("data-soure-price").indexOf("收费") != -1) {
        $(".hiddenByTime").attr("disabled", "disabled");
        $("#priceList").find(".priceLabel").css("backgroundImage", "none").css("border", "1px solid #c1c1c1");
        $(".spotTip").text("此活动为收费活动，具体价格待定，如需购买请致电400-003-3879")
    }
    if ($("#priceList").attr("data-soure-price").indexOf("待定") != -1) {
        $(".hiddenByTime").attr("disabled", "disabled");
        $("#priceList").find(".priceLabel").css("backgroundImage", "none").css("border", "1px solid #c1c1c1");
        $(".spotTip").text("此活动为收费活动，具体价格待定，如需购买请致电400-003-3879")
    }
    if ($("#priceList").attr("data-soure-price").indexOf("免费") != -1) {
        $(".hiddenByTime").attr("disabled", "disabled");
        $("#priceList").find(".priceLabel").css("backgroundImage", "none").css("border", "1px solid #c1c1c1");
        $(".spotTip").text("此活动为免费活动，名额有限，如需参加请到现场报名。")
    }
    if ($("#priceList").attr("data-soure-price").indexOf("售完") != -1) {
        var disabledArray = $("#priceList").find(".priceLabel").filter(function () {
            return $(this).find("a").text().indexOf("售完") != -1
        });
        disabledArray.css("backgroundImage", "none").css("border", "1px solid #c1c1c1").removeClass("selected");
        if (disabledArray.length === $("#priceList").attr("data-soure-price").split("/").length) {
            $(".spotTip").text("抱歉,此活动名额已完，您可以去瞧瞧其它活动")
			$(".hiddenByTime").attr({disable:true})
        } else {
            $($("#priceList").find(".priceLabel").filter(function () {
                return $(this).find("a").text().indexOf("售完") == -1
            })[0]).addClass("selected")
        }
    }
    if ($("#priceList").attr("data-soure-price").indexOf("现场") != -1) {
        $(".hiddenByTime").attr("disabled", "disabled");
        $("#priceList").find(".priceLabel").css("backgroundImage", "none").css("border", "1px solid #c1c1c1")
    }
    if ($(".hiddenByTime").text().indexOf("已过期") != -1) {
        $(".hiddenByTime").attr("disabled", "disabled");
        $("#priceList").find(".priceLabel").css("backgroundImage", "none").css("border", "1px solid #c1c1c1");
        $(".spotTip").text("此活动已过期，您可以去瞧瞧其它活动")
    }
}
function submitForm() {
    $(".searchInput").on("keyup", function (e) {
        if (e.keyCode == 13) {
            $(this).parents("form").submit()
        }
    });
    $("#searchIcon").on("click", function () {
        $(this).parents("form").submit()
    })
}
function selectPrice() {
    var priceList = $("#priceList");
    if (priceList.length <= 0) {
        return false
    } else {
        var dataSp = priceList.attr("data-soure-price");
        if (dataSp == "") {
            dataSp = "待定";
            priceList.attr("data-soure-price", dataSp)
        }
        var priceAry = dataSp.split("/");
        var priceAry2 = dataSp.split("/");
        if (priceAry.length > 1) {
            priceAry = priceAry.sort(function (a, b) {
                return parseInt(a) - parseInt(b)
            })
        }
        var tmpStr = "";
        if (dataSp != "") {
            if ($.trim(priceList.attr("data-discount-price")) == "") {
                for (var i = 0; i < priceAry.length; i++) {
                    if (i == 0) {
                        if (priceAry[i].indexOf("售完") != -1) {
                            ($("<li></li>").append($("<div></div>").addClass("disabledPriceLabel").addClass("priceLabel").addClass("selected").append($("<a></a>").attr("data-disabled", "true").addClass("currentPrice").text(priceAry[i])))).appendTo(priceList)
                        } else {
                            ($("<li></li>").append($("<div></div>").addClass("priceLabel").addClass("selected").append($("<a></a>").attr("data-disabled", "false").addClass("currentPrice").text(priceAry[i])))).appendTo(priceList)
                        }
                    } else {
                        if (priceAry[i].indexOf("售完") != -1) {
                            ($("<li></li>").append($("<div></div>").addClass("priceLabel").addClass("disabledPriceLabel").append($("<a></a>").attr("data-disabled", "true").addClass("currentPrice").text(priceAry[i])))).appendTo(priceList)
                        } else {
                            ($("<li></li>").append($("<div></div>").addClass("priceLabel").append($("<a></a>").attr("data-disabled", "false").addClass("currentPrice").text(priceAry[i])))).appendTo(priceList)
                        }
                    }
                }
            } else {
                if ($.trim(priceList.attr("data-discount-price")) != "") {
                    var discountPriceAry = priceList.attr("data-discount-price").split("/");
                    var dicountAry = priceList.attr("data-discount").split("/");
                    while (discountPriceAry.length < priceAry2.length) {
                        discountPriceAry[discountPriceAry.length] = priceAry2[discountPriceAry.length]
                    }
                    discountPriceAry = discountPriceAry.sort(function (a, b) {
                        return parseInt(a) - parseInt(b)
                    });
                    var discountHow = "";
                    for (var j = 0; j < priceAry.length; j++) {
                        discountHow = parseFloat((parseFloat(discountPriceAry[j]) / parseFloat(priceAry[j])).toFixed(1) * 10).toFixed(1);
                        if (parseInt(discountHow) == 10) {
                            discountHow = ""
                        } else {
                            discountHow += "折"
                        }
                        if (j == 0) {
                            if (priceAry[j].indexOf("售完") != -1) {
                                $("<li></li>").append($("<div></div>").addClass("priceLabel").addClass("disabledPriceLabel").addClass("selected").append($("<a></a>").css("display", "block").attr("data-disabled", "true").append($("<span></span>").addClass("currentPrice").text(discountPriceAry[j])))).appendTo(priceList)
                            } else {
                                $("<li></li>").append($("<span></span>").addClass("spanDiscountTip").text(discountHow)).append($("<div></div>").addClass("priceLabel").addClass("discountPriceLabel").addClass("selected").append($("<a></a>").css("display", "block").attr("data-disabled", "false").append($("<span></span>").addClass("currentPrice").text(discountPriceAry[j])).append($("<span></span>").addClass("sourcePrice").text("原价" + priceAry[j])))).appendTo(priceList)
                            }
                        } else {
                            if (priceAry[j].indexOf("售完") != -1) {
                                $("<li></li>").append($("<div></div>").addClass("priceLabel").addClass("disabledPriceLabel").append($("<a></a>").css("display", "block").attr("data-disabled", "true").append($("<span></span>").addClass("currentPrice").text(discountPriceAry[j])))).appendTo(priceList)
                            } else {
                                $("<li></li>").append($("<span></span>").addClass("spanDiscountTip").text(discountHow)).append($("<div></div>").addClass("priceLabel").addClass("discountPriceLabel").append($("<a></a>").css("display", "block").attr("data-disabled", "false").append($("<span></span>").addClass("currentPrice").text(discountPriceAry[j])).append($("<span></span>").addClass("sourcePrice").text("原价" + priceAry[j])))).appendTo(priceList)
                            }
                        }
                    }
                }
            }
            priceList.find("a").on("click", function () {
                if ($(this).attr("data-disabled") == "false") {
                    priceList.find("div").removeClass("selected");
                    $(this).parent("div").addClass("selected")
                }
                return false
            })
        }
    }
}
function discount() {
    if ($(".discountNum").length > 0) {
        $(".discountNum").each(function () {
            var tmp = $(this);
            var discount = tmp.attr("data-discount").split("/")[0];
            tmp.text(discount + "折")
        })
    }
}
function fillForm() {
    var price = $.trim($("#oneprice .purePrice").text());
    var sourcePrice = "";
    var sourceTotalPrice = "";
    if ($.trim($("#oneprice .purePrice").attr("data-price")) != "") {
        sourcePrice = $("#oneprice .purePrice").attr("data-price")
    }
    if (price == "") {
        $(".totalMoney .purePrice").text("0")
    }
    var num = 1;
    $("#total_num").attr("value", num);
    $("#ticketNum").change(function () {
        if (price != "") {
            var totalPrice = (parseFloat($.trim($("#oneprice .purePrice").text())) * parseInt($("#ticketNum")[0].value)).toFixed(2);
            if (sourcePrice != "") {
                sourceTotalPrice = (parseFloat($("#oneprice .purePrice").attr("data-price")) * parseInt($("#ticketNum")[0].value)).toFixed(2);
                $(".totalMoney .purePrice").attr("data-price", sourceTotalPrice)
            }
            $(".totalMoney .purePrice").text(totalPrice)
        }
        num = parseInt($("#ticketNum")[0].value);
        $("#total_num").attr("value", num)
    });
    if ($("#transformMoney").length > 0) {
        $("#transformMoney").toggle(function () {
            var tmpPrice = $("#oneprice .purePrice").text();
            $("#oneprice .purePrice").text($("#oneprice .purePrice").attr("data-price"));
            $("#oneprice .purePrice").attr("data-price", tmpPrice);
            $("#oneprice .priceUnit").text("(人民币)");
            var totalTmpPrice = $($(".totalMoney .purePrice")[0]).text();
            $(".totalMoney .purePrice").text($(".totalMoney .purePrice").attr("data-price"));
            $(".totalMoney .purePrice").attr("data-price", totalTmpPrice);
            $(".totalMoney .priceUnit").text("(人民币)")
        }, function () {
            var tmpPrice = $("#oneprice .purePrice").text();
            $("#oneprice .purePrice").text($("#oneprice .purePrice").attr("data-price"));
            $("#oneprice .purePrice").attr("data-price", tmpPrice);
            $("#oneprice .priceUnit").text("(" + $("#oneprice .priceUnit").attr("data-unit") + ")");
            var totalTmpPrice = $($(".totalMoney .purePrice")[0]).text();
            $(".totalMoney .purePrice").text($(".totalMoney .purePrice").attr("data-price"));
            $(".totalMoney .purePrice").attr("data-price", totalTmpPrice);
            $(".totalMoney .priceUnit").text("(" + $("#oneprice .priceUnit").attr("data-unit") + ")")
        })
    }
}
function countTimeStr() {
    if ($("#endTime").length > 0) {
        var dateValue = $("#endTime").attr("data-time");
        countDown("endTime", "timeTag", dateValue)
    }
}
function crumbsTag() {
    var crumbsTag = $(".crumbsTag");
    if (crumbsTag.length <= 0) {
        return false
    } else {
        var strtmp = "";
        var strArr = null;
        for (var i = 0; i < crumbsTag.length; i++) {
            strArr = ($(crumbsTag[i]).attr("data-tag")).split("/");
            for (var j = 0; j < strArr.length; j++) {
                if (j < strArr.length - 1) {
                    strtmp += '<li><a href="' + (strArr[i].split("$"))[0] + ">" + (strArr[i].split("$"))[1] + "</a></li>"
                } else {
                    strtmp += '<li><span class="currentStage">' + (strArr[i].split("$"))[1] + "</span></li>"
                }
            }
            $(crumbsTag[i]).parent("ul").html(strtmp)
        }
    }
}
function parseUrl() {
    var url = window.location.href;
    var length = url.length;
    var index = url.indexOf("order");
    var event_id = parseInt(url.substring(index + 6, length - 1));
    $("#event_id").attr("value", event_id)
}
function shotPrice() {
    if ($(".picPrice").length > 0) {
        $(".picPrice").each(function () {
            var tmp = $(this);
            var styleprice = $(this).attr("data-priceStyle");
            if (tmp.text().indexOf("/") != -1) {
                tmp.text(tmp.text().split("/")[0])
            }
            if (tmp.text().indexOf("收费") != -1) {
                tmp.text("收费")
            }
            if (tmp.text().indexOf("免费") != -1) {
                tmp.text("免费")
            }
            if (tmp.text().indexOf("待定") != -1) {
                tmp.text("待定")
            }
            if ($.trim(tmp.text()) == "") {
                tmp.text("待定")
            }
            if ($.trim(tmp.text()) !== "" && $.trim(tmp.text()) !== "收费" && $.trim(tmp.text()) !== "免费" && $.trim(tmp.text()) !== "待定") {
                tmp.append($("<span class='styleprice'>" + styleprice + "</span>"))
            }
        })
    }
}
function clearMoreTagByPaginationWrapper() {
    if ($(".dhd_pagination").length > 0) {
        $(".dhd_pagination").each(function () {
            var liArray = $(".dhd_pagination").find("li");
            for (var i = 0; i < liArray.length; i++) {
                if ($.trim($(liArray[i]).html()) == "") {
                    liArray[i].remove()
                }
            }
        })
    }
}
function scrollBottomDistance(mark) {
    var markObj = $("#" + mark);
    var markTop = markObj.offset().top;
    var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    var winHeight = document.documentElement.clientHeight;
    var intDistance = markTop - scrollTop - winHeight;
    return intDistance
}
function scrollTopDistance(mark) {
    var markObj = $("#" + mark);
    var markTop = markObj.offset().top;
    var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    var intDistance = markTop - scrollTop;
    return intDistance
}
function returnTop() {
    $backToTopEle = $('<div class="backToTop"><i class="iconfont" style="font-size:24px">&#xe60c;</i></div>').appendTo($("body")).click(function () {
        $("html, body").animate({scrollTop: 0}, 300)
    }), $backToTopFun = function () {
        var bodytop =  $("body").height();
        var st = $(document).scrollTop(), winh = $(window).height();
        (st > bodytop) ? $backToTopEle.show() : $backToTopEle.hide();
        (st > bodytop) ? $home.show() : $home.hide();
        if (!window.XMLHttpRequest) {
            $backToTopEle.css("top", st + winh - 126);
            $home.css("top", st + winh - 86)
        }
    };
    $home = $("<div class='new_weixing'><a class='iconfont' href='#'></a></div>" + "<div class='phone'><a href='#' class='iconfont'></a></div>" + "<a href='http://test3.huodongjia.com/app/' class='APP'><div></div></a>" + "<div class='backToTop'><a href='#' class='iconfont'></a></div>").appendTo($("body"));
    $(window).bind("scroll", $backToTopFun);
    $backToTopFun()
}
function GetRandomNum(Min, Max) {
    var Range = Max - Min;
    var Rand = Math.random();
    return (Min + Math.round(Rand * Range))
}
function formatTime(i) {
    if (i < 10) {
        i = "0" + i
    }
    return i
}
function changeListStatus() {
    var jumbotronListItem = $(".jumbotronListItem");
    var length = jumbotronListItem.length;
    var i = 0;
    var change = function () {
        i++;
        var k = i % length;
        jumbotronListItem.removeClass("active").eq(k).addClass("active")
    };
    setInterval(change, 5000)
}
function replaceStr(replaceStr, tmp) {
    var strArray = replaceStr.split(",");
    for (var i = 0; i < strArray.length; i++) {
        if (strArray[i] === tmp) {
            strArray.splice(i, 1);
            break
        }
    }
    return strArray.join(",")
}
function selectSubscription() {
    if ($(".subscriptionList span").length > 0) {
        var strSelected = $("#selectedSub").attr("value");
        $(".subscriptionList span").bind("click", function () {
            var selectedValue = $(this).text();
            if ($(this).hasClass("selected")) {
                $(this).removeClass("selected");
                if (strSelected.indexOf(selectedValue) != -1) {
                    strSelected = replaceStr(strSelected, selectedValue)
                }
            } else {
                $(this).addClass("selected");
                strSelected += selectedValue + ","
            }
            $("#selectedSub").attr("value", strSelected)
        });
        $("#subscriptionRow").click(function (e) {
            if (e.target.nodeName.toLowerCase() === "span") {
                var $spanTarget = $(e.target);
                var selectedValue = $spanTarget.text();
                if ($spanTarget.hasClass("selected")) {
                    $spanTarget.removeClass("selected");
                    if (strSelected.indexOf(selectedValue) != -1) {
                        strSelected = replaceStr(strSelected, selectedValue)
                    }
                    $spanTarget.parent().css("borderColor", "#d8d8d8").find(".subscriptionIcon").hide()
                } else {
                    $spanTarget.addClass("selected");
                    strSelected += selectedValue + ",";
                    $spanTarget.parent().css("borderColor", "#2c3e50").find(".subscriptionIcon").show()
                }
                $("#selectedSub").attr("value", strSelected)
            }
        });
        $(".subscriptionList li").mouseenter(function () {
            if (!$(this).find("span").hasClass("selected")) {
                $(this).css("borderColor", "#2c3e50").find(".subscriptionIcon").show()
            }
        });
        $(".subscriptionList li").mouseleave(function () {
            if (!$(this).find("span").hasClass("selected")) {
                $(this).css("borderColor", "#d8d8d8").find(".subscriptionIcon").hide()
            }
        })
    }
}
$(document).ready(function () {
    $("#changecityHead").hover(function () {
        $("#changecityHead a span").addClass("transform");
        $("#cityMap").css("left", "0")
    }, function () {
        $("#changecityHead a span").removeClass("transform");
        $("#cityMap").css("left", "-10000px")
    });
    if ($("#goIconSearch").length > 0) {
        $("#goIconSearch").click(function () {
            if ($("#ct-search").hasClass("ct-search-open")) {
                $("#ct-search").removeClass("ct-search-open")
            } else {
                $("#ct-search").addClass("ct-search-open");
                $("#topSearchForm .ct-search-input")[0].focus()
            }
        });
        $("#topSearchForm").submit(function () {
            if ($.trim($("#topSearchForm .ct-search-input").val()) == "") {
                $("#ct-search").removeClass("ct-search-open");
                return false
            }
        });
        $("#topSearchForm .ct-search-input").blur(function () {
            if (event.relatedTarget.id != "go") {
                $("#ct-search").removeClass("ct-search-open")
            }
        })
    }
    selectPrice();
    crumbsTag();
    var moreRecom = $(".moreRecom");
    if (moreRecom.length > 0) {
        moreRecom.click(function () {
            var that = this;
            $(this).siblings("div").slideDown("normal", function () {
                $(that).hide()
            })
        })
    }
    if ($("#priceList").length > 0) {
        disabledBtn()
    }
    $(".submitBtn").on("click", function () {
        var myprice = 0;
        if ($("#myPrice").length > 0 && parseFloat($("#myPrice")[0].value)) {
            myprice = parseFloat($("#myPrice")[0].value)
        }
        var selectedPrice = $(".priceLabel.selected").find(".currentPrice").text();
        if ($(".priceLabel.selected").find(".currentPrice").length > 0) {
            var rawPrice = $(".priceLabel.selected").find(".sourcePrice").text().substring(2);
            $("#rawPrice").attr("value", rawPrice)
        }
        if (myprice == 0 && parseFloat(selectedPrice)) {
            $("#myPrice").attr("value", parseFloat(selectedPrice))
        } else {
            $("#myPrice").attr("value", myprice)
        }
        $("#priceForm").submit()
    });
    if ($("#oneprice").length > 0) {
        fillForm()
    }
    parseUrl();
    submitForm();
    discount();
    shotPrice();
    $("#centerSearchIcon").click(function () {
        $(this).parent("form").submit()
    });
    function bindClick1() {
        var elemClone = $("#contactModal").clone();
        $("#guestMessageButton").click(function () {
            dialog({title: "留言咨询", content: elemClone, id: "questionMessage"}).showModal();
            $(".questionForm").validation()
        });
        $(".modal-body #contactModal").remove()
    }

    function bindClick2() {
        var elemClone2 = $("#suggestionModal").clone();
        $("#suggestionButton").click(function () {
            dialog({title: "检查纠错", content: elemClone2, id: "suggestionMessage"}).showModal();
            $(".suggestionForm").validation()
        });
        $(".modal-body #suggestionModal").remove()
    }

    if ($("#guestMessageButton").length > 0) {
        bindClick1()
    }
    if ($("#suggestionModal").length > 0) {
        bindClick2()
    }
    if ($(".slideLi").length > 0) {
        $(".slideLi").each(function () {
            $(this).parent().css("paddingLeft", "0");
            if ($(this).parent().find("ul").find("li").length <= 0) {
                $(this).parent().css("paddingLeft", ".6em");
                $(this).remove()
            }
        });
        $(".slideLi").toggle(function () {
            var lls = $(this).parent().find("li");
            lls.slideUp()
        }, function () {
            var lls = $(this).parent().find("li");
            lls.slideDown()
        })
    }
    returnTop();
    if ($(".backToTop").css("display") != "none" && $("#textMark").length > 0) {
        window.onscroll = function () {
            var newSbd = scrollTopDistance("textMark");
            if (newSbd <= 0) {
                $("#tabDiv .nav-tabs").addClass("fixedNav");
                $(".blank_block").show()
            } else {
                $("#tabDiv .nav-tabs").removeClass("fixedNav");
                $(".blank_block").hide()
            }
        }
    }
    if ($(".canjiaNum").length > 0) {
        $(".canjiaNum").each(function () {
            $(this).html(GetRandomNum(30, 100) + "<span style='color:#b5b5b5;'>人参加</span>")
        })
    }
    if ($(".likeNum").length > 0) {
        $(".likeNum").each(function () {
            $(this).html(GetRandomNum(50, 200) + "<span style='color:#b5b5b5;'>人喜欢</span>")
        })
    }
    if ($(".tagNum").length > 3) {
        var tagNumArray = $(".tagNum");
        for (var i = 3; i < tagNumArray.length; i++) {
            $(tagNumArray[i]).css({"color": "#fff", "backgroundColor": "#bbb"})
        }
    }
    if ($(".crowdingDiv").length > 0 && $("#beginPrice").length > 0 && $("#endPrice").length > 0) {
        var beginPrice = $("#beginPrice").text().substring(1);
        beginPrice = parseInt(beginPrice);
        var endPrice = $("#endPrice").text().substring(1);
        endPrice = parseInt(endPrice);
        var ss = 3;
        if (beginPrice != 0) {
            var ss = (parseInt(beginPrice) / parseInt(endPrice)) * 100
        }
        $(".crowdingInnerDiv").css("width", ss + "%").attr("aria-valuenow", ss).find("sr-only").text("已筹集:" + ss + "%");
        if ($("#timeH").length > 0) {
            var leftTime = 0;
            var todyDay = new Date();
            var endTime = new Date($("#timeH").attr("data-end-time"));
            var level1 = endTime.getTime() - todyDay.getTime();
            var date = formatTime(Math.floor(level1 / (24 * 3600 * 1000)));
            $("<h5>剩余时间</h5>").appendTo($("#timeLeft"));
            $("<h5></h5>").text(date + "天").appendTo($("#timeLeft"))
        }
    }
    countTimeStr();
    if ($(".tagDiv").length > 0) {
        $(".tagDiv").hover(function () {
            $(".tagDiv").removeClass("selectedTagDiv");
            $(this).addClass("selectedTagDiv")
        }, function () {
            $(this).removeClass("selectedTagDiv")
        })
    }
    if ($("#return").length > 0) {
        var href = window.location.href.replace("order/", "event-");
        href = href.substring(0, href.length - 1) + ".html";
        $("#return").attr("href", href)
    }
    if ($("#ticketNum").length > 0) {
        $("#ticketNum").blur(function () {
            var price = parseInt($(this).val());
            if (price) {
                $(this).attr("value", price)
            } else {
                $(this).attr("value", 1)
            }
            $("#ticketNum").trigger("change")
        });
        $("#ticketNum").trigger("change")
    }
    if ($(".clickNum").length > 0) {
        $("#minus").click(function () {
            var price = parseInt($("#ticketNum").val()) - 1;
            if (price <= 0) {
                price = 1
            }
            $("#ticketNum").attr("value", price);
            $("#ticketNum").trigger("change")
        });
        $("#plus").click(function () {
            var price = parseInt($("#ticketNum").val()) + 1;
            $("#ticketNum").attr("value", price);
            $("#ticketNum").trigger("change")
        })
    }
    if ($(".telphoneA").length > 0) {
        $(".telphoneA").attr("href", "tel:400-003-3879")
    }
    if ($(".telphoneB").length > 0) {
        $(".telphoneB").attr("href", "tel:028-85319761")
    }
    if ($("#captcha").length > 0) {
        $("#captcha").blur(function () {
            var value = $(this).val();
            var url = "/verify_tel_captcha/";
            var telephone = $("#telephone").val();
            if ($.trim(value) != "" && $("#captcha").attr("btvd-el") == undefined) {
                $.ajax({
                    type: "post",
                    url: url,
                    data: {captcha: value, mobilphone: telephone},
                    async: false,
                    success: function (data) {
                        var flag = jQuery.parseJSON(data).flag;
                        if (!flag) {
                            $("#captcha").attr("btvd-el", "errorValidateCode");
                            $("#captcha").trigger("blur")
                        }
                    }
                })
            }
        });
        $("#captcha").change(function () {
            $("#captcha").removeAttr("btvd-el")
        })
    }
    if ($(".spotTip").length > 0) {
        var dataTip = $(".spotTip").attr("data-tip");
        if (dataTip == 2 || dataTip == 3) {
            $(".spotTip").hide()
        }
    }
    if ($("#colorColumn").length > 0) {
        var leftSide = $("#colorColumn .inner_wrapper").eq(0).find(".col-md-6").clone();
        var rightSide = $("#colorColumn .inner_wrapper").eq(1).find(".col-md-6").clone();
        var leftLength = leftSide.length;
        var rightLength = rightSide.length;
        if ((leftLength + rightLength < 9) || ((leftLength + rightLength) > 8 && Math.abs(leftLength - rightLength) > 3)) {
            leftSide.removeClass("col-md-6").addClass("col-md-4");
            rightSide.removeClass("col-md-6").addClass("col-md-4");
            var hrefSpecial = $("#colorColumn .inner_wrapper").eq(0).find("h2 a").attr("href");
            $("#colorColumn").find("*").remove();
            $("#colorColumn").append($("<div class='inner_wrapper'></div>").append($("<h2></h2>").append($("<a></a>").attr("target", "_blank").attr("href", hrefSpecial).text("玩乐活动"))).append($("<h3>玩所未玩，精彩没有上限</h3>").append($("<a></a>").attr("target", "_blank").attr("href", hrefSpecial).text("更多"))).append($("<div class='row'></div>").append(leftSide).append(rightSide)))
        }
        var navUl = $("#navUl");
        var lis = $("#navUl").find("li");
        var cloneNavLi = new Array();
        for (var u = 0; u < lis.length; u++) {
            cloneNavLi[u] = lis[u]
        }
        navUl.find("li").remove();
        for (var k = cloneNavLi.length - 1; k > 0; k--) {
            navUl.append(cloneNavLi[k])
        }
    }
    if ($(".spotTab").length > 0) {
        $(".spotTab").find("a").attr("target", "_blank")
    }
    if ($(".payAttention .weixing").length > 0) {
        $(".payAttention .weixing").hover(function () {
            $(".weixingImg").addClass("transform")
        }, function () {
            $(".weixingImg").removeClass("transform")
        })
    }
    if ($("#categoryList").length > 0) {
        createListBySelected()
    }
    selectSubscription();
    if ($("#submitOrder").length > 0) {
        $("#subscriptionAlert").hide();
        $("#submitOrder").bind("click", function () {
            if ($("#selectedSub").attr("value") != "" || $("#customerKeywords").attr("value") != "") {
                $("#subscriptionForm").submit()
            } else {
                $("#subscriptionAlert").show()
            }
        })
    }
    if ($("#tabDiv").length > 0) {
        $("#tabDiv .tab-content .tab-pane").hide();
        $("#tabDiv .tab-content .active").show();
        $("#tabDiv .nav-tabs li").click(function () {
            $("#tabDiv .nav-tabs li").removeClass("active");
            $(this).addClass("active");
            var target = $(this).find("h2").attr("href").substring(1);
            $("#tabDiv .tab-content .tab-pane").hide();
            $("#tabDiv .tab-content .tab-pane").removeClass("active");
            $("#tabDiv").find("#" + target).addClass("active");
            $("#tabDiv .tab-content .active").show()
        })
    }
    if ($("#getCapcheByPhone").length > 0) {
        $("#getCapcheByPhone").click(function () {
            if (!$(this).hasClass("disabled")) {
                var url = "/send_check_mesage/";
                var tel = $("#telephone").val();
                if (tel != "" && (/^1[3-8]+\d{9}$/).test(tel)) {
                    $("#sendType").remove();
                    $("#leftTime").remove();
                    $("#miao").remove();
                    $("#getCapcheByPhone").after('<span id="leftTime" style="margin-left:2em;"></span><span id="miao">秒</span><p id="sendType">发送中..</p>');
                    $.get(url, {"tel": tel}, function (data) {
                        $("#getCapcheByPhone").css({"color": "#ccc", "cursor": "progress"}).addClass("disabled");
                        $("#sendType").text("亲,手机验证码已发送,如超过30秒后还未接收到手机短信，请重试!");
                        if (typeof(JSON) == "undefined") {
                            var dataJson = eval("(" + data + ")");
                            var flag = dataJson.flag
                        } else {
                            var flag = JSON.parse(data).flag
                        }
                        var index = 30;
                        if (flag) {
                            var handle = setInterval(function () {
                                $("#leftTime").text(index--)
                            }, "1000");
                            setTimeout(function () {
                                $("#getCapcheByPhone").css({
                                    "color": "#428bca",
                                    "cursor": "default"
                                }).removeClass("disabled");
                                $("#leftTime").remove();
                                $("#miao").remove();
                                clearInterval(handle)
                            }, "20000")
                        } else {
                            $("#sendType").text("手机验证码失败，请重试!")
                        }
                    })
                } else {
                    alert("请输入正确的手机号")
                }
            }
        })
    }
    function clearFile(fileInput) {
        var sourceParent = fileInput.parent();
        $("<form id='tempForm'></form>").appendTo(document.body);
        var tempForm = $("#tempForm");
        tempForm.append(fileInput);
        tempForm.get(0).reset();
        sourceParent.prepend(fileInput)
    }

    if ($("#fileUpload").length > 0) {
        var isIE = /msie/i.test(navigator.userAgent) && !window.opera;
        $("#publishForm").validation();
        $("#fileUpload").on("change", function () {
            var fileNameArray = [];
            if (isIE && !this.files) {
                var filePath = this.value;
                if (filePath.indexOf(".doc") == -1 && filePath.indexOf(".pdf") == -1) {
                    alert("您好!活动家暂时只接受pdf,和word类型的文档,请重新选择符合类型的文档!");
                    clearFile($(this))
                }
                var image = new Image();
                image.dynsrc = filePath;
                fileSize = image.fileSize;
                var size = fileSize / 1024;
                if (size > 1000) {
                    alert("注意!附件不能大于1M");
                    clearFile($(this))
                }
            } else {
                for (var i = 0; i < this.files.length; i++) {
                    fileSize = this.files[i].size;
                    if (this.files[i].name.indexOf(".pdf") == -1 && this.files[i].name.indexOf(".doc") == -1) {
                        sweetAlert("您好!活动家暂时只接受pdf,和word类型的文档,请重新选择符合类型的文档!", "error");
                        clearFile($(this))
                    }
                    if (fileSize / 1024 > 1000) {
                        fileNameArray[fileNameArray.length] = this.files[i].name
                    }
                }
                if (fileNameArray.length > 0) {
                    var fileNameStr = "";
                    for (var i = 0; i < fileNameArray.length; i++) {
                        fileNameStr += fileNameArray[i] + ","
                    }
                    fileNameStr = fileNameStr.substring(0, fileNameStr.length - 1);
                    sweetAlert("注意!上传文件大小不能超过1M", fileNameStr + "大小大于1M", "error");
                    clearFile($(this))
                }
            }
        })
    }
});
function bindListA(tmpId) {
    $(".secondLevelUl").hide();
    var relativeId = "";
    if (tmpId.target) {
        relativeId = $(tmpId.target).attr("id")
    } else {
        relativeId = tmpId
    }
    $(".secondLevelUl").filter(function () {
        return $(this).attr("data-id") == relativeId
    }).show()
}
function createListBySelected() {
    var selectedFlag = false;
    var selectedLi = null;
    var levelFlag = 0;
    var secondUL = $("#categoryList>ul").eq(1);
    var cloneList = {};
    var firstObject = {};
    var secondArray = [];
    var secondLength = 0;
    var tmp1 = null;
    var tmp2 = null;
    var tmp3 = null;
    var tmp4 = null;
    var tmp5 = null;
    var tmp6 = null;
    var parent = null;
    secondUL.find("li").each(function () {
        if ($(this).hasClass("selected")) {
            selectedFlag = true;
            selectedLi = $(this)
        }
        if ($(this).hasClass("selectedUl")) {
            selectedFlag = true;
            selectedLi = $(this);
            levelFlag = 1
        }
    });
    if (levelFlag != 1) {
        if (selectedFlag == true) {
            if (selectedLi.find(">ul").length < 1) {
                levelFlag = 3
            } else {
                if (selectedLi.find(">ul>li>>ul").length < 1) {
                    levelFlag = 2
                }
            }
        }
    }
    if (levelFlag == 1) {
        parent = selectedLi
    }
    if (levelFlag == 2) {
        parent = selectedLi.parent("ul").parent("li")
    }
    if (levelFlag == 3) {
        parent = selectedLi.parent("ul").parent("li").parent("ul").parent("li")
    }
    if (parent != null) {
        firstObject.name = parent.find(">a").text();
        firstObject.href = parent.find(">a").attr("href");
        tmp1 = parent.find(">ul>li");
        secondLength = tmp1.length;
        for (var i = 0; i < secondLength; i++) {
            tmp2 = tmp1.eq(i);
            tmp3 = {};
            tmp3.name = tmp2.find(">a").text();
            tmp3.href = tmp2.find(">a").attr("href");
            tmp3.objectArray = [];
            tmp4 = tmp2.find(">ul>li");
            if (tmp4.length > 0) {
                for (var j = 0; j < tmp4.length; j++) {
                    tmp5 = tmp4.eq(j);
                    tmp6 = {};
                    tmp6.name = tmp5.find(">a").text();
                    tmp6.href = tmp5.find(">a").attr("href");
                    tmp3.objectArray[j] = tmp6
                }
            }
            secondArray[i] = tmp3
        }
        firstObject.arrayObject = secondArray
    }
    if (firstObject.arrayObject.length > 0) {
        var fillDivArea = $("<div></div>").addClass("listArea").addClass("clearfix");
        var fillList = $("<ul></ul>").addClass("firstLevelUl");
        fillDivArea.append(fillList);
        var fillListSec = $("<ul></ul>").addClass("secondLevelUl");
        fillDivArea.append(fillListSec);
        var fillObjectArray = firstObject.arrayObject;
        for (var k = 0; k < fillObjectArray.length; k++) {
            if (k == 0) {
                $("<li></li>").append($("<a></a>").text("所有").css("color", "#000")).appendTo(fillList)
            }
            var fillObject = fillObjectArray[k];
            var tmpId = "fillLi" + k;
            var tmpa = $("<a></a>");
            tmpa.html(fillObject.name).attr("id", tmpId).attr("href", fillObject.href);
            $("<li></li>").append(tmpa).appendTo(fillList);
            if (fillObject.objectArray.length > 0) {
                var fillObjectArraySec = fillObject.objectArray;
                for (var h = 0; h < fillObjectArraySec.length; h++) {
                    var fillObjectSec = fillObjectArraySec[h];
                    $("<li></li>").append($("<a></a>").text(fillObjectSec.name).attr("href", fillObjectSec.href)).appendTo(fillListSec.attr("data-id", tmpId))
                }
            }
        }
        fillDivArea.insertAfter("ul.navigationUlist");
        var selectedLiText = "";
        var relativeId = "";
        $("#categoryList>ul").eq(1).find("li").each(function () {
            if ($(this).hasClass("selected")) {
                selectedLiText = $(this).find(">a").text()
            }
        });
        $(".listArea a").each(function () {
            if ($(this).text() == selectedLiText) {
                $(this).css("color", "#428bca");
                if ($(this).parent("li").parent("ul").hasClass("firstLevelUl")) {
                    relativeId = $(this).attr("id")
                } else {
                    relativeId = $(this).parent("li").parent("ul").attr("data-id")
                }
            }
        });
        if (parent) {
            var parentClone = parent.clone();
            parent.remove();
            $("#categoryList>ul").eq(1).prepend(parentClone)
        }
        $("#" + relativeId).css("color", "#428bca");
        bindListA(relativeId)
    }
}
function countDown(id, timeTag, endTime) {
    var placeTime = $("#" + id);
    if (!placeTime) {
        return false
    }
    endTime1 = new Date(endTime);
    function updateDate() {
        var today = new Date();
        if (today > endTime1) {
            $("#" + id).hide();
            $(".hiddenByTime").attr("disabled", "disabled");
            clearTimeout(t);
            return false
        }
        var level1 = endTime1.getTime() - today.getTime();
        var date = formatTime(Math.floor(level1 / (24 * 3600 * 1000)));
        var level2 = level1 % (24 * 3600 * 1000);
        var hour = formatTime(Math.floor(level2 / (3600 * 1000)));
        var level3 = level2 % (3600 * 1000);
        var minute = formatTime(Math.floor(level3 / (60 * 1000)));
        var level4 = level3 % (60 * 1000);
        var second = formatTime(Math.floor(level4 / 1000));
        var timeStr = ["<span>", date, "</span>", " 天 ", "<span>", hour, "</span>", " 小时 ", "<span>", minute, "</span>", " 分钟 ", "<span>", second, "</span>", " 秒"].join("");
        $("#" + id).html(timeStr);
        if (level1 < 10) {
            clearTimeout(t);
            $("#" + id).hide();
            $(".hiddenByTime").attr("disabled", "disabled")
        }
    }

    function formatTime(i) {
        if (i < 10) {
            i = "0" + i
        }
        return i
    }

    var t = setInterval(updateDate, 1000)
}
!function ($) {
    var obj;
    var isSubmit = false;
    $.fn.validation = function (options) {
        return this.each(function () {
            globalOptions = $.extend({}, $.fn.validation.defaults, options);
            obj = this;
            reg(obj);
            validationForm(obj)
        })
    };
    $.fn.validation.defaults = {
        validRules: [{
            name: "required", validate: function (value) {
                return ($.trim(value) == "")
            }, defaultMsg: "请输入内容。"
        }, {
            name: "number", validate: function (value) {
                return (!/^[0-9]\d*$/.test(value))
            }, defaultMsg: "请输入数字。"
        }, {
            name: "mail", validate: function (value) {
                return (!/^[a-zA-Z0-9]{1}([\._a-zA-Z0-9-]+)(\.[_a-zA-Z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+){1,3}$/.test(value))
            }, defaultMsg: "请输入邮箱地址。"
        }, {
            name: "char", validate: function (value) {
                return (!/^[a-z\_\-A-Z]*$/.test(value))
            }, defaultMsg: "请输入英文字符。"
        }, {
            name: "chinese", validate: function (value) {
                return (!/^[\u4e00-\u9fff]$/.test(value))
            }, defaultMsg: "请输入汉字。"
        }]
    };
    var formState = false, fieldState = false, wFocus = true, globalOptions = {};
    var validateField = function (field, valid) {
        var el = $(field), error = false, errorMsg = "", crule = (el.attr("btvd-el") == undefined) ? null : el.attr("btvd-el").split(" "), msg = (el.attr("btvd-err") == undefined) ? null : el.attr("btvd-err").split(" ");
        if (isSubmit) {
            if (crule) {
                if (crule[0] == "errorValidateCode") {
                    error = true;
                    errorMsg = "验证码错误"
                } else {
                    if ((crule[0].substr(0, 1) == "!") && eval(crule[0].substring(1)).test(el.val())) {
                        error = true;
                        errorMsg = msg
                    }
                    if ((crule[0].substr(0, 1) !== "!") && !eval(crule[0]).test(el.val())) {
                        error = true;
                        errorMsg = msg
                    }
                }
            } else {
                var isRequired = false;
                for (var j = 0; j < valid.length; j++) {
                    if (valid[j] == "required") {
                        isRequired = true;
                        break
                    }
                }
                if (!isRequired && $.trim(el.val()) == "") {
                } else {
                    for (i = 0; (i < valid.length); i++) {
                        var x = true, flag = valid[i];
                        if (flag.substr(0, 1) == "!") {
                            x = false;
                            flag = flag.substr(1, flag.length - 1)
                        }
                        var rules = globalOptions.validRules;
                        for (j = 0; j < rules.length; j++) {
                            var rule = rules[j];
                            if (flag == rule.name) {
                                if (rule.validate.call(field, $.trim(el.val())) == x) {
                                    error = true;
                                    errorMsg = (msg == null) ? rule.defaultMsg : msg;
                                    break
                                }
                            }
                        }
                        if (error) {
                            break
                        }
                    }
                }
            }
        }
        var controls = el.parent().find("a");
        var len = controls.length;
        if (error) {
            var d = dialog({content: errorMsg, quickClose: true});
            d.show(el[0]);
            setTimeout(function () {
                d.close().remove()
            }, 2000)
        }
        return !error
    };
    var reg = function (obj) {
        $("input, textarea").each(function () {
            var el = $(this), valid = (el.attr("btvd-type") == undefined) ? null : el.attr("btvd-type").split(" ");
            valid1 = (el.attr("btvd-el") == undefined) ? null : el.attr("btvd-el").split(" ");
            if (valid != null && valid.length > 0 || valid1 != null && valid1.length > 0) {
                el.blur(function () {
                    validateField(this, valid)
                })
            }
        })
    };
    var validationForm = function (obj) {
        $(obj).submit(function () {
            if (formState) {
                return false
            }
            if ($(obj).attr("id") == "publishForm") {
                if ($(obj).find("#url").val() == "" && $(obj).find("#fileUpload").val() == "") {
                    sweetAlert("亲!活动url和文档必须上传一样", "亲,请选择一样上传以方便我们了解您需要发布的活动", "error");
                    return false
                }
            }
            isSubmit = true;
            formState = true;
            var validationError = false;
            $("input, textarea", this).each(function () {
                var el = $(this), valid = (el.attr("btvd-type") == undefined) ? null : el.attr("btvd-type").split(" ");
                if (valid != null && valid.length > 0) {
                    if (!validateField(this, valid)) {
                        if (wFocus == false) {
                            scrollTo(0, el[0].offsetTop - 50);
                            wFocus = true
                        }
                        validationError = true
                    }
                }
            });
            fieldState = true;
            if (validationError) {
                formState = false;
                return false
            }
            return true
        })
    }
}(window.jQuery);
$(function ($) {
    $(".backToTop").on("click", function () {
        $("html,body").animate({scrollTop: 0}, 300)
    })
    $(".phone").hover(function () {
            $(this).stop().animate({width: "220px", paddingLeft: "10px"}, 300, function () {
                $(".phone a").text("400-003-3879").css({color: "#fff"})
            })
        },function(){
            $(this).stop().animate({paddingLeft: "0px", width: "72px"}, 300);
            $(".phone a").text("")
        }
    );
    $(".new_weixing a").append("<img src='http://pic.huodongjia.com/static/images/huodongjia_erweima.jpg'" + " width='100px' style='display:none;' alt='活动家微信二维码'>");
    $(".new_weixing a").css({display: "block", background: "#78c440", overflow: "hidden"});
    $(".new_weixing").hover(function () {
            $(this).stop().animate({width: "193px"}, 300, function () {
                $(".new_weixing a img").css({display: "block", margin: "10px"});
                $(".new_weixing").removeClass("overflow")
            });
            $(".new_weixing a").stop().animate({width: "120px", height: "120px"}, 300)
        },function(){
            $(this).stop().animate({paddingLeft: "0px", width: "72px"}, 300, function () {
                $(".new_weixing a img").css({display: "none"})
            });
            $(".new_weixing a").stop()  .animate({width: "0", height: "0"}, 300)
        }
    )
});
!function () {
    function a(b) {
        var d = c[b], e = "exports";
        return "object" == typeof d ? d : (d[e] || (d[e] = {}, d[e] = d.call(d[e], a, d[e], d) || d[e]), d[e])
    }

    function b(a, b) {
        c[a] = b
    }

    var c = {};
    b("jquery", function () {
        return jQuery
    }), b("popup", function (a) {
        function b() {
            this.destroyed = !1, this.__popup = c("<div />").attr({tabindex: "-1"}).css({
                display: "none",
                position: "absolute",
                outline: 0
            }).html(this.innerHTML).appendTo("body"), this.__backdrop = c("<div />"), this.node = this.__popup[0], this.backdrop = this.__backdrop[0], d++
        }

        var c = a("jquery"), d = 0, e = !("minWidth"in c("html")[0].style), f = !e;
        return c.extend(b.prototype, {
            node: null,
            backdrop: null,
            fixed: !1,
            destroyed: !0,
            open: !1,
            returnValue: "",
            autofocus: !0,
            align: "bottom left",
            backdropBackground: "#fff",
            backdropOpacity: 0.7,
            innerHTML: "",
            className: "ui-popup",
            show: function (a) {
                if (this.destroyed) {
                    return this
                }
                var b = this, d = this.__popup;
                return this.__activeElement = this.__getActive(), this.open = !0, this.follow = a || this.follow, this.__ready || (d.addClass(this.className), this.modal && this.__lock(), d.html() || d.html(this.innerHTML), e || c(window).on("resize", this.__onresize = function () {
                    b.reset()
                }), this.__ready = !0), d.addClass(this.className + "-show").attr("role", this.modal ? "alertdialog" : "dialog").css("position", this.fixed ? "fixed" : "absolute").show(), this.__backdrop.show(), this.reset().focus(), this.__dispatchEvent("show"), this
            },
            showModal: function () {
                return this.modal = !0, this.show.apply(this, arguments)
            },
            close: function (a) {
                return !this.destroyed && this.open && (void 0 !== a && (this.returnValue = a), this.__popup.hide().removeClass(this.className + "-show"), this.__backdrop.hide(), this.open = !1, this.blur(), this.__dispatchEvent("close")), this
            },
            remove: function () {
                if (this.destroyed) {
                    return this
                }
                this.__dispatchEvent("beforeremove"), b.current === this && (b.current = null), this.__unlock(), this.__popup.remove(), this.__backdrop.remove(), e || c(window).off("resize", this.__onresize), this.__dispatchEvent("remove");
                for (var a in this) {
                    delete this[a]
                }
                return this
            },
            reset: function () {
                var a = this.follow;
                return a ? this.__follow(a) : this.__center(), this.__dispatchEvent("reset"), this
            },
            focus: function () {
                var a = this.node, d = b.current;
                if (d && d !== this && d.blur(!1), !c.contains(a, this.__getActive())) {
                    var e = this.__popup.find("[autofocus]")[0];
                    !this._autofocus && e ? this._autofocus = !0 : e = a, this.__focus(e)
                }
                return b.current = this, this.__popup.addClass(this.className + "-focus"), this.__zIndex(), this.__dispatchEvent("focus"), this
            },
            blur: function () {
                var a = this.__activeElement, b = arguments[0];
                return b !== !1 && this.__focus(a), this._autofocus = !1, this.__popup.removeClass(this.className + "-focus"), this.__dispatchEvent("blur"), this
            },
            addEventListener: function (a, b) {
                return this.__getEventListener(a).push(b), this
            },
            removeEventListener: function (a, b) {
                for (var c = this.__getEventListener(a), d = 0; d < c.length; d++) {
                    b === c[d] && c.splice(d--, 1)
                }
                return this
            },
            __getEventListener: function (a) {
                var b = this.__listener;
                return b || (b = this.__listener = {}), b[a] || (b[a] = []), b[a]
            },
            __dispatchEvent: function (a) {
                var b = this.__getEventListener(a);
                this["on" + a] && this["on" + a]();
                for (var c = 0; c < b.length; c++) {
                    b[c].call(this)
                }
            },
            __focus: function (a) {
                try {
                    this.autofocus && !/^iframe$/i.test(a.nodeName) && a.focus()
                } catch (b) {
                }
            },
            __getActive: function () {
                try {
                    var a = document.activeElement, b = a.contentDocument, c = b && b.activeElement || a;
                    return c
                } catch (d) {
                }
            },
            __zIndex: function () {
                var a = b.zIndex++;
                this.__popup.css("zIndex", a), this.__backdrop.css("zIndex", a - 1), this.zIndex = a
            },
            __center: function () {
                var a = this.__popup, b = c(window), d = c(document), e = this.fixed, f = e ? 0 : d.scrollLeft(), g = e ? 0 : d.scrollTop(), h = b.width(), i = b.height(), j = a.width(), k = a.height(), l = (h - j) / 2 + f, m = 382 * (i - k) / 1000 + g, n = a[0].style;
                n.left = Math.max(parseInt(l), f) + "px", n.top = Math.max(parseInt(m), g) + "px"
            },
            __follow: function (a) {
                var b = a.parentNode && c(a), d = this.__popup;
                if (this.__followSkin && d.removeClass(this.__followSkin), b) {
                    var e = b.offset();
                    if (e.left * e.top < 0) {
                        return this.__center()
                    }
                }
                var f = this, g = this.fixed, h = c(window), i = c(document), j = h.width(), k = h.height(), l = i.scrollLeft(), m = i.scrollTop(), n = d.width(), o = d.height(), p = b ? b.outerWidth() : 0, q = b ? b.outerHeight() : 0, r = this.__offset(a), s = r.left, t = r.top, u = g ? s - l : s, v = g ? t - m : t, w = g ? 0 : l, x = g ? 0 : m, y = w + j - n, z = x + k - o, A = {}, B = this.align.split(" "), C = this.className + "-", D = {
                    top: "bottom",
                    bottom: "top",
                    left: "right",
                    right: "left"
                }, E = {top: "top", bottom: "top", left: "left", right: "left"}, F = [{
                    top: v - o,
                    bottom: v + q,
                    left: u - n,
                    right: u + p
                }, {top: v, bottom: v - o + q, left: u, right: u - n + p}], G = {
                    left: u + p / 2 - n / 2,
                    top: v + q / 2 - o / 2
                }, H = {left: [w, y], top: [x, z]};
                c.each(B, function (a, b) {
                    F[a][b] > H[E[b]][1] && (b = B[a] = D[b]), F[a][b] < H[E[b]][0] && (B[a] = D[b])
                }), B[1] || (E[B[1]] = "left" === E[B[0]] ? "top" : "left", F[1][B[1]] = G[E[B[1]]]), C += B.join("-") + " " + this.className + "-follow", f.__followSkin = C, b && d.addClass(C), A[E[B[0]]] = parseInt(F[0][B[0]]), A[E[B[1]]] = parseInt(F[1][B[1]]), d.css(A)
            },
            __offset: function (a) {
                var b = a.parentNode, d = b ? c(a).offset() : {left: a.pageX, top: a.pageY};
                a = b ? a : a.target;
                var e = a.ownerDocument, f = e.defaultView || e.parentWindow;
                if (f == window) {
                    return d
                }
                var g = f.frameElement, h = c(e), i = h.scrollLeft(), j = h.scrollTop(), k = c(g).offset(), l = k.left, m = k.top;
                return {left: d.left + l - i, top: d.top + m - j}
            },
            __lock: function () {
                var a = this, d = this.__popup, e = this.__backdrop, g = {
                    position: "fixed",
                    left: 0,
                    top: 0,
                    width: "100%",
                    height: "100%",
                    overflow: "hidden",
                    userSelect: "none",
                    opacity: 0,
                    background: this.backdropBackground
                };
                d.addClass(this.className + "-modal"), b.zIndex = b.zIndex + 2, this.__zIndex(), f || c.extend(g, {
                    position: "absolute",
                    width: c(window).width() + "px",
                    height: c(document).height() + "px"
                }), e.css(g).animate({opacity: this.backdropOpacity}, 150).insertAfter(d).attr({tabindex: "0"}).on("focus", function () {
                    a.focus()
                })
            },
            __unlock: function () {
                this.modal && (this.__popup.removeClass(this.className + "-modal"), this.__backdrop.remove(), delete this.modal)
            }
        }), b.zIndex = 1024, b.current = null, b
    }), b("dialog-config", {
        content: '<span class="ui-dialog-loading">Loading..</span>',
        title: "",
        statusbar: "",
        button: null,
        ok: null,
        cancel: null,
        okValue: "ok",
        cancelValue: "cancel",
        cancelDisplay: !0,
        width: "",
        height: "",
        padding: "",
        skin: "",
        quickClose: !1,
        cssUri: "../css/ui-dialog.css",
        innerHTML: '<div i="dialog" class="ui-dialog"><div class="ui-dialog-arrow-a"></div><div class="ui-dialog-arrow-b"></div><table class="ui-dialog-grid"><tr><td i="header" class="ui-dialog-header"><button i="close" class="ui-dialog-close">&#215;</button><div i="title" class="ui-dialog-title"></div></td></tr><tr><td i="body" class="ui-dialog-body"><div i="content" class="ui-dialog-content"></div></td></tr><tr><td i="footer" class="ui-dialog-footer"><div i="statusbar" class="ui-dialog-statusbar"></div><div i="button" class="ui-dialog-button"></div></td></tr></table></div>'
    }), b("dialog", function (a) {
        var b = a("jquery"), c = a("popup"), d = a("dialog-config"), e = d.cssUri;
        if (e) {
            var f = a[a.toUrl ? "toUrl" : "resolve"];
            f && (e = f(e), e = '<link rel="stylesheet" href="' + e + '" />', b("base")[0] ? b("base").before(e) : b("head").append(e))
        }
        var g = 0, h = new Date - 0, i = !("minWidth"in b("html")[0].style), j = "createTouch"in document && !("onmousemove"in document) || /(iPhone|iPad|iPod)/i.test(navigator.userAgent), k = !i && !j, l = function (a, c, d) {
            var e = a = a || {};
            ("string" == typeof a || 1 === a.nodeType) && (a = {
                content: a,
                fixed: !j
            }), a = b.extend(!0, {}, l.defaults, a), a._ = e;
            var f = a.id = a.id || h + g, i = l.get(f);
            return i ? i.focus() : (k || (a.fixed = !1), a.quickClose && (a.modal = !0, e.backdropOpacity || (a.backdropOpacity = 0)), b.isArray(a.button) || (a.button = []), void 0 !== d && (a.cancel = d), a.cancel && a.button.push({
                id: "cancel",
                value: a.cancelValue,
                callback: a.cancel,
                display: a.cancelDisplay
            }), void 0 !== c && (a.ok = c), a.ok && a.button.push({
                id: "ok",
                value: a.okValue,
                callback: a.ok,
                autofocus: !0
            }), l.list[f] = new l.create(a))
        }, m = function () {
        };
        m.prototype = c.prototype;
        var n = l.prototype = new m;
        return l.create = function (a) {
            var d = this;
            b.extend(this, new c);
            var e = b(this.node).html(a.innerHTML);
            return this.options = a, this._popup = e, b.each(a, function (a, b) {
                "function" == typeof d[a] ? d[a](b) : d[a] = b
            }), a.zIndex && (c.zIndex = a.zIndex), e.attr({
                "aria-labelledby": this._$("title").attr("id", "title:" + this.id).attr("id"),
                "aria-describedby": this._$("content").attr("id", "content:" + this.id).attr("id")
            }), this._$("close").css("display", this.cancel === !1 ? "none" : "").attr("title", this.cancelValue).on("click", function (a) {
                d._trigger("cancel"), a.preventDefault()
            }), this._$("dialog").addClass(this.skin), this._$("body").css("padding", this.padding), e.on("click", "[data-id]", function (a) {
                var c = b(this);
                c.attr("disabled") || d._trigger(c.data("id")), a.preventDefault()
            }), a.quickClose && b(this.backdrop).on("onmousedown"in document ? "mousedown" : "click", function () {
                return d._trigger("cancel"), !1
            }), this._esc = function (a) {
                var b = a.target, e = b.nodeName, f = /^input|textarea$/i, g = c.current === d, h = a.keyCode;
                !g || f.test(e) && "button" !== b.type || 27 === h && d._trigger("cancel")
            }, b(document).on("keydown", this._esc), this.addEventListener("remove", function () {
                b(document).off("keydown", this._esc), delete l.list[this.id]
            }), g++, l.oncreate(this), this
        }, l.create.prototype = n, b.extend(n, {
            content: function (a) {
                return this._$("content").empty("")["object" == typeof a ? "append" : "html"](a), this.reset()
            }, title: function (a) {
                return this._$("title").text(a), this._$("header")[a ? "show" : "hide"](), this
            }, width: function (a) {
                return this._$("content").css("width", a), this.reset()
            }, height: function (a) {
                return this._$("content").css("height", a), this.reset()
            }, button: function (a) {
                a = a || [];
                var c = this, d = "", e = 0;
                return this.callbacks = {}, "string" == typeof a ? d = a : b.each(a, function (a, b) {
                    b.id = b.id || b.value, c.callbacks[b.id] = b.callback;
                    var f = "";
                    b.display === !1 ? f = ' style="display:none"' : e++, d += '<button type="button" data-id="' + b.id + '"' + f + (b.disabled ? " disabled" : "") + (b.autofocus ? ' autofocus class="ui-dialog-autofocus"' : "") + ">" + b.value + "</button>"
                }), this._$("footer")[e ? "show" : "hide"](), this._$("button").html(d), this
            }, statusbar: function (a) {
                return this._$("statusbar").html(a)[a ? "show" : "hide"](), this
            }, _$: function (a) {
                return this._popup.find("[i=" + a + "]")
            }, _trigger: function (a) {
                var b = this.callbacks[a];
                return "function" != typeof b || b.call(this) !== !1 ? this.close().remove() : this
            }
        }), l.oncreate = b.noop, l.getCurrent = function () {
            return c.current
        }, l.get = function (a) {
            return void 0 === a ? l.list : l.list[a]
        }, l.list = {}, l.defaults = d, l
    }), window.dialog = a("dialog")
}();