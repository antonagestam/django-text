(function ($) {
    "use strict";

    var body = $('body'),
        handle = $('#djtext_toolbar_handle'),
        toolbar = $('#djtext_toolbar'),
        language = toolbar.data('language'),
        url_get_pattern = toolbar.data('url-pattern'),
        closer = $('.djtext_close_toolbar'),
        toolbar_active = false,
        menu_items = $('.djtext_menu li'),
        form = $('#djtext_form', toolbar),
        url_post_pattern = form.attr('action'),
        editor = $('.djtext_editor'),
        editor_element = $('.djtext_html_editor', form),
        content_element = $('.djtext_editor_input'),
        text_id = null,
        text_name = null,
        csrf_input = $('[name=csrfmiddlewaretoken]', form),
        name_element = $('.djtext_text_name'),
        start_element = $('.djtext_editor_start'),
        submit = $('.djtext_submit'),
        menu = $('.djtext_toolbar_menu', toolbar),
        tools = $('.djtext_toolbar_menu_tools', menu);

    function toggle_toolbar() {
        if (toolbar_active) {
            toolbar.removeClass('djtext_toggle');
            menu.hide();
            body.css('overflow', 'visible');
        } else {
            toolbar.addClass("djtext_toggle");
            menu.show();
            body.css('overflow', 'hidden');
        }
        toolbar_active = !toolbar_active;
    }

    submit.click(function() {
        form.submit();
        toggle_toolbar();
    });

    function init_toolbar_handles() {
        handle.on('click', toggle_toolbar);
        closer.on('click', toggle_toolbar);
    }

    function get_text_slug(name) {
        return name + '_' + language;
    }

    function get_url(name) {
        return url_get_pattern.replace('__id__', get_text_slug(name));
    }

    function post_url() {
        return url_post_pattern.replace('0', text_id);
    }

    function update_editor(text_data) {
        Object.keys(text_data).forEach(function (key) {
            $('#id_djtext_form-' + key, form).val(text_data[key]).change();
        });
        form.attr('action', post_url(text_data.name));
        name_element.text(get_text_slug(text_data.name));
        editor_element.html(text_data.render).focus();
        start_element.hide();
        editor.show();
        tools.css('opacity', 1);
    }

    function load_text() {
        var menu_item = $(this),
            name = menu_item.data('name'),
            url = get_url(name);
        $.getJSON(url, function (response) {
            update_editor(response);
            toolbar.scrollTop(0);
            text_id = response.id;
            text_name = response.name;
        });
    }

    function save_form() {
        $.ajax({
            url: post_url(),
            type: 'POST',
            data: form.serialize(),
            dataType: 'JSON',
            headers: {
                'X-CSRFToken': csrf_input.val()
            },
            success: function () {
                var selector = '.' + toolbar.data('inline-wrapper-class') + '[data-text-name="' + text_name + '"]';
                $(selector).html(content_element.val());
            }
        });
    }

    function init_form() {
        form.on('submit', function (e) {
            e.preventDefault();
            save_form();
            return false;
        });
    }

    function init_text_menu() {
        menu_items.on('click', load_text);
    }

    function init() {
        init_toolbar_handles();
        init_text_menu();
        init_form();
    }

    $(init);
}(Zepto));
