(function ($) {
    "use strict";

    function init_editor(textarea, editor) {
        new MediumEditor(editor.get(), {
            extensions: {
                markdown: new MeMarkdown(function (md) {
                    textarea.val(md);
                })
            }
        });
    }

    function text_mode(textarea, editor) {
        textarea.show();
        editor.hide();
    }

    function editor_mode(textarea, editor) {
        textarea.hide();
        editor.show();
    }

    $(function () {
        var textarea = $(".markdown"),
            editor = $(".editor"),
            type_select = $('#id_type');

        if (type_select.val() == 0) {
            text_mode(textarea, editor);
        } else {
            editor_mode(textarea, editor);
        }

        init_editor(textarea, editor);

        type_select.bind('change', function () {
            var val = type_select.val();
            if (val == 0) {
                text_mode(textarea, editor);
            } else {
                editor_mode(textarea, editor);
            }
        });
    });
}(django.jQuery));
