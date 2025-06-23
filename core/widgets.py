from django import forms
from django.utils.safestring import mark_safe

class RepeaterListWidget(forms.Widget):
    template_name = 'widgets/repeater_input.html'

    def value_from_datadict(self, data, files, name):
        values = data.getlist(name)
        return [v for v in values if v.strip()]

    def render(self, name, value, attrs=None, renderer=None):
        value = value or []
        if isinstance(value, str):
            import json
            value = json.loads(value)

        html = '<div class="repeater-list">'
        for item in value:
            html += f'<input type="text" name="{name}" value="{item}" class="repeater-item" /><br>'
        html += f'<input type="text" name="{name}" class="repeater-item" /><br>'
        html += f'<button type="button" onclick="addRepeaterInput(this)">➕ Add</button>'
        html += '</div>'

        # Add JavaScript inline
        html += """
        <script>
        function addRepeaterInput(btn) {
            const div = btn.parentElement;
            const input = document.createElement('input');
            input.type = 'text';
            input.name = btn.previousElementSibling.name;
            input.className = 'repeater-item';
            div.insertBefore(input, btn);
            div.insertBefore(document.createElement('br'), btn);
        }
        </script>
        """
        return mark_safe(html)
