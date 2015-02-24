(function ($) {
    "use strict";
    $(function () {
        var markDownEl = $(".markdown").hide();
        new MediumEditor($(".editor").get(), {
            extensions: {
                markdown: new MeMarkdown(function (md) {
                    markDownEl.val(md);
                })
            }
        });
    });
}(django.jQuery));
