
// Mousetrap.bind("4", function() { highlight(2); });
// Mousetrap.bind("x", function() { XXXXX(); });

Mousetrap.bind("ctrl+left", function() { annoFirst(); });
Mousetrap.bind("left", function() { annoPrevious(); });
Mousetrap.bind("right", function() { annoNext(); });
Mousetrap.bind("ctrl+right", function() { annoLast(); });

Mousetrap.bind("x", function() { annoSetQ0(); });
Mousetrap.bind("0", function() { annoSetQ0(); });
Mousetrap.bind("1", function() { annoSetQ1(); });
Mousetrap.bind("2", function() { annoSetQ2(); });
Mousetrap.bind("3", function() { annoSetQ03(); });
Mousetrap.bind("4", function() { annoSetQ04(); });