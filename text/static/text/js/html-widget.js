(function ($) {
    "use strict";

    function MEExtension(callback) {
        this.init = function (me_instance) {
            this.me_instance = me_instance;

            if (!this.me_instance.elements || !this.me_instance.elements.length) {
                return;
            }

            this.element = this.me_instance.elements[0];

            var handler = function () {
                callback(this.element.innerHTML);
            }.bind(this);

            ["input", "change"].forEach(function (c) {
                this.element.addEventListener(c, handler);
            }.bind(this));

            handler();
        };
    }


    function init_editor(textarea, editor) {
        new MediumEditor(editor.get(), {
            firstHeader: 'h1',
            secondHeader: 'h2',
            extensions: {
                markdown: new MEExtension(function (html) {
                    textarea.val(html);
                })
            }
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
                init_editor(textarea, editor);
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

}(
    (function () {
        "use strict";
        if (window.hasOwnProperty('Zepto')) {
            return window.Zepto;
        }
        return window.django.jQuery;
    }())
));
