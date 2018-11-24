var CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ -".split("");
var ICONS = [
    "001-angel.svg",
    "004-candle.svg",
    "008-christmas.svg",
    "010-star.svg",
    "011-christmas-tree.svg",
    "015-ornament.svg",
    "016-ornament-1.svg",
    "017-gift-box.svg",
    "024-snowflake.svg",
    "027-star-1.svg"
];
var ICON_COUNT = 4;
var SLOT_COUNT = CHARS.length + ICON_COUNT;
var OVERLAP = 4;
var TERMINAL_VELOCITY = 0.3;
var INTERVAL = 20;

if (!Array.prototype.indexOf) {
    // silly IE
    Array.prototype.indexOf = function(obj, start) {
        for (var i = (start || 0), j = this.length; i < j; i++) {
            if (this[i] === obj) { return i; }
        }
        return -1;
    };
}

function shuffle(o) {
    for (var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
}

function animate(el, start, end) {
    el.css({
        top: topOffset(start)
    });

    var v = 0;
    var state = -1;
    var t = 0;
    var x = start;
    var overturn = 3;

    var interval = window.setInterval(function() {
        if (state === -1) {
            if (t++ >= 30) {
                state = 0;
                t = 0;
            }
        } else if (state === 0) {
            v += Math.random() / (200 - Math.min(t * 10, 199));
            if (v >= TERMINAL_VELOCITY) {
                state = 2;
            }
        } else if (state == 1) {
            if (t++ > 100) {
                state = 2;
            }
        } else if (state == 2) {
            var d = x - end + SLOT_COUNT * overturn;
            break_time = 2 * d / v;
            break_acceleration = 2 * d / break_time / break_time;
            v -= break_acceleration;
            if (v < 0) {
                window.clearInterval(interval);
            }
            if (x - v < 0) {
                overturn--;
            }
        }
        x = (x - v + SLOT_COUNT) % SLOT_COUNT;
        el.css({
            top: topOffset(x)
        });
    }, INTERVAL);
}

function topOffset(index) {
    return -(index + OVERLAP) * 49 + 30;
}

function buildRow(el, target, length) {
    var padding_length = (length - target.length) / 2;
    target = padding(Math.floor(padding_length)) + target + padding(Math.ceil(padding_length));

    el.css({
        width: length * 50,
        left: 500 - length * 25
    });

    for (var i = 0; i < length; i++) {
        var slot = $("<div class='slot'>");
        el.append(slot);
        var band = $("<div class='band'>");
        slot.append(band);

        var slots = shuffle(CHARS.concat(shuffle(ICONS).slice(0, ICON_COUNT)));
        for (var j = -OVERLAP; j < SLOT_COUNT + OVERLAP; j++) {
            var cell = $("<span>");
            var char = slots[(j + SLOT_COUNT) % SLOT_COUNT];
            if (char.length === 1) {
                cell.text(char);
            }
            else {
                var img = $("<img src='/static/img/icon/" + char + "'>");
                cell.append(img);
            }
            band.append(cell);
        }
        animate(band, slots.indexOf(" "), slots.indexOf(target.charAt(i)));
    }
}

function padding(length) {
    var string = "";
    for (; length > 0; length--) {
        string += " ";
    }
    return string;
}

$(function() {
    var name = [secret1, secret2];
    var length = 20 + Math.max(name[0].length, name[1].length) % 2;
    $(function() {
        buildRow($("#row1"), name[0].toUpperCase(), length);
        buildRow($("#row2"), name[1].toUpperCase(), length);
    });
});
