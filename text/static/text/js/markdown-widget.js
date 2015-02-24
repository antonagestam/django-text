(function ($) {
    "use strict";
    $(function () {
        var markDownEl = document.querySelector(".markdown");
        markDownEl.style.display = 'none';
        new MediumEditor(document.querySelector(".editor"), {
            extensions: {
                markdown: new MeMarkdown(function (md) {
                    markDownEl.innerText = md;
                })
            }
        });
    });
}(django.jQuery));
