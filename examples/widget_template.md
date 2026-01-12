# Companion App Widget

<div align="center">
  <img width="151" height="100" hspace="15" alt="widget_template_scr1" src="https://github.com/user-attachments/assets/72bd7da5-7550-417c-b441-2c1a46cf0e49" />
  <img width="151" height="100" hspace="15" alt="widget_template_scr2" src="https://github.com/user-attachments/assets/8bb8f2ef-ebe3-4ccd-a75d-1c06f7a4cda4" />
  <img width="151" height="100" hspace="15" alt="widget_template_scr3" src="https://github.com/user-attachments/assets/b6487a71-3820-408c-97bd-d4a11aeddd37" />
</div>

This configuration creates a template sensor specifically designed for the **Home Assistant Companion App** on Android. It allows you to place a detailed, color-coded status card directly on your phone's home screen.

## Features:
* **State:** Provides a concise status (e.g., "💡 Включення о 18:00") suitable for simple State widgets.
* **Attribute (`html_card`):** Contains a detailed, color-coded HTML summary designed specifically for the **Template Widget**.

## YAML Configuration:
Add the following code to your `templates.yaml` file).

*Note: Replace `sensor.energyua_lvivska_grupa_1_1_...` with your actual entity IDs.*

```yaml
- sensor:
    - unique_id: energyua_widget
      name: "EnergyUA Widget"
      icon: mdi:flash-alert
      # Smart Status: Shows "On until...", "Off until...", or "No outages"
      state: >
        {% set o_state = states('sensor.energyua_lvivska_grupa_1_1_next_outage') %}
        {% set r_state = states('sensor.energyua_lvivska_grupa_1_1_next_restore') %}

        {% if o_state == 'unavailable' or r_state == 'unavailable' %}
          ⚠️ Дані недоступні
        {% elif o_state == 'unknown' and r_state == 'unknown' %}
          ✅ Немає відключень
        {% else %}
          {% set o = o_state | as_datetime(default=None) %}
          {% set r = r_state | as_datetime(default=None) %}
          {% if o %}{% set o = o | as_local %}{% endif %}
          {% if r %}{% set r = r | as_local %}{% endif %}

          {% if r and not o %}
            💡 Відновлення о {{ r.strftime('%H:%M') }}
          {% elif o %}
            🕯️ Відключення о {{ o.strftime('%H:%M') }}
          {% endif %}
        {% endif %}

      attributes:
        # Detailed HTML view for the Android Template Widget
        html_card: >
          {% set o_state = states('sensor.energyua_lvivska_grupa_1_1_next_outage') %}
          {% set r_state = states('sensor.energyua_lvivska_grupa_1_1_next_restore') %}

          {% if o_state == 'unavailable' or r_state == 'unavailable' %}
            ⚠️ Дані недоступні
          {% elif o_state == 'unknown' and r_state == 'unknown' %}
            ✅ Немає запланованих відключень
          {% else %}
            {% set o = o_state | as_datetime(default=None) %}
            {% set r = r_state | as_datetime(default=None) %}
            {% if o %}{% set o = o | as_local %}{% endif %}
            {% if r %}{% set r = r | as_local %}{% endif %}

            <p style="text-align:start">
              🕯️ Відключення:
              {{ '<font color="#f44336"><b>' ~ o.strftime("%H:%M") ~ '</b></font> ' ~
                 '<font color="#757575"><b>' ~ o.strftime("%d.%m") ~ '</b></font>'
                 if o else '<font color="#9e9e9e"><b>Невідомо</b></font>' }}
              <br>

              💡 Відновлення:
              {{ '<font color="#4caf50"><b>' ~ r.strftime("%H:%M") ~ '</b></font> ' ~
                 '<font color="#757575"><b>' ~ r.strftime("%d.%m") ~ '</b></font>'
                 if r else '<font color="#9e9e9e"><b>Невідомо</b></font>' }}
              <br>

              {% if not o and not r %}
                ⏱️ Тривалість: — —
              {% elif o and r %}
                {% set d = r - o %}
                {% set secs = d.total_seconds() %}
                ⏱️ Тривалість:
                {{ '<font color="#03a9f4"><b>' ~
                   (secs // 3600) | int ~ ':' ~
                   ('%02d' | format((secs % 3600) // 60)) ~
                   '</b></font>' }}
              {% elif o %}
                {% set d = o - now() %}
                {% if d.total_seconds() > 0 %}
                  {% set secs = d.total_seconds() %}
                  ⏱️ До відключення:
                  {{ '<font color="#ff9800"><b>' ~
                     (secs // 3600) | int ~ ':' ~
                     ('%02d' | format((secs % 3600) // 60)) ~
                     '</b></font>' }}
                {% else %}
                  ⏱️ До відключення: —
                {% endif %}
              {% elif r %}
                {% set d = r - now() %}
                {% if d.total_seconds() > 0 %}
                  {% set secs = d.total_seconds() %}
                  ⏱️ До відновлення:
                  {{ '<font color="#ffc107"><b>' ~
                     (secs // 3600) | int ~ ':' ~
                     ('%02d' | format((secs % 3600) // 60)) ~
                     '</b></font>' }}
                {% else %}
                  ⏱️ До відновлення: —
                {% endif %}
              {% endif %}
            </p>
        {% endif %}
```
## Setup Widget
1. Add a **Home Assistant Template Widget** to your home screen.
2. In the widget settings, paste one of the following codes:

   **Option A: Full Status Card**
   ```yaml
   {{ state_attr('sensor.energyua_widget', 'html_card') }}
   ```

   **Option B: Simple Text Status**
   ```yaml
   {{ states('sensor.energyua_widget') }}
   ```
