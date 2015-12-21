(function ($) {
    "use strict";

    function init_editor(editor) {
        new MediumEditor(editor.get(), {
            firstHeader: 'h1',
            secondHeader: 'h2'
        });
    }

    $(function () {
        var textarea = $(".djtext_editor_input"),
            editor = $(".djtext_html_editor"),
            type_select = editor.parents('form').find('[id$="type"]');

        function set_mode(mode) {
            if (mode == 'html') {
                textarea.hide();
                editor.show();
                init_editor(editor);
            } else {
                textarea.show();
                editor.hide();
            }
        }

        set_mode(type_select.val());

        type_select.bind('change', function () {
            set_mode(type_select.val());
        });
    });

}(window.Zepto));
