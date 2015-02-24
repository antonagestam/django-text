(function ($) {
    "use strict";
    $(function () {
        $(".markdown").hide().each(function () {
            var markDownEl = this;
            new MediumEditor(document.querySelector(".editor"), {
                extensions: {
                    markdown: new MeMarkdown(function (md) {
                        markDownEl.val(md);
                    })
                }
            });
        });
    });
}(django.jQuery));
