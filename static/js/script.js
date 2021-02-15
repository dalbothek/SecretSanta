var CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ -".split("");
var CHRISTMAS_ICONS = [
    "christmas/001-angel.svg",
    "christmas/004-candle.svg",
    "christmas/008-christmas.svg",
    "christmas/010-star.svg",
    "christmas/011-christmas-tree.svg",
    "christmas/015-ornament.svg",
    "christmas/016-ornament-1.svg",
    "christmas/017-gift-box.svg",
    "christmas/024-snowflake.svg",
    "christmas/027-star-1.svg"
];
var BIRTHDAY_ICONS = [
    "birthday/050-balloons.svg",
    "birthday/049-cake.svg",
    "birthday/046-wine.svg",
    "birthday/043-confetti.svg",
    "birthday/036-gift.svg",
    "birthday/029-invitation.svg",
    "birthday/019-party-horn.svg",
    "birthday/010-party-hat.svg",
    "birthday/001-bucket.svg",
    "birthday/005-drink-1.svg",
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

function animate(el, start, end, callback) {
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
            if (v < 0 || isNaN(v)) {
                window.clearInterval(interval);
                callback();
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
    return -(index + OVERLAP) * 49 + 17;
}

function buildRow(el, target, length) {
    var padding_length = (length - target.length) / 2;
    target = padding(Math.floor(padding_length)) + target + padding(Math.ceil(padding_length));

    el.css({
        width: length * 50,
        left: 500 - length * 25
    });

    var colors = [
        "color1",
        "color2",
        "color3",
        "color4"
    ];

    var active_count = 0;

    for (var i = 0; i < length; i++) {
        var slot = $("<div class='slot'>");
        el.append(slot);
        var band = $("<div class='band'>");
        slot.append(band);

        var color_cache = {};
        var icons = theme === 'birthday' ? BIRTHDAY_ICONS : CHRISTMAS_ICONS;
        var slots = shuffle(CHARS.concat(shuffle(icons).slice(0, ICON_COUNT)));
        for (var j = -OVERLAP; j < SLOT_COUNT + OVERLAP; j++) {
            var cell = $("<span>");
            var char = slots[(j + SLOT_COUNT) % SLOT_COUNT];
            if (char.length === 1) {
                cell.text(char);
                if (color_cache[char] != undefined) {
                    if (color_cache[char] != null) {
                        cell.addClass(color_cache[char]);
                    }
                }
                else {
                    var color;
                    if (Math.random() > 0.5) {
                        color = shuffle(colors)[0];
                        cell.addClass(color);
                    }
                    else {
                        color = null;
                    }
                    color_cache[char] = color;
                }
            }
            else {
                var img = $("<img src='/static/img/icon/" + char + "'>");
                cell.append(img);
            }
            band.append(cell);
        }
        active_count++;
        animate(band, slots.indexOf(" "), slots.indexOf(target.charAt(i)), function() {
            if (--active_count <= 0) {
                $("#text-below").animate({opacity: 1}, 1500);
            }
        });
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
